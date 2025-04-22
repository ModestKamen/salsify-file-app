import asyncio
import sys
from pathlib import Path
from file_api_app.repository import FileRepository
from file_api_app.file_index_repository import FileIndexRepository
from file_api_app.file_reader import FileReader
import pytest
import pytest_asyncio
from file_api_app.aiohttp_app import init_app


pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def get_1_100_shard_file_repository_index() -> FileIndexRepository:
    """Fixture to create a FileRepository instance for testing."""
    # Create a mock index repository
    index_file_reader = FileReader(
        file_path="tests/test_data/shard_1_100_index.txt",
    )

    return FileIndexRepository(
        first_line_number=1, last_line_number=100, file_reader=index_file_reader
    )


@pytest.fixture
def get_101_200_shard_file_repository_index() -> FileIndexRepository:
    """Fixture to create a FileRepository instance for testing."""
    # Create a mock index repository
    index_file_reader = FileReader(
        file_path="tests/test_data/shard_101_200_index.txt",
    )

    return FileIndexRepository(
        first_line_number=101,
        last_line_number=200,
        file_reader=index_file_reader,
    )


@pytest.fixture
def get_1_100_shard_repository() -> FileRepository:
    """Fixture to create a FileRepository instance for testing."""
    # Create a mock index repository
    index_file_reader = FileReader(
        file_path="tests/test_data/shard_1_100_index.txt",
    )
    repository_file_reader = FileReader(
        file_path="tests/test_data/shard_1_100.txt"
    )

    index_repository = FileIndexRepository(
        first_line_number=1, last_line_number=100, file_reader=index_file_reader
    )

    file_repository = FileRepository(
        index_repository=index_repository, file_reader=repository_file_reader
    )
    return file_repository


@pytest.fixture
def get_101_200_shard_repository() -> FileRepository:
    """Fixture to create a FileRepository instance for testing."""
    # Create a mock index repository
    index_file_reader = FileReader(
        file_path="tests/test_data/shard_101_200_index.txt",
    )
    repository_file_reader = FileReader(
        file_path="tests/test_data/shard_101_200.txt"
    )
    index_repository = FileIndexRepository(
        first_line_number=101,
        last_line_number=200,
        file_reader=index_file_reader,
    )

    file_repository = FileRepository(
        index_repository=index_repository, file_reader=repository_file_reader
    )
    return file_repository


@pytest_asyncio.fixture
async def get_1_100_shard_repository_app(
    get_1_100_shard_repository,
) -> FileRepository:
    """Fixture to create a FileRepository instance for testing."""
    # Create a mock index repository
    app = await init_app()
    app["file_repository"] = get_1_100_shard_repository
    return app


@pytest_asyncio.fixture
async def get_101_200_shard_repository_app(
    get_101_200_shard_repository,
) -> FileRepository:
    """Fixture to create a FileRepository instance for testing."""
    app = await init_app()
    app["file_repository"] = get_101_200_shard_repository
    return app
