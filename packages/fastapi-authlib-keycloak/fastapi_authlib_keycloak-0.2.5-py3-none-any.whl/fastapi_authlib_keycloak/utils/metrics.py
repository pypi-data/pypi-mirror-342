#!/usr/bin/env python3
"""
Metrics collection and observability utilities for FastAPI-Authlib-Keycloak.

This module provides functions for collecting and reporting metrics about
authentication and authorization operations, which can be used for monitoring,
performance analysis, and diagnostics.

Features:
- Support for multiple backends (Prometheus, logger, custom)
- Automatic collection of common authentication metrics
- FastAPI middleware for HTTP request metrics
- Context managers for timing operations
- Export capabilities for metrics data
"""

import os
import time
import json
import logging
import asyncio
import threading
import traceback
from contextlib import contextmanager
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Callable, Set, Iterator, TypeVar, Generator, ContextManager

# Try to import prometheus_client if available
try:
    import prometheus_client
    from prometheus_client import Counter, Histogram, Gauge, Info, Summary
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False


class MetricsBackend(str, Enum):
    """Enumeration of supported metrics backends."""
    NONE = "none"
    PROMETHEUS = "prometheus"
    LOGGER = "logger"
    CUSTOM = "custom"


# Default metrics backend
DEFAULT_BACKEND = MetricsBackend.NONE if not PROMETHEUS_AVAILABLE else MetricsBackend.PROMETHEUS

# Global metrics registry
_metrics = {}

# Global metrics configuration
_metrics_config = {
    "backend": DEFAULT_BACKEND,
    "enabled": False,
    "prefix": "keycloak_auth_",
    "labels": {},
    "custom_handler": None
}

# Logger for metrics
logger = logging.getLogger("fastapi-keycloak.metrics")


def configure_metrics(
    backend: Union[str, MetricsBackend] = DEFAULT_BACKEND,
    enabled: bool = True,
    prefix: str = "keycloak_auth_",
    labels: Dict[str, str] = None,
    custom_handler: Optional[Callable] = None,
    log_level: str = "INFO"
) -> None:
    """
    Configure the metrics collection system.
    
    Args:
        backend: Metrics backend to use
        enabled: Whether metrics collection is enabled
        prefix: Prefix for metric names
        labels: Global labels to apply to all metrics
        custom_handler: Custom handler function for the CUSTOM backend
        log_level: Log level for the metrics logger
    """
    global _metrics_config
    
    # Set logger level
    logger.setLevel(getattr(logging, log_level))
    
    # Normalize backend
    if isinstance(backend, str):
        backend = MetricsBackend(backend.lower())
        
    # Check if selected backend is available
    if backend == MetricsBackend.PROMETHEUS and not PROMETHEUS_AVAILABLE:
        logger.warning(
            "Prometheus metrics backend selected but prometheus_client is not installed. "
            "Falling back to logger backend."
        )
        backend = MetricsBackend.LOGGER
        
    # Configure metrics
    _metrics_config = {
        "backend": backend,
        "enabled": enabled,
        "prefix": prefix,
        "labels": labels or {},
        "custom_handler": custom_handler
    }
    
    # Log configuration
    logger.info(
        f"Metrics configured: backend={backend.value}, enabled={enabled}, "
        f"prefix={prefix}, labels={_metrics_config['labels']}"
    )
    
    # Initialize common metrics
    _initialize_common_metrics()


