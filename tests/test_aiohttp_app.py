import pytest

from file_api_app.aiohttp_app import init_app
from file_api_app.file_index_repository import FileIndexRepository
from file_api_app.repository import FileRepository

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
class TestGetLineHandler:
    async def test_get_first_line_from_1_100_shard(
        self, get_1_100_shard_repository_app, aiohttp_client
    ):
        # Arrange
        client = await aiohttp_client(get_1_100_shard_repository_app)
        expected_line = "1:c6ac2c49-c2d0-4ca3-8403-0998c67f8c31"

        # Act
        resp = await client.get("/lines/1")

        # Assert
        assert resp.status == 200
        data = await resp.json()
        assert data["line"] == expected_line

    async def test_get_last_line_from_1_100_shard(
        self, get_1_100_shard_repository_app, aiohttp_client
    ):
        # Arrange
        client = await aiohttp_client(get_1_100_shard_repository_app)
        expected_line = "100:b701c8da-b4d1-44f7-b116-131fed74f71d"

        # Act
        resp = await client.get("/lines/100")

        # Assert
        assert resp.status == 200
        data = await resp.json()
        assert data["line"] == expected_line

    async def test_get_negative_line_from_1_100_shard(
        self, get_1_100_shard_repository_app, aiohttp_client
    ):
        # Arrange
        client = await aiohttp_client(get_1_100_shard_repository_app)

        # Act
        resp = await client.get("/lines/-1")

        # Assert
        assert resp.status == 400

    async def test_get_out_of_index_line_from_1_100_shard(
        self, get_1_100_shard_repository_app, aiohttp_client
    ):
        # Arrange
        client = await aiohttp_client(get_1_100_shard_repository_app)

        # Act
        resp = await client.get("/lines/101")

        # Assert
        assert resp.status == 413

    async def test_get_zero_line_from_1_100_shard(
        self, get_1_100_shard_repository_app, aiohttp_client
    ):
        # Arrange
        client = await aiohttp_client(get_1_100_shard_repository_app)

        # Act
        resp = await client.get("/lines/0")

        # Assert
        assert resp.status == 404

    async def test_get_first_line_from_101_200_shard(
        self, get_101_200_shard_repository_app, aiohttp_client
    ):
        # Arrange
        client = await aiohttp_client(get_101_200_shard_repository_app)
        expected_line = "101:5cdb7794-88d7-47ac-a346-640e7ecd10c2"

        # Act
        resp = await client.get("/lines/101")

        # Assert
        assert resp.status == 200
        data = await resp.json()
        assert data["line"] == expected_line

    async def test_get_last_line_from_101_200_shard(
        self, get_101_200_shard_repository_app, aiohttp_client
    ):
        # Arrange
        client = await aiohttp_client(get_101_200_shard_repository_app)
        expected_line = "200:c62a989e-91bf-4039-a9ed-53416c4acac1"

        # Act
        resp = await client.get("/lines/200")

        # Assert
        assert resp.status == 200
        data = await resp.json()
        assert data["line"] == expected_line

    async def test_get_negative_line_from_101_200_shard(
        self, get_101_200_shard_repository_app, aiohttp_client
    ):
        # Arrange
        client = await aiohttp_client(get_101_200_shard_repository_app)

        # Act
        resp = await client.get("/lines/-1")

        # Assert
        assert resp.status == 400

    async def test_get_out_of_index_line_from_101_200_shard(
        self, get_101_200_shard_repository_app, aiohttp_client
    ):
        # Arrange
        client = await aiohttp_client(get_101_200_shard_repository_app)

        # Act
        resp = await client.get("/lines/201")

        # Assert
        assert resp.status == 413

    async def test_get_zero_line_from_101_200_shard(
        self, get_101_200_shard_repository_app, aiohttp_client
    ):
        # Arrange
        client = await aiohttp_client(get_101_200_shard_repository_app)

        # Act
        resp = await client.get("/lines/0")

        # Assert
        assert resp.status == 404
