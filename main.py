import os
import uvicorn
from core.config import config


def main():
    uvicorn.run(
        app="app.main:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.ENV != "production" else False,
        workers=config.WORKERS_COUNT,
    )


if __name__ == "__main__":
    main()
