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
DOUBLE_JUMP_COLOR = (0, 200, 255) # Голубой для двойного прыжка
GAP_COLOR = (139, 69, 19) # Коричневый для пропасти

# Параметры Динозавра
DINO_X = 50
DINO_WIDTH = 40
DINO_HEIGHT_NORMAL = 60
DINO_HEIGHT_DUCK = 30
JUMP_POWER = -13
GRAVITY = 0.6
MOVE_SPEED = 7
DOUBLE_JUMP_AVAILABLE = True  # Флаг доступности двойного прыжка

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

# Параметры пропасти (Gap)
GAP_WIDTH = 100
GAP_DEPTH = 20  # Визуальная глубина пропасти

# Сенсор
SENSOR_RANGE = 250

# --- НЕЙРОСЕТЬ (PYTORCH) ---
class DinoNet(nn.Module):
    def __init__(self, input_size=8, hidden_size=20, output_size=4):
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

# Действия: 0 = Ничего не делать (или бежать), 1 = Прыжок, 2 = Присед, 3 = Двойной прыжок
ACTION_NONE = 0
ACTION_JUMP = 1
ACTION_DUCK = 2
ACTION_DOUBLE_JUMP = 3

# --- КЛАССЫ ---

class Dinosaur:
    def __init__(self):
        self.rect = pygame.Rect(DINO_X, GROUND_Y - DINO_HEIGHT_NORMAL, DINO_WIDTH, DINO_HEIGHT_NORMAL)
        self.vel_y = 0
        self.is_jumping = False
        self.is_ducking = False
        self.color = DINO_COLOR
        self.original_height = DINO_HEIGHT_NORMAL
        self.can_double_jump = False  # Разрешение на двойной прыжок
        self.jump_count = 0  # Счетчик прыжков

    def jump(self):
        if not self.is_jumping and not self.is_ducking:
            self.vel_y = JUMP_POWER
            self.is_jumping = True
            self.color = JUMP_COLOR
            self.jump_count = 1

    def double_jump(self):
        """Выполняет двойной прыжок если доступен"""
        if self.is_jumping and not self.is_ducking and self.can_double_jump and self.jump_count < 2:
            self.vel_y = JUMP_POWER * 0.85  # Второй прыжок чуть слабее первого
            self.color = DOUBLE_JUMP_COLOR
            self.jump_count = 2
            return True
        return False

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

    def update(self, over_gap=False):
        # Гравитация
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Приземление (только если не над пропастью)
        if not over_gap and self.rect.y >= GROUND_Y - self.rect.height:
            self.rect.y = GROUND_Y - self.rect.height
            self.vel_y = 0
            self.is_jumping = False
            self.jump_count = 0
            self.can_double_jump = False
            if not self.is_ducking:
                self.color = DINO_COLOR
            else:
                self.color = DUCK_COLOR
        elif over_gap:
            # Над пропастью - динозавр в воздухе, разрешаем двойной прыжок
            if not self.is_jumping:
                self.is_jumping = True
            self.can_double_jump = True

        # Если приседаем в воздухе (редкий кейс, но для надежности)
        if self.is_ducking and not self.is_jumping:
             self.rect.y = GROUND_Y - self.rect.height

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Obstacle:
    def __init__(self, type_):
        self.type = type_ # 'cactus', 'bird' или 'gap'
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
        elif self.type == 'gap':
            # Пропасть - это разрыв в земле
            self.rect = pygame.Rect(self.x, GROUND_Y, GAP_WIDTH, GAP_DEPTH)
            self.color = GAP_COLOR
            self.speed = MOVE_SPEED

    def update(self):
        self.x -= self.speed
        self.rect.x = int(self.x)

    def draw(self, surface):
        if self.type == 'gap':
            # Рисуем пропасть как коричневый прямоугольник под землей
            pygame.draw.rect(surface, self.color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

class Sensor:
    def __init__(self, dino):
        self.dino = dino

    def scan(self, obstacles):
        """
        Возвращает вектор признаков для нейросети:
        [dist_cactus, height_diff_cactus, dist_bird, height_diff_bird, dist_gap, dy, is_jumping, can_double_jump]
        Все значения нормализуются примерно к [-1, 1] или [0, 1]
        """
        dist_cactus = SENSOR_RANGE
        h_diff_cactus = 0.0
        dist_bird = SENSOR_RANGE
        h_diff_bird = 0.0
        dist_gap = SENSOR_RANGE

        # Ищем ближайшее препятствие каждого типа в диапазоне сенсора
        for obs in obstacles:
            # Препятствие должно быть справа от динозавра (приближается) и в пределах SENSOR_RANGE
            if obs.x > self.dino.rect.right and obs.x < self.dino.rect.right + SENSOR_RANGE:
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
                
                elif obs.type == 'gap':
                    if dist < dist_gap:
                        dist_gap = dist

        # Нормализация дистанции (0..1 где 1 это далеко)
        norm_dist_cactus = min(dist_cactus / SENSOR_RANGE, 1.0)
        norm_dist_bird = min(dist_bird / SENSOR_RANGE, 1.0)
        norm_dist_gap = min(dist_gap / SENSOR_RANGE, 1.0)

        # Скорость по Y нормализуем
        norm_dy = self.dino.vel_y / abs(JUMP_POWER)

        # Флаг прыжка
        is_jumping = 1.0 if self.dino.is_jumping else 0.0
        
        # Флаг доступности двойного прыжка
        can_double_jump = 1.0 if self.dino.can_double_jump else 0.0

        # Вектор: [dist_cact, h_cact, dist_bird, h_bird, dist_gap, dy, jump_flag, double_jump_flag]
        return [norm_dist_cactus, h_diff_cactus, norm_dist_bird, h_diff_bird, norm_dist_gap, norm_dy, is_jumping, can_double_jump]

# --- ФУНКЦИИ ИГРЫ ---

def get_input_tensor(sensor, obstacles):
    data = sensor.scan(obstacles)
    return torch.FloatTensor(data).unsqueeze(0) # Размер [1, 8]

def generate_training_data(sensor, obstacles, dino):
    """Генерирует одно правильное действие на основе текущей ситуации"""
    inputs = sensor.scan(obstacles)
    target = ACTION_NONE

    dist_cact = inputs[0] * SENSOR_RANGE
    h_cact = inputs[1]
    dist_bird = inputs[2] * SENSOR_RANGE
    h_bird = inputs[3]
    dist_gap = inputs[4] * SENSOR_RANGE
    
    # Пороги расстояний для реакции (только близкие препятствия требуют действия)
    GAP_THRESHOLD = 180
    CACTUS_THRESHOLD = 150
    BIRD_THRESHOLD = 150
    
    # Минимальное расстояние для начала действия (должно быть достаточно рано для реакции)
    MIN_GAP_DIST = 50
    MIN_CACTUS_DIST = 40
    MIN_BIRD_DIST = 40
    
    # Флаг, что решение уже принято (для приоритетов)
    decision_made = False

    # 1. Пропасть близко - самый высокий приоритет
    if MIN_GAP_DIST < dist_gap < GAP_THRESHOLD and not decision_made:
        if not dino.is_jumping:
            target = ACTION_JUMP  # Сначала обычный прыжок
            decision_made = True
        elif dino.is_jumping and dino.can_double_jump and dino.jump_count < 2:
            target = ACTION_DOUBLE_JUMP  # Затем двойной прыжок
            decision_made = True

    # 2. Кактус близко (только если еще не решили для пропасти)
    if MIN_CACTUS_DIST < dist_cact < CACTUS_THRESHOLD and not decision_made:
        if not dino.is_jumping:
            target = ACTION_JUMP
            decision_made = True

    # 3. Птица близко (только если еще не решили для пропасти/кактуса)
    if MIN_BIRD_DIST < dist_bird < BIRD_THRESHOLD and not decision_made:
        # Птица летит низко - нужно присесть если стоим на земле
        if not dino.is_jumping:
            target = ACTION_DUCK
            decision_made = True
        # Если уже прыгнули достаточно высоко - ничего не делаем (перелетим)
        elif dino.rect.y < GROUND_Y - 40:
            target = ACTION_NONE
            decision_made = True

    # ГЛАВНОЕ ИЗМЕНЕНИЕ: Возвращаем ACTION_NONE если нет препятствий в зоне реакции
    # Это предотвратит обучение нейросети постоянным прыжкам
    if not decision_made:
        target = ACTION_NONE

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

                if event.key == pygame.K_d:
                    # Двойной прыжок по нажатию D (для ручного режима)
                    if not auto_play and not training_mode:
                        dino.double_jump()

                if event.key == pygame.K_a:
                    auto_play = not auto_play
                    print(f"Автопилот: {'ВКЛ' if auto_play else 'ВЫКЛ'}")

                if event.key == pygame.K_t:
                    # Запуск быстрого обучения (симуляция)
                    training_mode = not training_mode
                    if training_mode:
                        print("Начало сбора данных для обучения... (нажмите T снова для остановки и сохранения)")
                    else:
                        print("Остановка сбора данных. Обучение модели...")
                        if len(train_inputs) > 0:
                            loss = train_step(train_inputs, train_targets)
                            save_model()
                            print(f"Обучение завершено. Loss: {loss:.4f}")
                        train_inputs = []
                        train_targets = []

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
                if r < 0.5:
                    obstacles.append(Obstacle('cactus'))
                elif r < 0.75:
                    obstacles.append(Obstacle('bird'))
                else:
                    obstacles.append(Obstacle('gap'))  # Пропасть с вероятностью ~25%
                spawn_timer = 0

            # Обновление препятствий
            for obs in obstacles[:]:
                obs.update()
                if obs.x < -50:
                    obstacles.remove(obs)
                    score += 10

                # Коллизия (только для кактуса и птицы, пропасть обрабатывается отдельно)
                if obs.type in ['cactus', 'bird']:
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
            
            # Проверка падения в пропасть
            over_gap = False
            for obs in obstacles:
                if obs.type == 'gap':
                    # Проверяем, находится ли динозавр над пропастью
                    if dino.rect.centerx > obs.rect.left and dino.rect.centerx < obs.rect.right:
                        over_gap = True
                        # Если динозавр на земле (не прыгает), он падает в пропасть
                        if not dino.is_jumping and dino.rect.y >= GROUND_Y - dino.rect.height - 5:
                            game_over = True
                            if training_mode:
                                training_mode = False
                                print("Упал в пропасть! Данные сброшены.")
                                train_inputs = []
                                train_targets = []
                        break
            
            # Определение, находится ли динозавр над пропастью для update()
            for obs in obstacles:
                if obs.type == 'gap':
                    if dino.rect.centerx > obs.rect.left and dino.rect.centerx < obs.rect.right:
                        over_gap = True
                        break

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
                        pass
                elif action == ACTION_DOUBLE_JUMP:
                    # Двойной прыжок
                    if dino.is_jumping and not dino.is_ducking and dino.can_double_jump:
                        dino.double_jump()
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

        # Обновление динозавра с учетом пропасти
        dino.update(over_gap)

        # 3. Отрисовка
        if not training_mode:
            screen.fill(WHITE)

            # Земля (рисуем с разрывами для пропасти)
            ground_segments = [(0, GROUND_Y)]
            for obs in obstacles:
                if obs.type == 'gap':
                    # Добавляем разрыв в земле
                    if ground_segments[-1][0] < obs.rect.left:
                        ground_segments.append((obs.rect.left, GROUND_Y))
                    ground_segments.append((obs.rect.right, GROUND_Y))
            ground_segments.append((WIDTH, GROUND_Y))
            
            # Рисуем сегменты земли
            for i in range(0, len(ground_segments), 2):
                if i + 1 < len(ground_segments):
                    pygame.draw.line(screen, BLACK, 
                                     (ground_segments[i][0], ground_segments[i][1]),
                                     (ground_segments[i+1][0], ground_segments[i+1][1]), 2)

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

            # Инструкция по управлению
            instr_font = pygame.font.Font(None, 24)
            instr_text = "SPACE/W - Jump, S - Duck, D - Double Jump, A - AI, T - Train, R - Run Model"
            instr_surf = instr_font.render(instr_text, True, GRAY)
            screen.blit(instr_surf, (10, HEIGHT - 25))

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
