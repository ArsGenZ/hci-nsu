import pygame
import random
import sys
import pickle
import math

# Инициализация Pygame
pygame.init()

# --- КОНСТАНТЫ ---
WIDTH, HEIGHT = 800, 400
FPS = 60
GROUND_Y = 350  # Уровень земли (Y координата низа)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game with Sensor & AI")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Параметры Динозавра
DINO_X = 50
DINO_WIDTH = 40
DINO_HEIGHT_NORMAL = 60
DINO_HEIGHT_DUCK = 30
JUMP_POWER = -14
GRAVITY = 0.8
SPEED = 6

# Параметры Сенсора
SENSOR_RANGE = 250  # Дальность обзора
SENSOR_HEIGHT = 100 # Высота зоны сканирования

class Dinosaur:
    def __init__(self):
        self.rect = pygame.Rect(DINO_X, GROUND_Y - DINO_HEIGHT_NORMAL, DINO_WIDTH, DINO_HEIGHT_NORMAL)
        self.vel_y = 0
        self.is_jumping = False
        self.is_ducking = False
        self.color = BLACK
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_POWER
            self.is_jumping = True
            self.on_ground = False

    def duck(self, is_pressed):
        if is_pressed:
            if not self.is_jumping: # Приседать можно только на земле
                if not self.is_ducking:
                    self.is_ducking = True
                    self.rect.height = DINO_HEIGHT_DUCK
                    self.rect.y = GROUND_Y - DINO_HEIGHT_DUCK
                    self.color = GRAY
        else:
            if self.is_ducking:
                self.is_ducking = False
                self.rect.height = DINO_HEIGHT_NORMAL
                self.rect.y = GROUND_Y - DINO_HEIGHT_NORMAL
                self.color = BLACK

    def update(self):
        # Гравитация
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Проверка земли
        if self.rect.y >= GROUND_Y - self.rect.height:
            self.rect.y = GROUND_Y - self.rect.height
            self.vel_y = 0
            self.is_jumping = False
            self.on_ground = True
        else:
            self.on_ground = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Obstacle:
    def __init__(self, type_):
        self.type = type_ # 'cactus' или 'bird'
        self.speed = SPEED
        self.marked_for_deletion = False

        if self.type == 'cactus':
            self.width = 30
            self.height = 50
            self.x = WIDTH + random.randint(0, 200)
            self.y = GROUND_Y - self.height
            self.color = GREEN
        elif self.type == 'bird':
            self.width = 40
            self.height = 30
            self.x = WIDTH + random.randint(0, 200)
            # Птица летит на уровне, чтобы можно было прыгнуть ИЛИ присесть
            # Высота динозавра 60, присед 30.
            # Пусть птица будет на высоте 35 от земли.
            # Динозавр (60) заденет её головой. Динозавр (30) пролезет. Динозавр в прыжке перелетит.
            self.y = GROUND_Y - 45
            self.color = RED

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x -= self.speed
        self.rect.x = int(self.x)
        if self.x + self.width < 0:
            self.marked_for_deletion = True

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Sensor:
    """
    Сенсор сканирует пространство перед динозавром.
    Возвращает нормализованные данные для нейросети.
    """
    def __init__(self, dino):
        self.dino = dino
        self.range = SENSOR_RANGE
        self.data = {
            'dist_cactus': 1.0,   # Нормализованное расстояние до кактуса (0-1)
            'height_cactus': 0.0, # Относительная высота
            'dist_bird': 1.0,     # Нормализованное расстояние до птицы
            'height_bird': 0.0,   # Относительная высота
            'dino_vel_y': 0.0,    # Скорость динозавра
            'is_jumping': 0.0     # Флаг прыжка
        }

    def scan(self, obstacles):
        # Сброс данных по умолчанию (если препятствий нет в радиусе)
        closest_cactus_dist = self.range
        closest_bird_dist = self.range
        cactus_h = 0
        bird_h = 0

        dino_right = self.dino.rect.right

        for obs in obstacles:
            dist = obs.rect.left - dino_right

            if 0 < dist < self.range:
                if obs.type == 'cactus':
                    if dist < closest_cactus_dist:
                        closest_cactus_dist = dist
                        cactus_h = obs.height
                elif obs.type == 'bird':
                    if dist < closest_bird_dist:
                        closest_bird_dist = dist
                        bird_h = obs.rect.y # Абсолютная Y позиция птицы

        # Нормализация данных (0.0 - очень близко/высоко, 1.0 - далеко/нет препятствия)
        # Для расстояния: 0 = препятствие вплотную, 1 = за пределами сенсора
        self.data['dist_cactus'] = min(closest_cactus_dist / self.range, 1.0)
        self.data['dist_bird'] = min(closest_bird_dist / self.range, 1.0)

        # Для высоты: нормализуем относительно размера динозавра
        self.data['height_cactus'] = cactus_h / DINO_HEIGHT_NORMAL
        self.data['height_bird'] = bird_h / HEIGHT

        self.data['dino_vel_y'] = self.dino.vel_y / 15.0 # Примерная макс скорость
        self.data['is_jumping'] = 1.0 if self.dino.is_jumping else 0.0

        return [
            self.data['dist_cactus'],
            self.data['height_cactus'],
            self.data['dist_bird'],
            self.data['height_bird'],
            self.data['dino_vel_y'],
            self.data['is_jumping']
        ]

    def draw_debug(self, surface):
        # Визуализация сенсора (полупрозрачный прямоугольник)
        sensor_rect = pygame.Rect(self.dino.rect.right, self.dino.rect.top - 20, self.range, self.dino.rect.height + 40)
        s = pygame.Surface((sensor_rect.width, sensor_rect.height), pygame.SRCALPHA)
        s.fill((0, 255, 0, 50)) # Зеленый прозрачный
        surface.blit(s, sensor_rect.topleft)

