import pygame
import sys 
import random
import json
import os

# запускаем pygame
pygame.init() 

# размеры окна
height = 800
width = 600

#разделим дарогу на три полоса 
lanes = [70, 210, 410]
# создаем окно
ecran = pygame.display.set_mode((width, height))
pygame.display.set_caption("Racer ")

clock = pygame.time.Clock()

# переменная для игрового цикла
a = True

# загружаем фон
fon = pygame.image.load("images/AnimatedStreet.png")
fon = pygame.transform.scale(fon, (width, height))

# загружаем машину игрока
player = pygame.image.load("images/Player.png")
player = pygame.transform.scale(player, (50, 100))
player_x = 200
player_y = 650

player_speed = 3
slow = False
slow_timer = 0

fast = False
fast_timer = 0

# загружаем машину врага
enemy = pygame.image.load("images/Enemy.png")
enemy = pygame.transform.scale(enemy, (50, 100))
enemy_x = random.choice(lanes)
enemy_y = -100
enemy_shag = 2
score = 0
# второй враг
enemy2 = pygame.image.load("images/Enemy.png")
enemy2 = pygame.transform.scale(enemy2, (50, 100))
enemy2_x = random.choice(lanes)
enemy2_y = -400
enemy2_shag = 2
# третий враг
enemy3 = pygame.image.load("images/Enemy.png")
enemy3 = pygame.transform.scale(enemy3, (50, 100))
enemy3_x = random.choice(lanes)
enemy3_y = -700
enemy3_shag = 2


# загружаем монету
coin = pygame.image.load("images/Coin.png")
coin = pygame.transform.scale(coin, (60, 60))
coin_x = random.choice(lanes)
coin_y = -60
coin_shag = 2
point = 0
# загружаем камень 
obstacles = pygame.image.load("images/obstacles.png")
obstacles = pygame.transform.scale(obstacles, (80, 80))
obstacles_x = random.choice(lanes)
obstacles_y = -250
obstacles_shag = 2
#загужаем масляное пятно
oil = pygame.image.load("images/oil.png")
oil = pygame.transform.scale(oil, (100, 100))
oil_x = random.choice(lanes)
oil_y = -500
oil_shag = 2
# загружаем зону 
zone = pygame.image.load("images/zone.png")
zone = pygame.transform.scale(zone, (170, 50))
zone_x = random.choice(lanes)
zone_y = random.randint(-500,-100)
zone_shag = 2
#загружаем вторую зону 
zone2 = pygame.image.load("images/zone2.png")
zone2 = pygame.transform.scale(zone2, (200, 200))
zone2_x = random.choice(lanes)
zone2_y = random.randint(-500,-100)
zone2_shag = 2
# загружаем shield
shield = pygame.image.load("images/shield.png")
shield = pygame.transform.scale(shield, (60, 60))
shield_x = random.choice(lanes)
shield_y = random.randint(-700, -200)
shield_shag = 2
shield_active = False
# загружаем repair
repair = pygame.image.load("images/repair.png")
repair = pygame.transform.scale(repair, (60, 60))
repair_x = random.choice(lanes)
repair_y = random.randint(-900, -300)
repair_shag = 2
repair_count = 0
                      
# это для ускорение врага 
point_coin = 15
move = 1

# создаем шрифты
font = pygame.font.SysFont("Verdana", 80)
font_small = pygame.font.SysFont("Verdana", 20)



slip = False
slip_timer = 0

screen = "menu"
player_name = ""

def draw_button(text, x, y, w, h):
    pygame.draw.rect(ecran, (200, 200, 200), (x, y, w, h))
    pygame.draw.rect(ecran, (0, 0, 0), (x, y, w, h), 3)

    button_text = font_small.render(text, True, (0, 0, 0))
    ecran.blit(button_text, (x + 30, y + 15))

