import logging
from aiohttp import web
from file_api_app.aiohttp_app import init_app
from file_api_app.settings import Settings

logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting File API application")
    settings = Settings()
    app = init_app()
    logger.info(
        f"Application initialized, starting server on {settings.host}:{settings.port}"
    )
    web.run_app(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
