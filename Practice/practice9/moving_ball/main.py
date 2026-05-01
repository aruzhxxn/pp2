import pygame  # подключаем библиотеку pygame (для создания игр)

pygame.init()  # инициализируем все модули pygame

# размеры окна
WIDTH = 800
HEIGHT = 600

# создаем окно с заданными размерами
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# задаем название окна
pygame.display.set_caption("Moving Ball")

# создаем объект clock для контроля FPS (частоты кадров)
clock = pygame.time.Clock()

# начальная позиция мяча (по центру экрана)
ball_x = WIDTH // 2
ball_y = HEIGHT // 2

ball_radius = 25  # радиус мяча
step = 20  # шаг перемещения (на сколько пикселей двигается за нажатие)

running = True  # переменная для управления игровым циклом

# основной игровой цикл
while running:
    screen.fill((255,255,255))  # очищаем экран (заливаем белым цветом)

    # обработка событий (клики, нажатия клавиш и т.д.)
    for event in pygame.event.get():
        # если нажали на крестик окна — выходим из программы
        if event.type == pygame.QUIT:
            running = False

        # если нажата клавиша
        if event.type == pygame.KEYDOWN:
            # движение влево
            if event.key == pygame.K_LEFT:
                # проверяем, чтобы мяч не вышел за левую границу
                if ball_x - step - ball_radius >= 0:
                    ball_x -= step

            # движение вправо
            elif event.key == pygame.K_RIGHT:
                # проверяем правую границу
                if ball_x + step + ball_radius <= WIDTH:
                    ball_x += step

            # движение вверх
            elif event.key == pygame.K_UP:
                # проверяем верхнюю границу
                if ball_y - step - ball_radius >= 0:    
                    ball_y -= step

            # движение вниз
            elif event.key == pygame.K_DOWN:
                # проверяем нижнюю границу
                if ball_y + step + ball_radius <= HEIGHT:
                    ball_y += step

    # рисуем круг (мяч)
    # (экран, цвет RGB, координаты центра, радиус)
    pygame.draw.circle(screen, (255, 0, 0), (ball_x, ball_y), ball_radius)

    pygame.display.flip()  # обновляем экран (показываем все изменения)

    clock.tick(60)  # ограничиваем FPS до 60 кадров в секунду

pygame.quit()  # корректно закрываем pygame