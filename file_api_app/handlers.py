import logging
from aiohttp import web

from file_api_app.repository import FileRepository
from file_api_app.file_index_repository import (
    LineExceedsIndexRange,
    LineIsOutOfIndexRange,
    NegativeLineNumber,
)

logger = logging.getLogger(__name__)


async def get_line(request):
    """
    Handler that retrieves a specific line from the file using the repository from app state.
    """
    try:
        file_repository: FileRepository = request.app["file_repository"]
        line_number = int(request.match_info["line_number"])
        logger.debug(f"Processing request for line number: {line_number}")

        line = await file_repository.get_line(line_number)
        logger.debug(f"Successfully retrieved line {line_number}")
        return web.json_response({"line": line})
    except LineExceedsIndexRange as e:
        logger.warning(f"Line number exceeds index range: {line_number}")
        return web.json_response({"error": str(e)}, status=413)
    except NegativeLineNumber as e:
        logger.warning(f"Negative line number requested: {line_number}")
        return web.json_response({"error": str(e)}, status=400)
    except LineIsOutOfIndexRange as e:
        logger.warning(f"Line number out of index range: {line_number}")
        return web.json_response({"error": str(e)}, status=404)
    except Exception as e:
        logger.error(
            f"Unexpected error processing line {line_number}: {str(e)}",
            exc_info=True,
        )
        return web.json_response({"error": str(e)}, status=500)
