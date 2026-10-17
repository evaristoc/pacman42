from typing import Optional
from pydantic import Field, BaseModel, model_validator


class ValidBoardConfig(BaseModel):
    size: Optional[int] = Field(default=None, ge=500, le=1000)
    nb_cells: Optional[int] = Field(default=None, ge=10, le=30)


class ValidAppEntriesConfig(BaseModel):
    board: ValidBoardConfig

    @model_validator(mode='before')
    @classmethod
    def assemble_sub_configs(cls, data: dict) -> dict:
        if "board" not in data:
            data["board"] = {
                "size": data.get("size"),
                "nb_cells": data.get("nb_cells")
            }
        return data
