import logging
from collections import deque
from abc import ABC, abstractmethod
from pathlib import Path
from PIL import Image
from typing import Union, TypeVar, TYPE_CHECKING
from src.PacMan.validation_contracts.event_enums import (
                                            IEventEnums)
from src.PacMan.renderer.assets import (
                                Source,
                                ImgMetadata,
                                ImgsAsset
                                )
from src.PacMan.renderer.renderer_engine import (PyGMLXImageEmulator,
                                                 PyMLXPNGEmulator,)
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import GhostName
from src.PacMan.renderer.drawer_engine import BoardDrawerEngine
if TYPE_CHECKING:
    from src.PacMan.renderer.renderer_assembler import RendererAssembler


ConfiguratorT = TypeVar('ConfiguratorT', bound=Union[type[IEventEnums],
                                                     type[GhostName],
                                                     BoardDrawerEngine])

logger = logging.getLogger(__name__)


class ImageLoader(ABC):
    """The interface all specific image loaders must implement."""
    @abstractmethod
    def load(self,
             folder: str,
             assembler: 'RendererAssembler',
             configurator: ConfiguratorT | None = None) -> ImgsAsset:
        """The specific implementation of the loading logic."""
        pass


class BackgroundLoader(ImageLoader):
    def load(
            self,
            folder: str,
            assembler: 'RendererAssembler',
            configurator: ConfiguratorT | None = None
    ) -> ImgsAsset:
        if configurator:
            logger.error("configurator should not be accessed for this "
                         "strategy")
            raise SystemExit(1)
        if (assembler is None or
                assembler._config.hub_panels_prop is None or
                assembler._config.size is None):
            logger.error(f"Parameters of {folder} loader should have a value")
            raise SystemExit(1)
        else:
            w = assembler._config.size
            hub = int(assembler._config.size /
                      assembler._config.hub_panels_prop)
            h = w + 2 * hub
        metadata: ImgMetadata = ImgMetadata(
                x_pos_prop=0,
                y_pos_prop=0,
                bg_color=0xff000000
            )
        source = Source(
            img=PyGMLXImageEmulator(w, h),
            metadata=metadata,
        )
        for y in range(h):
            for x in range(w):
                if metadata.bg_color is not None:
                    source.img.pygput_pixel(
                        x,
                        y,
                        metadata.bg_color
                    )
        return ImgsAsset(
            asset_name=folder,
            sources={
                folder: source
            }
        )


