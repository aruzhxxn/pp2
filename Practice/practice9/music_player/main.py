import pygame
from player import MusicPlayer
import os

pygame.init()  # запускаем все модули pygame

# создаем окно программы размером 600 на 300 пикселей
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("Music Player")  # название окна

# создаем шрифт для вывода текста на экран
# None означает стандартный шрифт pygame, 30 — размер шрифта
font = pygame.font.SysFont(None, 30)

# создаем объект музыкального плеера
# "music" — это папка, где лежат музыкальные файлы
player = MusicPlayer("music")

running = True  # переменная для работы главного цикла программы
clock = pygame.time.Clock()  # объект для ограничения FPS

# функция для перевода миллисекунд в формат минуты:секунды
def format_time(ms):
    if ms < 0:  # если музыка не играет или позиция недоступна
        return "0:00"
    seconds = ms // 1000  # переводим миллисекунды в секунды
    m = seconds // 60     # находим количество полных минут
    s = seconds % 60      # находим оставшиеся секунды
    return f"{m}:{s:02}"  # форматируем, например 2:05

# главный цикл программы
while running:
    screen.fill((0, 0, 0))  # закрашиваем экран черным цветом перед каждым новым кадром

    # перебираем все события (нажатия клавиш, закрытие окна и т.д.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # если нажали на крестик окна
            running = False

        elif event.type == pygame.KEYDOWN:  # если нажата клавиша
            if event.key == pygame.K_p:
                player.play()  # запустить музыку
            elif event.key == pygame.K_s:
                player.stop()  # остановить музыку
            elif event.key == pygame.K_n:
                player.next_track()  # переключить на следующий трек
            elif event.key == pygame.K_b:
                player.prev_track()  # переключить на предыдущий трек
            elif event.key == pygame.K_q:
                running = False  # выйти из программы

    # определяем название текущего трека
    if player.playlist:
        # берем полный путь к файлу и оставляем только имя файла
        track = os.path.basename(player.playlist[player.current_index])
    else:
        track = "No music"  # если в плейлисте ничего нет

    # создаем текст с названием текущего трека
    text = font.render(f"Now Playing: {track}", True, (255, 255, 255))
    # рисуем этот текст на экране в точке (50, 50)
    screen.blit(text, (50, 50))
    
    # получаем текущую позицию музыки в миллисекундах
    pos = pygame.mixer.music.get_pos()

    # если музыка реально играет и позиция доступна
    if pos >= 0:
        # выводим текущее время воспроизведения
        time_text = font.render(f"Time: {format_time(pos)}", True, (255, 255, 0))
        screen.blit(time_text, (50, 100))
    else:
        # если музыка не играет, показываем 0:00
        time_text = font.render(f"Time: 0:00", True, (255, 255, 0))
        screen.blit(time_text, (50, 100))

    # параметры полосы прогресса
    bar_x = 50       # x-координата начала полосы
    bar_y = 150      # y-координата начала полосы
    bar_width = 500  # полная ширина полосы
    bar_height = 20  # высота полосы

    # рисуем серый фон полосы прогресса
    pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

    # безопасно рисуем прогресс только если музыка играет
    if pos >= 0 and player.is_playing:
        # считаем, сколько нужно закрасить
        # здесь 180000 = 180 секунд = 3 минуты
        # то есть предполагается, что длина трека примерно 3 минуты
        progress = min((pos / 180000) * bar_width, bar_width)

        # рисуем зеленую часть полосы — текущий прогресс
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, progress, bar_height))

    pygame.display.update()  # обновляем экран
    clock.tick(30)  # ограничиваем цикл до 30 кадров в секунду

pygame.quit()  # корректно завершаем работу pygame