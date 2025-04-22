from pydantic_settings import BaseSettings
from pydantic import FilePath, Field, validator


class Settings(BaseSettings):
    # Application settings
    host: str = "0.0.0.0"  # Default to all interfaces
    port: int = 8000  # Default port

    # File settings
    index_file_path: FilePath
    index_first_line_number: int = Field(gt=0)
    index_last_line_number: int = Field(gt=0)

    file_repository_file_path: FilePath

    @validator("index_last_line_number")
    def validate_line_numbers(cls, v, values):
        if "index_first_line_number" in values:
            if v < values["index_first_line_number"]:
                raise ValueError(
                    "last_line_number must be greater than or equal to first_line_number"
                )
        return v

    class Config:
        env_file = ".env-local"
        case_sensitive = False
