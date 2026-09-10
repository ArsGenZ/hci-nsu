import pygame
import numpy as np
import random
import pickle
import os
from collections import deque

# Инициализация Pygame
pygame.init()

# Константы игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
GROUND_Y = 350

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DINO_COLOR = (50, 50, 50)
DINO_SLIDE_COLOR = (0, 100, 200)  # Синий для скольжения
CACTUS_COLOR = (0, 150, 0)
BIRD_COLOR = (150, 50, 50)
BAR_COLOR = (100, 100, 100)
TEXT_COLOR = (50, 50, 50)

# Размеры
DINO_WIDTH = 40
DINO_HEIGHT = 60
DINO_SLIDE_HEIGHT = 30
CACTUS_WIDTH = 30
CACTUS_HEIGHT = 50
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
BAR_WIDTH = 80
BAR_HEIGHT = 15

# Физика
GRAVITY = 0.8
JUMP_STRENGTH = -15
SPEED = 6


class Dino:
    """Класс динозавра"""
    
    def __init__(self):
        self.x = 50
        self.y = GROUND_Y - DINO_HEIGHT
        self.width = DINO_WIDTH
        self.height = DINO_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False
        self.is_sliding = False
        self.slide_timer = 0
        self.color = DINO_COLOR
        
    def jump(self):
        """Прыжок (только одинарный)"""
        if not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
            self.color = DINO_COLOR
        # Двойной прыжок отключён - прыжок возможен только с земли
            
    def slide(self):
        """Приседание/скольжение"""
        if not self.is_sliding and not self.is_jumping:
            self.is_sliding = True
            self.height = DINO_SLIDE_HEIGHT
            self.y = GROUND_Y - DINO_SLIDE_HEIGHT
            self.color = DINO_SLIDE_COLOR
            self.slide_timer = 30  # Длительность скольжения в кадрах
            
    def update(self):
        """Обновление состояния динозавра"""
        # Применение гравитации
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # Проверка земли
        if self.is_sliding:
            ground_y = GROUND_Y - DINO_SLIDE_HEIGHT
            if self.y >= ground_y:
                self.y = ground_y
                self.velocity_y = 0
                self.slide_timer -= 1
                if self.slide_timer <= 0:
                    self.is_sliding = False
                    self.height = DINO_HEIGHT
                    self.y = GROUND_Y - DINO_HEIGHT
                    self.color = DINO_COLOR
        else:
            if self.y >= GROUND_Y - DINO_HEIGHT:
                self.y = GROUND_Y - DINO_HEIGHT
                self.velocity_y = 0
                self.is_jumping = False
                self.color = DINO_COLOR
                
    def draw(self, screen):
        """Отрисовка динозавра"""
        pygame.draw.rect(screen, self.color, 
                        (self.x, self.y, self.width, self.height))
        # Глаза для визуализации
        eye_color = WHITE if self.color == DINO_SLIDE_COLOR else BLACK
        pygame.draw.circle(screen, eye_color, 
                          (self.x + self.width - 10, self.y + 10), 5)
        
    def get_rect(self):
        """Получить прямоугольник коллизии"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Obstacle:
    """Базовый класс препятствия"""
    
    def __init__(self, obstacle_type):
        self.type = obstacle_type
        self.x = SCREEN_WIDTH
        self.marked_for_removal = False
        
        if obstacle_type == 'cactus':
            self.width = CACTUS_WIDTH
            self.height = CACTUS_HEIGHT
            self.y = GROUND_Y - self.height
            self.color = CACTUS_COLOR
        elif obstacle_type == 'bird':
            self.width = BIRD_WIDTH
            self.height = BIRD_HEIGHT
            # Птицы летают на разной высоте
            self.y = GROUND_Y - random.randint(70, 120)
            self.color = BIRD_COLOR
        elif obstacle_type == 'bar':
            self.width = BAR_WIDTH
            self.height = BAR_HEIGHT
            # Низкая перекладина на уровне груди динозавра
            self.y = GROUND_Y - 45
            self.color = BAR_COLOR
            
    def update(self, speed):
        """Обновление позиции препятствия"""
        self.x -= speed
        if self.x + self.width < 0:
            self.marked_for_removal = True
            
    def draw(self, screen):
        """Отрисовка препятствия"""
        if self.type == 'cactus':
            # Рисуем кактус (прямоугольник с шипами)
            pygame.draw.rect(screen, self.color, 
                           (self.x, self.y, self.width, self.height))
            # Шипы сверху
            spike_w = 8
            for i in range(3):
                sx = self.x + 5 + i * spike_w
                pygame.draw.polygon(screen, self.color,
                                  [(sx, self.y), (sx + spike_w//2, self.y - 10), 
                                   (sx + spike_w, self.y)])
        elif self.type == 'bird':
            # Рисуем птицу (эллипс с крыльями)
            pygame.draw.ellipse(screen, self.color,
                              (self.x, self.y, self.width, self.height))
            # Крыло
            pygame.draw.polygon(screen, self.color,
                              [(self.x + 10, self.y + 10),
                               (self.x + 25, self.y - 5),
                               (self.x + 40, self.y + 10)])
        elif self.type == 'bar':
            # Рисуем перекладину
            pygame.draw.rect(screen, self.color,
                           (self.x, self.y, self.width, self.height))
            # Опоры по бокам
            pygame.draw.rect(screen, self.color,
                           (self.x, self.y, 10, GROUND_Y - self.y))
            pygame.draw.rect(screen, self.color,
                           (self.x + self.width - 10, self.y, 10, GROUND_Y - self.y))
                           
    def get_rect(self):
        """Получить прямоугольник коллизии"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Sensor:
    """Сенсорная система для обнаружения препятствий"""
    
    def __init__(self, dino):
        self.dino = dino
        self.detection_range = 300
        
    def detect_obstacles(self, obstacles):
        """
        Обнаружение ближайших препятствий
        Возвращает информацию о ближайшем препятствии каждого типа
        """
        sensor_data = {
            'cactus_distance': float('inf'),
            'cactus_height': 0,
            'bird_distance': float('inf'),
            'bird_height': 0,
            'bar_distance': float('inf'),
            'bar_height': 0,
            'dino_y_velocity': 0,
            'dino_state': 0  # 0 - стоит, 1 - прыгает, 2 - приседает
        }
        
        for obstacle in obstacles:
            distance = obstacle.x - (self.dino.x + self.dino.width)
            
            if 0 < distance < self.detection_range:
                if obstacle.type == 'cactus':
                    if distance < sensor_data['cactus_distance']:
                        sensor_data['cactus_distance'] = distance
                        sensor_data['cactus_height'] = obstacle.height
                elif obstacle.type == 'bird':
                    if distance < sensor_data['bird_distance']:
                        sensor_data['bird_distance'] = distance
                        sensor_data['bird_height'] = obstacle.y
                elif obstacle.type == 'bar':
                    if distance < sensor_data['bar_distance']:
                        sensor_data['bar_distance'] = distance
                        sensor_data['bar_height'] = obstacle.y
                        
        # Добавляем информацию о состоянии динозавра
        sensor_data['dino_y_velocity'] = self.dino.velocity_y / JUMP_STRENGTH
        if self.dino.is_jumping:
            sensor_data['dino_state'] = 1
        elif self.dino.is_sliding:
            sensor_data['dino_state'] = 2
            
        # Нормализация данных
        sensor_data['cactus_distance'] = min(sensor_data['cactus_distance'], 
                                             self.detection_range) / self.detection_range
        sensor_data['bird_distance'] = min(sensor_data['bird_distance'], 
                                           self.detection_range) / self.detection_range
        sensor_data['bar_distance'] = min(sensor_data['bar_distance'], 
                                          self.detection_range) / self.detection_range
        sensor_data['cactus_height'] /= GROUND_Y
        sensor_data['bird_height'] /= GROUND_Y
        sensor_data['bar_height'] /= GROUND_Y
        
        return sensor_data
    
    def get_input_vector(self, obstacles):
        """Преобразование данных сенсора во входной вектор для нейросети"""
        data = self.detect_obstacles(obstacles)
        return np.array([
            data['cactus_distance'],
            data['cactus_height'],
            data['bird_distance'],
            data['bird_height'],
            data['bar_distance'],
            data['bar_height'],
            data['dino_y_velocity'],
            data['dino_state']
        ])


