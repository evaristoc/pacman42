from typing import Optional
from pydantic import Field, BaseModel, model_validator


class ValidBoardConfig(BaseModel):
    cheat: bool = Field(default=False)
    size: Optional[int] = Field(default=None, ge=500, le=1000)
    nb_cells: Optional[int] = Field(default=None, ge=10, le=30)
    hub_panels_prop: Optional[int] = Field(default=None, ge=0, le=5)


class ValidAppEntriesConfig(BaseModel):
    board: ValidBoardConfig

    @model_validator(mode='before')
    @classmethod
    def assemble_sub_configs(cls, data: dict) -> dict:
        if "board" not in data:
            data["board"] = {
                "cheat": data.get("cheat"),
                "size": data.get("size"),
                "nb_cells": data.get("nb_cells"),
                "hub_panels_prop": data.get("hub_panels_prop")
            }
        return data
