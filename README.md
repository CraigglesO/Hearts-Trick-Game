Hearts-Trick-Game
=================

Card Trick Game: HEARTS

Written in: Python

661 lines of code, 
80+ hours to complete, 
difficulty level: Intermediate


How to play:
http://www.toycrossing.com/hearts/passing-strategies.shtml

About this code:
The game is displayed in the terminal using ascii art to produce a means of objectifying the results
The AI is extremely smart, I havn't wont a game yet.
Basically, I studied the best strategies for the game and mixed in that strategy with my own strategy to make the AI seem more organic
The goal of making AI that's hard enough has been achieved

Things still needed to be done:
* AI never tries to shoot the moon
* User input error printouts need improvement
* For expert AI I only need to make some revisions to the section where the AI makes a decision if no one else has played yet, as of right now the AI always chooses the first card

Things I would have done differently:
* I didn't work in classes, that is a regret but this is the first program I have ever written in Python so it was a great learning experience regardless
* I realize now after seeing how other game developers create trick card games they always have one AI on expert, one AI on intermediate, and one AI on easy
	- I guess this would be achieved with easy AI checking which cards are legally playable and choosing a random card. Intermediate would be somewhere inbetween.
	- Since this is a trick card game and not for example chess, the user isn't going to think about decision making for 10 minutes each card, so obviously the AI that can exhaust the best possible card in milliseconds can't compare
	- "5 minute games" than should have a mixtured AI for a more pleasurable experience

What I learned:
* How to implement decision exhaustive AI
* Improved list comprehensions in Python
* The usefullness of .sort for arrays
	- unique difference in manipulation of String vs. Integer
* Expert level Heart strategy
* Added Array.extend(list) to my memories repertoire
* Use of try and except
* multi-dimensional arrays
* effective autamated testing / debugging
* Inheritance vs. Composition
* etc.


Please leave feedback if you have suggestions or comments, this was purely created for educational purposes and any advice would be invaluable to me


~Craiggles