class NeuralNetwork:
    """Нейронная сеть для управления динозавром"""
    
    def __init__(self, input_size=8, hidden_size=16, output_size=3):
        """
        input_size: количество входов (данные сенсора)
        hidden_size: количество нейронов в скрытом слое
        output_size: количество выходов (действия: прыжок, приседание, ничего)
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Инициализация весов
        self.W1 = np.random.randn(input_size, hidden_size) * 0.5
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.5
        self.b2 = np.zeros((1, output_size))
        
    def relu(self, x):
        """Функция активации ReLU"""
        return np.maximum(0, x)
    
    def softmax(self, x):
        """Функция активации Softmax"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def forward(self, X):
        """Прямое распространение"""
        if len(X.shape) == 1:
            X = X.reshape(1, -1)
        
        # Скрытый слой
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        
        # Выходной слой
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.softmax(self.z2)
        
        return self.a2
    
    def predict(self, X):
        """Предсказание действия"""
        output = self.forward(X)
        return np.argmax(output, axis=1)[0]
    
    def save(self, filename):
        """Сохранение модели"""
        model_data = {
            'W1': self.W1,
            'b1': self.b1,
            'W2': self.W2,
            'b2': self.b2,
            'input_size': self.input_size,
            'hidden_size': self.hidden_size,
            'output_size': self.output_size
        }
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
            
    def load(self, filename):
        """Загрузка модели"""
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)
        
        self.W1 = model_data['W1']
        self.b1 = model_data['b1']
        self.W2 = model_data['W2']
        self.b2 = model_data['b2']
        self.input_size = model_data['input_size']
        self.hidden_size = model_data['hidden_size']
        self.output_size = model_data['output_size']


