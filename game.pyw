import pygame, time, sys

version_ = '1.21'
type_ = 'alpha(discontinued)'

temp = open('data/options.txt').read().split('\n')[:-1]
print(temp)
options = []
for i in temp:
    try:
        options.append([i.split('=')[0],int(i.split('=')[1])])
    except:
        options.append([i.split('=')[0],i.split('=')[1]])

options.append(['reset to defaults','reset'])
options.append(['return to main screen','exit'])

starting_health = options[0][1]
jump_force = options[1][1]
speed = options[2][1]
ground_level = 300
double_jump = True if options[3][1] == 'on' else False
bullet_life = options[4][1]*60

print(options[4])

sec, min_ = 00,00

class Player:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.velocity = pygame.Vector2()
        self.on_floor = False
        self.on_wall = False
        self.color = color
        self.health = starting_health
        self.doubleJump = True
        self.face_offset = pygame.Vector2()
        self.bullet_delay = 0

    def draw(self, master):
        pygame.draw.rect(master, self.color, self.rect)

    def update(self, op):
        global winner, dead
        if self.rect.bottom >= ground_level and self.velocity.y > 0:
            self.rect.bottom = ground_level
            self.face_offset.y = 0
            self.on_floor = True
            self.doubleJump = True
        else:
            self.face_offset.y = self.velocity.y
            self.velocity.y += 0.1
            self.rect.y += self.velocity.y
            self.on_floor = False
        if self.rect.right <= 30 and self.velocity.x < 0:
            self.rect.right = 30
            self.on_wall = True
        elif self.rect.left >= window.get_width() - 30 and self.velocity.x > 0:
            self.rect.left = window.get_width() - 30
            self.on_wall = True
        else:
            self.rect.x += self.velocity.x
            self.on_wall = False

        if self.health <= 0:
            winner = op
            dead = True

        if self.bullet_delay > 0: self.bullet_delay -= 1

class Projectile:
    def __init__(self, side, opposite):
        self.rect = pygame.Rect(side.rect.x, side.rect.y-7, 16, 16)
        #self.rect = pygame.Rect(side.rect.x, y-7, 16, 16)
        self.opposite = opposite
        self.velocity = speed+2 if side == player else -speed-2
        self.side = side
        self.decay = 0
        self.gravity = 0
        #self.jump_force = 5

    def draw(self, master):
        if self.side == player:
            if player.color != (0,0,0): pygame.draw.rect(master, player2.color if self.side==player2 else player.color, self.rect)
            else: pygame.draw.rect(master, (255,255,255), self.rect)
        else:
            if player2.color != (0,0,0): pygame.draw.rect(master, player2.color if self.side==player2 else player.color, self.rect)
            else: pygame.draw.rect(master, (255,255,255), self.rect)

    def update(self):
        if self.rect.colliderect(self.opposite):
            self.rect.x = 1000000000
            self.opposite.health -= 1
            projectiles.pop(projectiles.index(self))
            damage.play()
        else:
            if self.rect.right <= 0:
                self.velocity *= -1
            elif self.rect.left >= window.get_width():
                self.velocity *= -1
            self.rect.x += self.velocity
        self.decay += 1
        if self.decay >= bullet_life:
            self.rect.x = 1000000000
            try:
                projectiles.pop(projectiles.index(self))
            except:
                pass
    

class Face:
    def __init__(self,parent,face):
        self.offset = parent.face_offset
        self.rect = parent.rect
        self.face = face

    def draw(self):
        window.blit(pygame.transform.scale(pygame.image.load(f'data/textures/face-{self.face}.png'),(30,30)),(self.rect.x+self.offset.x,self.rect.y+self.offset.y))

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((720,480),pygame.RESIZABLE)
pygame.display.set_caption("Square Tale")
pygame.display.set_icon(pygame.transform.scale(pygame.image.load("data/textures/icon.png"),(64,64)))

player = Player(100,0, (255, 0, 0))
player_face = Face(player,1)
player2 = Player(window.get_width()-100,0, (0, 0, 255))
player2_face = Face(player2,1)

projectiles = []

