## Description

We want to clarify the way that the states are going to change between rendering cycles and who does what.

We propose a single meta state which is the single point of thruth for the state at each cycle.

The renderer is the one capturing the events from keyboard and passing to the single meta state.

The single meta state at each cycle, with either event or not, inform the renderer of the state of the game.

Game uses the contracts (ghost, pacman, player) inside the meta state to update for next tick.

Game Engine only assessemble the game parts and get that ready for event catching. It might include the update function for each tick. It takes care of the order of their interation.

## Table

| State | Renderer | Logic | Condition? |
| ----------- | --------- | ------- | ------- |
| keyboard events | yes | no | -- |
| single meta state | no | yes | -- |
