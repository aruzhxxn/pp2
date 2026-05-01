import pygame
import datetime
import os
from clock import rotate_center  # функция для поворота изображения вокруг центра

# Настройки окна: ширина и высота экрана в пикселях
WIDTH, HEIGHT = 600, 600
# Количество кадров в секунду
FPS = 60

# Инициализация всех модулей Pygame
pygame.init()
# Создание игрового окна с заданными размерами
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Установка названия окна
pygame.display.set_caption("Mickey's Clock")
# Создание объекта Clock для контроля FPS
clock = pygame.time.Clock()

# Получаем абсолютный путь к папке, где находится текущий файл
BASE_PATH = os.path.dirname(__file__)
# Формируем путь к папке с изображениями
IMG_DIR = os.path.join(BASE_PATH, "images")

# Блок try-except нужен для обработки ошибок при загрузке картинок
try:
    # Загружаем изображение тела Микки и масштабируем до 600x600
    # convert_alpha() сохраняет прозрачность изображения
    mickey_body = pygame.transform.scale(
        pygame.image.load(os.path.join(IMG_DIR, "main-clock.png")).convert_alpha(),
        (600, 600)
    )

    # Загружаем правую руку (минутная стрелка) и изменяем размер
    right_hand = pygame.transform.scale(
        pygame.image.load(os.path.join(IMG_DIR, "right-hand.png")).convert_alpha(),
        (230, 500)
    )

    # Загружаем левую руку (секундная стрелка) и изменяем размер
    left_hand = pygame.transform.scale(
        pygame.image.load(os.path.join(IMG_DIR, "left-hand.png")).convert_alpha(),
        (230, 500)
    )

# Если возникла ошибка при загрузке изображений
except pygame.error as e:
    # Выводим сообщение об ошибке
    print(f"Ошибка загрузки: {e}")
    # Корректно завершаем Pygame
    pygame.quit()
    # Полностью выходим из программы
    exit()

# Вычисляем центр экрана, вокруг которого будут вращаться стрелки
CENTER = (mickey_body.get_width() // 2, mickey_body.get_height() // 2)

# Флаг для управления главным циклом программы
running = True

# Главный игровой цикл
while running:
    # Обрабатываем все события из очереди
    for event in pygame.event.get():
        # Если нажали на крестик окна, завершаем программу
        if event.type == pygame.QUIT:
            running = False

    # Получаем текущее время
    now = datetime.datetime.now()
    # Текущие секунды
    seconds = now.second
    # Текущие минуты
    minutes = now.minute
    # Доля секунды из микросекунд для плавного движения
    micro = now.microsecond / 1_000_000

    # Вычисляем угол поворота секундной стрелки
    # 360 градусов / 60 секунд = 6 градусов на каждую секунду
    # Знак минус нужен, потому что в Pygame ось Y направлена вниз
    sec_angle = -((seconds + micro) * 6)

    # Вычисляем угол поворота минутной стрелки
    # Добавляем долю от секунд, чтобы движение было плавным
    min_angle = -((minutes + (seconds / 60)) * 6)

    # Заливаем экран белым цветом
    screen.fill((255, 255, 255))

    # Рисуем тело Микки как фон часов
    screen.blit(mickey_body, (0, 0))

    # Поворачиваем правую руку (минутную стрелку) вокруг центра
    rot_min, min_rect = rotate_center(right_hand, min_angle, CENTER)
    # Отрисовываем повернутую минутную стрелку
    screen.blit(rot_min, min_rect)

    # Поворачиваем левую руку (секундную стрелку) вокруг центра
    rot_sec, sec_rect = rotate_center(left_hand, sec_angle, CENTER)
    # Отрисовываем повернутую секундную стрелку
    screen.blit(rot_sec, sec_rect)

    # Обновляем экран, показывая все изменения
    pygame.display.flip()

    # Ограничиваем скорость цикла до 60 кадров в секунду
    clock.tick(FPS)

# После выхода из цикла корректно завершаем Pygame
pygame.quit()