titleScreen = False
dead = False
optionsMenu = False
paused = False
winner = None
about = False
face_select = False
logo_gui = True

damage = pygame.mixer.Sound("data/sounds/damage.wav")
explosion = pygame.mixer.Sound("data/sounds/explosion.wav")
jump = pygame.mixer.Sound("data/sounds/jump.wav")
laser = pygame.mixer.Sound("data/sounds/laser.wav")
click = pygame.mixer.Sound("data/sounds/selected.wav")
select = pygame.mixer.Sound("data/sounds/select.wav")
intro = pygame.mixer.Sound("data/sounds/intro.wav")
start = pygame.mixer.Sound('data/sounds/start.wav')

font = pygame.font.Font("data/fonts/font.ttf", 40)
font_small = pygame.font.Font("data/fonts/font.ttf", 20)

two_position = pygame.Vector2(550,200)
two_velocity = 0

selected = 0
gui_main_menu = [
    ['play','startGame'],
    ['options','settings'],
    ['exit','exit']
]

selected_option = 0
current_part = 0
gui_options_parts = [
    'general',
    'video',
    'audio'
]

selected_dead = 0
gui_dead_menu = [
    ['play again','restart'],
    ['select character','charSelect'],
    ['return to main menu','mainMenu']
]

selected_paused = 0
gui_paused_menu = [
    ['resume','resume'],
    ['restart','playAgain'],
    ['main menu', 'mainMenu']
]

should_be_blue = False
maxormin = False

about_offset = 0

about_text_old = [
    'square tale is a small indie game',
    'developed by fireplace. it\'s really fun',
    'to play with your friends',
    'if u have any',
    '',
    'lmao just wait for the next update'
]

about_text = [
    '====developers====','',
    'veki','',
    '=port to windows 7=','',
    'jakipro99 ','',
    '======sound========','',
    'jsfxr','',
    '===font and style==','',
    'pico-8','',
    '====beta-testers===','',
    'jakipro99','djolemaster123','kasalo','gurgusovac'
]

joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()

controller_warning = False #True if len(joysticks) > 0 else False
gui_cw = [
    f'any new controller will not be registred',
    'so, you will need to restart the game.',
    'also, only two joysticks can be used.',
    '',
    'press space to continue'
]