class NeuralNetwork:
    def __init__(self, input_size=6, hidden_size=8, output_size=2):
        # Входы: [dist_cactus, h_cactus, dist_bird, h_bird, vel_y, is_jumping]
        # Выходы: [action_jump, action_duck]
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Инициализация весов случайными числами
        self.weights_ih = [[random.uniform(-1, 1) for _ in range(hidden_size)] for _ in range(input_size)]
        self.weights_ho = [[random.uniform(-1, 1) for _ in range(output_size)] for _ in range(hidden_size)]
        self.bias_h = [random.uniform(-1, 1) for _ in range(hidden_size)]
        self.bias_o = [random.uniform(-1, 1) for _ in range(output_size)]

    def sigmoid(self, x):
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            return 1.0 if x > 0 else 0.0

    def predict(self, inputs):
        # Hidden layer
        hidden = []
        for j in range(self.hidden_size):
            sum_val = self.bias_h[j]
            for i in range(self.input_size):
                sum_val += inputs[i] * self.weights_ih[i][j]
            hidden.append(self.sigmoid(sum_val))

        # Output layer
        outputs = []
        for k in range(self.output_size):
            sum_val = self.bias_o[k]
            for j in range(self.hidden_size):
                sum_val += hidden[j] * self.weights_ho[j][k]
            outputs.append(self.sigmoid(sum_val))

        return outputs

    def save(self, filename='dino_nn_model.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump({
                'weights_ih': self.weights_ih,
                'weights_ho': self.weights_ho,
                'bias_h': self.bias_h,
                'bias_o': self.bias_o
            }, f)
        print(f"Model saved to {filename}")

    def load(self, filename='dino_nn_model.pkl'):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                self.weights_ih = data['weights_ih']
                self.weights_ho = data['weights_ho']
                self.bias_h = data['bias_h']
                self.bias_o = data['bias_o']
            print(f"Model loaded from {filename}")
            return True
        except FileNotFoundError:
            print("No model found. Starting with random weights.")
            return False

