from typing import Optional
from pydantic import Field, BaseModel, model_validator


class ValidBoardConfig(BaseModel):
    cheat: bool = Field(default=False)
    nb_cells: int = Field(default=5, ge=5, le=30)
    hub_panels_prop: int = Field(default=5, ge=0, le=5)
    size: int = Field(default=500, ge=500, le=1000)


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