def _initialize_common_metrics() -> None:
    """Initialize common metrics used throughout the library."""
    if not _metrics_config["enabled"]:
        return
        
    # Authentication metrics
    register_counter(
        name="token_validations_total",
        description="Total number of token validations performed",
        labels=["method", "success"]
    )
    
    register_histogram(
        name="token_validation_duration_seconds",
        description="Token validation duration in seconds",
        labels=["method", "success"],
        buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
    )
    
    # JWKS metrics
    register_counter(
        name="jwks_fetches_total",
        description="Total number of JWKS fetches performed",
        labels=["success"]
    )
    
    register_histogram(
        name="jwks_fetch_duration_seconds",
        description="JWKS fetch duration in seconds",
        labels=["success"],
        buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
    )
    
    register_gauge(
        name="jwks_cache_age_seconds",
        description="Age of the JWKS cache in seconds",
        labels=[]
    )
    
    # Error metrics
    register_counter(
        name="auth_errors_total",
        description="Total number of authentication errors",
        labels=["error_type"]
    )
    
    # Introspection metrics
    register_counter(
        name="token_introspections_total",
        description="Total number of token introspections performed",
        labels=["success"]
    )
    
    register_histogram(
        name="token_introspection_duration_seconds",
        description="Token introspection duration in seconds",
        labels=["success"],
        buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
    )
    
    # Cache metrics
    register_counter(
        name="cache_hits_total",
        description="Total number of cache hits",
        labels=["cache_type"]
    )
    
    register_counter(
        name="cache_misses_total",
        description="Total number of cache misses",
        labels=["cache_type"]
    )
    
    # Token extraction metrics
    register_counter(
        name="token_extractions_total",
        description="Total number of token extractions from requests",
        labels=["source", "success"]
    )
    
    # Rate limiting metrics
    register_counter(
        name="rate_limit_hits_total",
        description="Total number of rate limit hits",
        labels=["endpoint"]
    )
    
    register_gauge(
        name="rate_limit_remaining",
        description="Remaining requests before rate limit is hit",
        labels=["endpoint"]
    )
    
    register_histogram(
        name="rate_limit_reset_seconds",
        description="Time until rate limit resets in seconds",
        labels=["endpoint"],
        buckets=[1, 5, 10, 30, 60, 300, 600, 1800, 3600]
    )
    
    # HTTP request metrics
    register_counter(
        name="http_requests_total",
        description="Total number of HTTP requests",
        labels=["method", "path", "status"]
    )
    
    register_histogram(
        name="http_request_duration_seconds",
        description="HTTP request duration in seconds",
        labels=["method", "path", "status"],
        buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
    )
    
    # System metrics
    register_info(
        name="system_info",
        description="System information"
    )
    
    # Set system info
    set_info(
        name="system_info",
        value={
            "start_time": datetime.utcnow().isoformat(),
            "hostname": os.uname().nodename if hasattr(os, 'uname') else "unknown",
            "version": "fastapi_authlib_keycloak",
        }
    )


def register_counter(
    name: str,
    description: str,
    labels: List[str] = None,
    namespace: str = ""
) -> None:
    """
    Register a counter metric.
    
    Args:
        name: Name of the metric
        description: Description of the metric
        labels: Labels for the metric
        namespace: Namespace for the metric (overrides prefix)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Format name with prefix
    prefix = namespace or _metrics_config["prefix"]
    full_name = f"{prefix}{name}"
    
    # Create metric based on backend
    backend = _metrics_config["backend"]
    labels = labels or []
    
    if backend == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
        _metrics[full_name] = Counter(
            full_name,
            description,
            labels + list(_metrics_config["labels"].keys())
        )
    elif backend == MetricsBackend.LOGGER:
        _metrics[full_name] = {
            "type": "counter",
            "description": description,
            "labels": labels,
            "value": 0
        }
    elif backend == MetricsBackend.CUSTOM:
        # Custom metrics are created through the handler
        pass


def register_gauge(
    name: str,
    description: str,
    labels: List[str] = None,
    namespace: str = ""
) -> None:
    """
    Register a gauge metric.
    
    Args:
        name: Name of the metric
        description: Description of the metric
        labels: Labels for the metric
        namespace: Namespace for the metric (overrides prefix)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Format name with prefix
    prefix = namespace or _metrics_config["prefix"]
    full_name = f"{prefix}{name}"
    
    # Create metric based on backend
    backend = _metrics_config["backend"]
    labels = labels or []
    
    if backend == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
        _metrics[full_name] = Gauge(
            full_name,
            description,
            labels + list(_metrics_config["labels"].keys())
        )
    elif backend == MetricsBackend.LOGGER:
        _metrics[full_name] = {
            "type": "gauge",
            "description": description,
            "labels": labels,
            "value": 0
        }
    elif backend == MetricsBackend.CUSTOM:
        # Custom metrics are created through the handler
        pass


