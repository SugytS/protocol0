"""
Главный файл игры
"""

import arcade
from menu import MenuView


def main():
    """Главная функция"""
    window = arcade.Window(
        width=1024,
        height=768,
        title="Dungeon Shooter",
        fullscreen=False
    )

    # Запускаем с главного меню
    menu_view = MenuView()
    window.show_view(menu_view)

    arcade.run()


if __name__ == "__main__":
    main()