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
from src.PacMan.renderer.renderer_engine import (PyGMLXImageEmulator,
                                                 PyMLXPNGEmulator,)
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import GhostName
from src.PacMan.renderer.drawer_engine import BoardDrawerEngine

if TYPE_CHECKING:  # only required for parameter type assignment 
    from src.PacMan.renderer.renderer_assembler import RendererAssembler

T = TypeVar('T', IEventEnums, GhostName, BoardDrawerEngine)

logger = logging.getLogger(__name__)


class ImageLoaderStrategy(ABC):
    """The interface all specific image loaders must implement."""
    
    # @abstractmethod
    # def can_handle(self, folder_path: Path, usage_type: str) -> bool:
    #     """Determines if this specific loader should process this case."""
    #     pass

    @overload
    def load(self,
             folder: str,
             assembler: RendererAssembler) -> ImgsAsset:
        ...

    @overload
    def load(self,
             folder: str,
             assembler: RendererAssembler,
             configurator: T) -> ImgsAsset:
        ...

    @abstractmethod
    def load(self,
             folder: str,
             assembler: RendererAssembler,
             configurator: T | None = None) -> ImgsAsset:
        """The specific implementation of the loading logic."""
        pass


class BackgroundLoaderStrategy(ImageLoaderStrategy):
    def load(
            self,
            folder: str,
            assembler: RendererAssembler
    ) -> ImgsAsset:
        w = assembler._config.size
        hub = int(assembler._config.size / assembler._config.hub_panels_prop)
        h = w + 2 * hub
        metadata: ImgMetadata = ImgMetadata(
                x_pos_prop=0,
                y_pos_prop=0,
                default_color=0xff000000
            )
        source = Source(
            img=PyGMLXImageEmulator(w, h),
            metadata=metadata
        )
        for y in range(h):
            for x in range(w):
                source.img.pygput_pixel(
                    x,
                    y,
                    metadata.default_color
                )
        return ImgsAsset(
            asset_name=folder,
            sources={
                folder: source
            }
        )



class LivesLoaderStrategy(ImageLoaderStrategy):
    def load(
            self,
            folder: str,
            assembler: RendererAssembler            
    ) -> ImgsAsset:
        _assets = assembler.cwd.parent / 'assets' / folder
        _names = [folder.split('/')[-1].upper() for i in range(3)]
        imgassets: ImgsAsset = ImgsAsset(asset_name=folder.split('/')[-1])
        try:
            for i, stem in enumerate(_names):
                path = _assets / Path(stem + '.png')
                if not path.is_file():
                    logger.exception(f"FATAL: we could not load image : {path}")
                    raise SystemExit(1)
                with Image.open(path) as img:
                    org_w, org_h = img.size
                metadata: ImgMetadata = ImgMetadata()
                img = PyMLXPNGEmulator(
                            org_w,
                            org_h
                        )
                img.pygput_from_png(
                            str(path)
                        )
                metadata.resize_w_prop = 1/(2 * assembler._config.nb_cells)
                metadata.resize_h_prop = 1/(2 * assembler._config.nb_cells)
                rsize_w = int(org_w * metadata.resize_w_prop)
                rsize_h = int(org_h * metadata.resize_h_prop)
                metadata.x_pos_prop = int(assembler._config.size / 2)
                num_slots = len(_names) + 4
                metadata.x_pos_prop += int(i * 2 * assembler._config.size / num_slots)
                metadata.y_pos_prop = assembler._config.size + int(assembler._config.size / assembler._config.hub_panels_prop)
                img.pygll_resize(
                            rsize_w,
                            rsize_h
                        )
                source = Source(
                    path=path,
                    img=img,
                    metadata=metadata
                )
                imgassets.sources.update(
                    {
                        stem: source
                    }
                )
            return imgassets
        except Exception as err:
            logger.exception(f"FATAL: we could not load images : {err}")
            raise SystemExit(1)


class BoardLoaderStrategy(ImageLoaderStrategy):
    def load(
            self,
            folder: str,
            assembler: RendererAssembler,
            configurator: BoardDrawerEngine
    ) -> ImgsAsset:
        source = Source(
            img=PyGMLXImageEmulator(
                    configurator.corrected_size[0],
                    configurator.corrected_size[0]
                ),
            metadata=ImgMetadata(
                x_pos_prop=int(configurator.margin / 2),
                y_pos_prop=int(configurator.margin / 2) + int(assembler._config.size / assembler._config.hub_panels_prop),
            )
        )
        return ImgsAsset(
            asset_name=folder,
            sources={
                folder: source
            }
        )


