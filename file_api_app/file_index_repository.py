import aiofiles
from .file_reader import FileReader


class LineExceedsIndexRange(Exception):
    """Exception raised when requested line number is outside the valid range."""

    pass


class LineIsOutOfIndexRange(Exception):
    """Exception raised when requested line number is outside the valid range."""

    pass


class NegativeLineNumber(ValueError):
    """Exception raised when line number is negative."""

    pass


class FileIndexRepository:
    def __init__(
        self,
        first_line_number: int,
        last_line_number: int,
        file_reader: FileReader,
    ):
        """
        Initialize the FileIndexRepository.

        :param first_line_number: First valid line number in the index (inclusive)
        :param last_line_number: Last valid line number in the index (inclusive)
        :param file_reader: FileReader instance for reading file content
        """
        self.entry_length = 13
        self.first_line_number = first_line_number
        self.last_line_number = last_line_number

        self.file_reader = file_reader
        self._first_file_value = self._get_first_entry_value()

    def _get_first_entry_value(self) -> int:
        raw_value = self.file_reader.read_line(0)
        value = raw_value.strip()
        return int(value.lstrip("0") or "0")

    def _check_line_fits_index_range(self, line_number: int) -> None:
        """
        Check if the line number is within the valid range.

        :param line_number: The line number to check.
        :raises LineExceedsIndexRange: If the line number is above the valid range.
        :raises LineIsOutOfIndexRange: If the line number is below the first line number.
        :raises NegativeLineNumber: If the line number is negative.
        """
        if line_number < 0:
            raise NegativeLineNumber(
                f"Line number {line_number} cannot be negative"
            )
        if line_number > self.last_line_number:
            raise LineExceedsIndexRange(
                f"Line number {line_number} is outside valid range [{self.first_line_number}, {self.last_line_number}]"
            )
        if line_number < self.first_line_number:
            raise LineIsOutOfIndexRange(
                f"Line number {line_number} is outside valid range [{self.first_line_number}, {self.last_line_number}]"
            )

    async def read_line_from_index(self, index_offset: int) -> int:
        raw_byte_position_str = await self.file_reader.async_read_line(
            index_offset
        )
        byte_position_str = raw_byte_position_str.strip()
        return (
            int(byte_position_str.lstrip("0") or "0") - self._first_file_value
        )

    def _calculate_line_byte_offset(self, line_number: int) -> int:
        """
        Calculate the byte offset in the file based on the index entry length and line number.

        :param line_number: The line number for which to calculate the byte offset.
        :return: The byte offset in the file.
        """
        return self.entry_length * (line_number - self.first_line_number)

    async def get_line_bytes_offset(self, line_number: int) -> int:
        """
        Get the byte position for a specific line number from the index file.

        :param line_number: The line number to get the byte position for
        :return: The byte position as an integer
        :raises LineExceedsIndexRange: If the line number is outside the valid range
        """
        self._check_line_fits_index_range(line_number)
        index_offset = self._calculate_line_byte_offset(line_number)
        return await self.read_line_from_index(index_offset)