volume = 0.5
intro.set_volume(volume)
changing_volume = True
colors = [
    (255,0,0),
    (0,0,255),
    (0,255,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (255,255,255),
    (0,0,0)
]
sel_c = 0
sel_c2 = 1
ready = [False,False]

logo_time = 0
logo = pygame.transform.scale(pygame.image.load("data/textures/logo.png"),(51*8,15*8))
while True:
    if player.color == (0,0,0) and player_face.face in [19,20,21]:
        player_face.face = 18
    if player2.color == (0,0,0) and player2_face.face in [19,20,21]:
        player2_face.face = 18
    player.color = colors[sel_c]
    player2.color = colors[sel_c2]
    ground_level = window.get_height()-120
    volume = max(0,min(volume,1))
    damage.set_volume(volume)
    explosion.set_volume(volume)
    jump.set_volume(volume)
    laser.set_volume(volume)
    click.set_volume(volume)
    select.set_volume(volume)
    intro.set_volume(volume)
    start.set_volume(volume)

    if logo_gui:
        if logo_time >= 300:
            logo_gui = False
            titleScreen = True
            intro.play()
        else:
            logo_time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.fill((0,0,0))

        window.blit(logo,(window.get_width()/2-logo.get_width()/2,window.get_height()/2-logo.get_height()/2))
        window.blit(font_small.render("@fireplace 2022-2022. all rights deserved", False, (128,128,128)),(window.get_width()/2-font_small.render("@fireplace 2022-2022. all rights deserved", False, (128,128,128)).get_width()/2,window.get_height()-font_small.get_height()))
        
        pygame.display.flip()
        
    
    elif controller_warning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    controller_warning = False
                    titleScreen = True

        window.fill((0,0,0))
        pygame.draw.rect(window,(255,255,255),(0,950+about_offset,720,400),3)

        window.blit(font.render("warning", False, (255,0,0)), (window.get_width()/2-font.render("warning", False, (255,0,0)).get_width()/2, 70))

        for i in gui_cw:
            window.blit(font_small.render(i, False, (255,255,255)), (window.get_width()/2-font_small.render(i, False, (255,0,0)).get_width()/2, 160+gui_cw.index(i)*40))

        
        pygame.display.flip()
        

    elif titleScreen:
        selected = max(0,min(selected,len(gui_main_menu)-1))
        two_position.x += two_velocity

        by_veki = font_small.render("by fireplace", False, (255,255,255) if not should_be_blue else (255, 255, 0))
        
        (mouseX, mouseY) = pygame.mouse.get_pos()

        if by_veki.get_rect(x=10, y=window.get_height()-font_small.get_height()).collidepoint(mouseX, mouseY):
            should_be_blue = True
        else:
            should_be_blue = False
        
        window.fill((0,0,0))
        window.blit(font.render("square tale", False, (255,0,0)), (window.get_width()/2-font.render("square tale", False, (255,0,0)).get_width()/2, 200))
        #window.blit(pygame.transform.rotate(font.render("2", False, (0,255,0)),0), two_position)
        window.blit(by_veki, (10, window.get_height()-font_small.get_height()))
        #window.blit(font_small.render("press space to begin", False, (255, 255, 255)), (200, 400))
        for i in gui_main_menu:
            window.blit(font_small.render(i[0], False, (255, 255, 255) if selected != gui_main_menu.index(i) else (255,255,0)), (window.get_width()/2-font_small.render(i[0], False, (255, 255, 255)).get_width()/2, 300+gui_main_menu.index(i)*50))
            if selected == gui_main_menu.index(i):
                window.blit(font_small.render('>', False, (0, 255, 0)), (window.get_width()/2-120, 300+gui_main_menu.index(i)*50))
                window.blit(font_small.render('<', False, (0, 255, 0)), (window.get_width()/2+100, 300+gui_main_menu.index(i)*50))
        #window.blit(font_small.render("press space to begin", False, (255, 255, 255)), (200, 400))
        window.blit(font_small.render(version_ if type_ == 'vannila' else type_ + ' ' + version_, False, (255,255,255)), (window.get_width()-font_small.render(version_ if type_ == 'vannila' else type_ + ' ' + version_, False, (255,255,255)).get_width(), window.get_height()-font_small.get_height()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    click.play()
                    command = gui_main_menu[selected][1]
                    if command == 'startGame':
                        start.play()
                        titleScreen = False
                        optionsMenu = False
                        face_select = True
                    elif command == 'exit':
                        time.sleep(0.3)
                        sys.exit()
                    elif command == 'settings':
                        titleScreen = False
                        optionsMenu = True
                if event.key == pygame.K_LEFT:
                    two_velocity = -5
                elif event.key == pygame.K_RIGHT:
                    two_velocity = 5
                if event.key == pygame.K_UP:
                    selected -= 1
                    select.play()
                elif event.key == pygame.K_DOWN:
                    selected += 1
                    select.play()
                if event.key == pygame.K_KP_PLUS or event.key == pygame.K_PLUS:
                    volume += 0.1
                    click.play()
                elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS:
                    volume -= 0.1
                    click.play()
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    two_velocity = 0

            if event.type == pygame.WINDOWSIZECHANGED:
                player.rect.x, player2.rect.x = 100,window.get_width()-100
                ground_level = window.get_height()-120
            #elif event.type == pygame.JOYBUTTONDOWN:
            #    if event.joy == 0:
                    
                

        
        if pygame.mouse.get_pressed()[0] and by_veki.get_rect(x=10, y=window.get_height()-font_small.get_height()).collidepoint(pygame.mouse.get_pos()):
            about = True
            about_offset = 0
            titleScreen = False
            
        """for i in range(int(volume*10)):
                pygame.draw.rect(window,(255,255,255),(100+i*50,40,50,20))"""

        
        pygame.display.flip()
        clock.tick(60)
        
    elif about:
        about_offset -= 1
        about_offset = max(-3000,about_offset)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    about = False
                    titleScreen = True

        window.fill((0,0,0))
        #pygame.draw.rect(window,(255,255,255),(0,950+about_offset,720,400),3)
        
        #window.blit(font.render("credits", False, (255,255,255)), (window.get_width()/2-font.render("credits", False, (255,0,0)).get_width()/2, 500+about_offset))

        window.blit(logo,(window.get_width()/2-logo.get_width()/2,400+about_offset))
        
        for i in about_text:
            window.blit(font_small.render(i, False, (255,255,255) if not '=' in i else (255,255,0)), (window.get_width()/2-font_small.render(i, False, (255,0,0)).get_width()/2, 590+about_text.index(i)*40+about_offset))

        window.blit(font_small.render('thanks to all people/teams', False, (0,0,255) ), (window.get_width()/2-font_small.render('thanks to all people/teams', False, (255,0,0)).get_width()/2, 590+26*40+about_offset))
        window.blit(font_small.render('that helped <) - veki', False, (0,0,255) ), (window.get_width()/2-font_small.render('that helped <) - veki', False, (255,0,0)).get_width()/2, 590+27*40+about_offset))

        
        pygame.display.flip()
        clock.tick(60)
        
    elif dead:
        selected_dead = max(0,min(selected_dead,len(gui_dead_menu)-1))
        window.fill((0,0,0))
        window.blit(font.render("p1 wins" if winner == player else "p2 wins", False, (255, 0,0) if winner == player else (0, 0, 255)), (window.get_width()/2-font.render("p1 wins" if winner == player else "p2 wins", False, (255, 0,0) if winner == player else (0, 0, 255)).get_width()/2, 200))
        window.blit(pygame.transform.rotate(font.render("gg", False, (255, 255, 255)), 45), (600, 50))
        #window.blit(font_small.render("press space to restart", False, (255, 255, 255)), (200, 400))
        #window.blit(font_small.render("press escape to return", False, (255, 255, 255)), (200, 300))
        for i in gui_dead_menu:
            window.blit(font_small.render(i[0], False, (255, 255, 255) if selected_dead != gui_dead_menu.index(i) else (255,255,0)), (window.get_width()/2-font_small.render(i[0], False, (255, 255, 255)).get_width()/2, 300+gui_dead_menu.index(i)*50))
            if selected_dead == gui_dead_menu.index(i):
                window.blit(font_small.render('>', False, (0, 255, 0)), (window.get_width()/2-220, 300+gui_dead_menu.index(i)*50))
                window.blit(font_small.render('<', False, (0, 255, 0)), (window.get_width()/2+200, 300+gui_dead_menu.index(i)*50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    select.play()
                    selected_dead -= 1
                if event.key == pygame.K_DOWN:
                    select.play()
                    selected_dead += 1
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    click.play()
                    command = gui_dead_menu[selected_dead][1]
                    if command == 'restart':
                        dead = False
                        start.play()
                        player.health = starting_health
                        player2.health = starting_health
                        player.rect.y, player2.rect.y = 0,0
                        player.rect.x, player2.rect.x = 100,window.get_width()-100
                        player.velocity.y, player2.velocity.y = 0,0
                        player.velocity.x, player2.velocity.x = 0,0
                        projectiles = []
                        sec, min_ = 0,0
                        click.play()
                    elif command == 'charSelect':
                        dead = False
                        start.play()
                        player.health = starting_health
                        player2.health = starting_health
                        player.rect.y, player2.rect.y = 0,0
                        player.rect.x, player2.rect.x = 100,window.get_width()-100
                        player.velocity.y, player2.velocity.y = 0,0
                        player.velocity.x, player2.velocity.x = 0,0
                        projectiles = []
                        sec, min_ = 0,0
                        click.play()
                        face_select = True
                    elif command == 'mainMenu':
                        dead = False
                        player.health = starting_health
                        player2.health = starting_health
                        player.rect.y, player2.rect.y = 0,0
                        player.rect.x, player2.rect.x = 100,window.get_width()-100
                        player.velocity.y, player2.velocity.y = 0, 0
                        player.velocity.x, player2.velocity.x = 0, 0
                        projectiles = []
                        sec, min_ = 0,0
                        titleScreen = True
                        intro.play()
                    """dead = False
                    player.health = starting_health
                    player2.health = starting_health
                    player.rect.y, player2.rect.y = 0,0
                    player.rect.x, player2.rect.x = 100,window.get_width()-100
                    player.velocity.y, player2.velocity.y = 0,0
                    player.velocity.x, player2.velocity.x = 0,0
                    projectiles = []
                    click.play()"""
                """elif event.key == pygame.K_ESCAPE:
                    dead = False
                    player.health = starting_health
                    player2.health = starting_health
                    player.rect.y, player2.rect.y = 0,0
                    player.rect.x, player2.rect.x = 100,window.get_width()-100
                    player.velocity.y, player2.velocity.y = 0, 0
                    player.velocity.x, player2.velocity.x = 0, 0
                    projectiles = []
                    titleScreen = True
                    intro.play()"""
        window.blit(font_small.render(version_ if type_ == 'vannila' else type_ + ' ' + version_, False, (255,255,255)), (window.get_width()-font_small.render(version_ if type_ == 'vannila' else type_ + ' ' + version_, False, (255,255,255)).get_width(), window.get_height()-font_small.get_height()))

        pygame.display.flip()
        clock.tick(60)
        
    elif optionsMenu:
        options[0][1] = max(5,min(options[0][1],50))
        options[1][1] = max(2,min(options[1][1],7))
        options[2][1] = max(1,min(options[2][1],15))
        options[4][1] = max(3,min(options[4][1],10))
        selected_option = max(0,min(selected_option,len(options)-1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option -= 1
                    select.play()
                elif event.key == pygame.K_DOWN:
                    selected_option += 1
                    select.play()
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    click.play()
                    value = options[selected_option][1]
                    if value == 'exit':
                        optionsUpdated = ""
                        options.pop(len(options)-1)
                        options.pop(len(options)-1)
                        for setting in options:
                            optionsUpdated += f"{setting[0]}={setting[1]}\n"
                        options.append(['reset to defaults','reset'])
                        options.append(['return to main screen','exit'])
                        print(optionsUpdated)
                        with open('data/options.txt','w') as f:
                            f.write(optionsUpdated)
                            f.close()
                        starting_health = options[0][1]
                        jump_force = options[1][1]
                        speed = options[2][1]
                        double_jump = True if options[3][1] == 'on' else False
                        bullet_life = options[4][1]*60
                        player.health, player2.health = starting_health, starting_health
                        optionsMenu = False
                        titleScreen = True
                    elif value == 'reset':
                        options[0][1] = 20
                        options[1][1] = 3
                        options[2][1] = 300
                        options[3][1] = 'on'
                        options[4][1] = 5
                if event.key == pygame.K_RIGHT:
                    try:
                        options[selected_option][1] += 1 if not maxormin else 999999
                    except:
                        if not options[selected_option][1] in ['exit','reset']: options[selected_option][1] = 'on'
                    click.play()
                if event.key in [pygame.K_RCTRL, pygame.K_LCTRL]:
                    maxormin = True if maxormin == False else False

                elif event.key == pygame.K_LEFT:
                    try:
                        options[selected_option][1] -= 1 if not maxormin else 999999
                    except:
                        if not options[selected_option][1] in ['exit','reset']: options[selected_option][1] = 'off'
                    click.play()

        window.fill((0,0,0))

        window.blit(font_small.render("settings", False, (255,255,255)), (window.get_width()/2-font_small.render("settings", False, (255,0,0)).get_width()/2, 40))

        options_gui = [i for i in options]
        pygame.draw.line(window, (255,255,255), (0,70),(99999,70),3)
        for setting in options_gui:
            if not setting[1] in ['exit','reset'] and not setting[0] == 'volume':
                window.blit(font_small.render(setting[0] + ' : ' + str(setting[1]), False, (255, 255, 255) if selected_option != options_gui.index(setting) else (255,255,0)), (window.get_width()/2-font_small.render(setting[0] + ' : ' + str(setting[1]), False, (255,0,0)).get_width()/2, 100+options_gui.index(setting)*50))
                if selected_option == options.index(setting):
                    window.blit(font_small.render('>', False, (0, 255, 0) if not maxormin else (255,0,0)), (window.get_width()/2-220, 100+options_gui.index(setting)*50))
                    window.blit(font_small.render('<', False, (0, 255, 0) if not maxormin else (255,0,0)), (window.get_width()/2+200, 100+options_gui.index(setting)*50))
            elif not setting[0] == 'volume':
                window.blit(font_small.render(setting[0], False, (255, 255, 255) if selected_option != options.index(setting) else (255,255,0)), (window.get_width()/2-font_small.render(setting[0], False, (255,0,0)).get_width()/2, 140+options.index(setting)*50))
                if selected_option == options.index(setting):
                    window.blit(font_small.render('>', False, (0, 255, 0)), (window.get_width()/2-220, 140+options.index(setting)*50))
                    window.blit(font_small.render('<', False, (0, 255, 0)), (window.get_width()/2+200, 140+options.index(setting)*50))

        pygame.draw.line(window, (255,255,255), (0,360),(99999,360),3)
        pygame.draw.line(window, (255,255,255), (0,500),(99999,460),3)
        window.blit(font_small.render(version_ if type_ == 'vannila' else type_ + ' ' + version_, False, (255,255,255)), (window.get_width()-font_small.render(version_ if type_ == 'vannila' else type_ + ' ' + version_, False, (255,255,255)).get_width(), window.get_height()-font_small.get_height()))
        
        pygame.display.flip()
        clock.tick(60)
        
    elif paused:
        selected_paused = max(0,min(selected_paused,len(gui_paused_menu)-1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    click.play()
                    command = gui_paused_menu[selected_paused][1]
                    if command == 'resume':
                        paused = False
                    elif command == 'playAgain':
                        start.play()
                        paused = False
                        face_select = True
                        player.health = starting_health
                        player2.health = starting_health
                        player.rect.y, player2.rect.y = 0,0
                        player.rect.x, player2.rect.x = 100,window.get_width()-100
                        player.velocity.y, player2.velocity.y = 0, 0
                        player.velocity.x, player2.velocity.x = 0, 0
                        projectiles = []
                        sec, min_ = 0,0
                    elif command == 'mainMenu':
                        paused = False
                        player.health = starting_health
                        player2.health = starting_health
                        player.rect.y, player2.rect.y = 0,0
                        player.rect.x, player2.rect.x = 100,window.get_width()-100
                        player.velocity.y, player2.velocity.y = 0, 0
                        player.velocity.x, player2.velocity.x = 0, 0
                        projectiles = []
                        sec, min_ = 0,0
                        titleScreen = True
                        intro.play()
                if event.key == pygame.K_UP:
                    select.play()
                    selected_paused -= 1
                if event.key == pygame.K_DOWN:
                    select.play()
                    selected_paused += 1

        pygame.draw.rect(window,(0,0,0),(window.get_width()/2-175,window.get_height()/2-150,350,300))
        pygame.draw.rect(window,(255,255,255),(window.get_width()/2-175,window.get_height()/2-150,350,300),3)
        
        window.blit(font_small.render("paused", False, (0,0,255) if player2.health > player.health else (255,0,0)), (window.get_width()/2-font_small.render("paused", False, (255,0,0)).get_width()/2, window.get_height()/2-120))

        for i in gui_paused_menu:
            window.blit(font_small.render(i[0], False, (255, 255, 255) if selected_paused != gui_paused_menu.index(i) else (255,255,0)), (window.get_width()/2-font_small.render(i[0], False, (255, 255, 255)).get_width()/2, window.get_height()/2-40+gui_paused_menu.index(i)*50))
            if selected_paused == gui_paused_menu.index(i):
                window.blit(font_small.render('>', False, (0, 255, 0)), (window.get_width()/2-120, window.get_height()/2-40+gui_paused_menu.index(i)*50))
                window.blit(font_small.render('<', False, (0, 255, 0)), (window.get_width()/2+100, window.get_height()/2-40+gui_paused_menu.index(i)*50))

        window.blit(font_small.render(version_ if type_ == 'vannila' else type_ + ' ' + version_, False, (255,255,255)), (window.get_width()-font_small.render(version_ if type_ == 'vannila' else type_ + ' ' + version_, False, (255,255,255)).get_width(), window.get_height()-font_small.get_height()))
        
        pygame.display.flip()
        clock.tick(60)
        #
    elif face_select:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    if player_face.face < 21:
                        player_face.face += 1
                    else:
                        player_face.face = 1
                    select.play()
                elif event.key == pygame.K_a:
                    if player_face.face > 1:
                        player_face.face -= 1
                    else:
                        player_face.face = 21
                    select.play()
                if event.key == pygame.K_RIGHT:
                    if player2_face.face < 21:
                        player2_face.face += 1
                    else:
                        player2_face.face = 1
                    select.play()
                elif event.key == pygame.K_LEFT:
                    if player2_face.face > 1:
                        player2_face.face -= 1
                    else:
                        player2_face.face = 21
                    select.play()
                if event.key == pygame.K_w:
                    if sel_c < 7:
                        sel_c += 1
                    else:
                        sel_c = 0
                    select.play()
                elif event.key == pygame.K_s:
                    if sel_c > 0:
                        sel_c -= 1
                    else:
                        sel_c = 7
                    select.play()
                if event.key == pygame.K_UP:
                    if sel_c2 < 7:
                        sel_c2 += 1
                    else:
                        sel_c2 = 0
                    select.play()
                elif event.key == pygame.K_DOWN:
                    if sel_c2 > 0:
                        sel_c2 -= 1
                    else:
                        sel_c2 = 7
                    select.play()
                elif event.key == pygame.K_LSHIFT:
                    ready[0] = True if not ready[0] else False
                    click.play()
                elif event.key == pygame.K_RSHIFT:
                    ready[1] = True if not ready[1] else False
                    click.play()

        
        window.fill((0,0,0))
        window.blit(font_small.render('select character', False, (255,255,255)), (window.get_width()/4-font_small.render('select character', False, (255,255,255)).get_width()/2, 30))
        window.blit(font_small.render('select character', False, (255,255,255)), ((window.get_width()/2+window.get_width()/4)-font_small.render('select character', False, (255,255,255)).get_width()/2, 30))
        pygame.draw.rect(window,player.color,(window.get_width()/4-90,window.get_height()/2-90,180,180))
        window.blit(pygame.transform.scale(pygame.image.load(f'data/textures/face-{player_face.face}.png'),(180,180)),(window.get_width()/4-90,window.get_height()/2-90))
        pygame.draw.rect(window,player2.color,((window.get_width()/2+window.get_width()/4)-90,window.get_height()/2-90,180,180))
        window.blit(pygame.transform.scale(pygame.image.load(f'data/textures/face-{player2_face.face}.png'),(180,180)),((window.get_width()/2+window.get_width()/4)-90,window.get_height()/2-90))

        if ready[0]:
            pygame.draw.rect(window,(0,0,0),(0,0,window.get_width()/2,window.get_height()))
            window.blit(font_small.render('ready', False, player.color), (window.get_width()/4-font_small.render('ready', False, (255,255,255)).get_width()/2, 30))
        if ready[1]:
            pygame.draw.rect(window,(0,0,0),(window.get_width()/2,0,window.get_width()/2,window.get_height()))
            window.blit(font_small.render('ready', False, player2.color), ((window.get_width()/2+window.get_width()/4)-font_small.render('ready', False, (255,255,255)).get_width()/2, 30))
        if ready[0] and ready[1]:
            ready = [False,False]
            face_select = False
        
        pygame.draw.line(window, (255, 255, 255), (window.get_width()/2, 0), (window.get_width()/2, 99999), 3)
        
        pygame.display.flip()
        clock.tick(60)
        
    else:
        if sec > 60:
            sec = 0
            min_ += 1
        else:
            sec += 1/max(clock.get_fps(),0.00000001)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and player.on_floor:
                    player.velocity.y = -jump_force
                    player.face_offset.y = player.velocity.y
                    jump.play()
                elif event.key == pygame.K_w and player.on_wall:
                    player.velocity.y = -jump_force - 2
                    player.face_offset.y = player.velocity.y
                    player.face_offset.x *= -1
                    player.velocity.x *= -1
                    explosion.play()
                elif event.key == pygame.K_w and player.doubleJump and double_jump:
                    player.velocity.y = -jump_force + 1
                    player.face_offset.y = player.velocity.y
                    jump.play()
                    player.doubleJump = False
                if event.key == pygame.K_d:
                    player.velocity.x = speed
                    player.face_offset.x = 5
                elif event.key == pygame.K_a:
                    player.velocity.x = -speed
                    player.face_offset.x = -5
                elif event.key == pygame.K_s and player.bullet_delay == 0:
                    projectiles.append(Projectile(player, player2))
                    player.bullet_delay = 30
                    laser.play()
                if event.key == pygame.K_UP and player2.on_floor:
                    player2.velocity.y = -jump_force
                    player2.face_offset.y = player2.velocity.y
                    jump.play()
                elif event.key == pygame.K_UP and player2.on_wall:
                    player2.velocity.y = -jump_force - 2
                    player2.face_offset.y = player2.velocity.y
                    player2.face_offset.x *= -1
                    player2.velocity.x *= -1
                    explosion.play()
                elif event.key == pygame.K_UP and player2.doubleJump and double_jump:
                    player2.velocity.y = -jump_force + 1
                    player2.face_offset.y = player2.velocity.y
                    jump.play()
                    player2.doubleJump = False
                if event.key == pygame.K_RIGHT:
                    player2.velocity.x = speed
                    player2.face_offset.x = 5
                elif event.key == pygame.K_LEFT:
                    player2.velocity.x = -speed
                    player2.face_offset.x = -5
                elif event.key == pygame.K_DOWN and player2.bullet_delay == 0:
                    projectiles.append(Projectile(player2, player))
                    player2.bullet_delay = 30
                    laser.play()
                elif event.key == pygame.K_ESCAPE:
                    player.velocity.x, player2.velocity.x = 0,0
                    click.play()
                    paused = True
                    
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_d, pygame.K_a]:
                    player.velocity.x = 0
                    player.face_offset.x = 0
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    player2.velocity.x = 0
                    player2.face_offset.x = 0

        window.fill((0,0,0))
        
        player.draw(window)
        player_face.draw()
        player.update(player2)
        player2.draw(window)
        player2_face.draw()
        player2.update(player)

        for i in projectiles:
            i.draw(window)
            i.update()

        pygame.draw.line(window, (255, 255, 255), (window.get_width()/2, 0), (window.get_width()/2, ground_level), 3)
        pygame.draw.line(window, (255, 255, 255), (0, ground_level), (99999, ground_level), 3)

        window.blit(font.render(str(player.health), False, player.color if player.color != (0,0,0) else (255,255,255)), (window.get_width()/2-80, 100))
        window.blit(font.render(str(player2.health), False, player2.color if player2.color != (0,0,0) else (255,255,255)), (window.get_width()/2+20, 100))

        window.blit(font_small.render(str(str(int(min_)) if len(str(int(min_))) == 2 else '0' + str(int(min_)))+':'+str(str(int(sec)) if len(str(int(sec))) == 2 else '0' + str(int(sec))), False, (255,255,255)), (window.get_width()-font_small.render(str(str(int(min_)) if len(str(int(min_))) == 2 else '0' + str(int(min_)))+':'+str(str(int(sec)) if len(str(int(sec))) == 2 else '0' + str(int(sec))), False, (255,255,255)).get_width(), 0))
        window.blit(font_small.render('fps: ' + str(int(clock.get_fps())), False, (255,255,255) if clock.get_fps() > 30 else (255,0,0)), (0, 0))

        pygame.display.flip()
        clock.tick(60)
        
