import pygame
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from enum import IntEnum
from typing import Any, Callable, TypeAlias
from src.PacMan.app.observer import Observer

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
        self.view_w, self.view_h = self.screen.get_size()

        pygame.display.set_caption(title)
        self._loop_hook: TLoopHookCB | None = None
        self._loop_param: Any = None

    def pygmlx_new_image(self,
                         width: int,
                         height: int) -> 'PyGMLXImageEmulator':
        # Equivalent to mlx_new_image + mlx_get_data_addr
        return PyGMLXImageEmulator(width, height)

    def pygmlx_new_png_image(self,
                             width: int,
                             height: int) -> 'PyMLXPNGEmulator':
        # Equivalent to mlx_new_image + mlx_get_data_addr
        return PyMLXPNGEmulator(width, height)

    def pygmlx_new_text_image(self,
                              width: int,
                              height: int,
                              font: int = 16,
                              color: int = 0xFFF) -> 'PyGMLXTextEmulator':
        return PyGMLXTextEmulator(
            width=width,
            height=height,
            font_size=font)

    def pygmlx_put_image_to_window(self,
                                   img: 'PyGMLXImageEmulator',
                                   x: int,
                                   y: int) -> None:
        # Equivalent to mlx_put_image_to_window + screen refresh (flip)
        # print(type(img))
        surface = pygame.image.frombuffer(img.buffer.tobytes(),
                                          (img.width, img.height),
                                          "RGBA")
        # pygame.image.save(surface, "debug_pygame_surface.png")
        self.screen.blit(surface, (x, y))
        pygame.display.flip()

    # def pygmlx_string_put(self,
    #                       x: int,
    #                       y: int,
    #                       color: int,
    #                       text: str,
    #                       ttf: str = 'CONSOLA.TTF') -> None:
    #     """
    #     Renders text directly onto the image buffer using Pillow, 
    #     matching your existing image manipulation workflow.
    #     """
    #     # Convert integer color (0xRRGGBB) to an RGBA tuple
    #     r = (color >> 16) & 0xFF
    #     g = (color >> 8) & 0xFF
    #     b = color & 0xFF
    #     a = 255
    #     # Recreate a Pillow image from your current NumPy buffer
    #     pil_img = Image.fromarray(self.buffer, mode="RGBA")
    #     draw = ImageDraw.Draw(pil_img)
    #     font_path = "../assets/fonts/" + ttf
    #     font_size = 14
    #     try:
    #         font = ImageFont.truetype(font_path, font_size)
    #     except IOError:
    #         # Fallback to default if the system path isn't found
    #         # (Pillow has a built-in bitmap font)
    #         font = ImageFont.load_default()

    #     # Draw the text onto the image
    #     draw.text((x, y), text, fill=(r, g, b, a), font=font)

    #     # Sync changes back to your NumPy buffer
    #     self.buffer = np.array(pil_img, dtype=np.uint8)

    def mlx_loop_hook(self,
                      funct_ptr: TLoopHookCB | None,
                      param: Any = None
                      ) -> None:
        self._loop_hook = funct_ptr
        self._loop_param = param

    def pygmlx_loop(self, observer: Observer) -> None:
        clock: pygame.time.Clock = pygame.time.Clock()
        running = True
        while running:
            event: pygame.event.Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                observer.actions(event=event)
            if self._loop_hook is not None:
                result: int = self.mlx_loop_hook(self._loop_param)
                if result == 0:
                    break
            clock.tick(60)


# class PyGMLXImageEmulator:
#     def __init__(self, width: int, height: int, buffer: np.ndarray = None) -> None:
#         self.width = width
#         self.height = height
#         if buffer is not None:
#             self.buffer = buffer
#         else:
#             self.buffer = np.zeros((self.height, self.width, 4), dtype=np.uint8)

#     def pygput_pixel(self, x: int, y: int, color: int) -> None:
#         r = (color >> 16) & 0xFF
#         g = (color >> 8) & 0xFF
#         b = color & 0xFF
#         self.buffer[y, x, 0] = r
#         self.buffer[y, x, 1] = g
#         self.buffer[y, x, 2] = b
#         self.buffer[y, x, 3] = 255

#     def pygll_save_img(self, filepath: str) -> None:
#         pil_img = Image.fromarray(self.buffer, mode="RGBA")
#         pil_img.save(filepath)

#     def pygll_resize(self, new_width: int, new_height: int) -> None:
#         pil_img = Image.fromarray(self.buffer, mode="RGBA")
#         resized_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
#         self.width = new_width
#         self.height = new_height
#         self.buffer = np.array(resized_img, dtype=np.uint8)

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
        # if y > 300 or x > 300:
        #     return
        # print("inside put", x, y)
        self.buffer[y, x, RGBA.R] = r
        self.buffer[y, x, RGBA.G] = g
        self.buffer[y, x, RGBA.B] = b
        self.buffer[y, x, RGBA.A] = a

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


class PyMLXPNGEmulator(PyGMLXImageEmulator):
    def pygput_from_png(self,
                        file_path: str
                        ) -> None:
        with Image.open(file_path) as pil_img:
            rgba_img = pil_img.convert("RGBA")
            w, h = rgba_img.size
            self.width = w
            self.height = h
            self.buffer[:] = np.array(rgba_img,
                                      dtype=np.uint8)


class PyGMLXTextEmulator(PyGMLXImageEmulator):
    def __init__(
        self,
        width: int,
        height: int,
        font_path: str = "CONSOLAS.TTF",
        font_size: int = 16,
        color: int = 0xFFFFFF
    ) -> None:
        super().__init__(width, height)
        self.font_path = "../assets/fonts/" + font_path
        self.font_size = font_size
        self.color = color
        self._load_font()

    def _load_font(self) -> None:
        try:
            self.font = ImageFont.truetype(self.font_path, self.font_size)
        except IOError:
            self.font = ImageFont.load_default()

    def pygput_from_text(
            self,
            x: int,
            y: int,
            text: str) -> None:
        # rgba inconsistent manipulation compared to other sections of the
        # code, but required for this case
        r = (self.color >> 16) & 0xFF
        g = (self.color >> 8) & 0xFF
        b = self.color & 0xFF
        a = 255
        # self.buffer[:, :, 3] = 255
        pil_img = Image.fromarray(self.buffer,
                                  mode="RGBA")
        draw = ImageDraw.Draw(pil_img)
        draw.text((x, y),
                  text,
                  fill=(r, g, b, a),
                  font=self.font)
        # print(draw)
        # print(draw._image.size, draw._image.mode)
        # draw._image.save("debug_text_output.png")
        self.buffer[:] = np.array(pil_img,
                                  dtype=np.uint8)

    def _measure_text(self, text: str) -> tuple[int, int, int, int]:
        dummy_img = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(dummy_img)
        return draw.textbbox((0, 0), text, font=self.font)

    def pygll_put_text_fitted(
            self,
            x: int,
            y: int,
            text: str) -> None:
        # Enhancement layer using textbbox to handle fitting/clipping
        bbox = self._measure_text(text)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Clamp coordinates or adjust to guarantee it fits inside
        # self.width / self.height
        target_x = min(max(x, 0), self.width - text_w)
        target_y = min(max(y, 0), self.height - text_h)
        self.pygput_from_text(target_x, target_y, text)
