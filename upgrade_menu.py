"""
Тестирование системы улучшений (отдельный модуль)
Запускается отдельно для демонстрации системы улучшений
"""

import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player


class UpgradeTestView(arcade.View):
    """Тестовое представление для демонстрации системы улучшений"""
    
    def __init__(self):
        super().__init__()
        self.player = Player()  # Создаем тестового игрока
        self.selected_upgrade = None
        self.upgrades = [
            {
                "name": "Увеличить здоровье",
                "type": "health", 
                "value": 25,
                "description": "+25 к максимальному здоровью",
                "color": arcade.color.RED
            },
            {
                "name": "Увеличить урон",
                "type": "damage",
                "value": 1.2,
                "description": "+20% к урону",
                "color": arcade.color.ORANGE
            },
            {
                "name": "Увеличить скорость",
                "type": "speed",
                "value": 1.15,
                "description": "+15% к скорости движения",
                "color": arcade.color.BLUE
            },
            # Убраны: "Восстановить здоровье" и "Увеличить патроны"
        ]
    
    def on_draw(self):
        """Отрисовка тестового интерфейса улучшений"""
        self.clear(arcade.color.DARK_SLATE_GRAY)
        
        # Заголовок
        arcade.draw_text(
            "СИСТЕМА УЛУЧШЕНИЙ - ТЕСТОВЫЙ РЕЖИМ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.9,
            arcade.color.GOLD,
            font_size=30,
            anchor_x="center",
            bold=True
        )
        
        arcade.draw_text(
            "Выберите улучшение для применения",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.85,
            arcade.color.LIGHT_GRAY,
            font_size=20,
            anchor_x="center"
        )
        
        # Текущие характеристики игрока
        stats_y = SCREEN_HEIGHT * 0.75
        arcade.draw_text(
            "ТЕКУЩИЕ ХАРАКТЕРИСТИКИ:",
            SCREEN_WIDTH // 2,
            stats_y,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="center",
            bold=True
        )
        
        stats = [
            f"Здоровье: {self.player.health}/{self.player.max_health}",
            f"Множитель урона: {self.player.damage_multiplier:.1f}x",
            f"Скорость: {self.player.speed:.0f}",
            f"Патроны: {self.player.ammo}"
        ]
        
        for i, stat in enumerate(stats):
            arcade.draw_text(
                stat,
                SCREEN_WIDTH // 2,
                stats_y - 30 - (i * 30),
                arcade.color.LIGHT_GRAY,
                font_size=18,
                anchor_x="center"
            )
        
        # Кнопки улучшений (только 3 теперь)
        button_width = 350
        button_height = 70
        start_y = SCREEN_HEIGHT * 0.55
        spacing = 85
        
        for i, upgrade in enumerate(self.upgrades):
            y_pos = start_y - (i * spacing)
            
            # Рисуем кнопку
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2,
                y_pos,
                button_width,
                button_height,
                upgrade["color"]
            )
            
            # Рамка кнопки
            arcade.draw_rectangle_outline(
                SCREEN_WIDTH // 2,
                y_pos,
                button_width,
                button_height,
                arcade.color.WHITE,
                2
            )
            
            # Название улучшения
            arcade.draw_text(
                upgrade["name"],
                SCREEN_WIDTH // 2,
                y_pos + 10,
                arcade.color.WHITE,
                font_size=22,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )
            
            # Описание улучшения
            arcade.draw_text(
                upgrade["description"],
                SCREEN_WIDTH // 2,
                y_pos - 10,
                arcade.color.WHITE,
                font_size=16,
                anchor_x="center",
                anchor_y="center"
            )
        
        # Кнопка сброса
        reset_y = SCREEN_HEIGHT * 0.12
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2,
            reset_y,
            250,
            50,
            arcade.color.DARK_RED
        )
        
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH // 2,
            reset_y,
            250,
            50,
            arcade.color.WHITE,
            2
        )
        
        arcade.draw_text(
            "СБРОС ХАРАКТЕРИСТИК",
            SCREEN_WIDTH // 2,
            reset_y,
            arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
            anchor_y="center"
        )
        
        # Кнопка выхода
        exit_y = SCREEN_HEIGHT * 0.05
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2,
            exit_y,
            150,
            40,
            arcade.color.DARK_GRAY
        )
        
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH // 2,
            exit_y,
            150,
            40,
            arcade.color.WHITE,
            2
        )
        
        arcade.draw_text(
            "ВЫХОД",
            SCREEN_WIDTH // 2,
            exit_y,
            arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
            anchor_y="center"
        )
        
        # Показываем выбранное улучшение
        if self.selected_upgrade:
            arcade.draw_text(
                f"Выбрано: {self.selected_upgrade['name']}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT * 0.95,
                arcade.color.GREEN,
                font_size=18,
                anchor_x="center"
            )
    
    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка кликов мыши"""
        button_width = 350
        button_height = 70
        start_y = SCREEN_HEIGHT * 0.55
        spacing = 85
        
        # Проверяем клики по кнопкам улучшений
        for i, upgrade in enumerate(self.upgrades):
            y_pos = start_y - (i * spacing)
            
            if (SCREEN_WIDTH // 2 - button_width // 2 <= x <= SCREEN_WIDTH // 2 + button_width // 2 and
                y_pos - button_height // 2 <= y <= y_pos + button_height // 2):
                
                self.selected_upgrade = upgrade
                result = self.player.apply_upgrade(upgrade["type"], upgrade["value"])
                print(f"Применено улучшение: {result}")
                
                # Показываем сообщение в консоли
                print(f"Новые характеристики:")
                print(f"  Здоровье: {self.player.health}/{self.player.max_health}")
                print(f"  Урон: {self.player.damage_multiplier:.1f}x")
                print(f"  Скорость: {self.player.speed:.0f}")
                print(f"  Патроны: {self.player.ammo}")
                break
        
        # Кнопка сброса
        reset_y = SCREEN_HEIGHT * 0.12
        if (SCREEN_WIDTH // 2 - 125 <= x <= SCREEN_WIDTH // 2 + 125 and
            reset_y - 25 <= y <= reset_y + 25):
            
            # Сбрасываем характеристики игрока
            self.player = Player()
            self.selected_upgrade = None
            print("Характеристики сброшены к исходным")
        
        # Кнопка выхода
        exit_y = SCREEN_HEIGHT * 0.05
        if (SCREEN_WIDTH // 2 - 75 <= x <= SCREEN_WIDTH // 2 + 75 and
            exit_y - 20 <= y <= exit_y + 20):
            
            arcade.close_window()
    
    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш (для удобства тестирования)"""
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.R:
            # Сброс по клавише R
            self.player = Player()
            self.selected_upgrade = None
            print("Характеристики сброшены к исходным")
        elif key == arcade.key.H:
            # Применение улучшения здоровья по клавише H
            self.selected_upgrade = self.upgrades[0]
            result = self.player.apply_upgrade("health", 25)
            print(f"Применено улучшение здоровья: {result}")
        elif key == arcade.key.D:
            # Применение улучшения урона по клавише D
            self.selected_upgrade = self.upgrades[1]
            result = self.player.apply_upgrade("damage", 1.2)
            print(f"Применено улучшение урона: {result}")
        elif key == arcade.key.S:
            # Применение улучшения скорости по клавише S
            self.selected_upgrade = self.upgrades[2]
            result = self.player.apply_upgrade("speed", 1.15)
            print(f"Применено улучшение скорости: {result}")
        elif key == arcade.key.ENTER:
            # Тестирование всех улучшений по очереди
            print("\n=== Тестирование всех улучшений ===")
            for upgrade in self.upgrades:
                self.player.apply_upgrade(upgrade["type"], upgrade["value"])
                print(f"Применено: {upgrade['name']}")
            print("=== Тест завершен ===\n")