class Trainer:
    """Класс для обучения нейронной сети"""
    
    def __init__(self, nn, learning_rate=0.01):
        self.nn = nn
        self.learning_rate = learning_rate
        
    def train_step(self, X, y_true):
        """
        Один шаг обучения
        X: входные данные (batch_size, input_size)
        y_true: правильные действия (batch_size,)
        """
        batch_size = X.shape[0]
        
        # Прямое распространение
        output = self.nn.forward(X)
        
        # One-hot кодирование правильных ответов
        y_one_hot = np.zeros_like(output)
        y_one_hot[np.arange(batch_size), y_true] = 1
        
        # Обратное распространение
        # Градиент выходного слоя
        dz2 = output - y_one_hot
        dW2 = np.dot(self.nn.a1.T, dz2) / batch_size
        db2 = np.mean(dz2, axis=0, keepdims=True)
        
        # Градиент скрытого слоя
        da1 = np.dot(dz2, self.nn.W2.T)
        dz1 = da1 * (self.nn.z1 > 0)  # Производная ReLU
        dW1 = np.dot(X.T, dz1) / batch_size
        db1 = np.mean(dz1, axis=0, keepdims=True)
        
        # Обновление весов
        self.nn.W2 -= self.learning_rate * dW2
        self.nn.b2 -= self.learning_rate * db2
        self.nn.W1 -= self.learning_rate * dW1
        self.nn.b1 -= self.learning_rate * db1
        
        # Вычисление потери
        loss = -np.mean(np.sum(y_one_hot * np.log(output + 1e-10), axis=1))
        return loss


