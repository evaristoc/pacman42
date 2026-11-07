import logging
from collections import deque
from abc import ABC, abstractmethod
from pathlib import Path
from PIL import Image
from typing import Any, TypeVar, overload, TYPE_CHECKING
from src.PacMan.validation_contracts.event_enums import (
                                            IEventEnums)
from src.PacMan.renderer.assets import (
                                Source,
                                ImgMetadata,
                                TextMetadata,
                                ImgsAsset,
                                )
from src.PacMan.renderer.renderer_engine import (PyGMLXTextEmulator)
if TYPE_CHECKING:  # only required for parameter type assignment 
    from src.PacMan.renderer.renderer_assembler import RendererAssembler


logger = logging.getLogger(__name__)


class TextLoaderStrategy(ABC):
    @abstractmethod
    def upload_text(
            self,
            asset_name: str,
            msg: str,
            assembler: RendererAssembler
            ) -> ImgsAsset:
        ...


class HubTextLoaderStrategy(TextLoaderStrategy):
    def upload_text(
            self,
            asset_name: str,
            msg: str,
            assembler: RendererAssembler
            ) -> ImgsAsset:
        imgasset: ImgsAsset = ImgsAsset(asset_name=asset_name)
        metadata: TextMetadata = TextMetadata()
        metadata.text = msg
        metadata.font_path = 'CONSOLA.ttf'
        metadata.font_size_prop = 20.8
        metadata.color = 0xF6303F
        metadata.text_x_prop = 5
        metadata.text_y_prop = 5
        metadata.x_pos_prop = 0
        metadata.y_pos_prop = 0 if 'top' in asset_name else (
            assembler._config.size + int(assembler._config.size /
                                         assembler._config.hub_panels_prop)
            )
        source = Source(
            img=PyGMLXTextEmulator(
                            assembler._config.size,
                            int(
                                assembler._config.size /
                                assembler._config.hub_panels_prop),
                            metadata.font_path,
                            int(assembler._config.size *
                                metadata.font_size_prop),
                            metadata.color
                            ),
            metadata=metadata
        )
        source.img.pygput_from_text(
                            metadata.text_x_prop,
                            metadata.text_y_prop,
                            metadata.text)
        imgasset.sources.update(
            {
                asset_name: source
            }
        )
        return imgasset
