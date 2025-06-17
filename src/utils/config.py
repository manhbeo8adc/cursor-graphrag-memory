"""
Configuration Management
Mục đích: Centralized configuration với environment variables
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30


@dataclass
class RedisConfig:
    """Redis configuration"""
    url: str
    

@dataclass
class GeminiConfig:
    """Gemini AI configuration"""
    api_key: str
    model: str = "gemini-2.5-flash"
    temperature: float = 0.1
    max_tokens: int = 2048


@dataclass
class MCPConfig:
    """MCP Server configuration"""
    server_name: str = "cursor-graphiti-memory"
    server_version: str = "1.0.0"
    port: int = 8000


@dataclass
class AppConfig:
    """Main application configuration"""
    project_name: str
    environment: str
    log_level: str
    database: DatabaseConfig
    redis: RedisConfig
    gemini: GeminiConfig
    mcp: MCPConfig


def load_config() -> AppConfig:
    """
    Load configuration from environment variables
    SRP: Chỉ lo việc load config
    """
    # Required environment variables
    required_vars = {
        "GEMINI_API_KEY": "Gemini API key is required",
        "DATABASE_URL": "Database URL is required",
        "REDIS_URL": "Redis URL is required"
    }
    
    # Check required variables
    missing_vars = []
    for var, message in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"{var}: {message}")
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables:\n" + "\n".join(missing_vars))
    
    # Create configuration
    return AppConfig(
        project_name=os.getenv("PROJECT_NAME", "cursor_graphrag_memory"),
        environment=os.getenv("ENVIRONMENT", "development"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        
        database=DatabaseConfig(
            url=os.getenv("DATABASE_URL"),
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
            pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30"))
        ),
        
        redis=RedisConfig(
            url=os.getenv("REDIS_URL")
        ),
        
        gemini=GeminiConfig(
            api_key=os.getenv("GEMINI_API_KEY"),
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            temperature=float(os.getenv("GEMINI_TEMPERATURE", "0.1")),
            max_tokens=int(os.getenv("GEMINI_MAX_TOKENS", "2048"))
        ),
        
        mcp=MCPConfig(
            server_name=os.getenv("MCP_SERVER_NAME", "cursor-graphiti-memory"),
            server_version=os.getenv("MCP_SERVER_VERSION", "1.0.0"),
            port=int(os.getenv("MCP_SERVER_PORT", "8000"))
        )
    )


# Global config instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """
    Get global configuration instance - Singleton pattern
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config
