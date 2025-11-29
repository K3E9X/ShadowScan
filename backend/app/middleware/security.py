"""
Security Middleware
Implements various security controls including anti-SSRF, security headers, and request logging
"""

import re
import time
import ipaddress
import structlog
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from fastapi import status

logger = structlog.get_logger(__name__)

# Private IP ranges (RFC 1918, RFC 4193, loopback, link-local)
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("::1/128"),
]


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"

        # Remove server header
        response.headers.pop("Server", None)

        return response


class AntiSSRFMiddleware(BaseHTTPMiddleware):
    """
    Prevent Server-Side Request Forgery attacks
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check for URL parameters in request body
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                content_type = request.headers.get("content-type", "")
                if "application/json" in content_type:
                    body = await request.json()
                    if self._contains_suspicious_url(body):
                        logger.warning(
                            "Potential SSRF attempt detected",
                            path=request.url.path,
                            ip=request.client.host
                        )
                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={"detail": "Invalid URL detected"}
                        )
            except Exception:
                pass

        response = await call_next(request)
        return response

    def _contains_suspicious_url(self, data: dict) -> bool:
        """
        Recursively check for suspicious URLs in request data
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if self._is_suspicious_url_field(key, value):
                    return True
                if isinstance(value, (dict, list)):
                    if self._contains_suspicious_url(value):
                        return True
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    if self._contains_suspicious_url(item):
                        return True
        return False

    def _is_suspicious_url_field(self, key: str, value: any) -> bool:
        """
        Check if a field contains a suspicious URL
        """
        if not isinstance(value, str):
            return False

        # Check if key suggests URL content
        url_keys = ["url", "uri", "link", "href", "callback", "webhook"]
        if any(k in key.lower() for k in url_keys):
            # Check for private IP addresses
            if self._contains_private_ip(value):
                return True

            # Check for localhost, metadata endpoints
            suspicious_patterns = [
                r"localhost",
                r"127\.0\.0\.1",
                r"0\.0\.0\.0",
                r"169\.254\.169\.254",  # AWS metadata
                r"metadata\.google\.internal",  # GCP metadata
                r"\[::1\]",
                r"file://",
            ]
            for pattern in suspicious_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    return True

        return False

    def _contains_private_ip(self, value: str) -> bool:
        """
        Check if string contains private IP address
        """
        # Extract potential IP addresses
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        potential_ips = re.findall(ip_pattern, value)

        for ip_str in potential_ips:
            try:
                ip = ipaddress.ip_address(ip_str)
                for network in PRIVATE_IP_RANGES:
                    if ip in network:
                        return True
            except ValueError:
                continue

        return False


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Log all requests with timing information
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Extract request details
        request_id = request.headers.get("X-Request-ID", "unknown")
        user_agent = request.headers.get("User-Agent", "unknown")
        client_ip = request.client.host if request.client else "unknown"

        logger.info(
            "Request started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            ip=client_ip,
            user_agent=user_agent
        )

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration = time.time() - start_time

        # Log response
        logger.info(
            "Request completed",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2)
        )

        # Add request ID to response
        response.headers["X-Request-ID"] = request_id

        return response


class InputSanitizationMiddleware(BaseHTTPMiddleware):
    """
    Sanitize input to prevent injection attacks
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check for common injection patterns
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                content_type = request.headers.get("content-type", "")
                if "application/json" in content_type:
                    body = await request.json()
                    if self._contains_injection_patterns(body):
                        logger.warning(
                            "Potential injection attempt detected",
                            path=request.url.path,
                            ip=request.client.host
                        )
                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={"detail": "Invalid input detected"}
                        )
            except Exception:
                pass

        response = await call_next(request)
        return response

    def _contains_injection_patterns(self, data: any) -> bool:
        """
        Check for SQL injection, XSS, and command injection patterns
        """
        if isinstance(data, str):
            # SQL injection patterns
            sql_patterns = [
                r"(\bunion\b.*\bselect\b)",
                r"(\bor\b\s*\d+\s*=\s*\d+)",
                r"(;\s*drop\s+table)",
                r"(--\s*$)",
                r"(/\*.*\*/)",
            ]

            # Command injection patterns
            cmd_patterns = [
                r"(\||&&|;)\s*(cat|ls|wget|curl|nc|bash|sh)",
                r"`.*`",
                r"\$\(.*\)",
            ]

            all_patterns = sql_patterns + cmd_patterns
            for pattern in all_patterns:
                if re.search(pattern, data, re.IGNORECASE):
                    return True

        elif isinstance(data, dict):
            for value in data.values():
                if self._contains_injection_patterns(value):
                    return True

        elif isinstance(data, list):
            for item in data:
                if self._contains_injection_patterns(item):
                    return True

        return False
