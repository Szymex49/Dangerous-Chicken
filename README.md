# Dangerous Chicken
## Author: Szymon Malec

### Short description
A simple arcade game where you play as a chicken with special abilities. You need to defend yourself from the bad gang of animals, otherwise, when they get to you, you'll be torn into pieces.

The game offers four difficulty levels. You get points for defeating enemies. What score will you achieve? Are you brave enough to try hardcore mode?

![Screenshot](/files/screenshot1.png)
![Screenshot](/files/screenshot2.png)

### Technologies
**Python** - a programming language in which the whole game is written. <br>
**Pygame** - a set of Python modules designed for creating video games. <br>
**Gimp** - for editing images. <br>
**Canva** - for creating simple graphics.

### Technical information
The game consists of three python files which are:
- **tools.py** - module which is game's base. It contains many useful functions designed for creating the game. It also contains basic variables such as screen size or volume.
- **classes.py** - module containing all classes used for creating objects such as player, enemies or missiles.
- **DangerousChicken.py** - main file containing the actual game. The costruction is based on a few functions which are executed in an infinite loop. When you run the game, the menu function executes. Then, depending on what option in menu the user will enter, the other function starts looping. When the user decides to come back to menu, the current loop breaks and we come back to the previous menu loop.

### How to run this app?
1. Clone the project: <br>
`git clone  https://github.com/Szymex49/Dangerous-Chicken.git DangerousChicken` <br>
`cd DangerousChicken`
2. Install the project's development and runtime requirements: <br>
`pip install -r requirements.txt`
3. Run the game: <br>
`python DangerousChicken.py`