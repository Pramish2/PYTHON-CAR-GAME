import pygame, time, random, pygame_menu
from pygame_menu.examples import create_example_window

pygame.init()
display_width = 1280
display_height = 720
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
brown = (165, 42, 42)
car_width = 60
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Lets Race")
clock = pygame.time.Clock()
CarA = pygame.image.load("car1.jpeg")
CarB = pygame.image.load("car2.jpeg")
pygame.mixer.init()
crash_sound = pygame.mixer.Sound("crash.ogg")
car_sound = pygame.mixer.Sound("race.ogg")




players = []


def get_high_score():
    high_score = 0
    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
    except IOError:
        print("There is no high score yet.")
    except ValueError:
        print("I'm confused. Starting with no high score.")
    return high_score


def save_high_score(new_high_score):
    try:
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        print("Unable to save the high score.")


def things_dodged(count):
    high_score = get_high_score()
    font = pygame.font.SysFont(None, 40)
    text = font.render("Score " + str(count), True, black)
    if count > high_score:
        save_high_score(count)
    highScore = font.render("High Score " + str(high_score), True, black)
    gameDisplay.blit(text, (20, 20))
    gameDisplay.blit(highScore, (20, 50))


def car1(x, y):
    gameDisplay.blit(CarA, (x, y))


def car2(x, y):
    gameDisplay.blit(CarB, (x, y))


def things(thingx, thingy, thingw, thingh, color):
    color = brown
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 3))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()


def message_display2(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 3))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)


def crash(car):
    car_sound.stop()
    crash_sound.play()
    if len(players) == 0:
        message = 'Player' + car + ' Crashed'
    else:
        message = (players[int(car) - 1] + ' Crashed')
    message_display(message)


def crash3():
    car_sound.stop()
    crash_sound.play()
    message_display('Collision')


def game_loop():
    global players
    car_sound.play(-1)
    thing_speed = 14
    gameDisplay.fill(white)
    if len(players) == 0:
        message_display2('Player1 VS Player2')
    else:
        message_display2(players[0] + ' VS ' + players[1])
    y_change = 0
    y2_change = 0
    x = (display_width * 0.48 / 2)
    y = (display_height * 0.79)
    x2 = (display_width * 0.48 * 1.5)
    y2 = (display_height * 0.79)
    x_change = 0
    x2_change = 0
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_width = 50
    thing_height = 50
    dodged = 0
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_change = -8
                    y_change = 0
                elif event.key == pygame.K_d:
                    x_change = 8
                    y_change = 0
                elif event.key == pygame.K_w:
                    x_change = 0
                    y_change = -8
                elif event.key == pygame.K_s:
                    x_change = -0
                    y_change = 8
                if event.key == pygame.K_LEFT:
                    x2_change = -8
                    y2_change = 0
                elif event.key == pygame.K_RIGHT:
                    x2_change = 8
                    y2_change = 0
                elif event.key == pygame.K_UP:
                    x2_change = 0
                    y2_change = -8
                elif event.key == pygame.K_DOWN:
                    x2_change = -0
                    y2_change = 8
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    x2_change = 0
                    y2_change = 0
                if event.key == pygame.K_d or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_w:
                    x_change = 0
                    y_change = 0
        x += x_change
        if y + y_change >= display_height * 0.79:
            y_change = 0
        elif y + y_change <= 0:
            y_change = 0
        y += y_change
        x2 += x2_change
        if y2 + y2_change >= display_height * 0.79:
            y2_change = 0
        elif y2 + y2_change <= 0:
            y2_change = 0
        y2 += y2_change
        gameDisplay.fill(white)
        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed
        car1(x, y)
        car2(x2, y2)
        things_dodged(dodged)
        if ((x + car_width > x2 and x < x2 + car_width) and (y - 125 < y2 and y > y2 - 125)):
            crash3()
        if x > display_width - car_width or x < 0:
            crash('1')
        if x2 > display_width - car_width or x2 < 0:
            crash('2')
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            if thing_speed < 20:
                thing_speed += 0.3
        if y < thing_starty + thing_height:
            if ((x > thing_startx and x < thing_startx + thing_width) and (
                    y > thing_starty and y < thing_starty + thing_height)) or (
                    (x + car_width > thing_startx and x + car_width < thing_startx + thing_width) and (
                    y > thing_starty and y < thing_starty + thing_height)):
                crash('1')
        if y2 < thing_starty + thing_height:
            if ((x2 > thing_startx and x2 < thing_startx + thing_width) and (
                    y2 > thing_starty and y2 < thing_starty + thing_height)) or (
                    (x2 + car_width > thing_startx and x2 + car_width < thing_startx + thing_width) and (
                    y2 > thing_starty and y2 < thing_starty + thing_height)):
                crash('2')
        pygame.display.update()
        clock.tick(60)


surface = create_example_window('Racing Game', (1280, 720))


def start_the_game():
    game_loop()
    pygame.quit()
    quit()


def check_name(value):
    global players
    players.append(value)


def check_name2(value):
    global players
    players.append(value)


menu = pygame_menu.Menu(height=720, theme=pygame_menu.themes.THEME_BLUE, title="Pramish's Racing Game", width=1280)
player1 = menu.add.text_input('P1 Name:- ', default='Player1', onreturn=check_name)
player2 = menu.add.text_input('P2 Name:- ', default='Player2', onreturn=check_name2)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
HELP = "\n\n\n!!! AFTER CHANGING NAME PRESS ENTER FOR EACH INPUT OR NAME WON'T CHANGE !!!\nMADE BY PRAMISH"
menu.add.label(HELP, max_char=-1, font_size=20)
menu.mainloop(surface)