class LivesLoader(ImageLoader):
    def load(
            self,
            folder: str,
            assembler: 'RendererAssembler',
            configurator: ConfiguratorT | None = None
    ) -> ImgsAsset:
        if configurator:
            logger.error("configurator should not be accessed for this "
                         "strategy")
            raise SystemExit(1)
        if (assembler is None or
                assembler._config.hub_panels_prop is None or
                assembler._config.size is None):
            logger.error(f"Parameters of {folder} loader should have a value")
            raise SystemExit(1)
        _assets = assembler.cwd.parent / 'assets' / folder
        _names = [folder.split('/')[-1].upper() for i in range(3)]
        imgassets: ImgsAsset = ImgsAsset(asset_name=folder.split('/')[-1])
        try:
            for i, stem in enumerate(_names):
                path = _assets / Path(stem + '.png')
                if not path.is_file():
                    logger.exception("FATAL: we could not load image"
                                     f" : {path}")
                    raise SystemExit(1)
                with Image.open(path) as imgf:
                    org_w, org_h = imgf.size
                metadata: ImgMetadata = ImgMetadata()
                img = PyMLXPNGEmulator(
                            org_w,
                            org_h
                        )
                img.pygput_from_png(
                            str(path)
                        )
                if (assembler is not None or
                        assembler._config is not None or
                        assembler._config.nb_cells is not None and
                        assembler._config.size is not None or
                        assembler._config.hub_panels_prop is not None):
                    if assembler._config.nb_cells is not None:
                        metadata.resize_w_prop = 1/(2 * assembler
                                                    ._config.nb_cells)
                        metadata.resize_h_prop = 1/(2 * assembler
                                                    ._config.nb_cells)
                        rsize_w = int(org_w * metadata.resize_w_prop)
                        rsize_h = int(org_h * metadata.resize_h_prop)
                    metadata.x_pos_prop = int(assembler._config.size / 2)
                    num_slots = len(_names) + 4
                    metadata.x_pos_prop += int(i * 2 *
                                               assembler
                                               ._config.size / num_slots)
                    metadata.y_pos_prop = (
                        assembler
                            ._config.size + int(assembler._config.size /
                                                assembler
                                                ._config.hub_panels_prop))
                img.pygll_resize(
                            rsize_w,
                            rsize_h
                        )
                source = Source(
                    path=path,
                    img=img,
                    metadata=metadata,
                    type='png'
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


class BoardLoader(ImageLoader):
    def load(
            self,
            folder: str,
            assembler: 'RendererAssembler',
            configurator: ConfiguratorT | None = None
    ) -> ImgsAsset:
        assert configurator is not None
        if (assembler is None or
                assembler._config is None or
                assembler._config.nb_cells is None and
                assembler._config.size is None or
                assembler._config.hub_panels_prop is None):
            logger.error(f"Parameters of {folder} loader should have a value")
            raise SystemExit(1)
        if (isinstance(configurator, BoardDrawerEngine)
                and assembler._config.size is not None):
            metadata: ImgMetadata = ImgMetadata(
                    x_pos_prop=int(configurator.margin / 2),
                    y_pos_prop=(int(configurator.margin / 2)
                                + int(assembler._config.size /
                                      assembler._config.hub_panels_prop)),
                    bg_color=0xFF000000
                )
            source = Source(
                img=PyGMLXImageEmulator(
                        configurator.corrected_size[0],
                        configurator.corrected_size[0]
                    ),
                metadata=metadata
            )
            for y in range(configurator.corrected_size[0]):
                for x in range(configurator.corrected_size[0]):
                    if metadata.bg_color is not None:
                        source.img.pygput_pixel(
                            x,
                            y,
                            metadata.bg_color
                        )
        return ImgsAsset(
            asset_name=folder,
            sources={
                folder: source
            }
        )


class MenuLoader(ImageLoader):
    def load(
            self,
            folder: str,
            assembler: 'RendererAssembler',
            configurator: ConfiguratorT | None = None
    ) -> ImgsAsset:
        assert configurator is not None
        if (assembler is None or
                assembler._config is None or
                assembler._config.nb_cells is None and
                assembler._config.size is None or
                assembler._config.hub_panels_prop is None):
            logger.error(f"Parameters of {folder} loader should have a value")
            raise SystemExit(1)
        _assets = assembler.cwd.parent / 'assets' / folder
        try:
            _names = getattr(configurator, '_member_names_')[:]
        except Exception as err:
            logger.exception("FATAL: a specific configurator type is required"
                             f" : {err}")
            raise SystemExit(1)
        imgassets: ImgsAsset = ImgsAsset(asset_name=folder.split('/')[-1])
        # max_w: float = assembler._config.size * .7
        # max_wpb: int = int(max_w / len(_names))
        max_h: int = int(assembler._config.size / 15)
        try:
            for i, stem in enumerate(_names):
                print(folder, stem)
                path = _assets / Path(stem + '.png')
                if not path.is_file():
                    logger.exception("FATAL: we could not load image"
                                     f" : {path}")
                    raise SystemExit(1)
                with Image.open(path) as imgf:
                    org_w, org_h = imgf.size
                    # max_wpb = max(min(org_w, max_wpb), int(assembler._config.size * .3))
                    # max_hpb: int = int(max_wpb / max_w * org_h)
                metadata: ImgMetadata = ImgMetadata()
                img = PyMLXPNGEmulator(
                            org_w,
                            org_h
                        )
                img.pygput_from_png(
                            str(path)
                        )
                # metadata.resize_w_prop = 1/3
                # metadata.resize_h_prop = 1/4
                # rsize_w = int(org_w * metadata.resize_w_prop)
                # rsize_h = int(org_h * metadata.resize_h_prop)
                # rsize_w = max_wpb
                # rsize_h = max_hpb
                rsize_h = int(sum([max_h, org_h]) / 2)
                wh_ratio: float = org_w / org_h
                rsize_w: int = int(wh_ratio * max_h)
                if assembler._config.size is not None:
                    metadata.x_pos_prop = (
                        int(assembler._config.size / 2) - int(rsize_w / 2))
                    metadata.y_pos_prop = (int(assembler._config.size /
                                               assembler
                                               ._config.hub_panels_prop))
                    num_slots = len(_names) + 11
                    metadata.y_pos_prop += (int((i + 1) * 2 * assembler
                                                ._config.size / num_slots))
                img.pygll_resize(
                            rsize_w,
                            rsize_h
                        )
                source = Source(
                    event_name=stem,
                    path=path,
                    img=img,
                    metadata=metadata,
                    type='png'
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


class GhostsLoader(ImageLoader):
    def load(
            self,
            folder: str,
            assembler: 'RendererAssembler',
            configurator: ConfiguratorT | None = None
    ) -> ImgsAsset:
        assert configurator is not None
        if (assembler is None or
                assembler._config is None or
                assembler._config.nb_cells is None and
                assembler._config.size is None or
                assembler._config.hub_panels_prop is None):
            logger.error(f"Parameters of {folder} loader should have a value")
            raise SystemExit(1)
        _assets = assembler.cwd.parent / 'assets' / folder
        try:
            # print(folder, vars(configurator))
            _names = getattr(configurator, '_member_names_')[:]
            if configurator is GhostName:
                _names = _names + ['DEAD', 'POWERUP']
            else:
                raise
        except Exception as err:
            logger.exception("FATAL: a specific configurator type is required"
                             f" : {err}")
            raise SystemExit(1)
        imgassets: ImgsAsset = ImgsAsset(asset_name=folder.split('/')[-1])
        try:
            for stem in _names:
                # print(folder, stem)
                path = _assets / Path(stem + '.png')
                if not path.is_file():
                    logger.exception("FATAL: we could not load image"
                                     f" : {path}")
                    raise SystemExit(1)
                with Image.open(path) as imgf:
                    org_w, org_h = imgf.size
                # print(fname, org_w)
                img = PyMLXPNGEmulator(
                            org_w,
                            org_h
                        )
                img.pygput_from_png(
                            str(path)
                        )
                metadata: ImgMetadata = ImgMetadata()
                if assembler._config.nb_cells is not None:
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
                    metadata=metadata,
                    type='png'
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


class PacManLoader(ImageLoader):
    def load(
            self,
            folder: str,
            assembler: 'RendererAssembler',
            configurator: ConfiguratorT | None = None
    ) -> ImgsAsset:
        assert configurator is not None
        if (assembler is None or
                assembler._config is None or
                assembler._config.nb_cells is None and
                assembler._config.size is None or
                assembler._config.hub_panels_prop is None):
            logger.error(f"Parameters of {folder} loader should have a value")
            raise SystemExit(1)
        _assets = assembler.cwd.parent / 'assets' / folder
        # folder, vars(configurator))
        try:
            _names = getattr(configurator, '_member_names_')[:]
            _names.remove('PAUSE')
            _names.remove('LEVEL_SKIP')
            _temp_sources: list[Source] = []
            _files = [f'{n}-{str(v)}' for v in range(1, 4, 1) for n in _names]
        except Exception as err:
            logger.exception("FATAL: a specific configurator type is required"
                             f" : {err}")
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
                        logger.exception("FATAL: we could not load image"
                                         f" : {path}")
                        raise SystemExit(1)
                    with Image.open(path) as imgf:
                        org_w, org_h = imgf.size
                    # print(fname, org_w)
                    img = PyMLXPNGEmulator(
                                org_w,
                                org_h
                            )
                    img.pygput_from_png(
                                str(path)
                            )
                    metadata: ImgMetadata = ImgMetadata()
                    if assembler._config.nb_cells is not None:
                        metadata.resize_w_prop = 1/(2 *
                                                    assembler._config.nb_cells)
                        metadata.resize_h_prop = 1/(2 *
                                                    assembler._config.nb_cells)
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
                        metadata=metadata,
                        type='deque_png'
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
