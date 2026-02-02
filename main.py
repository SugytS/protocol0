import arcade
from menu import MenuView

def main():
    window = arcade.Window(1024, 768, "Protocol0")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()