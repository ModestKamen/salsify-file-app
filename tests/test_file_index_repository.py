import pytest
from file_api_app.file_index_repository import (
    FileIndexRepository,
    LineExceedsIndexRange,
    LineIsOutOfIndexRange,
    NegativeLineNumber,
)


@pytest.mark.asyncio
class TestRepositoryFileIndex:
    @pytest.mark.asyncio
    async def test_get_first_line_bytes_offset_ok(
        self, get_1_100_shard_file_repository_index
    ):
        """Test successful byte offset retrieval within valid range."""
        index_repository = get_1_100_shard_file_repository_index
        # Test line number in valid range (1-100)
        byte_offset = await index_repository.get_line_bytes_offset(1)
        assert isinstance(byte_offset, int)
        assert byte_offset == 0

    @pytest.mark.asyncio
    async def test_get_second_line_bytes_offset_ok(
        self, get_1_100_shard_file_repository_index
    ):
        """Test successful byte offset retrieval within valid range."""
        index_repository = get_1_100_shard_file_repository_index
        # Test line number in valid range (1-100)
        byte_offset = await index_repository.get_line_bytes_offset(2)
        assert isinstance(byte_offset, int)
        assert byte_offset == 39

    @pytest.mark.asyncio
    async def test_line_exceeds_index_range(
        self, get_1_100_shard_file_repository_index
    ):
        """Test when line number is above the valid range."""
        index_repository = get_1_100_shard_file_repository_index
        with pytest.raises(LineExceedsIndexRange) as exc_info:
            await index_repository.get_line_bytes_offset(101)
        assert "Line number 101 is outside valid range [1, 100]" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_line_is_out_of_index_range(
        self, get_1_100_shard_file_repository_index
    ):
        """Test when line number is below the valid range but positive."""
        index_repository = get_1_100_shard_file_repository_index
        with pytest.raises(LineIsOutOfIndexRange) as exc_info:
            await index_repository.get_line_bytes_offset(0)
        assert "Line number 0 is outside valid range [1, 100]" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_negative_line_number(
        self, get_1_100_shard_file_repository_index
    ):
        """Test when line number is negative."""
        index_repository = get_1_100_shard_file_repository_index
        with pytest.raises(NegativeLineNumber) as exc_info:
            await index_repository.get_line_bytes_offset(-1)
        assert "Line number -1 cannot be negative" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_boundary_conditions(
        self, get_1_100_shard_file_repository_index
    ):
        """Test boundary conditions (first and last valid line numbers)."""
        index_repository = get_1_100_shard_file_repository_index

        # Test first valid line number
        first_offset = await index_repository.get_line_bytes_offset(1)
        assert isinstance(first_offset, int)
        assert first_offset == 0

        # Test last valid line number
        last_offset = await index_repository.get_line_bytes_offset(100)
        assert isinstance(last_offset, int)
        assert last_offset == 3951
