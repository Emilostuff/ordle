# ORDLE
A command line implementation of Wordle in Danish. You can either play the game yourself, or you can try to write a bot that plays the game (pleasant testing environment included).

<img src="https://i.imgur.com/3cpl4DZ.gif" width="600"/>

# How to Play
Open a terminal window in the project directory and run:
```bash
python3 src/ordle
```

# How to Make Your Own Bot
1. Make a new file and implement a class that inherits from ```Bot```. 
2. Implement the ```play()``` method to make your bot play a game.
3. Add your bot class to the list of ```BOTS``` in ```__main__.py```.
4. run: ```python3 src/ordle test [number of tests]``` to see how your bot performs.

Can you beat my bot?


# Credits
Thanks to The Society for Danish Language and Literature [DSL](https://dsl.dk) for providing access to their comprehensive list of Danish words.
