## Description
This is a table resulting from a brainstorm about the behaviors which the game needs to be able to display.

## Table

| Behaviour | Initiator | Affected | Condition |
|-----------|---------|-------|-------|
|Pacman moves | Player | Pacman | Player presses the buttons, which have been configured to make pacman move
|Pacman eats regular pellet | Player | Pacman, Pellet, Scoreboard | Pacman collides with regular pellet and 'eats it'
|Pacman eats big pellet | Player | Pacman, Pellet, Scoreboard, Ghosts | Pacman collides with big pellet and 'eats it'|
| Pacman eats ghost after eating big pellet | Player | Pacman, Scoreboard, Ghost | Pacman collides with ghost in 'ate big pellet'-state |
| Ghost moves | Ghost | Ghost | Game is started and ghosts start moving |
| Ghost becomes frightened | Player/Pacman | Ghost | Pacman eats big pellet |
| Ghost eats pacman | Ghost | Pacman, LivesTracker | Ghost finds/collides with pacman in regular state|
| Each ghost moves differently | Ghost-AI | Ghosts | Game is started and each ghost moves corresponding to their individual 'AI'|
| Pause menu pops up | Player | All Game Entities, Time Tracker, Pause Menu | Player presses button, which is configured to open the pause menu, while game is playing |
| Pause menu closes | Player | All Game Entities, Time Tracker, Pause Menu | Player presses button, which is configured to close the pause menu, while game is paused |
