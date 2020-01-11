

Game instance - this is represents the state of a connect4 game at a given point.
has methods - place piece in a given column that just appends that piece and if that's not possible. raises an exception? or returns if it was successful or not?  - ✅

Once this is done - add some tests - or should i have TDD'ed? - ✅

Then be able to represent this in the UI. Some curses programming. - ✅

Then be able to make moves via UI and see the game update. ✅

Last would be the game over code. Be able to recognise when a player has won.

Then better UI. Draw game boundaries and also better UI for accepting input.


# Next step
implement retry mechanism given user input - done. probably needs to be refactored.

Implement game over code.
 - either no moves left or 4 balls have been connected.
 - can do it such that I only check from the last move if 4 balls have been conected.
 - so part of play move. is determine if game is at game_over state.