def register_histogram(
    name: str,
    description: str,
    labels: List[str] = None,
    buckets: List[float] = None,
    namespace: str = ""
) -> None:
    """
    Register a histogram metric.
    
    Args:
        name: Name of the metric
        description: Description of the metric
        labels: Labels for the metric
        buckets: Histogram buckets
        namespace: Namespace for the metric (overrides prefix)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Format name with prefix
    prefix = namespace or _metrics_config["prefix"]
    full_name = f"{prefix}{name}"
    
    # Create metric based on backend
    backend = _metrics_config["backend"]
    labels = labels or []
    buckets = buckets or [0.1, 0.5, 1.0, 5.0, 10.0]
    
    if backend == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
        _metrics[full_name] = Histogram(
            full_name,
            description,
            labels + list(_metrics_config["labels"].keys()),
            buckets=buckets
        )
    elif backend == MetricsBackend.LOGGER:
        _metrics[full_name] = {
            "type": "histogram",
            "description": description,
            "labels": labels,
            "buckets": buckets,
            "values": []
        }
    elif backend == MetricsBackend.CUSTOM:
        # Custom metrics are created through the handler
        pass


def register_summary(
    name: str,
    description: str,
    labels: List[str] = None,
    namespace: str = ""
) -> None:
    """
    Register a summary metric.
    
    Args:
        name: Name of the metric
        description: Description of the metric
        labels: Labels for the metric
        namespace: Namespace for the metric (overrides prefix)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Format name with prefix
    prefix = namespace or _metrics_config["prefix"]
    full_name = f"{prefix}{name}"
    
    # Create metric based on backend
    backend = _metrics_config["backend"]
    labels = labels or []
    
    if backend == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
        _metrics[full_name] = Summary(
            full_name,
            description,
            labels + list(_metrics_config["labels"].keys())
        )
    elif backend == MetricsBackend.LOGGER:
        _metrics[full_name] = {
            "type": "summary",
            "description": description,
            "labels": labels,
            "count": 0,
            "sum": 0
        }
    elif backend == MetricsBackend.CUSTOM:
        # Custom metrics are created through the handler
        pass


def register_info(
    name: str,
    description: str,
    namespace: str = ""
) -> None:
    """
    Register an info metric.
    
    Args:
        name: Name of the metric
        description: Description of the metric
        namespace: Namespace for the metric (overrides prefix)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Format name with prefix
    prefix = namespace or _metrics_config["prefix"]
    full_name = f"{prefix}{name}"
    
    # Create metric based on backend
    backend = _metrics_config["backend"]
    
    if backend == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
        _metrics[full_name] = Info(
            full_name,
            description
        )
    elif backend == MetricsBackend.LOGGER:
        _metrics[full_name] = {
            "type": "info",
            "description": description,
            "value": {}
        }
    elif backend == MetricsBackend.CUSTOM:
        # Custom metrics are created through the handler
        pass


def increment_counter(
    name: str,
    labels: Dict[str, str] = None,
    value: float = 1.0,
    namespace: str = ""
) -> None:
    """
    Increment a counter metric.
    
    Args:
        name: Name of the metric
        labels: Labels for the metric
        value: Value to increment by
        namespace: Namespace for the metric (overrides prefix)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Format name with prefix
    prefix = namespace or _metrics_config["prefix"]
    full_name = f"{prefix}{name}"
    
    # Get combined labels
    combined_labels = {**_metrics_config["labels"], **(labels or {})}
    
    # Update metric based on backend
    backend = _metrics_config["backend"]
    
    if backend == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
        if full_name in _metrics:
            _metrics[full_name].labels(**combined_labels).inc(value)
    elif backend == MetricsBackend.LOGGER:
        if full_name in _metrics:
            _metrics[full_name]["value"] += value
            logger.debug(
                f"Metric {full_name} (counter) incremented by {value}: "
                f"new value = {_metrics[full_name]['value']}, labels = {combined_labels}"
            )
    elif backend == MetricsBackend.CUSTOM:
        if _metrics_config["custom_handler"]:
            _metrics_config["custom_handler"](
                name=full_name,
                metric_type="counter",
                operation="increment",
                value=value,
                labels=combined_labels
            )


