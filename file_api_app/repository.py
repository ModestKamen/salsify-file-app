import aiofiles

from .file_index_repository import FileIndexRepository
from .file_reader import FileReader


class FileRepository:
    def __init__(
        self, index_repository: FileIndexRepository, file_reader: FileReader
    ):
        """
        Initialize the FileRepository with file path and index repository.

        :param index_repository: Instance of FileIndexRepository for handling index operations.
        :param file_reader: FileReader instance for reading file content.
        """
        self.index_repository = index_repository
        self.file_reader = file_reader

    async def get_line_content_data(self, byte_position: int) -> str:
        """
        Read a line from the main file starting at the given byte position.

        :param byte_position: The byte position to start reading from
        :return: The content of the line as a string, with trailing newlines removed
        """
        line = await self.file_reader.async_read_line(byte_position)
        return line.rstrip("\n")

    async def get_line(self, line_number: int) -> str:
        """
        Get a specific line from the file using the index file for positioning.

        :param line_number: The line number to retrieve
        :return: The content of the requested line
        """
        # Get byte position from index repository
        byte_position = await self.index_repository.get_line_bytes_offset(
            line_number
        )

        return await self.get_line_content_data(byte_position)
