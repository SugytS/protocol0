import arcade
from game import DungeonGame


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.game_view = None

    def on_draw(self):
        # В View не нужно вызывать arcade.start_render()
        # Arcade делает это автоматически

        # Очищаем экран
        self.clear()

        # Простой фон с двумя цветами
        # Верхняя часть - темнее (bottom=384, top=768)
        arcade.draw_lrbt_rectangle_filled(0, 1024, 384, 768, arcade.color.DARK_SLATE_GRAY)

        # Нижняя часть - светлее (bottom=0, top=384)
        arcade.draw_lrbt_rectangle_filled(0, 1024, 0, 384, arcade.color.DARK_BLUE_GRAY)

        # Добавим простой узор
        for i in range(0, 1024, 100):
            arcade.draw_line(i, 0, i, 768, arcade.color.BLACK, 1)

        for i in range(0, 768, 100):
            arcade.draw_line(0, i, 1024, i, arcade.color.BLACK, 1)

        # Рисуем заголовок игры
        title_text = arcade.Text("PROTOCOL0", 512, 550, arcade.color.CYAN, 72,
                                 anchor_x="center", anchor_y="center",
                                 bold=True)
        title_text.draw()

        # Подзаголовок
        subtitle_text = arcade.Text("Dungeon Crawler", 512, 470,
                                    arcade.color.LIGHT_CYAN, 32,
                                    anchor_x="center", anchor_y="center")
        subtitle_text.draw()

        # Инструкция
        instruction_text = arcade.Text("НАЖМИТЕ ЛКМ ЧТОБЫ НАЧАТЬ", 512, 350,
                                       arcade.color.WHITE, 28,
                                       anchor_x="center", anchor_y="center")
        instruction_text.draw()

        # Управление
        controls_text = arcade.Text("Управление: WASD - движение, ЛКМ - стрельба",
                                    512, 250, arcade.color.LIGHT_GRAY, 20,
                                    anchor_x="center", anchor_y="center")
        controls_text.draw()

        # Дополнительная информация
        info_text = arcade.Text("Очищайте комнаты, уничтожайте врагов, улучшайте персонажа!",
                                512, 180, arcade.color.GRAY, 16,
                                anchor_x="center", anchor_y="center")
        info_text.draw()

        # Версия
        version_text = arcade.Text("v1.0", 512, 50, arcade.color.GRAY, 14,
                                   anchor_x="center", anchor_y="center")
        version_text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            print("Запуск игры...")
            self.game_view = DungeonGame()
            self.window.show_view(self.game_view)