def set_gauge(
    name: str,
    value: float,
    labels: Dict[str, str] = None,
    namespace: str = ""
) -> None:
    """
    Set a gauge metric.
    
    Args:
        name: Name of the metric
        value: Value to set
        labels: Labels for the metric
        namespace: Namespace for the metric (overrides prefix)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Format name with prefix
    prefix = namespace or _metrics_config["prefix"]
    full_name = f"{prefix}{name}"
    
    # Get combined labels
    combined_labels = {**_metrics_config["labels"], **(labels or {})}
    
    # Update metric based on backend
    backend = _metrics_config["backend"]
    
    if backend == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
        if full_name in _metrics:
            _metrics[full_name].labels(**combined_labels).set(value)
    elif backend == MetricsBackend.LOGGER:
        if full_name in _metrics:
            old_value = _metrics[full_name]["value"]
            _metrics[full_name]["value"] = value
            logger.debug(
                f"Metric {full_name} (gauge) set from {old_value} to {value}, "
                f"labels = {combined_labels}"
            )
    elif backend == MetricsBackend.CUSTOM:
        if _metrics_config["custom_handler"]:
            _metrics_config["custom_handler"](
                name=full_name,
                metric_type="gauge",
                operation="set",
                value=value,
                labels=combined_labels
            )


def observe_histogram(
    name: str,
    value: float,
    labels: Dict[str, str] = None,
    namespace: str = ""
) -> None:
    """
    Observe a value for a histogram metric.
    
    Args:
        name: Name of the metric
        value: Value to observe
        labels: Labels for the metric
        namespace: Namespace for the metric (overrides prefix)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Format name with prefix
    prefix = namespace or _metrics_config["prefix"]
    full_name = f"{prefix}{name}"
    
    # Get combined labels
    combined_labels = {**_metrics_config["labels"], **(labels or {})}
    
    # Update metric based on backend
    backend = _metrics_config["backend"]
    
    if backend == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
        if full_name in _metrics:
            _metrics[full_name].labels(**combined_labels).observe(value)
    elif backend == MetricsBackend.LOGGER:
        if full_name in _metrics:
            _metrics[full_name]["values"].append(value)
            logger.debug(
                f"Metric {full_name} (histogram) observed value {value}, "
                f"labels = {combined_labels}"
            )
    elif backend == MetricsBackend.CUSTOM:
        if _metrics_config["custom_handler"]:
            _metrics_config["custom_handler"](
                name=full_name,
                metric_type="histogram",
                operation="observe",
                value=value,
                labels=combined_labels
            )


def observe_summary(
    name: str,
    value: float,
    labels: Dict[str, str] = None,
    namespace: str = ""
) -> None:
    """
    Observe a value for a summary metric.
    
    Args:
        name: Name of the metric
        value: Value to observe
        labels: Labels for the metric
        namespace: Namespace for the metric (overrides prefix)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Format name with prefix
    prefix = namespace or _metrics_config["prefix"]
    full_name = f"{prefix}{name}"
    
    # Get combined labels
    combined_labels = {**_metrics_config["labels"], **(labels or {})}
    
    # Update metric based on backend
    backend = _metrics_config["backend"]
    
    if backend == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
        if full_name in _metrics:
            _metrics[full_name].labels(**combined_labels).observe(value)
    elif backend == MetricsBackend.LOGGER:
        if full_name in _metrics:
            _metrics[full_name]["count"] += 1
            _metrics[full_name]["sum"] += value
            logger.debug(
                f"Metric {full_name} (summary) observed value {value}, "
                f"count = {_metrics[full_name]['count']}, "
                f"sum = {_metrics[full_name]['sum']}, "
                f"labels = {combined_labels}"
            )
    elif backend == MetricsBackend.CUSTOM:
        if _metrics_config["custom_handler"]:
            _metrics_config["custom_handler"](
                name=full_name,
                metric_type="summary",
                operation="observe",
                value=value,
                labels=combined_labels
            )


def set_info(
    name: str,
    value: Dict[str, str],
    namespace: str = ""
) -> None:
    """
    Set an info metric.
    
    Args:
        name: Name of the metric
        value: Dictionary of labels to values
        namespace: Namespace for the metric (overrides prefix)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Format name with prefix
    prefix = namespace or _metrics_config["prefix"]
    full_name = f"{prefix}{name}"
    
    # Update metric based on backend
    backend = _metrics_config["backend"]
    
    if backend == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
        if full_name in _metrics:
            _metrics[full_name].info(value)
    elif backend == MetricsBackend.LOGGER:
        if full_name in _metrics:
            _metrics[full_name]["value"] = value
            logger.debug(
                f"Metric {full_name} (info) set to {value}"
            )
    elif backend == MetricsBackend.CUSTOM:
        if _metrics_config["custom_handler"]:
            _metrics_config["custom_handler"](
                name=full_name,
                metric_type="info",
                operation="set",
                value=value,
                labels={}
            )


