"""
Application settings and configuration
Loads from environment variables and TOML config file
"""
import os
import toml
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict


class Settings(BaseSettings):
    """Application settings"""
    
    # App Configuration
    app_name: str = "Smart App"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database Configuration
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./smtapp.db"
    )
    
    # Ollama Configuration
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://192.168.100.25:11434")
    ollama_timeout: int = 120
    ollama_default_model: str = "llama2"
    
    # HuggingFace Configuration
    huggingface_api_key: Optional[str] = os.getenv("HUGGINGFACE_API_KEY")
    huggingface_cache_dir: str = "./models/huggingface"
    default_embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # File Processing
    max_file_size_mb: int = 100
    upload_dir: str = "./uploads"
    temp_dir: str = "./temp"
    supported_formats: List[str] = [
        "pdf", "docx", "doc", "txt", "md",
        "xlsx", "xls", "csv",
        "json", "xml",
        "jpg", "jpeg", "png", "gif",
        "mp3", "wav", "mp4", "avi"
    ]
    
    # Vector Configuration
    vector_dimensions: int = 384
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # TOML Config
    toml_config: Optional[Dict] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached)
    Loads from environment variables and TOML config
    """
    settings = Settings()
    
    # Try to load TOML configuration
    toml_path = Path(__file__).parent.parent.parent / "config" / "app.toml"
    if toml_path.exists():
        try:
            settings.toml_config = toml.load(toml_path)
            
            # Override with TOML values if available
            if "app" in settings.toml_config:
                app_config = settings.toml_config["app"]
                settings.app_name = app_config.get("name", settings.app_name)
                settings.app_version = app_config.get("version", settings.app_version)
                settings.debug = app_config.get("debug", settings.debug)
            
            if "ollama" in settings.toml_config:
                ollama_config = settings.toml_config["ollama"]
                settings.ollama_base_url = ollama_config.get("base_url", settings.ollama_base_url)
                settings.ollama_timeout = ollama_config.get("timeout", settings.ollama_timeout)
                settings.ollama_default_model = ollama_config.get("default_model", settings.ollama_default_model)
            
            if "processing" in settings.toml_config:
                proc_config = settings.toml_config["processing"]
                settings.max_file_size_mb = proc_config.get("max_file_size_mb", settings.max_file_size_mb)
                settings.upload_dir = proc_config.get("upload_dir", settings.upload_dir)
                settings.temp_dir = proc_config.get("temp_dir", settings.temp_dir)
                
        except Exception as e:
            print(f"Warning: Could not load TOML config: {e}")
    
    # Create necessary directories
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.temp_dir).mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    return settings


def get_toml_config(section: Optional[str] = None) -> Dict:
    """
    Get TOML configuration
    
    Args:
        section: Optional section name to get specific config section
        
    Returns:
        Dictionary with configuration
    """
    settings = get_settings()
    if settings.toml_config is None:
        return {}
    
    if section:
        return settings.toml_config.get(section, {})
    
    return settings.toml_config

