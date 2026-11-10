import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from src.PacMan.renderer.assets import (
                                Source,
                                TextMetadata,
                                ImgsAsset,
                                )
from src.PacMan.renderer.renderer_engine import (
                                    PyGMLXTextEmulator)
# only required for parameter type assignment
if TYPE_CHECKING:
    from src.PacMan.renderer.renderer_assembler import RendererAssembler


logger = logging.getLogger(__name__)


class TextLoaderStrategy(ABC):
    @abstractmethod
    def upload_text(
            self,
            asset_name: str,
            msg: str,
            assembler: 'RendererAssembler'
            ) -> ImgsAsset:
        ...


class HubTextLoaderStrategy(TextLoaderStrategy):
    def upload_text(
            self,
            folder: str,
            msg: str,
            assembler: 'RendererAssembler'
            ) -> ImgsAsset:
        if (assembler is None or
                assembler._config is None or
                assembler._config.nb_cells is None and
                assembler._config.size is None or
                assembler._config.hub_panels_prop is None):
            logger.error(f"Parameters of {folder} loader should have a value")
            raise SystemExit(1)
        imgasset: ImgsAsset = ImgsAsset(asset_name=folder)
        metadata: TextMetadata = TextMetadata()
        metadata.text_template = msg
        metadata.text = msg
        metadata.font_path = 'CONSOLA.ttf'
        metadata.font_size_prop = 20.8
        metadata.color = 0xF6303F
        metadata.text_x_prop = 5
        metadata.text_y_prop = 5
        metadata.x_pos_prop = 0
        if assembler._config.size is not None:
            metadata.y_pos_prop = 0 if 'top' in folder else (
                assembler._config.size + int(assembler._config.size /
                                             assembler._config.hub_panels_prop)
                )
            w = assembler._config.size
            h = int(assembler._config.size /
                    assembler._config.hub_panels_prop)
            font_size = int(assembler._config.size /
                            metadata.font_size_prop)
            source = Source(
                img=PyGMLXTextEmulator(
                                width=w,
                                height=h,
                                font_path=metadata.font_path,
                                font_size=font_size,
                                color=metadata.color
                                ),
                metadata=metadata,
            )
        if metadata and metadata.bg_color is not None:
            for y in range(h):
                for x in range(w):
                    source.img.pygput_pixel(
                        x,
                        y,
                        metadata.bg_color
                    )
        if isinstance(source.img, PyGMLXTextEmulator):
            source.img.pygput_from_text(
                                metadata.text_x_prop,
                                metadata.text_y_prop,
                                metadata.text)
        imgasset.sources.update(
            {
                folder: source,
            }
        )
        return imgasset
