import pytest

from file_api_app.file_index_repository import (
    FileIndexRepository,
    LineExceedsIndexRange,
    LineIsOutOfIndexRange,
)
from file_api_app.repository import FileRepository
from file_api_app.file_reader import FileReader


@pytest.mark.asyncio
async def test_get_first_line(get_1_100_shard_repository):
    """Test retrieving the first line from the repository."""
    # Test first line (line 1)
    line_content = await get_1_100_shard_repository.get_line(1)
    assert isinstance(line_content, str)
    assert len(line_content) > 0


@pytest.mark.asyncio
async def test_get_last_line(get_1_100_shard_repository):
    """Test retrieving the last line from the repository."""
    # Test last line (line 100)
    line_content = await get_1_100_shard_repository.get_line(100)
    assert isinstance(line_content, str)
    assert len(line_content) > 0


@pytest.mark.asyncio
async def test_get_middle_line(get_1_100_shard_repository):
    """Test retrieving a line from the middle of the repository."""
    # Test middle line (line 50)
    line_content = await get_1_100_shard_repository.get_line(50)
    assert isinstance(line_content, str)
    assert len(line_content) > 0


@pytest.mark.asyncio
async def test_second_shard_boundaries(get_101_200_shard_repository):
    """Test boundary conditions for the second shard."""
    # Test first line of second shard
    first_line = await get_101_200_shard_repository.get_line(101)
    assert isinstance(first_line, str)
    assert len(first_line) > 0

    # Test last line of second shard
    last_line = await get_101_200_shard_repository.get_line(200)
    assert isinstance(last_line, str)
    assert len(last_line) > 0