def main_menu():
    ecran.fill((255, 255, 255))

    title = font.render("RACER", True, (0, 0, 0))
    ecran.blit(title, (150, 120))

    draw_button("PLAY", 200, 250, 200, 60)
    draw_button("LEADERBOARD", 200, 330, 200, 60)
    draw_button("SETTINGS", 200, 410, 200, 60)
    draw_button("QUIT", 200, 490, 200, 60)

def leaderboard_screen():
    ecran.fill((255, 255, 255))

    title = font_small.render("LEADERBOARD", True, (0, 0, 0))
    ecran.blit(title, (220, 80))

    scores = load_scores()

    y = 150

    if len(scores) == 0:
        text = font_small.render("No scores yet", True, (0, 0, 0))
        ecran.blit(text, (220, 200))
    else:
        for i, item in enumerate(scores):
            line = font_small.render(
                f"{i + 1}. {item['name']} | Score: {item['score']} | Coins: {item['coins']}",
                True,
                (0, 0, 0)
            )
            ecran.blit(line, (80, y))
            y += 35

    draw_button("BACK", 200, 650, 200, 60)

sound = True
car_color = "Blue"
difficulty = "Normal"
def settings_screen():
    ecran.fill((255, 255, 255))

    title = font_small.render("SETTINGS", True, (0, 0, 0))
    ecran.blit(title, (240, 100))

    text1 = font_small.render(f"Sound: {sound}", True, (0, 0, 0))
    ecran.blit(text1, (220, 180))

    text2 = font_small.render(f"Car Color: {car_color}", True, (0, 0, 0))
    ecran.blit(text2, (200, 270))

    text3 = font_small.render(f"Difficulty: {difficulty}", True, (0, 0, 0))
    ecran.blit(text3, (190, 360))

    draw_button("CHANGE SOUND", 180, 210, 240, 50)
    draw_button("CHANGE CAR", 180, 300, 240, 50)
    draw_button("CHANGE LEVEL", 180, 390, 240, 50)
    draw_button("BACK", 200, 650, 200, 60)

def game_over_screen():
    ecran.fill((255, 0, 0))

    title = font.render("GAME OVER", True, (0, 0, 0))
    ecran.blit(title, (60, 180))

    result = font_small.render(f"Score: {score} | Coins: {point}", True, (0, 0, 0))
    ecran.blit(result, (170, 300))

    draw_button("RETRY", 200, 420, 200, 60)
    draw_button("MAIN MENU", 200, 510, 200, 60)

def name_screen():
    ecran.fill((255, 255, 255))

    title = font_small.render("ENTER YOUR NAME:", True, (0, 0, 0))
    ecran.blit(title, (190, 200))

    # поле для ввода имени
    pygame.draw.rect(ecran, (240, 240, 240), (150, 270, 300, 50))
    pygame.draw.rect(ecran, (0, 0, 0), (150, 270, 300, 50), 3)

    name_text = font_small.render(player_name, True, (0, 0, 0))
    ecran.blit(name_text, (165, 285))

    draw_button("START", 200, 380, 200, 60)

def reset_game():
    global player_x, player_y, player_speed
    global enemy_y, enemy2_y, enemy3_y, enemy_x, enemy2_x, enemy3_x
    global coin_y, coin_x, obstacles_y, obstacles_x, oil_y, oil_x
    global zone_y, zone_x, zone2_y, zone2_x
    global shield_y, shield_x, repair_y, repair_x
    global score, point, move, point_coin
    global slip, slip_timer, slow, slow_timer, fast, fast_timer
    global shield_active, repair_count

    player_x = 200
    player_y = 650
    player_speed = 3

    enemy_x = random.choice(lanes)
    enemy_y = -100
    enemy2_x = random.choice(lanes)
    enemy2_y = -400
    enemy3_x = random.choice(lanes)
    enemy3_y = -700

    coin_x = random.choice(lanes)
    coin_y = -60

    obstacles_x = random.choice(lanes)
    obstacles_y = -250

    oil_x = random.choice(lanes)
    oil_y = -500

    zone_x = random.choice(lanes)
    zone_y = random.randint(-500, -100)

    zone2_x = random.choice(lanes)
    zone2_y = random.randint(-500, -100)

    shield_x = random.choice(lanes)
    shield_y = random.randint(-700, -200)

    repair_x = random.choice(lanes)
    repair_y = random.randint(-900, -300)

    score = 0
    point = 0
    move = 1
    point_coin = 15

    slip = False
    slip_timer = 0
    slow = False
    slow_timer = 0
    fast = False
    fast_timer = 0

    shield_active = False
    repair_count = 0

