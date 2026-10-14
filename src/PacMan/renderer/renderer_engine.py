import pygame
import numpy as np
from PIL import Image
from enum import IntEnum
from typing import Any, Callable, TypeAlias


TLoopHookCB: TypeAlias = Callable[[Any], int]
PixelBuffer: TypeAlias = np.ndarray


class RGBA(IntEnum):
    R = 0
    G = 1
    B = 2
    A = 3


class PyGMiniLibXEmulator:
    def __init__(self,
                 width: int,
                 height: int,
                 title: str = "Pygame MiniLibX Emulator") -> None:
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width,
                                               self.height))
        pygame.display.set_caption(title)
        self._loop_hook: TLoopHookCB | None = None
        self._loop_param: Any = None

    def pygmlx_new_image(self,
                         width: int,
                         height: int) -> 'PyGMLXImageEmulator':
        # Equivalent to mlx_new_image + mlx_get_data_addr
        return PyGMLXImageEmulator(width, height)

    def pygmlx_put_image_to_window(self,
                                   img: 'PyGMLXImageEmulator',
                                   x: int,
                                   y: int) -> None:
        # Equivalent to mlx_put_image_to_window + screen refresh (flip)
        surface = pygame.image.frombuffer(img.buffer.tobytes(),
                                          (img.width, img.height),
                                          "RGBA")
        self.screen.blit(surface, (x, y))
        pygame.display.flip()

    def mlx_loop_hook(self,
                      funct_ptr: TLoopHookCB | None,
                      param: Any = None
                      ) -> None:
        self._loop_hook = funct_ptr
        self._loop_param = param

    def pygmlx_loop(self) -> None:
        clock: pygame.time.Clock = pygame.time.Clock()
        self.running = True
        while self.running:
            event: pygame.event.Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if self._loop_hook is not None:
                result: int = self._loop_hook(self._loop_param)
                if result == 0:
                    break
            clock.tick(60)


class PyGMLXImageEmulator:
    def __init__(self,
                 width: int,
                 height: int
                 ) -> None:
        self.width = width
        self.height = height
        # Raw pixel buffer layout: height x width x 4 (RGBA)
        # Raw pixel buffer: height x width x 4 (RGBA)
        self.buffer = np.zeros((self.height,
                                self.width,
                                4), dtype=np.uint8)

    def pygput_pixel(self,
                     x: int,
                     y: int,
                     color: int) -> None:
        r: int = (color >> 16) & 0xFF
        g: int = (color >> 8) & 0xFF
        b: int = color & 0xFF
        a: int = 255  # Fully opaque default unless an alpha channel is packed
        if y > 300 or x > 300:
            return
        self.buffer[y, x, RGBA.R] = r
        self.buffer[y, x, RGBA.G] = g
        self.buffer[y, x, RGBA.B] = b
        self.buffer[y, x, RGBA.A] = a

    def pygput_from_png(self,
                        file_path: str
                        ) -> None:
        with Image.open(file_path) as pil_img:
            rgba_img = pil_img.convert("RGBA")
            w, h = rgba_img.size
            self.width = w
            self.height = h
            self.buffer[:] = np.array(rgba_img, dtype=np.uint8)

    def pygget_data_addr(self) -> tuple[PixelBuffer, int, int]:
        # Returns raw buffer and line size for direct manipulation
        line_size = self.width * 4
        return self.buffer, 32, line_size

    def pygll_process_pixels_loop(self) -> None:
        """
        Example loop iterating through the 3D array space
        (simulating manual pixel manipulation like mlx_pixel_put)
        """
        for y in range(self.height):
            for x in range(self.width):
                # Access pixel channels directly: [R, G, B, A]
                r, g, b, a = self.buffer[y, x]
                # Example manipulation: Invert the red channel just
                # to test loop modification
                self.buffer[y, x, 0] = 255 - r

    def pygll_save_img(self, filepath: str) -> None:
        """Export the NumPy buffer back to an image file via Pillow"""
        pil_img = Image.fromarray(self.buffer, mode="RGBA")
        pil_img.save(filepath)

    def pygll_resize(self, new_width: int, new_height: int) -> None:
        pil_img = Image.fromarray(self.buffer, mode="RGBA")
        resized_img = pil_img.resize((new_width,
                                      new_height),
                                     Image.Resampling.LANCZOS)
        self.width = new_width
        self.height = new_height
        self.buffer = np.array(resized_img, dtype=np.uint8)
