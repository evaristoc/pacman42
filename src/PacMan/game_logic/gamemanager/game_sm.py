from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager


class IGameState:
    def __init__(self, context: GameLogicManager):
        self.context = context


class OpeningMenuState(IGameState):
    pass


class PlayingGameState(IGameState):
    pass

    def update_logic(self, delta_ticks):
        self.context.character_manager.update(delta_ticks)
