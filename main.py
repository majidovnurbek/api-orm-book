from fastapi import FastAPI, Depends
from config import get_settings, Settings

app = FastAPI()


@app.get("/")
def read_root(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "debug_mode": settings.app_debug,
        "version": settings.app_version,
    }


@app.get("/db")
def get_db_config(settings: Settings = Depends(get_settings)):
    return {
        "host": settings.db_host,
        "port": settings.db_port,
        "user": settings.db_user,
        "database": settings.db_name,
        "tk": settings.token,
    }