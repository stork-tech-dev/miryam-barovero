"""
Configuraciones específicas para Railway (referencia / futuro).
"""
import os


def get_railway_config():
    config = {}
    if "PORT" in os.environ:
        config["PORT"] = os.environ["PORT"]
    if "DATABASE_URL" in os.environ:
        config["DATABASE_URL"] = os.environ["DATABASE_URL"]
    if "RAILWAY_STATIC_URL" in os.environ:
        config["STATIC_URL"] = os.environ["RAILWAY_STATIC_URL"]
    return config


RAILWAY_RECOMMENDATIONS = {
    "DEBUG": False,
    "IS_PRODUCTION": True,
    "DB_ENGINE": "postgresql",
}
