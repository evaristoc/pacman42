import json
import logging
from typing import Any
from src.PacMan.validation_contracts.valid_game_config import (
                                    ValidAppEntriesConfig)

logger = logging.getLogger(__name__)


# TODO work on error handling
class DataProcessor:
    @staticmethod
    def load_dataset(valid_path: str) -> dict[str, Any]:
        """
        Loads JSON dataset.
        """
        try:
            with open(valid_path, "r", encoding="utf-8") as f:
                raw_data: dict[str, Any] = json.load(f)
            if raw_data is None:
                raise FileNotFoundError("config file not found at:"
                                        f"{valid_path}")
            return raw_data
        except (json.JSONDecodeError, KeyError):
            logger.critical("FATAL: unable to load config json.")
            raise SystemExit()
        except Exception:
            logger.critical("FATAL: unknown error when trying to"
                            "load config json.")
            raise SystemExit()

    @classmethod
    def resolve_and_validate(cls, **kwargs: Any) -> ValidAppEntriesConfig:
        payload: dict[str, Any] = {}
        # Discover all submodels and their fields
        submodels: dict[str, Any] = {}
        for model_name, field_info\
                in ValidAppEntriesConfig.model_fields.items():
            sub_model = field_info.annotation
            if sub_model is not None and hasattr(sub_model, "model_fields"):
                submodels[model_name] = sub_model.model_fields
        # Count how many submodels contain each field
        field_occurrences: dict[str, int] = {}
        for fields in submodels.values():
            for field_name in fields:
                field_occurrences[field_name] = (
                    field_occurrences.get(field_name, 0) + 1
                )
        # Resolve each submodel
        for model_name, fields in submodels.items():
            submodel_payload = {}
            for field_name in fields:
                if field_occurrences[field_name] > 1:
                    # Ambiguous → identity is required
                    input_name = f"{model_name.upper()}_{field_name.upper()}"
                else:
                    # Unique → generic name
                    input_name = field_name
                val = kwargs.get(input_name)
                if val is None:
                    # TODO temporary set to None while I revise its use later
                    val = None
                if val is not None:
                    submodel_payload[field_name] = val
            if submodel_payload:
                payload[model_name] = submodel_payload
        try:
            return ValidAppEntriesConfig(**payload)
        except Exception:
            raise