def test_upgrade_system():
    """Основная функция для тестирования системы улучшений"""
    
    # Тестируем улучшения в консоли
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ СИСТЕМЫ УЛУЧШЕНИЙ")
    print("=" * 50)
    
    test_player = Player()
    print("\nИсходные характеристики игрока:")
    print(f"  Здоровье: {test_player.health}/{test_player.max_health}")
    print(f"  Урон: {test_player.damage_multiplier:.1f}x")
    print(f"  Скорость: {test_player.speed:.0f}")
    print(f"  Патроны: {test_player.ammo}")
    
    print("\nПрименяем улучшения:")
    
    # Улучшение здоровья
    result = test_player.apply_upgrade("health", 25)
    print(f"1. {result}")
    
    # Улучшение урона
    result = test_player.apply_upgrade("damage", 1.2)
    print(f"2. {result}")
    
    # Улучшение скорости
    result = test_player.apply_upgrade("speed", 1.15)
    print(f"3. {result}")
    
    print("\nИтоговые характеристики игрока:")
    print(f"  Здоровье: {test_player.health}/{test_player.max_health}")
    print(f"  Урон: {test_player.damage_multiplier:.1f}x")
    print(f"  Скорость: {test_player.speed:.0f}")
    print(f"  Патроны: {test_player.ammo}")
    print("=" * 50)


def main():
    """Главная функция запуска тестирования"""
    
    # Сначала показываем тест в консоли
    test_upgrade_system()
    
    # Затем запускаем графический интерфейс
    window = arcade.Window(
        SCREEN_WIDTH, 
        SCREEN_HEIGHT, 
        "Тестирование системы улучшений"
    )
    
    upgrade_view = UpgradeTestView()
    window.show_view(upgrade_view)
    
    print("\n" + "="*50)
    print("ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ТЕСТИРОВАНИЯ")
    print("="*50)
    print("Управление в GUI:")
    print("  • Клик по кнопке - применить улучшение")
    print("  • H/D/S - применить улучшения здоровья/урона/скорости (горячие клавиши)")
    print("  • ENTER - применить все улучшения по очереди")
    print("  • R - сбросить характеристики")
    print("  • ESC - выход\n")
    
    arcade.run()


if __name__ == "__main__":
    main()
