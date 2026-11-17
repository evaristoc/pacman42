import pygame


class HighScoreRegisterState:
    def __init__(self, screen):
        self.screen = screen
        self.username = ""
        self.active = True
        self.font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 60)
        pygame.key.start_text_input()
        pygame.key.set_text_input_rect(pygame.Rect(200, 340, 300, 40))

    def handle_event(self, event):
        if not self.active:
            return
        if event.type == pygame.TEXTINPUT:
            remaining = 12 - len(self.username)
            if remaining > 0:
                self.username += event.text[:remaining]
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            elif event.key == pygame.K_RETURN:
                self.register()

    def register(self):
        self.active = False
        pygame.key.stop_text_input()
        print(f"Registering: {self.username}")

    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.title_font.render(
            "REGISTER HIGH SCORE", True, (255, 255, 0)
        )
        prompt = self.font.render(
            "Enter your name:", True, (255, 255, 255)
        )
        username = self.font.render(
            self.username + "_", True, (0, 255, 0)
        )
        self.screen.blit(title, (200, 150))
        self.screen.blit(prompt, (200, 280))
        self.screen.blit(username, (200, 340))