# High-level metric recording functions for common operations

def record_token_validation(
    method: str,
    success: bool,
    duration_seconds: float = None,
    error: str = None
) -> None:
    """
    Record a token validation operation.
    
    This is a high-level function that updates multiple metrics:
    - token_validations_total
    - token_validation_duration_seconds
    - auth_errors_total (if error)
    
    Args:
        method: Validation method (jwt, introspection)
        success: Whether validation was successful
        duration_seconds: Duration of validation in seconds
        error: Error message (if validation failed)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Increment validation counter
    increment_counter(
        name="token_validations_total",
        labels={"method": method, "success": str(success).lower()}
    )
    
    # Record validation duration if provided
    if duration_seconds is not None:
        observe_histogram(
            name="token_validation_duration_seconds",
            value=duration_seconds,
            labels={"method": method, "success": str(success).lower()}
        )
        
    # Record error if validation failed
    if not success and error:
        increment_counter(
            name="auth_errors_total",
            labels={"error_type": "token_validation"}
        )


def record_jwks_fetch(
    success: bool,
    duration_seconds: float = None,
    error: str = None
) -> None:
    """
    Record a JWKS fetch operation.
    
    This is a high-level function that updates multiple metrics:
    - jwks_fetches_total
    - jwks_fetch_duration_seconds
    - auth_errors_total (if error)
    
    Args:
        success: Whether fetch was successful
        duration_seconds: Duration of fetch in seconds
        error: Error message (if fetch failed)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Increment fetch counter
    increment_counter(
        name="jwks_fetches_total",
        labels={"success": str(success).lower()}
    )
    
    # Record fetch duration if provided
    if duration_seconds is not None:
        observe_histogram(
            name="jwks_fetch_duration_seconds",
            value=duration_seconds,
            labels={"success": str(success).lower()}
        )
        
    # Record error if fetch failed
    if not success and error:
        increment_counter(
            name="auth_errors_total",
            labels={"error_type": "jwks_fetch"}
        )


def record_jwks_cache_age(age_seconds: float) -> None:
    """
    Record the age of the JWKS cache.
    
    Args:
        age_seconds: Age of cache in seconds
    """
    if not _metrics_config["enabled"]:
        return
        
    # Set gauge
    set_gauge(
        name="jwks_cache_age_seconds",
        value=age_seconds
    )


def record_token_introspection(
    success: bool,
    duration_seconds: float = None,
    error: str = None
) -> None:
    """
    Record a token introspection operation.
    
    This is a high-level function that updates multiple metrics:
    - token_introspections_total
    - token_introspection_duration_seconds
    - auth_errors_total (if error)
    
    Args:
        success: Whether introspection was successful
        duration_seconds: Duration of introspection in seconds
        error: Error message (if introspection failed)
    """
    if not _metrics_config["enabled"]:
        return
        
    # Increment introspection counter
    increment_counter(
        name="token_introspections_total",
        labels={"success": str(success).lower()}
    )
    
    # Record introspection duration if provided
    if duration_seconds is not None:
        observe_histogram(
            name="token_introspection_duration_seconds",
            value=duration_seconds,
            labels={"success": str(success).lower()}
        )
        
    # Record error if introspection failed
    if not success and error:
        increment_counter(
            name="auth_errors_total",
            labels={"error_type": "token_introspection"}
        )


def record_cache_access(
    cache_type: str,
    hit: bool
) -> None:
    """
    Record a cache access operation.
    
    Args:
        cache_type: Type of cache (jwks, introspection, etc.)
        hit: Whether the access was a hit or miss
    """
    if not _metrics_config["enabled"]:
        return
        
    if hit:
        increment_counter(
            name="cache_hits_total",
            labels={"cache_type": cache_type}
        )
    else:
        increment_counter(
            name="cache_misses_total",
            labels={"cache_type": cache_type}
        )


def record_token_extraction(
    source: str,
    success: bool
) -> None:
    """
    Record a token extraction operation.
    
    Args:
        source: Source of the token (header, cookie, query)
        success: Whether extraction was successful
    """
    if not _metrics_config["enabled"]:
        return
        
    increment_counter(
        name="token_extractions_total",
        labels={"source": source, "success": str(success).lower()}
    )