class MenuLoaderStrategy(ImageLoaderStrategy):
    def load(
            self,
            folder: str,
            assembler: RendererAssembler,
            configurator: IEventEnums
    ) -> ImgsAsset:
        _assets = assembler.cwd.parent / 'assets' / folder
        try:
            _names = getattr(configurator, '_member_names_')
        except Exception as err:
            logger.exception(f"FATAL: a specific configurator type is required : {err}")
            raise SystemExit(1)    
        imgassets: ImgsAsset = ImgsAsset(asset_name=folder.split('/')[-1])
        try:
            for i, stem in enumerate(_names):
                path = _assets / Path(stem + '.png')
                if not path.is_file():
                    logger.exception(f"FATAL: we could not load image : {path}")
                    raise SystemExit(1)
                with Image.open(path) as img:
                    org_w, org_h = img.size
                metadata: ImgMetadata = ImgMetadata()
                img = PyMLXPNGEmulator(
                            org_w,
                            org_h
                        )
                img.pygput_from_png(
                            str(path)
                        )
                metadata.resize_w_prop = 1/3
                metadata.resize_h_prop = 1/4
                rsize_w = int(org_w * metadata.resize_w_prop)
                rsize_h = int(org_h * metadata.resize_h_prop)
                metadata.x_pos_prop = (assembler._config.size / 2) - int(rsize_w / 2)
                metadata.y_pos_prop = int(assembler._config.size / assembler._config.hub_panels_prop)
                num_slots = len(_names) + 11
                metadata.y_pos_prop += int((i + 1) * 2 * assembler._config.size / num_slots)
                img.pygll_resize(
                            rsize_w,
                            rsize_h
                        )
                source = Source(
                    path=path,
                    img=img,
                    metadata=metadata
                )
                imgassets.sources.update(
                    {
                        stem: source
                    }
                )
            return imgassets
        except Exception as err:
            logger.exception(f"FATAL: we could not load images : {err}")
            raise SystemExit(1)


class GhostsLoaderStrategy(ImageLoaderStrategy):
    def load(
            self,
            folder: str,
            assembler: RendererAssembler,
            configurator: GhostName
    ) -> ImgsAsset:
        _assets = assembler.cwd.parent / 'assets' / folder
        try:
            print(folder, vars(configurator))
            _names = getattr(configurator, '_member_names_')
            if configurator.__name__ == 'GhostName':
                _names = _names + ['DEAD', 'POWERUP']
            else:
                raise
        except Exception as err:
            logger.exception(f"FATAL: a specific configurator type is required : {err}")
            raise SystemExit(1)    
        imgassets: ImgsAsset = ImgsAsset(asset_name=folder.split('/')[-1])
        try:
            for stem in _names:
                print(folder, stem)
                path = _assets / Path(stem + '.png')
                if not path.is_file():
                    logger.exception(f"FATAL: we could not load image : {path}")
                    raise SystemExit(1)
                with Image.open(path) as img:
                    org_w, org_h = img.size
                # print(fname, org_w)
                img = PyMLXPNGEmulator(
                            org_w,
                            org_h
                        )
                img.pygput_from_png(
                            str(path)
                        )
                metadata: ImgMetadata = ImgMetadata()
                metadata.resize_w_prop = 1/(2 * assembler._config.nb_cells)
                metadata.resize_h_prop = 1/(2 * assembler._config.nb_cells)
                rsize_w = int(org_w * metadata.resize_w_prop)
                rsize_h = int(org_h * metadata.resize_h_prop)
                img.pygll_resize(
                            rsize_w,
                            rsize_h
                        )
                source = Source(
                    path=path,
                    img=img,
                    metadata=metadata
                )
                imgassets.sources.update(
                    {
                        stem: source
                    }
                )
            return imgassets
        except Exception as err:
            logger.exception(f"FATAL: we could not load images : {err}")
            raise SystemExit(1)


class PacManLoaderStrategy(ImageLoaderStrategy):
    def load(
            self,
            folder: str,
            assembler: RendererAssembler,
            configurator: IEventEnums
    ) -> ImgsAsset:
        _assets = assembler.cwd.parent / 'assets' / folder
        print(folder, vars(configurator))
        try:
            _names = getattr(configurator, '_member_names_')
            _names.remove('PAUSE')
            _temp_sources: list[Source] = []
            _files = [f'{n}-{str(v)}' for v in range(1, 4, 1) for n in _names]
        except Exception as err:
            logger.exception(f"FATAL: a specific configurator type is required : {err}")
            raise SystemExit(1)            
        imgassets: ImgsAsset = ImgsAsset(asset_name=folder.split('/')[-1])
        try:
            for stem in _names:
                for f in _files:
                    if stem in f:
                        path = _assets / stem / Path(f + '.png')
                    else:
                        continue
                    if not path.is_file():
                        logger.exception(f"FATAL: we could not load image : {path}")
                        raise SystemExit(1)
                    with Image.open(path) as img:
                        org_w, org_h = img.size
                    # print(fname, org_w)
                    img = PyMLXPNGEmulator(
                                org_w,
                                org_h
                            )
                    img.pygput_from_png(
                                str(path)
                            )
                    metadata: ImgMetadata = ImgMetadata()
                    metadata.resize_w_prop = 1/(2 * assembler._config.nb_cells)
                    metadata.resize_h_prop = 1/(2 * assembler._config.nb_cells)
                    rsize_w = int(org_w * metadata.resize_w_prop)
                    rsize_h = int(org_h * metadata.resize_h_prop) 
                    img.pygll_resize(
                                rsize_w,
                                rsize_h
                            )
                    source = Source(
                        event_name=f,
                        path=path,
                        img=img,
                        metadata=metadata
                    )
                    _temp_sources.append(source)
            for e in _names:
                q = []
                for s in _temp_sources:
                    if e in s.event_name:
                        q.append(s)
                q = sorted(
                    q,
                    key=lambda iats: int(iats.event_name.split('-')[-1])
                )
                imgassets.sources[e] = deque(q)
            return imgassets
        except Exception as err:
            logger.exception(f"FATAL: we could not load images : {err}")
            raise SystemExit(1)