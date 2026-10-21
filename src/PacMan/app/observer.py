from typing import Any
from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager
from src.PacMan.game_logic.gamemanager.game_sm import (
									IGameState,
									PlayingGameState,
									OpeningMenuState)

class RenderState:
	def actions(self) -> None:
		...


class PlayRenderState(RenderState):
	def actions(self) -> None:
		print(f"this is {self.__class__.__name__}")


class Observer:
	def __init__(self, glm: GameLogicManager) -> None:
		self._registry: dict[str, Any] | None = None
		self._glm = glm
		self.render_state: RenderState = RenderState

	def register_assets(self, asset: dict[str, Any]) -> None:
		if not self._registry:
			self._registry = {}
		self._registry = self._registry | asset

	def actions(self, gs: IGameState) -> None:
		if isinstance(gs, IGameState):
			if gs == PlayingGameState:
				self.state = PlayRenderState()
				self.state.actions()
			if gs == OpeningMenuState:
				self.state 
			self._update()