def main():
    dino = Dinosaur()
    sensor = Sensor(dino)
    nn = NeuralNetwork()

    # Попытка загрузить модель, если есть
    nn.load()

    obstacles = []
    spawn_timer = 0
    score = 0
    game_over = False
    auto_mode = False # Режим автопилота

    running = True
    while running:
        clock.tick(FPS)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # Рестарт игры
                        dino = Dinosaur()
                        obstacles = []
                        score = 0
                        game_over = False
                        spawn_timer = 0
                    else:
                        if not auto_mode:
                            dino.jump()

                if event.key == pygame.K_a:
                    auto_mode = not auto_mode
                    print(f"Auto mode: {auto_mode}")

                if event.key == pygame.K_s and not game_over and not auto_mode:
                    dino.duck(True)

                if event.key == pygame.K_t:
                    # Тренировка (упрощенная генерация данных для примера)
                    print("Training placeholder...")
                    nn.save()

                if event.key == pygame.K_l:
                    nn.load()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    dino.duck(False)

        if not game_over:
            # Логика ИИ
            if auto_mode:
                inputs = sensor.scan(obstacles)
                outputs = nn.predict(inputs)

                # outputs[0] -> Jump, outputs[1] -> Duck
                if outputs[0] > 0.7: # Порог для прыжка
                    dino.jump()
                elif outputs[1] > 0.7: # Порог для приседа
                    dino.duck(True)
                else:
                    dino.duck(False)
            else:
                sensor.scan(obstacles) # Просто обновляем сенсор для отладки

            # Спавн препятствий
            spawn_timer += 1
            if spawn_timer > random.randint(60, 150):
                spawn_timer = 0
                # 70% кактус, 30% птица
                type_ = 'cactus' if random.random() < 0.7 else 'bird'
                obstacles.append(Obstacle(type_))

            # Обновление объектов
            dino.update()
            for obs in obstacles:
                obs.update()

            # Удаление старых препятствий
            obstacles = [obs for obs in obstacles if not obs.marked_for_deletion]

            # Проверка столкновений
            # Уменьшаем хитбокс для более честной игры (padding)
            padding = 5
            dino_hitbox = pygame.Rect(dino.rect.x + padding, dino.rect.y + padding,
                                      dino.rect.width - 2*padding, dino.rect.height - 2*padding)

            for obs in obstacles:
                obs_hitbox = pygame.Rect(obs.rect.x + padding, obs.rect.y + padding,
                                         obs.rect.width - 2*padding, obs.rect.height - 2*padding)
                if dino_hitbox.colliderect(obs_hitbox):
                    game_over = True

            score += 0.1

        # Отрисовка
        screen.fill(WHITE)

        # Земля
        pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

        dino.draw(screen)
        for obs in obstacles:
            obs.draw(screen)

        # Отрисовка сенсора (для наглядности)
        if auto_mode or True: # Всегда рисуем для отладки
            sensor.draw_debug(screen)

        # Интерфейс
        score_text = font.render(f"Score: {int(score)}", True, BLACK)
        screen.blit(score_text, (10, 10))

        mode_text = font.render("AUTO" if auto_mode else "MANUAL", True, BLUE)
        screen.blit(mode_text, (10, 50))

        info_text = font.render("Space: Jump/Restart | S: Duck | A: Auto | L: Load", True, GRAY)
        small_font = pygame.font.Font(None, 24)
        info_surf = small_font.render("Space: Jump/Restart | S: Duck | A: Auto | L: Load", True, GRAY)
        screen.blit(info_surf, (10, HEIGHT - 30))

        if game_over:
            over_text = font.render("GAME OVER", True, RED)
            rect = over_text.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(over_text, rect)
            restart_text = small_font.render("Press SPACE to restart", True, BLACK)
            rect2 = restart_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 30))
            screen.blit(restart_text, rect2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
