"""
Система меню игры (исправленная версия)
"""

import arcade
from config import *


class MenuView(arcade.View):
    """Главное меню игры"""

    def __init__(self):
        super().__init__()

    def on_draw(self):
        """Отрисовка меню"""
        self.clear(arcade.color.DARK_SLATE_GRAY)

        # Заголовок
        arcade.draw_text(
            "DUNGEON SHOOTER",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.7,
            arcade.color.GOLD,
            font_size=50,
            anchor_x="center",
            font_name="Arial",
            bold=True
        )

        # Кнопки
        button_height = 50
        button_width = 200
        start_y = SCREEN_HEIGHT * 0.5

        # Кнопка "Новая игра"
        left = SCREEN_WIDTH // 2 - button_width // 2
        right = SCREEN_WIDTH // 2 + button_width // 2
        top = start_y + button_height // 2
        bottom = start_y - button_height // 2

        # Исправленный вызов: draw_lrbt_rectangle_filled(left, right, bottom, top)
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.DARK_GREEN)
        arcade.draw_text(
            "НОВАЯ ИГРА",
            SCREEN_WIDTH // 2,
            start_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

        # Кнопка "Выход"
        start_y_exit = start_y - 80
        top_exit = start_y_exit + button_height // 2
        bottom_exit = start_y_exit - button_height // 2

        arcade.draw_lrbt_rectangle_filled(left, right, bottom_exit, top_exit, arcade.color.DARK_RED)
        arcade.draw_text(
            "ВЫХОД",
            SCREEN_WIDTH // 2,
            start_y_exit,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

        # Инструкции
        arcade.draw_text(
            "Управление: WASD/Стрелки - движение, ЛКМ - стрельба",
            SCREEN_WIDTH // 2,
            50,
            arcade.color.LIGHT_GRAY,
            font_size=16,
            anchor_x="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка кликов по меню"""
        button_height = 50
        button_width = 200
        start_y = SCREEN_HEIGHT * 0.5

        if (SCREEN_WIDTH // 2 - button_width // 2 <= x <= SCREEN_WIDTH // 2 + button_width // 2 and
            start_y - button_height // 2 <= y <= start_y + button_height // 2):
            # Импортируем внутри метода, чтобы избежать циклического импорта
            from game import DungeonGame
            game_view = DungeonGame()
            self.window.show_view(game_view)

        elif (SCREEN_WIDTH // 2 - button_width // 2 <= x <= SCREEN_WIDTH // 2 + button_width // 2 and
              start_y - 80 - button_height // 2 <= y <= start_y - 80 + button_height // 2):
            arcade.close_window()


class UpgradeMenuView(arcade.View):
    """Меню улучшений после уровня"""

    def __init__(self, game_view, callback):
        super().__init__()
        self.game_view = game_view
        self.callback = callback
        self.upgrades = [
            {"name": "Увеличить урон на 20%", "type": "damage", "value": 1.2},
            {"name": "Увеличить здоровье на 25", "type": "health", "value": 25},
            {"name": "Увеличить скорость на 15%", "type": "speed", "value": 1.15},
        ]

    def on_draw(self):
        """Отрисовка меню улучшений"""
        self.clear(arcade.color.DARK_SLATE_GRAY)

        # Полупрозрачный затемняющий слой - ИСПРАВЛЕНО
        # draw_lrbt_rectangle_filled(left, right, bottom, top, color)
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,  # left, right, bottom, top
            (0, 0, 0, 200)  # цвет с прозрачностью
        )

        # Заголовок
        arcade.draw_text(
            "ВЫБЕРИТЕ УЛУЧШЕНИЕ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.8,
            arcade.color.GOLD,
            font_size=40,
            anchor_x="center",
            bold=True
        )

        # Текущие характеристики
        arcade.draw_text(
            f"Урон: {self.game_view.player.damage_multiplier:.1f}x  |  "
            f"Здоровье: {self.game_view.player.health}/{self.game_view.player.max_health}  |  "
            f"Скорость: {self.game_view.player.speed:.0f}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.7,
            arcade.color.LIGHT_GRAY,
            font_size=18,
            anchor_x="center"
        )

        # Кнопки улучшений
        button_height = 50
        button_width = 400
        start_y = SCREEN_HEIGHT * 0.55
        spacing = 70

        for i, upgrade in enumerate(self.upgrades):
            y_pos = start_y - i * spacing

            # Кнопка - используем draw_lrbt_rectangle_filled
            left = SCREEN_WIDTH // 2 - button_width // 2
            right = SCREEN_WIDTH // 2 + button_width // 2
            top = y_pos + button_height // 2
            bottom = y_pos - button_height // 2

            # ИСПРАВЛЕНО: draw_lrbt_rectangle_filled(left, right, bottom, top, color)
            arcade.draw_lrbt_rectangle_filled(
                left, right, bottom, top,  # left, right, bottom, top
                arcade.color.DARK_BLUE
            )

            # Рамка кнопки - ИСПРАВЛЕНО: используем draw_lrbt_rectangle_outline (такой же порядок параметров)
            arcade.draw_lrbt_rectangle_outline(
                left, right, bottom, top,  # left, right, bottom, top
                arcade.color.GOLD,
                2
            )

            # Текст улучшения
            arcade.draw_text(
                upgrade["name"],
                SCREEN_WIDTH // 2,
                y_pos,
                arcade.color.WHITE,
                font_size=22,
                anchor_x="center",
                anchor_y="center"
            )

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка выбора улучшения"""
        button_height = 50
        button_width = 400
        start_y = SCREEN_HEIGHT * 0.55
        spacing = 70

        for i, upgrade in enumerate(self.upgrades):
            y_pos = start_y - i * spacing

            left = SCREEN_WIDTH // 2 - button_width // 2
            right = SCREEN_WIDTH // 2 + button_width // 2
            top = y_pos + button_height // 2
            bottom = y_pos - button_height // 2

            if (left <= x <= right and bottom <= y <= top):
                self.callback(upgrade["type"], upgrade["value"])
                self.window.show_view(self.game_view)
                break


class GameOverView(arcade.View):
    """Экран завершения игры"""

    def __init__(self, score, level, window):
        super().__init__()
        self.score = score
        self.level = level
        self.window_ref = window  # Сохраняем ссылку на окно

    def on_draw(self):
        """Отрисовка экрана завершения"""
        self.clear(arcade.color.DARK_SLATE_GRAY)

        # Полупрозрачный затемняющий слой - ИСПРАВЛЕНО
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,  # left, right, bottom, top
            (0, 0, 0, 200)
        )

        # Заголовок
        arcade.draw_text(
            "ИГРА ОКОНЧЕНА",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.7,
            arcade.color.RED,
            font_size=50,
            anchor_x="center",
            bold=True
        )

        # Статистика
        arcade.draw_text(
            f"Достигнут уровень: {self.level}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.55,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Общий счет: {self.score}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.45,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center"
        )

        # Кнопки
        button_height = 50
        button_width = 200
        start_y = SCREEN_HEIGHT * 0.3

        # Кнопка "В меню"
        left = SCREEN_WIDTH // 2 - button_width // 2
        right = SCREEN_WIDTH // 2 + button_width // 2
        top_menu = start_y + button_height // 2
        bottom_menu = start_y - button_height // 2

        # ИСПРАВЛЕНО: draw_lrbt_rectangle_filled(left, right, bottom, top, color)
        arcade.draw_lrbt_rectangle_filled(left, right, bottom_menu, top_menu, arcade.color.DARK_GREEN)
        arcade.draw_text(
            "В МЕНЮ",
            SCREEN_WIDTH // 2,
            start_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

        # Кнопка "Выход"
        start_y_exit = start_y - 80
        top_exit = start_y_exit + button_height // 2
        bottom_exit = start_y_exit - button_height // 2

        # ИСПРАВЛЕНО: draw_lrbt_rectangle_filled(left, right, bottom, top, color)
        arcade.draw_lrbt_rectangle_filled(left, right, bottom_exit, top_exit, arcade.color.DARK_RED)
        arcade.draw_text(
            "ВЫХОД",
            SCREEN_WIDTH // 2,
            start_y_exit,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка кликов"""
        button_height = 50
        button_width = 200
        start_y = SCREEN_HEIGHT * 0.3

        left = SCREEN_WIDTH // 2 - button_width // 2
        right = SCREEN_WIDTH // 2 + button_width // 2
        top_menu = start_y + button_height // 2
        bottom_menu = start_y - button_height // 2

        if (left <= x <= right and bottom_menu <= y <= top_menu):
            # Возвращаемся в главное меню
            menu_view = MenuView()
            self.window.show_view(menu_view)

        elif (left <= x <= right and (start_y - 80 - button_height // 2) <= y <= (start_y - 80 + button_height // 2)):
            arcade.close_window()
