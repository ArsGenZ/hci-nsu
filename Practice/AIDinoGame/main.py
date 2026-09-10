import pygame
import random
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import pickle
import os

# --- КОНСТАНТЫ И НАСТРОЙКИ ---
WIDTH, HEIGHT = 800, 400
FPS = 60
GROUND_Y = HEIGHT - 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
DINO_COLOR = BLACK
DUCK_COLOR = (50, 50, 50) # Темно-серый для приседа
JUMP_COLOR = (0, 100, 255) # Синий для прыжка

# Параметры Динозавра
DINO_X = 50
DINO_WIDTH = 40
DINO_HEIGHT_NORMAL = 60
DINO_HEIGHT_DUCK = 30
JUMP_POWER = -13
GRAVITY = 0.6
MOVE_SPEED = 7

# Параметры Препятствий
CACTUS_WIDTH = 30
CACTUS_HEIGHT = 50
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
# Высота птицы: должна быть проходимой прыжком или приседом
# Земля на GROUND_Y. Динозавр стоит на GROUND_Y - 60.
# Птица летит на уровне "головы" динозавра, чтобы под нее можно было присесть,
# но если прыгнуть - перелететь её, или если не прыгать - она врежется, если не присесть.
# Пусть птица летит на высоте 30 пикселей от земли (низко), но динозавр высокий.
# Логика: Птица летит так, что её нижний край выше присевшего динозавра, но ниже стоящего.
BIRD_Y_RELATIVE = 25 # Расстояние от земли до низа птицы

# Сенсор
SENSOR_RANGE = 250

