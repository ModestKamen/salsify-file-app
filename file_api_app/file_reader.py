import aiofiles


class FileReader:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    async def async_read_line(self, bytes_offset: int) -> str:
        """
        Asynchronously read lines from a file starting from a given byte offset.

        :param bytes_offset: The byte offset to start reading from
        :return: The read string
        """
        async with aiofiles.open(self.file_path) as file:
            await file.seek(bytes_offset)
            line = await file.readline()
            return line

    def read_line(self, bytes_offset: int) -> str:
        """
        Synchronously read line from a file starting from a given byte offset.

        :param bytes_offset: The byte offset to start reading from
        :return: The read string
        """
        with open(self.file_path) as file:
            file.seek(bytes_offset)
            line = file.readline()
            return line
