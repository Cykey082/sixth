# sixth
 A chess-like game

size:5*4
chess:Each has 0~9,barrier,4 directions
Each side operate if possible else pass, until both pass.
The one with more values on board wins.

Operation includes:
1.Put:(when the destination is empty)
    Put a number chess onto the board.
2.Swap:(when the destination is one of your smaller number)
    Same as put, but gives back the original number.
3.Block:(when the destination is empty)
    Same as put, but using barrier chess.
4.Move:(when the move is valid)
    Consume your direction chess to move any chess on board in the direction to a empty place next to it.

When the board is changed,every row/column with 2 or more numbers summing 6n will be cleared.KILLED.
Barrier divides one line into three:one side,another,itself.
When put,0 can become anyone of your numbers killed.It's considered killing 0 and putting the number.

Tip:Try to keep your chess from being killed,especially by an enemy's smaller chess!

It's an inspiration from a friend of mine though.
In the future, it might be GiftCorridorSkylightStudio(maybe?).
Have fun anyway. I said so.