# --- НЕЙРОСЕТЬ (PYTORCH) ---
class DinoNet(nn.Module):
    def __init__(self, input_size=6, hidden_size=16, output_size=3):
        super(DinoNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Глобальные переменные для модели
model = DinoNet()
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()
MODEL_PATH = "dino_model_pytorch.pth"

# Действия: 0 = Ничего не делать (или бежать), 1 = Прыжок, 2 = Присед
ACTION_NONE = 0
ACTION_JUMP = 1
ACTION_DUCK = 2

# --- КЛАССЫ ---

class Dinosaur:
    def __init__(self):
        self.rect = pygame.Rect(DINO_X, GROUND_Y - DINO_HEIGHT_NORMAL, DINO_WIDTH, DINO_HEIGHT_NORMAL)
        self.vel_y = 0
        self.is_jumping = False
        self.is_ducking = False
        self.color = DINO_COLOR
        self.original_height = DINO_HEIGHT_NORMAL

    def jump(self):
        if not self.is_jumping and not self.is_ducking:
            self.vel_y = JUMP_POWER
            self.is_jumping = True
            self.color = JUMP_COLOR

    def duck(self, is_ducking):
        if self.is_ducking != is_ducking and not self.is_jumping:
            self.is_ducking = is_ducking
            if self.is_ducking:
                self.rect.height = DINO_HEIGHT_DUCK
                self.rect.y = GROUND_Y - DINO_HEIGHT_DUCK
                self.color = DUCK_COLOR
            else:
                self.rect.height = DINO_HEIGHT_NORMAL
                self.rect.y = GROUND_Y - DINO_HEIGHT_NORMAL
                self.color = DINO_COLOR

    def update(self):
        # Гравитация
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Приземление
        if self.rect.y >= GROUND_Y - self.rect.height:
            self.rect.y = GROUND_Y - self.rect.height
            self.vel_y = 0
            self.is_jumping = False
            if not self.is_ducking:
                self.color = DINO_COLOR
            else:
                self.color = DUCK_COLOR

        # Если приседаем в воздухе (редкий кейс, но для надежности)
        if self.is_ducking and not self.is_jumping:
             self.rect.y = GROUND_Y - self.rect.height

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Obstacle:
    def __init__(self, type_):
        self.type = type_ # 'cactus' или 'bird'
        self.x = WIDTH + random.randint(0, 100)

        if self.type == 'cactus':
            self.rect = pygame.Rect(self.x, GROUND_Y - CACTUS_HEIGHT, CACTUS_WIDTH, CACTUS_HEIGHT)
            self.color = GREEN
            self.speed = MOVE_SPEED
        elif self.type == 'bird':
            # Птица летит на фиксированной высоте от земли
            y_pos = GROUND_Y - BIRD_Y_RELATIVE - BIRD_HEIGHT
            self.rect = pygame.Rect(self.x, y_pos, BIRD_WIDTH, BIRD_HEIGHT)
            self.color = RED
            self.speed = MOVE_SPEED * 1.2 # Птицы чуть быстрее

    def update(self):
        self.x -= self.speed
        self.rect.x = int(self.x)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Sensor:
    def __init__(self, dino):
        self.dino = dino

    def scan(self, obstacles):
        """
        Возвращает вектор признаков для нейросети:
        [dist_cactus, height_diff_cactus, dist_bird, height_diff_bird, dy, is_jumping]
        Все значения нормализуются примерно к [-1, 1] или [0, 1]
        """
        dist_cactus = SENSOR_RANGE
        h_diff_cactus = 0.0
        dist_bird = SENSOR_RANGE
        h_diff_bird = 0.0

        # Ищем ближайшее препятствие каждого типа в диапазоне сенсора
        for obs in obstacles:
            if obs.x < self.dino.rect.right and obs.x > self.dino.rect.left - SENSOR_RANGE:
                dist = obs.x - self.dino.rect.right

                if obs.type == 'cactus':
                    if dist < dist_cactus:
                        dist_cactus = dist
                        # Разница высот: центр кактуса относительно центра динозавра
                        h_diff_cactus = (obs.rect.centery - self.dino.rect.centery) / HEIGHT

                elif obs.type == 'bird':
                    if dist < dist_bird:
                        dist_bird = dist
                        h_diff_bird = (obs.rect.centery - self.dino.rect.centery) / HEIGHT

        # Нормализация дистанции (0..1 где 1 это далеко)
        norm_dist_cactus = min(dist_cactus / SENSOR_RANGE, 1.0)
        norm_dist_bird = min(dist_bird / SENSOR_RANGE, 1.0)

        # Скорость по Y нормализуем
        norm_dy = self.dino.vel_y / abs(JUMP_POWER)

        # Флаг прыжка
        is_jumping = 1.0 if self.dino.is_jumping else 0.0

        # Вектор: [dist_cact, h_cact, dist_bird, h_bird, dy, jump_flag]
        return [norm_dist_cactus, h_diff_cactus, norm_dist_bird, h_diff_bird, norm_dy, is_jumping]

# --- ФУНКЦИИ ИГРЫ ---

def get_input_tensor(sensor, obstacles):
    data = sensor.scan(obstacles)
    return torch.FloatTensor(data).unsqueeze(0) # Размер [1, 6]

def generate_training_data(sensor, obstacles, dino):
    """Генерирует одно правильное действие на основе текущей ситуации"""
    inputs = sensor.scan(obstacles)
    target = ACTION_NONE

    dist_cact = inputs[0] * SENSOR_RANGE
    h_cact = inputs[1]
    dist_bird = inputs[2] * SENSOR_RANGE
    h_bird = inputs[3]

    # Логика принятия решений для учителя (Supervised Learning)

    # 1. Кактус близко
    if dist_cact < 120 and dist_cact > 0:
        if not dino.is_jumping:
            target = ACTION_JUMP

    # 2. Птица близко
    if dist_bird < 120 and dist_bird > 0:
        # Птица летит низко.
        # Если мы стоим - нужно присесть (птица заденет голову)
        # Если мы в воздухе - мы можем перелететь её, но если мы слишком низко - врежемся.
        # Упрощенная логика: если птица близко и мы не в высоком прыжке -> присесть.
        # Если мы на земле -> присесть.
        if not dino.is_jumping or (dino.is_jumping and dino.rect.y > GROUND_Y - 40):
             target = ACTION_DUCK
        else:
             # Если уже высоко прыгнули, ничего не делаем
             target = ACTION_NONE

    # Приоритет: если оба близко, кактус опаснее для ног, птица для головы.
    # Но обычно они не спавнятся в одной точке X.

    return inputs, target

def train_step(inputs_list, targets_list):
    if len(inputs_list) == 0:
        return 0.0

    X = torch.FloatTensor(inputs_list)
    y = torch.LongTensor(targets_list)

    optimizer.zero_grad()
    outputs = model(X)
    loss = criterion(outputs, y)
    loss.backward()
    optimizer.step()

    return loss.item()

def save_model():
    torch.save(model.state_dict(), MODEL_PATH)
    print("Модель сохранена в", MODEL_PATH)

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH))
        model.eval()
        print("Модель загружена.")
        return True
    else:
        print("Модель не найдена.")
        return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dino Game (PyTorch AI)")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    dino = Dinosaur()
    sensor = Sensor(dino)
    obstacles = []

    score = 0
    game_over = False
    auto_play = False
    training_mode = False # Режим быстрой генерации данных без отрисовки

    spawn_timer = 0

    # Данные для обучения
    train_inputs = []
    train_targets = []

    running = True
    while running:
        # 1. Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    if game_over:
                        # Рестарт
                        dino = Dinosaur()
                        obstacles = []
                        score = 0
                        game_over = False
                        train_inputs = []
                        train_targets = []
                    elif not auto_play and not training_mode:
                        dino.jump()

                if event.key == pygame.K_s:
                    if not auto_play and not training_mode and not dino.is_jumping:
                        dino.duck(True)

                if event.key == pygame.K_a:
                    auto_play = not auto_play
                    print(f"Автопилот: {'ВКЛ' if auto_play else 'ВЫКЛ'}")

                if event.key == pygame.K_t:
                    # Запуск быстрого обучения (симуляция)
                    training_mode = True
                    print("Начало сбора данных для обучения... (нажмите T снова для остановки и сохранения)")

                if event.key == pygame.K_l:
                    load_model()

                if event.key == pygame.K_r:
                    # Тестирование
                    if load_model():
                        auto_play = True
                        print("Запуск тестирования модели...")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    if not auto_play and not training_mode:
                        dino.duck(False)

        # 2. Логика игры
        if not game_over:
            # Спавн препятствий
            spawn_timer += 1
            # Случайный интервал спавна
            if spawn_timer > random.randint(60, 140):
                r = random.random()
                if r < 0.7:
                    obstacles.append(Obstacle('cactus'))
                else:
                    obstacles.append(Obstacle('bird'))
                spawn_timer = 0

            # Обновление препятствий
            for obs in obstacles[:]:
                obs.update()
                if obs.x < -50:
                    obstacles.remove(obs)
                    score += 10

                # Коллизия
                # Уменьшаем хитбокс для честности (padding)
                padding = 5
                dino_hitbox = pygame.Rect(dino.rect.x + padding, dino.rect.y + padding,
                                          dino.rect.width - 2*padding, dino.rect.height - 2*padding)
                obs_hitbox = pygame.Rect(obs.rect.x + padding, obs.rect.y + padding,
                                         obs.rect.width - 2*padding, obs.rect.height - 2*padding)

                if dino_hitbox.colliderect(obs_hitbox):
                    game_over = True
                    if training_mode:
                        training_mode = False
                        print("Столкновение! Данные сброшены.")
                        train_inputs = []
                        train_targets = []

            # Логика AI / Обучения
            if auto_play or training_mode:
                inputs = get_input_tensor(sensor, obstacles)
                with torch.no_grad():
                    prediction = model(inputs)
                    action = torch.argmax(prediction, dim=1).item()

                # Выполнение действия
                if action == ACTION_JUMP:
                    if not dino.is_jumping and not dino.is_ducking:
                        dino.jump()
                elif action == ACTION_DUCK:
                    if not dino.is_jumping:
                        dino.duck(True)
                    else:
                        # Если в прыжке и сеть говорит присесть - отпускаем присед (если был)
                        # Но в нашей логике duck(False) вызывается при отпускании клавиши.
                        # Здесь просто гарантируем, что мы не застрянем в приседе если это опасно
                        pass
                else:
                    # ACTION_NONE
                    if not auto_play and not training_mode:
                         pass # Человек управляет
                    else:
                        # AI отпускает присед если он был зажат
                        if dino.is_ducking:
                            dino.duck(False)

                # Сбор данных для обучения если режим тренировки
                if training_mode:
                    inp_list, tgt = generate_training_data(sensor, obstacles, dino)
                    train_inputs.append(inp_list)
                    train_targets.append(tgt)

                    # Периодическое обучение батчами
                    if len(train_inputs) % 50 == 0 and len(train_inputs) > 0:
                        loss = train_step(train_inputs[-100:], train_targets[-100:]) # Берем последние 100
                        # print(f"Loss: {loss:.4f}")

        # 3. Отрисовка
        if not training_mode:
            screen.fill(WHITE)

            # Земля
            pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

            # Сенсор (визуализация)
            if auto_play:
                sensor_rect = pygame.Rect(dino.rect.right, dino.rect.y - 50, SENSOR_RANGE, dino.rect.height + 50)
                pygame.draw.rect(screen, (200, 200, 255), sensor_rect, 1)

            dino.draw(screen)
            for obs in obstacles:
                obs.draw(screen)

            # Счет
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            status_text = ""
            if auto_play: status_text = "Mode: AI (PyTorch)"
            elif training_mode: status_text = "Mode: Training..."
            else: status_text = "Mode: Manual"

            mode_surf = font.render(status_text, True, BLUE)
            screen.blit(mode_surf, (10, 50))

            if game_over:
                over_text = font.render("GAME OVER (Press SPACE)", True, RED)
                screen.blit(over_text, (WIDTH//2 - 150, HEIGHT//2))

            pygame.display.flip()
        else:
            # В режиме тренировки можно не отрисовывать каждый кадр для скорости,
            # но для наглядности оставим отрисовку, просто игра идет сама.
            pass

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Попытка загрузить модель при старте (опционально)
    if os.path.exists(MODEL_PATH):
        load_model()

    main()
