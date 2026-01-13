import arcade
from game import DungeonGame


def main():
    game = DungeonGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()