def record_rate_limit_hit(
    endpoint: str,
    remaining: int,
    reset_seconds: float
) -> None:
    """
    Record a rate limit hit.
    
    Args:
        endpoint: Endpoint that was rate limited
        remaining: Number of requests remaining
        reset_seconds: Seconds until rate limit resets
    """
    if not _metrics_config["enabled"]:
        return
        
    increment_counter(
        name="rate_limit_hits_total",
        labels={"endpoint": endpoint}
    )
    
    set_gauge(
        name="rate_limit_remaining",
        value=remaining,
        labels={"endpoint": endpoint}
    )
    
    observe_histogram(
        name="rate_limit_reset_seconds",
        value=reset_seconds,
        labels={"endpoint": endpoint}
    )


def record_http_request(
    method: str,
    path: str,
    status: int,
    duration: float
) -> None:
    """
    Record an HTTP request.
    
    Args:
        method: HTTP method
        path: Request path
        status: Response status code
        duration: Request duration in seconds
    """
    if not _metrics_config["enabled"]:
        return
        
    increment_counter(
        name="http_requests_total",
        labels={"method": method, "path": path, "status": str(status)}
    )
    
    observe_histogram(
        name="http_request_duration_seconds",
        value=duration,
        labels={"method": method, "path": path, "status": str(status)}
    )


class MetricsTimer:
    """
    Context manager for timing operations and recording metrics.
    
    This class provides a simple way to time operations and record
    the duration to a histogram or summary metric.
    
    Example:
        ```python
        with MetricsTimer("operation_duration_seconds", labels={"operation": "fetch"}):
            # Timed operation
            result = fetch_data()
        ```
    """
    
    def __init__(
        self,
        metric_name: str,
        labels: Dict[str, str] = None,
        namespace: str = "",
        metric_type: str = "histogram"
    ):
        """
        Initialize the timer.
        
        Args:
            metric_name: Name of the metric to record to
            labels: Labels for the metric
            namespace: Namespace for the metric (overrides prefix)
            metric_type: Type of metric (histogram or summary)
        """
        self.metric_name = metric_name
        self.labels = labels or {}
        self.namespace = namespace
        self.metric_type = metric_type
        self.start_time = None
        self.duration = None
        
    def __enter__(self) -> "MetricsTimer":
        """Start the timer."""
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Stop the timer and record the duration.
        
        Args:
            exc_type: Exception type (if an exception occurred)
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        if self.start_time is None:
            return
            
        # Calculate duration
        self.duration = time.time() - self.start_time
        
        # Add exception information to labels if an exception occurred
        if exc_type is not None:
            self.labels["exception"] = exc_type.__name__
        
        # Record the duration
        if self.metric_type == "histogram":
            observe_histogram(
                name=self.metric_name,
                value=self.duration,
                labels=self.labels,
                namespace=self.namespace
            )
        elif self.metric_type == "summary":
            observe_summary(
                name=self.metric_name,
                value=self.duration,
                labels=self.labels,
                namespace=self.namespace
            )


# Asynchronous version of MetricsTimer
class AsyncMetricsTimer:
    """
    Asynchronous context manager for timing operations and recording metrics.
    
    This class provides a simple way to time asynchronous operations and record
    the duration to a histogram or summary metric.
    
    Example:
        ```python
        async with AsyncMetricsTimer("operation_duration_seconds", labels={"operation": "fetch"}):
            # Timed operation
            result = await fetch_data()
        ```
    """
    
    def __init__(
        self,
        metric_name: str,
        labels: Dict[str, str] = None,
        namespace: str = "",
        metric_type: str = "histogram"
    ):
        """
        Initialize the timer.
        
        Args:
            metric_name: Name of the metric to record to
            labels: Labels for the metric
            namespace: Namespace for the metric (overrides prefix)
            metric_type: Type of metric (histogram or summary)
        """
        self.metric_name = metric_name
        self.labels = labels or {}
        self.namespace = namespace
        self.metric_type = metric_type
        self.start_time = None
        self.duration = None
        
    async def __aenter__(self) -> "AsyncMetricsTimer":
        """Start the timer."""
        self.start_time = time.time()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Stop the timer and record the duration.
        
        Args:
            exc_type: Exception type (if an exception occurred)
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        if self.start_time is None:
            return
            
        # Calculate duration
        self.duration = time.time() - self.start_time
        
        # Add exception information to labels if an exception occurred
        if exc_type is not None:
            self.labels["exception"] = exc_type.__name__
        
        # Record the duration
        if self.metric_type == "histogram":
            observe_histogram(
                name=self.metric_name,
                value=self.duration,
                labels=self.labels,
                namespace=self.namespace
            )
        elif self.metric_type == "summary":
            observe_summary(
                name=self.metric_name,
                value=self.duration,
                labels=self.labels,
                namespace=self.namespace
            )


