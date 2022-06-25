# ORDLE
A command line implementation of Wordle in Danish. 

You can either **play the game yourself** or try to **write a bot that plays the game** (can you beat my bot?).

<img src="https://i.imgur.com/3cpl4DZ.gif" width="600"/>

# How to Play
Open a terminal window in the project directory and run:
```bash
python3 src/ordle
```

# How to Make Your Own Bot
Make a new file in ```/bots``` and define a class that inherits from ```Bot```:
```python
from bot import Bot
from game import Game


class MyBot(Bot):
    def play(self, game: Game):
        # replace this with your fancy algorithm:
        while game.get_state() == Game.State.ACTIVE:
            game.make_guess("PESTO")

```
Then implement the ```play()``` method to make your bot play a game.

### Guidance
The get familiar with the game interface, start by taking a look at the ```Game``` class.

You can also take a inspiration from my bot ```EmiloBot```, but be careful - it might ruin the fun of inventing your own.



# Testing Your Bot
### Setup
In ```__main__.py``` import your bot and set it as BOT_UNDER_DEV:
```python
from bots.my_bot import MyBot

[...]

BOT_UNDER_DEV = MyBot
```

### Running Tests
To test your bot, run one of the following commands:
- ```python3 src/ordle -t``` to see how your bot performs against existing bot(s).
- ```python3 src/ordle -t -dev``` to exclusively test your bot (faster).

If your bot performs well, open a pull request to add it to the repo.

### Advanced Options
For more options consult help: ```python3 src/ordle -h```:
```
options:
  -h, --help  show this help message and exit
  -t          Run in test mode
  -dev        Test only bot under development
  -n N        Number of games to be played in test mode
  -show       Show games in test mode
  -seed SEED  Use specific seed in test mode
  ```






# Credits
Thanks to The Society for Danish Language and Literature [DSL](https://dsl.dk) for providing access to their comprehensive list of Danish words.
