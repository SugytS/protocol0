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
        
        # Получаем информацию об улучшениях из игрока - ТОЛЬКО ДВА УЛУЧШЕНИЯ
        self.upgrades = []
        self.load_upgrades()

    def load_upgrades(self):
        """Загрузка информации об улучшениях"""
        player = self.game_view.player
        
        # Получаем информацию о каждом типе улучшений (ТОЛЬКО ДВА)
        damage_info = player.get_upgrade_info("damage")
        speed_info = player.get_upgrade_info("speed")
        
        self.upgrades = [
            {
                "name": f"УРОН +20%",
                "type": "damage",
                "value": 1.2,
                "description": f"Текущий: {damage_info['current_value']} → {damage_info['next_value']}",
                "price": damage_info["price"],
                "purchased": damage_info["purchased"],
                "can_afford": damage_info["can_afford"],
                "color": arcade.color.ORANGE
            },
            {
                "name": f"СКОРОСТЬ +15%",
                "type": "speed",
                "value": 1.15,
                "description": f"Текущий: {speed_info['current_value']} → {speed_info['next_value']}",
                "price": speed_info["price"],
                "purchased": speed_info["purchased"],
                "can_afford": speed_info["can_afford"],
                "color": arcade.color.BLUE
            }
        ]

    def on_draw(self):
        """Отрисовка меню улучшений"""
        self.clear(arcade.color.DARK_SLATE_GRAY)

        # Полупрозрачный затемняющий слой
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (0, 0, 0, 200)
        )

        # Заголовок
        arcade.draw_text(
            "МАГАЗИН УЛУЧШЕНИЙ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.85,
            arcade.color.GOLD,
            font_size=40,
            anchor_x="center",
            bold=True
        )

        # Информация о монетах
        arcade.draw_text(
            f"МОНЕТЫ: {self.game_view.player.coins}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.78,
            arcade.color.GOLD,
            font_size=30,
            anchor_x="center",
            bold=True
        )

        # Кнопки улучшений (ТОЛЬКО ДВЕ)
        button_width = 450
        button_height = 90  # Увеличиваем высоту для лучшего отображения
        start_y = SCREEN_HEIGHT * 0.65
        spacing = 120  # Увеличиваем расстояние между кнопками

        for i, upgrade in enumerate(self.upgrades):
            y_pos = start_y - i * spacing

            # Цвет кнопки в зависимости от доступности
            if not upgrade["can_afford"]:
                button_color = arcade.color.DARK_GRAY
                text_color = arcade.color.LIGHT_GRAY
            else:
                button_color = upgrade["color"]
                text_color = arcade.color.WHITE

            # Кнопка
            left = SCREEN_WIDTH // 2 - button_width // 2
            right = SCREEN_WIDTH // 2 + button_width // 2
            top = y_pos + button_height // 2
            bottom = y_pos - button_height // 2

            arcade.draw_lrbt_rectangle_filled(
                left, right, bottom, top,
                button_color
            )

            # Рамка кнопки
            border_color = arcade.color.GOLD if upgrade["can_afford"] else arcade.color.DARK_SLATE_GRAY
            arcade.draw_lrbt_rectangle_outline(
                left, right, bottom, top,
                border_color,
                3
            )

            # Название улучшения (крупнее)
            arcade.draw_text(
                upgrade["name"],
                SCREEN_WIDTH // 2,
                y_pos + 20,
                text_color,
                font_size=28,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

            # Описание улучшения
            arcade.draw_text(
                upgrade["description"],
                SCREEN_WIDTH // 2,
                y_pos - 10,
                text_color,
                font_size=18,
                anchor_x="center",
                anchor_y="center"
            )

            # Цена и количество покупок
            price_text = f"Цена: {upgrade['price']} монет"
            if upgrade["purchased"] > 0:
                price_text += f" (куплено: {upgrade['purchased']})"
                
            arcade.draw_text(
                price_text,
                SCREEN_WIDTH // 2,
                y_pos - 35,
                text_color,
                font_size=16,
                anchor_x="center",
                anchor_y="center"
            )

        # Кнопка пропуска покупки
        skip_y = SCREEN_HEIGHT * 0.1
        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_WIDTH // 2 + 150,
            skip_y - 25,
            skip_y + 25,
            arcade.color.DARK_GRAY
        )
        
        arcade.draw_lrbt_rectangle_outline(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_WIDTH // 2 + 150,
            skip_y - 25,
            skip_y + 25,
            arcade.color.LIGHT_GRAY,
            2
        )
        
        arcade.draw_text(
            "ПРОПУСТИТЬ ПОКУПКУ",
            SCREEN_WIDTH // 2,
            skip_y,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка выбора улучшения"""
        button_width = 450
        button_height = 90
        start_y = SCREEN_HEIGHT * 0.65
        spacing = 120

        # Проверяем клики по кнопкам улучшений
        for i, upgrade in enumerate(self.upgrades):
            y_pos = start_y - i * spacing

            left = SCREEN_WIDTH // 2 - button_width // 2
            right = SCREEN_WIDTH // 2 + button_width // 2
            top = y_pos + button_height // 2
            bottom = y_pos - button_height // 2

            if (left <= x <= right and bottom <= y <= top and upgrade["can_afford"]):
                # Пытаемся купить улучшение
                success, message = self.game_view.player.apply_upgrade(upgrade["type"], upgrade["value"])
                
                # Обновляем информацию об улучшениях
                self.load_upgrades()
                
                # Сообщаем результат
                self.callback(upgrade["type"], upgrade["value"], success, message)
                
                if success:
                    # Если покупка успешна, сразу переходим на следующий уровень
                    self.window.show_view(self.game_view)
                else:
                    # Если не хватило денег, остаемся в магазине
                    pass
                break

        # Проверяем клик по кнопке пропуска
        skip_y = SCREEN_HEIGHT * 0.1
        if (SCREEN_WIDTH // 2 - 150 <= x <= SCREEN_WIDTH // 2 + 150 and
            skip_y - 25 <= y <= skip_y + 25):
            # Пропускаем покупку и переходим на следующий уровень
            self.callback(None, None, True, "Покупка пропущена")
            self.window.show_view(self.game_view)


class GameOverView(arcade.View):
    """Экран завершения игры"""

    def __init__(self, score, level, coins, window):
        super().__init__()
        self.score = score
        self.level = level
        self.coins = coins
        self.window_ref = window  # Сохраняем ссылку на окно

    def on_draw(self):
        """Отрисовка экрана завершения"""
        self.clear(arcade.color.DARK_SLATE_GRAY)

        # Полупрозрачный затемняющий слой
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
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
            SCREEN_HEIGHT * 0.5,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center"
        )
        
        # Монеты
        arcade.draw_text(
            f"Накоплено монет: {self.coins}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.45,
            arcade.color.GOLD,
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