def save_score():
    data = []

    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r") as file:
            data = json.load(file)

    data.append({
        "name": player_name,
        "score": score,
        "coins": point
    })

    data = sorted(data, key=lambda x: x["score"], reverse=True)
    data = data[:10]

    with open("leaderboard.json", "w") as file:
        json.dump(data, file)


def load_scores():
    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r") as file:
            return json.load(file)
    return []

# главный цикл игры
while a:
    if screen == "menu":
        main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if 200 <= mx <= 400 and 250 <= my <= 310:
                    screen = "name"

                elif 200 <= mx <= 400 and 330 <= my <= 390:
                    screen = "leaderboard"

                elif 200 <= mx <= 400 and 410 <= my <= 470:
                    screen = "settings"

                elif 200 <= mx <= 400 and 490 <= my <= 550:
                    a = False

        pygame.display.update()
        clock.tick(60)
        continue

    if screen == "name":
        name_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]

                elif event.key == pygame.K_RETURN:
                    if player_name == "":
                        player_name = "Player"
                    screen = "game"

                else:
                    player_name += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if 200 <= mx <= 400 and 380 <= my <= 440:
                    if player_name == "":
                        player_name = "Player"
                    screen = "game"

        pygame.display.update()
        clock.tick(60)
        continue

    if screen == "leaderboard":
        leaderboard_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if 200 <= mx <= 400 and 650 <= my <= 710:
                    screen = "menu"

        pygame.display.update()
        clock.tick(60)
        continue
    
    if screen == "settings":
        settings_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if 180 <= mx <= 420 and 210 <= my <= 260:
                    sound = not sound

                elif 180 <= mx <= 420 and 300 <= my <= 350:
                    if car_color == "Blue":
                        car_color = "Red"
                    elif car_color == "Red":
                        car_color = "Green"
                    else:
                        car_color = "Blue"

                elif 180 <= mx <= 420 and 390 <= my <= 440:
                    if difficulty == "Easy":
                        difficulty = "Normal"
                    elif difficulty == "Normal":
                        difficulty = "Hard"
                    else:
                        difficulty = "Easy"

                elif 200 <= mx <= 400 and 650 <= my <= 710:
                    screen = "menu"

        pygame.display.update()
        clock.tick(60)
        continue
    if screen == "game_over":
        game_over_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if 200 <= mx <= 400 and 420 <= my <= 480:
                    reset_game()
                    screen = "game"

                elif 200 <= mx <= 400 and 510 <= my <= 570:
                    screen = "menu"

        pygame.display.update()
        clock.tick(60)
        continue


    # двигаем врага и монету вниз
    enemy_y += enemy_shag + move
    coin_y += coin_shag
    obstacles_y += obstacles_shag
    oil_y += oil_shag
    zone_y += zone_shag
    zone2_y += zone2_shag
    shield_y += shield_shag
    repair_y += repair_shag
    enemy2_y += enemy2_shag + move
    enemy3_y += enemy3_shag + move


    # создаем области для проверки столкновений
    player_rect = player.get_rect(topleft=(player_x, player_y))
    enemy_rect = enemy.get_rect(topleft=(enemy_x, enemy_y))
    coin_rect = coin.get_rect(topleft=(coin_x, coin_y))
    obstacles_rect = obstacles.get_rect(topleft=(obstacles_x, obstacles_y))
    oil_rect = oil.get_rect(topleft=(oil_x, oil_y))
    zone_rect = zone.get_rect(topleft=(zone_x, zone_y))
    zone2_rect = zone2.get_rect(topleft=(zone2_x, zone2_y))
    shield_rect = shield.get_rect(topleft=(shield_x, shield_y))
    repair_rect = repair.get_rect(topleft=(repair_x, repair_y))
    enemy2_rect = enemy2.get_rect(topleft=(enemy2_x, enemy2_y))
    enemy3_rect = enemy3.get_rect(topleft=(enemy3_x, enemy3_y))
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # проверяем нажатые клавиши
    keys = pygame.key.get_pressed()
    
    # если враг ушел вниз, возвращаем его наверх
    if enemy_y > height:
        score += 1
        enemy_y = -100
        enemy_x = random.choice(lanes)
    if enemy2_y > height:
        score += 1
        enemy2_y = -400
        enemy2_x = random.choice(lanes)    
    if enemy3_y > height:
        score += 1
        enemy3_y = -700
        enemy3_x = random.choice(lanes)

    # если монета ушла вниз, возвращаем ее наверх
    if coin_y > height:
        coin_y = -60
        coin_x = random.choice(lanes)

    # если препятствия ушла вниз возвращаем ее наверх
    if obstacles_y > height:
        obstacles_y = -250
        obstacles_x = random.choice(lanes)
    # вторая препятсва
    if oil_y > height:
        oil_y = -500
        oil_x = random.choice(lanes)

    if zone_y > height:
        zone_x = random.choice(lanes)
        zone_y = random.randint(-500,-100)
    if zone2_y > height:
        zone2_x = random.choice(lanes)
        zone2_y = random.randint(-500,-100)

    # создаем текст очков
    text = font_small.render(f"SCORE: {score}", True, (0, 0, 0))
    text2 = font_small.render(f"POINT: {point}", True, (0, 0, 0))
    text3 = font_small.render(f"SHIELD: {shield_active}", True, (0, 0, 0))
    text4 = font_small.render(f"REPAIR: {repair_count}", True, (0, 0, 0))

    # движение игрока влево и вправо
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - 70:
        player_x += player_speed
    # если игрок столнеться с маслом он шатаеться
    if slip:
        player_x += random.randint(-10, 10)
        slip_timer -= 1

        if slip_timer <= 0:
            slip = False

    if slow:
        player_speed = 1
        slow_timer -= 1

        if slow_timer <= 0:
            slow = False
            player_speed = 3

    if fast:
        player_speed = 8
        fast_timer -= 1

        if fast_timer <= 0:
            fast = False
            player_speed = 3

    # проверка столкновения с врагом
    if player_rect.colliderect(enemy_rect):
        if shield_active:
            shield_active = False
            enemy_y = -100
            enemy_x = random.choice(lanes)
        elif repair_count > 0:
            repair_count -= 1
            enemy_y = -100
            enemy_x = random.choice(lanes)
        else:
            ecran.fill((255, 0, 0))
            text = font.render("Game Over", True, (0, 0, 0))
            ecran.blit(text, (10, 250))
            pygame.display.update()
            pygame.time.delay(2000)
            save_score()
            screen = "game_over"

    if player_rect.colliderect(enemy2_rect):
        if shield_active:
            shield_active = False
            enemy2_y = -400
            enemy2_x = random.choice(lanes)
        elif repair_count > 0:
            repair_count -= 1
            enemy2_y = -400
            enemy2_x = random.choice(lanes)
        else:
            ecran.fill((255, 0, 0))
            text = font.render("Game Over", True, (0, 0, 0))
            ecran.blit(text, (10, 250))
            pygame.display.update()
            pygame.time.delay(2000)
            save_score()
            screen = "game_over"

    if player_rect.colliderect(enemy3_rect):
        if shield_active:
            shield_active = False
            enemy3_y = -700
            enemy3_x = random.choice(lanes)
        elif repair_count > 0:
            repair_count -= 1
            enemy3_y = -700
            enemy3_x = random.choice(lanes)
        else:
            ecran.fill((255, 0, 0))
            text = font.render("Game Over", True, (0, 0, 0))
            ecran.blit(text, (10, 250))
            pygame.display.update()
            pygame.time.delay(2000)
            save_score()
            screen = "game_over"

    # проверка столкновения с препятсвиям
    if player_rect.colliderect(obstacles_rect):
        if shield_active:
            shield_active = False
            obstacles_y = -250
            obstacles_x = random.choice(lanes)
        elif repair_count > 0:
            repair_count -= 1
            obstacles_y = -250
            obstacles_x = random.choice(lanes)
        else:
            ecran.fill((255, 0, 0))
            text = font.render("Game Over", True, (0, 0, 0))
            ecran.blit(text, (10, 250))
            pygame.display.update()
            pygame.time.delay(2000)
            save_score()
            screen = "game_over"

    if player_rect.colliderect(oil_rect):
        if repair_count > 0:
            repair_count -= 1
            oil_y = -500
            oil_x = random.choice(lanes)
        else:
            slip = True
            slip_timer = 120
            oil_y = -500
            oil_x = random.choice(lanes)

    if player_x < 0:
        player_x = 0

    if player_x > width - 50:
        player_x = width - 50

    if player_rect.colliderect(zone_rect):
        slow = True
        slow_timer = 200

    if player_rect.colliderect(zone2_rect):
        fast = True
        fast_timer = 200

    if player_rect.colliderect(shield_rect):
        shield_active = True
        shield_y = random.randint(-700, -200)
        shield_x = random.choice(lanes)

    if player_rect.colliderect(repair_rect):
        repair_count += 1
        repair_y = random.randint(-900, -300)
        repair_x = random.choice(lanes)

    # проверка сбора монеты
    if player_rect.colliderect(coin_rect):
        point += random.randint(1,6)
        coin_y = -60
        coin_x = random.choice(lanes)

    # после каждый 15 очков враг ускориться
    if point >= point_coin:
        move += 1
        point_coin += 15

    # рисуем фон
    ecran.blit(fon, (0, 0))

    # рисуем счетчики
    ecran.blit(text, (7, 5))
    ecran.blit(text2, (470, 5))
    ecran.blit(text3, (7, 30))
    ecran.blit(text4, (470, 30))
    
    pygame.draw.line(ecran, (255, 255, 255), (200, 0), (200, height), 5)
    pygame.draw.line(ecran, (255, 255, 255), (400, 0), (400, height), 5) 
    name_text = font_small.render(f"PLAYER: {player_name}", True, (0, 0, 0))
    ecran.blit(name_text, (7, 55))
    # рисуем игрока, врага и монету
    ecran.blit(text3, (7, 30))
    ecran.blit(text4, (470, 30))
    ecran.blit(zone, (zone_x, zone_y))
    ecran.blit(zone2, (zone2_x, zone2_y))
    ecran.blit(player, (player_x, player_y))
    ecran.blit(enemy, (enemy_x, enemy_y))
    ecran.blit(enemy2, (enemy2_x, enemy2_y))
    ecran.blit(enemy3, (enemy3_x, enemy3_y))
    ecran.blit(coin, (coin_x, coin_y))
    ecran.blit(obstacles, (obstacles_x, obstacles_y))
    ecran.blit(oil, (oil_x, oil_y))
    ecran.blit(shield, (shield_x, shield_y))
    ecran.blit(repair, (repair_x, repair_y))
    
    
    
    clock.tick(60)
    # обновляем экран
    pygame.display.update()
pygame.quit()