def time_function(
    metric_name: str,
    labels: Dict[str, str] = None,
    namespace: str = "",
    metric_type: str = "histogram"
) -> Callable:
    """
    Decorator for timing function calls and recording metrics.
    
    This decorator provides a simple way to time function calls and record
    the duration to a histogram or summary metric.
    
    Example:
        ```python
        @time_function("function_duration_seconds", labels={"function": "fetch_data"})
        def fetch_data():
            # Implementation
        ```
    
    Args:
        metric_name: Name of the metric to record to
        labels: Labels for the metric
        namespace: Namespace for the metric (overrides prefix)
        metric_type: Type of metric (histogram or summary)
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            with MetricsTimer(metric_name, labels, namespace, metric_type):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def time_async_function(
    metric_name: str,
    labels: Dict[str, str] = None,
    namespace: str = "",
    metric_type: str = "histogram"
) -> Callable:
    """
    Decorator for timing asynchronous function calls and recording metrics.
    
    This decorator provides a simple way to time asynchronous function calls
    and record the duration to a histogram or summary metric.
    
    Example:
        ```python
        @time_async_function("function_duration_seconds", labels={"function": "fetch_data"})
        async def fetch_data():
            # Implementation
        ```
    
    Args:
        metric_name: Name of the metric to record to
        labels: Labels for the metric
        namespace: Namespace for the metric (overrides prefix)
        metric_type: Type of metric (histogram or summary)
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            async with AsyncMetricsTimer(metric_name, labels, namespace, metric_type):
                return await func(*args, **kwargs)
        return wrapper
    return decorator


# Metrics export functions

def get_metrics_data() -> Dict[str, Any]:
    """
    Get all metrics in a standardized format.
    
    Returns:
        Dict[str, Any]: Metrics data
    """
    result = {}
    
    # Get current timestamp
    timestamp = datetime.utcnow().isoformat()
    
    for name, metric in _metrics.items():
        backend = _metrics_config["backend"]
        
        if backend == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
            # For Prometheus, get the samples
            if hasattr(metric, '_metrics'):
                # Counter, Gauge
                samples = []
                for m in metric._metrics.values():
                    samples.append({
                        "value": m._value.get(),
                        "labels": m._labelvalues
                    })
                
                result[name] = {
                    "type": metric.__class__.__name__.lower(),
                    "description": metric._documentation,
                    "samples": samples,
                    "timestamp": timestamp
                }
            elif hasattr(metric, '_sum') and hasattr(metric, '_count'):
                # Summary, Histogram
                samples = []
                for m in metric._metrics.values():
                    samples.append({
                        "sum": m._sum.get(),
                        "count": m._count.get(),
                        "labels": m._labelvalues
                    })
                
                result[name] = {
                    "type": metric.__class__.__name__.lower(),
                    "description": metric._documentation,
                    "samples": samples,
                    "timestamp": timestamp
                }
        elif backend == MetricsBackend.LOGGER:
            # For logger, return the raw data
            result[name] = {
                **metric,
                "timestamp": timestamp
            }
    
    return result


def export_metrics_json() -> str:
    """
    Export metrics as JSON.
    
    Returns:
        str: JSON-formatted metrics
    """
    metrics_data = get_metrics_data()
    return json.dumps(metrics_data, indent=2)


