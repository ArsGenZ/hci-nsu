import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

# Создаем папку для результатов
os.makedirs("results", exist_ok=True)

#  ШАГ 1: Создание изображения
print("Шаг 1: Создание изображения с элементами...")

# Создаем вертикальный градиент 500x500
gradient_img = np.zeros((500, 500), dtype=np.uint8)
for i in range(255):
    gradient_img[i, :] = i

# Конвертируем в BGR для цветных элементов
gradient_bgr = cv2.cvtColor(gradient_img, cv2.COLOR_GRAY2BGR)

# Красный прямоугольник 100x100 в центре (OpenCV использует BGR!)
cv2.rectangle(gradient_bgr, (200, 200), (300, 300), (0, 0, 255), -1)

# Зеленая окружность радиусом 50 в левом верхнем углу
cv2.circle(gradient_bgr, (50, 50), 50, (0, 255, 0), -1)

# Желтый текст "OpenCV" в правом нижнем углу (BGR: 0,255,255 = желтый)
cv2.putText(
    gradient_bgr, "OpenCV", (350, 480), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2
)

# Сохраняем результат
cv2.imwrite("results/step1_gradient.jpg", gradient_bgr)
print("Изображение с элементами сохранено: results/step1_gradient.jpg")


#  ШАГ 2: Работа с цветными изображениями

print("\nШаг 2: Загрузка и обработка цветного изображения...")

# Загружаем тестовое изображение (можно заменить на свое)
image = cv2.imread("image.jpg")

# Разделяем на каналы BGR (OpenCV использует BGR, не RGB!)
b, g, r = cv2.split(image)

image7 = np.empty_like(image)
image5 = np.empty_like(image)
image6 = np.empty_like(image)
image7[:, :, 0] = r
image5[:, :, 1] = g
image6[:, :, 2] = b

# Отображаем каналы через matplotlib (конвертируем BGR→RGB для отображения)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
axes[0, 0].set_title("Original")
axes[0, 0].axis("off")

axes[0, 1].imshow(image7)
axes[0, 1].set_title("Red Channel")
axes[0, 1].axis("off")

axes[1, 0].imshow(image5)
axes[1, 0].set_title("Green Channel")
axes[1, 0].axis("off")

axes[1, 1].imshow(image6)
axes[1, 1].set_title("Blue Channel")
axes[1, 1].axis("off")

plt.tight_layout()
plt.savefig("results/step2_channels.png")
plt.close()

# Сохраняем зеленый канал как отдельное изображение
cv2.imwrite("results/green_channel.png", g)


# Конвертируем в серый и сохраняем
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("results/grey.jpg", gray_img)
print("Каналы сохранены, grey.jpg создан")


#  ШАГ 3: Фильтрация и анализ
print("\nШаг 3: Применение фильтров...")

# Гауссово размытие
blurred = cv2.GaussianBlur(gray_img, (3, 3), 0)

# Обнаружение краев Собелем
sobelx = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
sobel_combined = cv2.convertScaleAbs(cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0))

# Отображение результатов
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(gray_img, cmap="gray")
axes[0].set_title("Original Gray")
axes[0].axis("off")

axes[1].imshow(blurred, cmap="gray")
axes[1].set_title("Gaussian Blur")
axes[1].axis("off")

axes[2].imshow(sobel_combined, cmap="gray")
axes[2].set_title("Sobel Edges")
axes[2].axis("off")

plt.tight_layout()
plt.savefig("results/step3_filters.png")
plt.close()
print("Фильтры применены, результат сохранен")


#  ШАГ 4: Гистограмма и нормализация
print("\nШаг 4: Гистограмма и эквализация...")

# Гистограмма яркости
hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])

plt.figure(figsize=(10, 4))
plt.plot(hist, color="black")
plt.title("Histogram of Grayscale Image")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")
plt.grid(True)
plt.savefig("results/step4_histogram.png")
plt.close()

# Нормализация (эквализация гистограммы)
normalized = cv2.equalizeHist(gray_img)
cv2.imwrite("results/normalized.jpg", normalized)
print("Гистограмма построена, normalized.jpg сохранен")

# ШАГ 5: Изменение размеров и поворот
print("\nШаг 5: Масштабирование и поворот...")

# Уменьшение в 2 раза
resized = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2))

# Поворот на 45 градусов вокруг центра
(h, w) = resized.shape[:2]
center = (w // 2, h // 2)
rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(resized, rotation_matrix, (w, h))

cv2.imwrite("results/rotated.jpg", rotated)
print("rotated.jpg сохранен")


#  ШАГ 6: Контурный анализ
print("\nШаг 6: Поиск контуров...")

# Применяем пороговую обработку для лучшего поиска контуров
_, thresh = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

# Поиск контуров
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Рисуем контуры на копии изображения
contour_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)

cv2.imwrite("results/contours.jpg", contour_img)
print(f"Найдено {len(contours)} контуров, contours.jpg сохранен")