class Game:
    """Основной класс игры"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dino Game - 3 типа препятствий")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
        
        # Сенсор и нейронная сеть
        self.sensor = Sensor(self.dino)
        self.nn = NeuralNetwork()
        self.trainer = Trainer(self.nn)
        
        # Режимы игры
        self.auto_mode = False  # Автоматический режим с ИИ
        self.training_mode = False
        
        # Скорость игры
        self.game_speed = SPEED
        
        # Статистика
        self.generation_data = []
        
    def reset_game(self):
        """Сброс игры"""
        self.dino = Dino()
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.obstacle_timer = 0
        self.min_obstacle_interval = 60
        self.max_obstacle_interval = 120
        self.game_speed = SPEED
        
    def spawn_obstacle(self):
        """Создание случайного препятствия"""
        obstacle_types = ['cactus', 'bird', 'bar']
        weights = [0.5, 0.3, 0.2]  # Вероятности появления
        
        obstacle_type = random.choices(obstacle_types, weights=weights)[0]
        self.obstacles.append(Obstacle(obstacle_type))
        
    def check_collision(self):
        """Проверка столкновений"""
        dino_rect = self.dino.get_rect()
        
        for obstacle in self.obstacles:
            obs_rect = obstacle.get_rect()
            
            # Уменьшаем хитбокс для более честной игры
            dino_hitbox = dino_rect.inflate(-10, -10)
            obs_hitbox = obs_rect.inflate(-5, -5)
            
            if dino_hitbox.colliderect(obs_hitbox):
                return True
        return False
    
    def get_optimal_action(self, sensor_data):
        """
        Определение оптимального действия на основе данных сенсора
        Используется для генерации обучающих данных
        """
        cactus_dist = sensor_data['cactus_distance'] * 300
        bird_dist = sensor_data['bird_distance'] * 300
        bar_dist = sensor_data['bar_distance'] * 300
        
        # Приоритеты действий
        # 0 - ничего не делать
        # 1 - прыжок
        # 2 - приседание
        
        action = 0
        
        # Проверка перекладины - нужно приседать (высший приоритет)
        if bar_dist < 200 and bar_dist > 0:
            if not self.dino.is_sliding and not self.dino.is_jumping:
                action = 2
                
        # Проверка птицы - нужно приседать или прыгать в зависимости от высоты
        elif bird_dist < 200 and bird_dist > 0:
            bird_y = sensor_data['bird_height'] * GROUND_Y
            if bird_y < GROUND_Y - 80:  # Птица высоко - можно пробежать
                action = 0
            elif bird_y > GROUND_Y - 50:  # Птица низко - нужно приседать
                if not self.dino.is_sliding and not self.dino.is_jumping:
                    action = 2
            else:  # Птица на средней высоте - прыгать
                if not self.dino.is_jumping:
                    action = 1
                    
        # Проверка кактуса - нужно прыгать
        elif cactus_dist < 200 and cactus_dist > 0:
            if not self.dino.is_jumping:
                action = 1
                
        return action
    
    def auto_play(self):
        """Автоматическое управление с помощью нейронной сети"""
        sensor_input = self.sensor.get_input_vector(self.obstacles)
        action = self.nn.predict(sensor_input)
        
        if action == 1:  # Прыжок
            self.dino.jump()
        elif action == 2:  # Приседание
            self.dino.slide()
            
    def generate_training_data(self, num_samples=1000):
        """Генерация обучающих данных"""
        X_data = []
        y_data = []
        
        for _ in range(num_samples):
            # Создаем случайную ситуацию
            self.reset_game()
            
            # Генерируем случайное препятствие на разном расстоянии
            obstacle_type = random.choice(['cactus', 'bird', 'bar'])
            obstacle = Obstacle(obstacle_type)
            obstacle.x = random.randint(50, 250)
            self.obstacles = [obstacle]
            
            # Получаем данные сенсора
            sensor_data = self.sensor.detect_obstacles(self.obstacles)
            sensor_input = self.sensor.get_input_vector(self.obstacles)
            
            # Определяем правильное действие
            correct_action = self.get_optimal_action(sensor_data)
            
            X_data.append(sensor_input)
            y_data.append(correct_action)
            
        return np.array(X_data), np.array(y_data)
    
    def train_nn(self, epochs=100, batch_size=32):
        """Обучение нейронной сети"""
        print("Генерация обучающих данных...")
        X_train, y_train = self.generate_training_data(2000)
        
        print(f"Обучение нейронной сети ({epochs} эпох)...")
        
        for epoch in range(epochs):
            # Перемешивание данных
            indices = np.random.permutation(len(X_train))
            X_train = X_train[indices]
            y_train = y_train[indices]
            
            total_loss = 0
            batches = 0
            
            for i in range(0, len(X_train), batch_size):
                X_batch = X_train[i:i+batch_size]
                y_batch = y_train[i:i+batch_size]
                
                loss = self.trainer.train_step(X_batch, y_batch)
                total_loss += loss
                batches += 1
                
            avg_loss = total_loss / batches
            
            if (epoch + 1) % 10 == 0:
                print(f"Эпоха {epoch+1}/{epochs}, Потеря: {avg_loss:.4f}")
                
        print("Обучение завершено!")
        
        # Сохранение модели
        self.nn.save('dino_nn_model.pkl')
        print("Модель сохранена в 'dino_nn_model.pkl'")
        
    def test_nn(self, num_games=10):
        """Тестирование обученной модели"""
        scores = []
        
        for game_num in range(num_games):
            self.reset_game()
            game_frames = 0
            max_frames = 3600  # Максимум 60 секунд на тест
            
            while not self.game_over and game_frames < max_frames:
                self.handle_events()
                self.auto_play()
                self.update()
                self.draw()
                game_frames += 1
                
            scores.append(self.score)
            print(f"Игра {game_num+1}: Счёт = {self.score}")
            
        avg_score = sum(scores) / len(scores)
        print(f"\nСредний счёт за {num_games} игр: {avg_score:.1f}")
        return avg_score
        
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.dino.jump()
                        
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if not self.game_over:
                        self.dino.slide()
                        
                elif event.key == pygame.K_t:
                    # Обучение нейронной сети
                    self.train_nn()
                    
                elif event.key == pygame.K_a:
                    # Переключение автоматического режима
                    self.auto_mode = not self.auto_mode
                    print(f"Автоматический режим: {'ВКЛ' if self.auto_mode else 'ВЫКЛ'}")
                    
                elif event.key == pygame.K_l:
                    # Загрузка модели
                    if os.path.exists('dino_nn_model.pkl'):
                        self.nn.load('dino_nn_model.pkl')
                        print("Модель загружена!")
                    else:
                        print("Модель не найдена! Сначала обучите сеть (клавиша T)")
                        
                elif event.key == pygame.K_r:
                    # Тестирование модели
                    if os.path.exists('dino_nn_model.pkl'):
                        self.nn.load('dino_nn_model.pkl')
                        self.test_nn()
                    else:
                        print("Модель не найдена! Сначала обучите сеть (клавиша T)")
                        
        return True
    
    def update(self):
        """Обновление игрового состояния"""
        if self.game_over:
            return
            
        # Обновление динозавра
        self.dino.update()
        
        # Обновление препятствий
        for obstacle in self.obstacles:
            obstacle.update(self.game_speed)
            
        # Удаление прошедших препятствий
        self.obstacles = [obs for obs in self.obstacles if not obs.marked_for_removal]
        
        # Создание новых препятствий
        self.obstacle_timer += 1
        if self.obstacle_timer >= random.randint(self.min_obstacle_interval, 
                                                  self.max_obstacle_interval):
            self.spawn_obstacle()
            self.obstacle_timer = 0
            
        # Увеличение сложности со временем
        if self.score > 0 and self.score % 500 == 0:
            self.game_speed = min(6 + self.score // 1000, 12)
            
        # Увеличение счёта
        self.score += 1
        
        # Проверка столкновений
        if self.check_collision():
            self.game_over = True
            
    def draw(self):
        """Отрисовка игры"""
        self.screen.fill(WHITE)
        
        # Земля
        pygame.draw.line(self.screen, BLACK, (0, GROUND_Y), 
                        (SCREEN_WIDTH, GROUND_Y), 2)
        
        # Отрисовка препятствий
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
            
        # Отрисовка динозавра
        self.dino.draw(self.screen)
        
        # Отрисовка счёта
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        
        # Отрисовка режима
        mode_text = self.small_font.render(
            f"Mode: {'AUTO' if self.auto_mode else 'MANUAL'}", 
            True, TEXT_COLOR)
        self.screen.blit(mode_text, (10, 40))
        
        # Подсказки по управлению
        if not self.auto_mode:
            hints = [
                "SPACE - Jump",
                "DOWN/S - Slide",
                "A - Toggle Auto",
                "T - Train NN",
                "L - Load Model",
                "R - Test Model"
            ]
            for i, hint in enumerate(hints):
                hint_text = self.small_font.render(hint, True, (100, 100, 100))
                self.screen.blit(hint_text, (SCREEN_WIDTH - 150, 10 + i * 20))
        
        # Экран проигрыша
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
            
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                            SCREEN_HEIGHT//2 - 30))
            self.screen.blit(restart_text,
                           (SCREEN_WIDTH//2 - restart_text.get_width()//2,
                            SCREEN_HEIGHT//2 + 10))
        
        pygame.display.flip()
        
    def run(self):
        """Запуск игрового цикла"""
        running = True
        
        print("=" * 50)
        print("DINO GAME - 3 типа препятствий")
        print("=" * 50)
        print("\nУправление:")
        print("  SPACE - Прыжок")
        print("  DOWN/S - Приседание (скольжение)")
        print("  A - Включить/выключить авто-режим")
        print("  T - Обучить нейронную сеть")
        print("  L - Загрузить модель")
        print("  R - Тестировать модель")
        print("\nПрепятствия:")
        print("  Кактус (зелёный) - прыгать")
        print("  Птица (красная) - прыгать или приседать")
        print("  Перекладина (серая) - приседать")
        print("=" * 50)
        
        while running:
            running = self.handle_events()
            
            if self.auto_mode and not self.game_over:
                self.auto_play()
                
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()