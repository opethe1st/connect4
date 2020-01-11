

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


What's left?
Tidy up the UI. but I might just leave this so I don't fall into the trap of unending refinement.
Wish I recorded myself solving this. That would have been nice. Want to do this for a snake game too and record it and post it.
Also tic-tac-toe?

Just realise this doesn't handle draws and when there are no valid moves left.

Also possible enhancement. Do this in React or PyQt for just kicks. Should be simple.


# Done!
What else could I do?
Show which pieces connected?
Let the user specify a different board size?
Echo the input to the user.
Draw the game borders.
Implement this with PyQyt how much would this have to change?
Does this need more tests?
