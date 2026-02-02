import arcade
import random
import math
from enemy import Enemy
from door import Door
from upgrade_menu import UpgradeMenu

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Protocol0"


class DungeonGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.current_level = 1
        self.current_room_index = 0
        self.rooms = []
        self.doors = []
        self.enemies = []
        self.bullets = []
        self.player = None
        self.physics_engine = None
        self.door_list = arcade.SpriteList()
        self.score = 0
        self.room_cleared = False
        self._should_show_upgrade = False

        # Статистика игрока
        self.player_health = 100
        self.player_max_health = 100
        self.player_damage = 10
        self.player_speed = 5
        self.fire_rate = 0.5
        self.fire_timer = 0

        self.setup_level(self.current_level)

    def setup_level(self, level):
        print(f"Запуск уровня {level}")
        self.generate_rooms(level)
        self.setup_current_room()
        print("Настройка завершена")

    def generate_rooms(self, level):
        num_rooms = level
        print(f"Генерация уровня {level} с {num_rooms} комнатами")
        self.rooms = []

        for i in range(num_rooms):
            room = {
                'index': i,
                'enemies': random.randint(1, 3 + level),
                'cleared': False
            }
            self.rooms.append(room)

            if i < num_rooms - 1:
                door = Door(i, i + 1)
                self.doors.append(door)

        final_door = Door(num_rooms - 1, -1)
        self.doors.append(final_door)

    def setup_current_room(self):
        self.enemies = []
        self.bullets = []
        self.door_list = arcade.SpriteList()
        self.room_cleared = False

        self.player = arcade.SpriteCircle(20, arcade.color.BLUE)
        self.player.center_x = SCREEN_WIDTH // 4
        self.player.center_y = SCREEN_HEIGHT // 2

        room = self.rooms[self.current_room_index]
        for i in range(room['enemies']):
            enemy = Enemy()
            enemy.center_x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
            enemy.center_y = random.randint(50, SCREEN_HEIGHT - 50)
            enemy.health = 30 + (self.current_level * 5)
            enemy.max_health = 30 + (self.current_level * 5)
            enemy.damage = 5 + self.current_level
            self.enemies.append(enemy)

        if self.current_room_index < len(self.doors):
            door = self.doors[self.current_room_index]
            door_sprite = arcade.SpriteCircle(30, arcade.color.GREEN)
            door_sprite.center_x = SCREEN_WIDTH // 2
            door_sprite.center_y = SCREEN_HEIGHT // 2
            door_sprite.destination_room = door.destination_room  # ПРАВИЛЬНО!
            self.door_list.append(door_sprite)
            print(f"Дверь создана в центре комнаты ({door_sprite.center_x}, {door_sprite.center_y})")

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, arcade.SpriteList())
        self.fire_timer = 0

    def on_draw(self):
        # В View используем self.clear() вместо arcade.start_render()
        self.clear()

        # Рисуем фон
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                                          arcade.color.DARK_SLATE_GRAY)

        # Рисуем игрока
        self.player.draw()

        # Рисуем врагов
        for enemy in self.enemies:
            enemy.draw()

            if enemy.health < enemy.max_health:
                health_width = 40
                health_height = 5
                health_x = enemy.center_x - health_width // 2
                health_y = enemy.center_y + 30

                arcade.draw_rectangle_filled(
                    health_x + health_width // 2,
                    health_y,
                    health_width,
                    health_height,
                    arcade.color.RED
                )

                health_percentage = enemy.health / enemy.max_health
                arcade.draw_rectangle_filled(
                    health_x + (health_width * health_percentage) // 2,
                    health_y,
                    health_width * health_percentage,
                    health_height,
                    arcade.color.GREEN
                )

        # Рисуем пули
        for bullet in self.bullets:
            bullet.draw()

        # Рисуем дверь, если комната очищена
        if self.room_cleared:
            self.door_list.draw()

        # Рисуем UI
        health_text = arcade.Text(
            f"HP: {int(self.player_health)}/{self.player_max_health}",
            10, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 16
        )
        health_text.draw()

        level_text = arcade.Text(
            f"Уровень: {self.current_level} | Комната: {self.current_room_index + 1}/{len(self.rooms)}",
            10, SCREEN_HEIGHT - 60,
            arcade.color.WHITE, 16
        )
        level_text.draw()

        score_text = arcade.Text(
            f"Счет: {self.score}",
            SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 16
        )
        score_text.draw()

        stats_text = arcade.Text(
            f"Урон: {self.player_damage} | Скорость: {self.player_speed} | Скорострельность: {self.fire_rate:.1f}/сек",
            10, SCREEN_HEIGHT - 90,
            arcade.color.WHITE, 14
        )
        stats_text.draw()

    def on_update(self, delta_time):
        if self._should_show_upgrade:
            self._should_show_upgrade = False
            self.show_upgrade_menu()
            return

        self.fire_timer += delta_time

        self.physics_engine.update()

        for enemy in self.enemies:
            enemy.update(self.player)

            if arcade.check_for_collision(enemy, self.player):
                self.player_health -= enemy.damage * delta_time
                if self.player_health <= 0:
                    self.game_over()

        bullets_to_remove = []
        for bullet in self.bullets:
            bullet.center_x += bullet.change_x * delta_time * 500
            bullet.center_y += bullet.change_y * delta_time * 500

            if (bullet.center_x < 0 or bullet.center_x > SCREEN_WIDTH or
                    bullet.center_y < 0 or bullet.center_y > SCREEN_HEIGHT):
                bullets_to_remove.append(bullet)
                continue

            for enemy in self.enemies:
                if arcade.check_for_collision(bullet, enemy):
                    enemy.take_damage(self.player_damage)
                    bullets_to_remove.append(bullet)

                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.score += 10
                        print(f"Враг уничтожен! Очков: {self.score}")
                    break

        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)

        if not self.room_cleared and len(self.enemies) == 0:
            self.room_cleared = True
            print("Комната очищена! Дверь открыта в центре комнаты.")
            self.check_collisions()

        if self.player_health <= 0:
            self.game_over()

    def check_collisions(self):
        if self.room_cleared:
            hit_list = arcade.check_for_collision_with_list(self.player, self.door_list)
            if hit_list:
                self.transition_to_room(hit_list[0].destination_room)

    def transition_to_room(self, room_index):
        print(f"Переход: {room_index}")

        if room_index == -1:
            print("Последняя комната уровня пройдена! Показываем меню улучшений.")
            self._should_show_upgrade = True
        elif 0 <= room_index < len(self.rooms):
            self.current_room_index = room_index
            self.setup_current_room()
        else:
            self.current_level += 1
            self.current_room_index = 0
            self.setup_level(self.current_level)

    def show_upgrade_menu(self):
        upgrade_menu = UpgradeMenu(self)
        upgrade_menu.setup()

        window = self.window if hasattr(self, 'window') else arcade.get_window()
        if window:
            window.show_view(upgrade_menu)
        else:
            print("Ошибка: Окно не найдено")

    def game_over(self):
        from menu import MenuView
        print(f"Игра окончена! Итоговый счет: {self.score}")

        menu_view = MenuView()
        window = self.window if hasattr(self, 'window') else arcade.get_window()
        if window:
            window.show_view(menu_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = self.player_speed
        elif key == arcade.key.S:
            self.player.change_y = -self.player_speed
        elif key == arcade.key.A:
            self.player.change_x = -self.player_speed
        elif key == arcade.key.D:
            self.player.change_x = self.player_speed

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.fire_timer >= 1 / self.fire_rate:
            self.shoot(x, y)
            self.fire_timer = 0

    def shoot(self, target_x, target_y):
        bullet = arcade.SpriteCircle(5, arcade.color.YELLOW)
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y

        dx = target_x - self.player.center_x
        dy = target_y - self.player.center_y
        distance = max(math.sqrt(dx * dx + dy * dy), 0.1)

        bullet.change_x = dx / distance
        bullet.change_y = dy / distance

        self.bullets.append(bullet)