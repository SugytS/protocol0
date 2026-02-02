import arcade


class UpgradeMenu(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.buttons = []

    def setup(self):
        self.buttons = []

        upgrades = [
            {"name": "Увеличить здоровье", "cost": 50, "action": self.upgrade_health,
             "desc": "+20 к максимальному здоровью"},
            {"name": "Увеличить урон", "cost": 50, "action": self.upgrade_damage, "desc": "+5 к урону"},
            {"name": "Увеличить скорость", "cost": 50, "action": self.upgrade_speed, "desc": "+1 к скорости движения"},
            {"name": "Увеличить скорострельность", "cost": 50, "action": self.upgrade_fire_rate,
             "desc": "+20% к скорострельности"},
            {"name": "Продолжить игру", "cost": 0, "action": self.continue_game, "desc": "Начать следующий уровень"}
        ]

        for i, upgrade in enumerate(upgrades):
            button = {
                "text": upgrade["name"],
                "x": 512,
                "y": 450 - i * 80,
                "width": 400,
                "height": 60,
                "action": upgrade["action"],
                "cost": upgrade["cost"],
                "desc": upgrade["desc"],
                "hover": False
            }
            self.buttons.append(button)

    def on_draw(self):
        # В View используем self.clear() вместо arcade.start_render()
        self.clear()

        # Фон - темно-синий градиент (имитация)
        arcade.draw_lrbt_rectangle_filled(0, 1024, 384, 768, arcade.color.DARK_BLUE)
        arcade.draw_lrbt_rectangle_filled(0, 1024, 0, 384, arcade.color.DARK_SLATE_BLUE)

        # Добавим звезды или точки для красоты
        for i in range(50):
            x = i * 20 + 12
            y = (i * 13) % 768
            arcade.draw_circle_filled(x, y, 2, arcade.color.LIGHT_BLUE)

        # Заголовок
        title = arcade.Text("МЕНЮ УЛУЧШЕНИЙ", 512, 650,
                            arcade.color.GOLD, 48,
                            anchor_x="center", anchor_y="center",
                            bold=True)
        title.draw()

        # Подзаголовок
        subtitle = arcade.Text("Потратьте очки на улучшение характеристик", 512, 590,
                               arcade.color.LIGHT_GOLDENROD_YELLOW, 20,
                               anchor_x="center", anchor_y="center")
        subtitle.draw()

        # Панель счета
        arcade.draw_rectangle_filled(512, 530, 300, 50, arcade.color.DARK_BLUE)
        arcade.draw_rectangle_outline(512, 530, 300, 50, arcade.color.GOLD, 3)

        score_text = arcade.Text(f"ДОСТУПНО ОЧКОВ: {self.game_view.score}", 512, 530,
                                 arcade.color.WHITE, 28,
                                 anchor_x="center", anchor_y="center",
                                 bold=True)
        score_text.draw()

        # Кнопки
        for button in self.buttons:
            if button["hover"]:
                bg_color = arcade.color.BLUEBERRY
                border_color = arcade.color.CYAN
            elif button["cost"] > 0 and self.game_view.score < button["cost"]:
                bg_color = arcade.color.DARK_GRAY
                border_color = arcade.color.DARK_RED
            elif button["cost"] == 0:
                bg_color = arcade.color.DARK_GREEN
                border_color = arcade.color.GREEN
            else:
                bg_color = arcade.color.DARK_BLUE
                border_color = arcade.color.BLUE

            arcade.draw_rectangle_filled(button["x"], button["y"],
                                         button["width"], button["height"],
                                         bg_color)
            arcade.draw_rectangle_outline(button["x"], button["y"],
                                          button["width"], button["height"],
                                          border_color, 3)

            text_color = arcade.color.WHITE
            if button["cost"] > 0 and self.game_view.score < button["cost"]:
                text_color = arcade.color.LIGHT_GRAY

            button_text = arcade.Text(button["text"], button["x"], button["y"] + 15,
                                      text_color, 24,
                                      anchor_x="center", anchor_y="center")
            button_text.draw()

            desc_text = arcade.Text(button["desc"], button["x"], button["y"] - 10,
                                    arcade.color.LIGHT_GRAY, 14,
                                    anchor_x="center", anchor_y="center")
            desc_text.draw()

            if button["cost"] > 0:
                cost_text = arcade.Text(f"Цена: {button['cost']} очков",
                                        button["x"], button["y"] - 25,
                                        arcade.color.YELLOW, 16,
                                        anchor_x="center", anchor_y="center")
                cost_text.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for button in self.buttons:
            button["hover"] = (abs(x - button["x"]) < button["width"] / 2 and
                               abs(y - button["y"]) < button["height"] / 2)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for btn in self.buttons:
                if (abs(x - btn["x"]) < btn["width"] / 2 and
                        abs(y - btn["y"]) < btn["height"] / 2):
                    btn["action"]()
                    break

    def upgrade_health(self):
        if self.game_view.score >= 50:
            self.game_view.player_max_health += 20
            self.game_view.player_health = self.game_view.player_max_health
            self.game_view.score -= 50
            print("Здоровье увеличено на 20!")
        else:
            print("Недостаточно очков!")

    def upgrade_damage(self):
        if self.game_view.score >= 50:
            self.game_view.player_damage += 5
            self.game_view.score -= 50
            print("Урон увеличен на 5!")
        else:
            print("Недостаточно очков!")

    def upgrade_speed(self):
        if self.game_view.score >= 50:
            self.game_view.player_speed += 1
            self.game_view.score -= 50
            print("Скорость увеличена на 1!")
        else:
            print("Недостаточно очков!")

    def upgrade_fire_rate(self):
        if self.game_view.score >= 50:
            self.game_view.fire_rate += 0.2
            self.game_view.score -= 50
            print("Скорострельность увеличена на 20%!")
        else:
            print("Недостаточно очков!")

    def continue_game(self):
        self.game_view.current_level += 1
        self.game_view.current_room_index = 0
        self.game_view.setup_level(self.game_view.current_level)

        self.window.show_view(self.game_view)