import logging
from aiohttp import web
from aiohttp.web_middlewares import middleware

from file_api_app.file_index_repository import FileIndexRepository
from file_api_app.handlers import get_line
from file_api_app.repository import FileRepository
from file_api_app.settings import Settings
from file_api_app.file_reader import FileReader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@middleware
async def request_logging_middleware(request, handler):
    """Middleware to log all incoming requests and their processing time"""
    import time

    start_time = time.time()

    response = await handler(request)

    duration = time.time() - start_time
    logger.info(
        f"Request {request.method} {request.path} completed with status {response.status} in {duration:.3f}s"
    )
    return response


async def init_app() -> web.Application:
    app = web.Application(middlewares=[request_logging_middleware])
    settings = Settings()
    app["settings"] = settings

    logger.info(f"Initializing application on {settings.host}:{settings.port}")

    index_file_reader = FileReader(file_path=settings.index_file_path)
    repository_file_reader = FileReader(settings.file_repository_file_path)

    index_repository = FileIndexRepository(
        first_line_number=settings.index_first_line_number,
        last_line_number=settings.index_last_line_number,
        file_reader=index_file_reader,
    )

    file_repository = FileRepository(
        file_reader=repository_file_reader,
        index_repository=index_repository,
    )

    # Store repository in app state
    app["file_repository"] = file_repository
    logger.info(
        f"File repository initialized with index range: {settings.index_first_line_number}-{settings.index_last_line_number}"
    )

    # Setup routes
    app.router.add_get("/lines/{line_number}", get_line)
    logger.info("Routes configured successfully")

    return app
