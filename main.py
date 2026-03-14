import uvicorn

from src.config.fastapi import fastapi_app_factory

app = fastapi_app_factory()

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