def export_metrics_prometheus() -> str:
    """
    Export metrics in Prometheus format.
    
    Returns:
        str: Prometheus-formatted metrics
    """
    if _metrics_config["backend"] == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
        return prometheus_client.generate_latest().decode("utf-8")
    else:
        # Convert non-Prometheus metrics to Prometheus format
        lines = []
        
        for name, data in get_metrics_data().items():
            # Add metric metadata
            metric_type = data.get("type", "unknown")
            description = data.get("description", "")
            
            lines.append(f"# HELP {name} {description}")
            lines.append(f"# TYPE {name} {metric_type}")
            
            # Add samples
            samples = data.get("samples", [])
            for sample in samples:
                # Format labels
                sample_labels = sample.get("labels", {})
                if sample_labels:
                    labels_str = ",".join([f'{k}="{v}"' for k, v in sample_labels.items()])
                    labels_str = f"{{{labels_str}}}"
                else:
                    labels_str = ""
                
                # Format value based on metric type
                if metric_type in ("counter", "gauge"):
                    value = sample.get("value", 0)
                    lines.append(f"{name}{labels_str} {value}")
                elif metric_type in ("histogram", "summary"):
                    sum_value = sample.get("sum", 0)
                    count_value = sample.get("count", 0)
                    lines.append(f"{name}_sum{labels_str} {sum_value}")
                    lines.append(f"{name}_count{labels_str} {count_value}")
        
        return "\n".join(lines)


def create_fastapi_metrics_endpoint(prefix: str = "/metrics") -> Callable:
    """
    Create a FastAPI endpoint for exposing Prometheus metrics.
    
    This function returns a FastAPI route handler that can be used to
    expose Prometheus metrics on a given endpoint.
    
    Args:
        prefix: URL prefix for the metrics endpoint
        
    Returns:
        Callable: FastAPI route handler
    """
    if not _metrics_config["enabled"]:
        return None
        
    async def metrics_endpoint():
        """Expose Prometheus metrics."""
        if _metrics_config["backend"] == MetricsBackend.PROMETHEUS and PROMETHEUS_AVAILABLE:
            return prometheus_client.generate_latest()
        else:
            # Return metrics in Prometheus format even if using a different backend
            return export_metrics_prometheus()
        
    return metrics_endpoint


def get_metrics_status() -> Dict[str, Any]:
    """
    Get the current status of the metrics system.
    
    This function returns a dictionary with information about the
    metrics system configuration and registered metrics.
    
    Returns:
        Dict[str, Any]: Metrics system status
    """
    return {
        "enabled": _metrics_config["enabled"],
        "backend": _metrics_config["backend"].value,
        "prefix": _metrics_config["prefix"],
        "labels": _metrics_config["labels"],
        "metrics_count": len(_metrics),
        "metrics_names": list(_metrics.keys()),
        "timestamp": datetime.utcnow().isoformat()
    }


class MetricsMiddleware:
    """
    FastAPI middleware for collecting authentication metrics.
    
    This middleware automatically collects metrics for authentication
    operations on FastAPI requests.
    """
    
    def __init__(self, app, enable_timing: bool = True):
        """
        Initialize the middleware.
        
        Args:
            app: FastAPI application
            enable_timing: Whether to enable request timing
        """
        self.app = app
        self.enable_timing = enable_timing
        
    async def __call__(self, scope, receive, send):
        """
        Process a request and collect metrics.
        
        Args:
            scope: ASGI scope
            receive: ASGI receive function
            send: ASGI send function
        """
        if scope["type"] != "http":
            # Call the next middleware/app directly for non-HTTP requests
            await self.app(scope, receive, send)
            return
            
        # Start timing if enabled
        start_time = time.time() if self.enable_timing else None
        
        # Extract request details
        method = scope.get("method", "UNKNOWN")
        path = scope.get("path", "UNKNOWN")
        
        # Wrap the send function to capture response status
        auth_error = False
        status_code = 500  # Default to 500 if not set
        original_send = send
        
        async def wrapped_send(message):
            nonlocal auth_error, status_code
            if message["type"] == "http.response.start":
                # Capture status code
                status_code = message["status"]
                
                # Check if this was an authentication error
                if message["status"] in (401, 403):
                    auth_error = True
                    if _metrics_config["enabled"]:
                        increment_counter(
                            name="auth_errors_total",
                            labels={"error_type": f"http_{message['status']}"}
                        )
            
            await original_send(message)
            
        # Call the next middleware/app
        try:
            await self.app(scope, receive, wrapped_send)
        finally:
            # Record timing metrics if enabled
            if self.enable_timing and start_time is not None and _metrics_config["enabled"]:
                duration = time.time() - start_time
                
                # Record HTTP request metrics
                record_http_request(
                    method=method,
                    path=path,
                    status=status_code,
                    duration=duration
                )
