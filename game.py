"""
Основной класс игры
"""

import arcade
import math
from config import *
from player import Player
from enemy import Enemy
from room import RoomGenerator
from weapon import Bullet

class DungeonGame(arcade.Window):
    """Главный класс игры"""

    def __init__(self):
        """Инициализация игры"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Игровые объекты
        self.player = None
        self.rooms = None
        self.current_room = None
        self.enemies = None
        self.bullets = None
        self.items = None

        # Списки для рисования
        self.wall_list = None
        self.floor_list = None
        self.player_list = None
        self.enemy_list = None
        self.bullet_list = None
        self.item_list = None

        # UI текстовые объекты (для производительности)
        self.health_text = None
        self.ammo_text = None
        self.score_text = None
        self.level_text = None

        # Управление
        self.keys_pressed = set()
        self.mouse_position = (0, 0)

        # Состояние игры
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False

        # Таймеры
        self.fire_timer = 0

    def setup(self):
        """Настройка начального состояния игры"""
        print("Настройка игры...")

        # Инициализируем списки спрайтов
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()

        # Создаем игрока
        self.player = Player()
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player)

        # Создаем UI текстовые объекты
        self.health_text = arcade.Text("", 10, SCREEN_HEIGHT - 30, UI_COLOR, 20, font_name="Arial")
        self.ammo_text = arcade.Text("", 10, SCREEN_HEIGHT - 60, UI_COLOR, 20, font_name="Arial")
        self.score_text = arcade.Text("", SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30, UI_COLOR, 20, font_name="Arial")
        self.level_text = arcade.Text("", SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60, UI_COLOR, 20, font_name="Arial")

        # Генерируем комнаты
        self.rooms = RoomGenerator()
        self.current_room = self.rooms.generate_room()

        # Добавляем стены и пол текущей комнаты
        for tile in self.current_room["walls"]:
            wall = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, WALL_COLOR)
            wall.center_x = tile[0] * TILE_SIZE + TILE_SIZE // 2
            wall.center_y = tile[1] * TILE_SIZE + TILE_SIZE // 2
            self.wall_list.append(wall)

        for tile in self.current_room["floor"]:
            floor = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, FLOOR_COLOR)
            floor.center_x = tile[0] * TILE_SIZE + TILE_SIZE // 2
            floor.center_y = tile[1] * TILE_SIZE + TILE_SIZE // 2
            self.floor_list.append(floor)

        # Добавляем врагов
        self.enemies = arcade.SpriteList()
        for enemy_data in self.current_room["enemies"]:
            enemy = Enemy(enemy_data["type"])
            enemy.center_x = enemy_data["x"]
            enemy.center_y = enemy_data["y"]
            self.enemy_list.append(enemy)

        # Сбрасываем счет
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False

        print("Настройка завершена")

    def on_draw(self):
        """Отрисовка игры"""
        self.clear()

        # Рисуем в правильном порядке (сзади наперед)
        self.floor_list.draw()
        self.wall_list.draw()
        self.item_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()

        # Рисуем UI
        self.draw_ui()

    def draw_ui(self):
        """Отрисовка интерфейса"""
        # Обновляем текстовые объекты
        self.health_text.value = f"HP: {self.player.health}"
        self.ammo_text.value = f"Ammo: {self.player.ammo}"
        self.score_text.value = f"Score: {self.score}"
        self.level_text.value = f"Level: {self.level}"

        # Рисуем UI объекты
        self.health_text.draw()
        self.ammo_text.draw()
        self.score_text.draw()
        self.level_text.draw()

        # Сообщение о паузе
        if self.paused:
            arcade.draw_text("PAUSED", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2,
                           arcade.color.RED, 50, font_name="Arial", bold=True)

        # Сообщение о конце игры
        if self.game_over:
            arcade.draw_text("GAME OVER", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2,
                           arcade.color.RED, 50, font_name="Arial", bold=True)
            arcade.draw_text(f"Final Score: {self.score}", SCREEN_WIDTH // 2 - 120,
                           SCREEN_HEIGHT // 2 - 60, UI_COLOR, 30, font_name="Arial")

    def on_update(self, delta_time):
        """Обновление игровой логики"""
        if self.game_over or self.paused:
            return

        # Обновляем таймер стрельбы
        if self.fire_timer > 0:
            self.fire_timer -= delta_time

        # Обновляем игрока
        self.player.update(delta_time, self.keys_pressed)

        # Обновляем врагов (НЕ вызываем enemy_list.update()!)
        for enemy in self.enemy_list:
            enemy.update_ai(self.player, delta_time)

        # Обновляем пули
        self.bullet_list.update(delta_time)

        # Проверяем столкновения
        self.check_collisions()

        # Проверяем смерть игрока
        if self.player.health <= 0:
            self.game_over = True

    def check_collisions(self):
        """Проверка всех столкновений"""
        # Пули с врагами
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for enemy in hit_list:
                enemy.take_damage(BULLET_DAMAGE)
                bullet.remove_from_sprite_lists()
                if enemy.health <= 0:
                    enemy.remove_from_sprite_lists()
                    self.score += 10  # Очки за убийство врага

        # Игрок с врагами
        hit_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        for enemy in hit_list:
            if enemy.attack_cooldown <= 0:
                self.player.take_damage(10)
                enemy.attack_cooldown = 1.0  # 1 секунда между атаками
            else:
                enemy.attack_cooldown -= 0.016  # Примерно 1 кадр при 60 FPS

        # Игрок с предметами
        hit_list = arcade.check_for_collision_with_list(self.player, self.item_list)
        for item in hit_list:
            item.collect(self.player)
            item.remove_from_sprite_lists()
            self.score += ITEM_SCORES.get(item.type, 0)

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.P:
            self.paused = not self.paused
        elif key == arcade.key.R and self.game_over:
            self.setup()  # Рестарт

        # Управление движением
        movement_keys = {
            arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D,
            arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT
        }
        if key in movement_keys:
            self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_motion(self, x, y, dx, dy):
        """Обработка движения мыши"""
        self.mouse_position = (x, y)

        # Поворачиваем игрока в сторону курсора
        if self.player:
            delta_x = x - self.player.center_x
            delta_y = y - self.player.center_y
            self.player.angle = math.degrees(math.atan2(delta_y, delta_x))

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка нажатия кнопки мыши"""
        if button == arcade.MOUSE_BUTTON_LEFT and not self.game_over and not self.paused:
            self.fire_bullet()

    def fire_bullet(self):
        """Создание пули"""
        if self.fire_timer <= 0 and self.player.ammo > 0:
            # Создаем пулю
            bullet = Bullet()
            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.center_y

            # Направление к курсору
            target_x, target_y = self.mouse_position
            bullet.set_direction(target_x, target_y)

            # Добавляем пулю в список
            self.bullet_list.append(bullet)

            # Обновляем таймер и патроны
            self.fire_timer = FIRE_RATE
            self.player.ammo -= 1

            # TODO: Добавить звук выстрела
            # arcade.play_sound(self.shoot_sound)