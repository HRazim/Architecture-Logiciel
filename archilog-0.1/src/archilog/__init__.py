import os
import logging
from dataclasses import dataclass

@dataclass
class Config:
    DATABASE_URL: str
    DEBUG: bool
    SECRET_KEY: str
    LOG_LEVEL: str

# Configuration par défaut
config = Config(
    DATABASE_URL=os.getenv("ARCHILOG_DATABASE_URL", "sqlite:///data.db"),
    DEBUG=os.getenv("ARCHILOG_DEBUG", "False") == "True",
    SECRET_KEY=os.getenv("ARCHILOG_FLASK_SECRET_KEY", "your_secret_key_here"),
    LOG_LEVEL=os.getenv("ARCHILOG_LOG_LEVEL", "INFO")
)

"""Configure le système de logging"""
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("archilog.log"),
        logging.StreamHandler()
    ]
)