"""
Application Configuration
Centralized configuration using Pydantic Settings
"""

from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with validation
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )

    # Application
    APP_NAME: str = "ShadowScan"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = Field(default="production", pattern="^(development|staging|production)$")

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # Security
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALLOWED_HOSTS: List[str] = ["*"]

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://shadowscan:shadowscan@localhost:5432/shadowscan"
    )
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600  # 1 hour

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # AI Services
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    AI_MODEL_CODE: str = "claude-3-5-sonnet-20241022"
    AI_MODEL_VISION: str = "claude-3-5-sonnet-20241022"
    AI_MAX_TOKENS: int = 4096
    AI_TEMPERATURE: float = 0.1

    # File Upload
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/png", "image/jpeg", "image/svg+xml"]
    ALLOWED_CODE_EXTENSIONS: List[str] = [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go",
        ".rs", ".c", ".cpp", ".php", ".rb", ".cs", ".swift", ".kt"
    ]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_PER_HOUR: int = 1000
    ANALYSIS_RATE_LIMIT: str = "10/hour"  # Max 10 analyses per hour per user

    # Security Analysis
    CODE_MAX_LINES: int = 10000
    CODE_ANALYSIS_TIMEOUT: int = 300  # 5 minutes
    DIAGRAM_ANALYSIS_TIMEOUT: int = 300

    # Monitoring
    ENABLE_METRICS: bool = True
    LOG_LEVEL: str = "INFO"

    # External Services
    SEMGREP_TIMEOUT: int = 120
    BANDIT_TIMEOUT: int = 60

    # Storage
    STORAGE_BACKEND: str = Field(default="local", pattern="^(local|s3|gcs)$")
    STORAGE_PATH: str = "./storage"
    S3_BUCKET: Optional[str] = None
    S3_REGION: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None

    # Email (for notifications)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None

    # Feature Flags
    ENABLE_AUTH: bool = False  # Disable auth for MVP
    ENABLE_CODE_ANALYSIS: bool = True
    ENABLE_DIAGRAM_ANALYSIS: bool = True
    ENABLE_SECRETS_DETECTION: bool = True
    ENABLE_DEPENDENCY_SCANNING: bool = True


# Global settings instance
settings = Settings()
