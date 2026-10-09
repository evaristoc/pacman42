import pygame
import numpy as np


class PyGMiniLibXEmulator:
    def __init__(self, width: int, height: int, title="Pygame MiniLibX Emulator"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width,
                                               self.height))
        pygame.display.set_caption(title)

    def pygmlx_new_image(self, width, height):
        # Equivalent to mlx_new_image + mlx_get_data_addr
        return PyGMLXImageEmulator(width, height)

    def pygmlx_put_image_to_window(self, img, x, y):
        # Equivalent to mlx_put_image_to_window + screen refresh (flip)
        surface = pygame.image.frombuffer(img.buffer.tobytes(),
                                          (img.width, img.height),
                                          "RGBA")
        self.screen.blit(surface, (x, y))
        pygame.display.flip()


class PyGMLXImageEmulator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Raw pixel buffer layout: height x width x 4 (RGBA)
        # Raw pixel buffer: height x width x 4 (RGBA)
        self.buffer = np.zeros((self.height,
                                self.width,
                                4), dtype=np.uint8)

    def pygput_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y, x] = color  # (R, G, B, A)

    def pygget_data_addr(self):
        # Returns raw buffer and line size for direct manipulation
        line_size = self.width * 4
        return self.buffer, 32, line_size
