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


class TextLoader(ABC):
    @abstractmethod
    def upload_text(
            self,
            asset_name: str,
            msg: str,
            assembler: 'RendererAssembler'
            ) -> ImgsAsset:
        ...


class InputTextLoader(TextLoader):
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
        metadata.font_path = 'CHANGO.TTF'
        metadata.font_size_prop = 18.8
        metadata.color = 0x2D2D2D
        metadata.bg_color = 0xFFFFFFFF
        metadata.text_x_prop = 5
        metadata.text_y_prop = 5
        if assembler._config.size is not None:
            tot_w = assembler._config.size
            hub = int(assembler._config.size /
                      assembler._config.hub_panels_prop)
            tot_h = tot_w + 2 * hub
            font_size = int(assembler._config.size /
                            metadata.font_size_prop)
            h = 2 * font_size
            w = 15 * font_size
            metadata.x_pos_prop = int(tot_w / 2) - int(w / 2)
            metadata.y_pos_prop = int(tot_h / 2)
            source = Source(
                img=PyGMLXTextEmulator(
                                width=w,
                                height=h,
                                font_path=metadata.font_path,
                                font_size=font_size,
                                color=metadata.color
                                ),
                metadata=metadata,
                type='computed'
            )
        if metadata and metadata.bg_color is not None:
            for y in range(h):
                for x in range(w):
                    source.img.pygput_pixel(
                        x,
                        y,
                        metadata.bg_color
                    )
        # if isinstance(source.img, PyGMLXTextEmulator):
        #     source.img.pygput_from_text(
        #                         metadata.text_x_prop,
        #                         metadata.text_y_prop,
        #                         metadata.text)
        imgasset.sources.update(
            {
                folder: source,
            }
        )
        return imgasset


class MsgTextLoader(TextLoader):
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
        metadata.font_path = 'CHANGO.TTF'
        metadata.font_size_prop = 40.8
        metadata.color = 0xCBCBCB
        metadata.bg_color = 0xFF000000
        metadata.text_x_prop = 0
        metadata.text_y_prop = 0
        if assembler._config.size is not None:
            tot_w = assembler._config.size
            hub = int(assembler._config.size /
                      assembler._config.hub_panels_prop)
            tot_h = tot_w + 2 * hub
            font_size = int(assembler._config.size /
                            metadata.font_size_prop)
            h = int(30 * font_size)
            w = int(tot_w * 2 / 3)
            above_fontsize = int(assembler._config.size / 23)
            metadata.x_pos_prop = int(tot_w / 2) - int(w / 2)
            metadata.y_pos_prop = int(tot_h / 2) + 3 * above_fontsize
            source = Source(
                img=PyGMLXTextEmulator(
                                width=w,
                                height=h,
                                font_path=metadata.font_path,
                                font_size=font_size,
                                color=metadata.color
                                ),
                metadata=metadata,
                type='computed'
            )
        if metadata and metadata.bg_color is not None:
            for y in range(h):
                for x in range(w):
                    source.img.pygput_pixel(
                        x,
                        y,
                        metadata.bg_color
                    )
        # if isinstance(source.img, PyGMLXTextEmulator):
        #     source.img.pygput_from_text(
        #                         metadata.text_x_prop,
        #                         metadata.text_y_prop,
        #                         metadata.text)
        imgasset.sources.update(
            {
                folder: source,
            }
        )
        return imgasset


class HubTextLoader(TextLoader):
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
        metadata.font_path = 'CHANGO.TTF'
        metadata.font_size_prop = 22.8
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
                type='computed'
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


class InfoTextLoader(TextLoader):
    def upload_text(
            self,
            folder: str,
            msg: str,
            assembler: 'RendererAssembler'
            ) -> ImgsAsset:
        if (assembler is None or
                assembler._config is None or
                assembler._config.size is None or
                assembler._config.hub_panels_prop is None):
            logger.error(f"Parameters of {folder} loader should have a value")
            raise SystemExit(1)
        imgasset: ImgsAsset = ImgsAsset(asset_name=folder)
        metadata: TextMetadata = TextMetadata()
        metadata.text_template = msg
        metadata.text = msg
        metadata.font_path = 'CHANGO.TTF'
        metadata.font_size_prop = 22.8
        metadata.color = 0xF6303F
        metadata.text_x_prop = 5
        metadata.text_y_prop = 5
        metadata.x_pos_prop = 0
        if (assembler._config.size is not None
                and assembler._config.hub_panels_prop is not None):
            metadata.y_pos_prop = int(assembler._config.size /
                                      assembler._config.hub_panels_prop)
            w = assembler._config.size
            h = assembler._config.size
            font_size = int(assembler._config.size /
                            metadata.font_size_prop)
            source = Source(
                event_name=folder,
                img=PyGMLXTextEmulator(
                                width=w,
                                height=h,
                                font_path=metadata.font_path,
                                font_size=font_size,
                                color=metadata.color
                                ),
                metadata=metadata,
                type='computed'
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
