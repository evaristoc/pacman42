from typing import Optional
from pydantic import Field, BaseModel, model_validator


class ValidBoardConfig(BaseModel):
    width: Optional[int] = Field(default=None, ge=3, le=20)
    height: Optional[int] = Field(default=None, ge=3, le=20)


class ValidAppEntriesConfig(BaseModel):
    board: ValidBoardConfig

    @model_validator(mode='before')
    @classmethod
    def assemble_sub_configs(cls, data: dict) -> dict:
        if "board" not in data:
            data["board"] = {
                "width": data.get("width"),
                "height": data.get("height")
            }
        return data
