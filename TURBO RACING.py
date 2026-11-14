
import pygame, random, math

pygame.init()

W,H=700,750
screen=pygame.display.set_mode((W,H))
pygame.display.set_caption("TURBO RACING PRO")
clock=pygame.time.Clock()

font=pygame.font.SysFont("Arial",24,bold=True)
big=pygame.font.SysFont("Arial",55,bold=True)
title_font=pygame.font.SysFont("Arial",65,bold=True)

WHITE=(255,255,255)
GREEN=(25,110,45)
ROAD=(43,45,52)
GOLD=(255,195,0)

game_state="menu"
menu_time=0
fade=255
countdown=0
count_time=0
shake=0
nitro=100
speed_lines=[]
particles=[]
popups=[]
tyre_marks=[]
rain=[]
for i in range(100):
    rain.append([random.randrange(W),random.randrange(H),
                 random.randint(5,13)])

def draw_car(s,x,y,color,angle=0):
    car=pygame.Surface((70,110),pygame.SRCALPHA)
    pygame.draw.ellipse(car,(0,0,0,100),(5,9,62,98))

    for tx in [1,56]:
        for ty in [22,72]:
            pygame.draw.rect(car,(12,12,16),
                (tx,ty,13,24),border_radius=5)

    pygame.draw.polygon(car,color,[
        (35,2),(49,12),(61,32),(65,82),
        (54,105),(16,105),(5,82),(9,32),(21,12)])

    pygame.draw.polygon(car,(255,255,255,65),[
        (35,7),(43,17),(35,25),(27,17)])

    pygame.draw.polygon(car,(25,55,80),[
        (17,29),(53,29),(56,48),(14,48)])

    pygame.draw.polygon(car,(20,40,60),[
        (15,77),(55,77),(49,92),(21,92)])

    pygame.draw.polygon(car,color,[
        (15,49),(55,49),(53,74),(17,74)])

    pygame.draw.rect(car,(255,255,160),(9,5,13,7),
                     border_radius=3)
    pygame.draw.rect(car,(255,255,160),(48,5,13,7),
                     border_radius=3)

    pygame.draw.rect(car,(255,0,0),(9,98,13,6))
    pygame.draw.rect(car,(255,0,0),(48,98,13,6))

    rotated=pygame.transform.rotate(car,angle)
    s.blit(rotated,rotated.get_rect(center=(int(x),int(y))))

def draw_coin(s,x,y,t):
    width=max(3,int(13*abs(math.cos(t))))
    pygame.draw.ellipse(s,(120,75,0),
                        (x-width,y-13,width*2,26))
    pygame.draw.ellipse(s,GOLD,
                        (x-width+2,y-11,max(2,width*2-4),22))
    pygame.draw.circle(s,(255,245,130),(x,y),5)

    if math.sin(t*2)>0.65:
        pygame.draw.circle(s,WHITE,(x-5,y-7),3)

def draw_menu():
    screen.fill((10,17,34))
    pygame.draw.rect(screen,(42,43,51),(175,0,350,H))

    for y in range(0,H,110):
        pygame.draw.rect(screen,WHITE,(345,y,8,60))

    for y in range(50,H,150):
        for x in [90,610]:
            pygame.draw.circle(screen,(20,85,35),(x,y),30)
            pygame.draw.circle(screen,(35,150,55),(x,y),22)

    draw_car(screen,280,390,(230,25,35),-12)
    draw_car(screen,420,390,(30,100,255),12)

    title=title_font.render("TURBO",True,GOLD)
    title2=title_font.render("RACING",True,WHITE)
    screen.blit(title,title.get_rect(center=(350,120)))
    screen.blit(title2,title2.get_rect(center=(350,185)))

    subtitle=font.render("THE ULTIMATE RACING GAME",True,(180,200,220))
    screen.blit(subtitle,subtitle.get_rect(center=(350,250)))

    pulse=abs(math.sin(menu_time*0.07))
    button=pygame.Rect(190,510,320,75)
    shade=(180+int(pulse*60),20,30)

    pygame.draw.rect(screen,(255,190,40),
                     button.inflate(12,12),border_radius=20)
    pygame.draw.rect(screen,shade,button,border_radius=15)

    label=big.render("START RACE",True,WHITE)
    screen.blit(label,label.get_rect(center=button.center))

    hint=font.render("CLICK TO START",True,GOLD)
    screen.blit(hint,hint.get_rect(center=(350,630)))

def reset_game():
    global px,py,score,road_scroll,game_over
    global enemies,coin_list,particles,popups
    global tyre_marks,nitro,shake,fade,countdown,count_time

    px,py=350,590
    score=0
    road_scroll=0
    game_over=False
    nitro=100
    shake=0
    fade=255
    countdown=3
    count_time=0
    particles=[]
    popups=[]
    tyre_marks=[]

    enemies=[
        [random.randint(240,460),-i*180,
         random.choice(colors),random.uniform(3,5)]
        for i in range(5)
    ]

    coin_list=[
        [random.randint(220,480),-i*130-100,
         random.random()*6.28]
        for i in range(8)
    ]

colors=[
    (30,100,255),(255,190,20),(20,220,130),
    (180,50,220),(240,240,240)
]

reset_game()
running=True
game_started=False

# Rain
for i in range(100):
    rain[i][0]=random.randrange(W)
    rain[i][1]=random.randrange(H)

while running:
    dt=min(clock.tick(60)/16.67,2)
    menu_time+=dt

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.MOUSEBUTTONDOWN:
            if game_state=="menu":
                if pygame.Rect(190,510,320,75).collidepoint(event.pos):
                    reset_game()
                    game_state="playing"

        if event.type==pygame.KEYDOWN:
            if game_state=="gameover":
                if event.key==pygame.K_r:
                    reset_game()
                    game_state="playing"
                if event.key==pygame.K_ESCAPE:
                    game_state="menu"

            elif game_state=="playing":
                if event.key==pygame.K_ESCAPE:
                    game_state="menu"

    if game_state=="menu":
        draw_menu()
        pygame.display.flip()
        continue

    keys=pygame.key.get_pressed()
    moving=game_state=="playing" and countdown<=0 and not game_over

    if game_state=="playing" and not game_over:

        # Countdown
        if countdown>0:
            count_time+=dt
            if count_time>=60:
                countdown-=1
                count_time=0

        if moving:
            old_px,old_py=px,py
            player_angle=0
            drifting=keys[pygame.K_SPACE]

            # Movement
            if keys[pygame.K_LEFT]:
                px-=5*dt
                player_angle=12
            if keys[pygame.K_RIGHT]:
                px+=5*dt
                player_angle=-12
            if keys[pygame.K_UP]:
                py-=5*dt
            if keys[pygame.K_DOWN]:
                py+=5*dt

            px=max(175,min(525,px))
            py=max(80,min(680,py))

            # Nitro
            boosting=keys[pygame.K_LSHIFT] and nitro>0

            if boosting:
                nitro=max(0,nitro-0.8*dt)
            else:
                nitro=min(100,nitro+0.18*dt)

            road_speed=11 if boosting else 7
            road_scroll=(road_scroll+road_speed*dt)%100

            # Nitro flames
            if boosting:
                for i in range(3):
                    particles.append([
                        px+random.randint(-12,12),
                        py+65,
                        random.uniform(-1,1),
                        random.uniform(2,6),
                        random.randint(10,20),
                        random.choice([(30,140,255),(50,220,255),GOLD])
                    ])

                if random.random()<0.3:
                    speed_lines.append([
                        random.randrange(170,530),
                        random.randrange(H),random.randint(20,50)
                    ])

            # Drift smoke and tyre marks
            if drifting and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
                for i in range(2):
                    particles.append([
                        px+random.randint(-25,25),
                        py+random.randint(15,35),
                        random.uniform(-1,1),
                        random.uniform(-2,1),
                        random.randint(15,28),
                        (170,170,170)
                    ])

                if len(tyre_marks)<35:
                    tyre_marks.append([px-17,py+25,40])
                    tyre_marks.append([px+17,py+25,40])

            # Enemy movement
            for e in enemies:
                e[1]+=(e[3]+2+(4 if boosting else 0))*dt

                if e[1]>H+100:
                    e[1]=-120
                    e[0]=random.randint(240,460)
                    score+=10

                if abs(px-e[0])<43 and abs(py-e[1])<65:
                    game_over=True
                    game_state="gameover"
                    shake=20

                    for i in range(35):
                        particles.append([
                            px,py,random.uniform(-6,6),
                            random.uniform(-6,6),random.randint(15,35),
                            random.choice([GOLD,(255,70,20),WHITE])
                        ])

            # Coins
            for c in coin_list:
                c[1]+=road_speed*dt
                c[2]+=0.12*dt

                if c[1]>H+30:
                    c[1]=-random.randint(100,500)
                    c[0]=random.randint(220,480)

                if math.hypot(px-c[0],py-c[1])<42:
                    score+=10
                    popups.append([px,py-30,35])
                    c[1]=-random.randint(100,400)
                    c[0]=random.randint(220,480)

                    for j in range(12):
                        particles.append([
                            px,py,random.uniform(-4,4),
                            random.uniform(-4,4),20,GOLD
                        ])

            # Rain splashes
            for r in rain:
                r[1]+=14*dt
                r[0]-=2*dt
                if r[1]>H:
                    r[0]=random.randrange(W)
                    r[1]=0

        # Particle update
    for p in particles[:]:
        p[0]+=p[2]*dt
        p[1]+=p[3]*dt
        p[4]-=dt
        if p[4]<=0:
            particles.remove(p)

    for m in tyre_marks[:]:
        m[2]-=dt
        if m[2]<=0:
            tyre_marks.remove(m)

    for p in popups[:]:
        p[1]-=1.2*dt
        p[2]-=dt
        if p[2]<=0:
            popups.remove(p)

    for line in speed_lines[:]:
        line[1]+=line[2]*dt
        if line[1]>H:
            speed_lines.remove(line)

    # Camera shake
    ox=oy=0
    if shake>0:
        ox=random.randint(-int(shake),int(shake))
        oy=random.randint(-int(shake),int(shake))
        shake=max(0,shake-0.7*dt)

    # Draw world
    screen.fill(GREEN)

    for y in range(-30,H,100):
        yy=(y+road_scroll*0.5)%(H+100)-50
        for x in [45,650]:
            pygame.draw.circle(screen,(15,80,30),(x,yy),27)
            pygame.draw.circle(screen,(35,150,55),(x,yy),20)

    pygame.draw.rect(screen,ROAD,(150,0,400,H))

    # Kerbs
    for y in range(-50,H,60):
        yy=(y+road_scroll)%60
        for x in [150,540]:
            pygame.draw.rect(screen,(230,40,40),(x,yy,10,30))
            pygame.draw.rect(screen,WHITE,(x,yy+30,10,30))

    # Lane markings
    for y in range(-100,H,150):
        yy=y+road_scroll
        pygame.draw.rect(screen,WHITE,(280,yy,6,75))
        pygame.draw.rect(screen,WHITE,(420,yy,6,75))

    # Tyre marks
    for m in tyre_marks:
        pygame.draw.circle(screen,(25,25,28),
                           (int(m[0]+ox),int(m[1]+oy)),3)

    # Speed lines
    for line in speed_lines:
        pygame.draw.line(screen,(180,210,255),
                         (line[0],line[1]),
                         (line[0],line[1]+line[2]),2)

    # Coins
    for c in coin_list:
        draw_coin(screen,int(c[0]+ox),int(c[1]+oy),c[2])

    # Enemies
    for e in enemies:
        draw_car(screen,e[0]+ox,e[1]+oy,e[2])

    # Player car
    if game_state!="menu":
        angle=0
        if moving and keys[pygame.K_LEFT]:
            angle=12
        if moving and keys[pygame.K_RIGHT]:
            angle=-12
        draw_car(screen,px+ox,py+oy,(230,25,35),angle)

    # Rain
    for r in rain:
        pygame.draw.line(screen,(155,195,220),
                         (int(r[0]),int(r[1])),
                         (int(r[0]-3),int(r[1]+r[2])),1)

    # Rain splashes near player
    if moving and random.random()<0.12:
        particles.append([
            px+random.randint(-35,35),py+35,
            random.uniform(-2,2),random.uniform(-3,1),
            10,(120,190,220)
        ])

    # Particles
    for p in particles:
        radius=max(1,int(p[4]/4))
        pygame.draw.circle(screen,p[5],
                           (int(p[0]+ox),int(p[1]+oy)),radius)

    # Popups
    for p in popups:
        label=font.render("+10",True,GOLD)
        label.set_alpha(max(0,min(255,int(p[2]*8))))
        screen.blit(label,(int(p[0]),int(p[1])))

    # HUD
    pygame.draw.rect(screen,(15,18,25),(10,10,230,110),
                     border_radius=12)

    screen.blit(font.render("SCORE: "+str(score),True,WHITE),(22,20))
    screen.blit(font.render("COINS: "+str(score),True,GOLD),(22,58))

    # Nitro meter
    pygame.draw.rect(screen,(15,18,25),(490,15,195,40),
                     border_radius=8)
    pygame.draw.rect(screen,(50,50,60),(502,28,165,12))
    pygame.draw.rect(screen,(20,150,255),
                     (502,28,int(165*nitro/100),12))
    screen.blit(font.render("NITRO",True,WHITE),(540,0))

    # Countdown overlay
    if countdown>0 and game_state=="playing":
        count_text="GO!" if countdown==0 else str(countdown)
        label=big.render(count_text,True,GOLD)
        screen.blit(label,label.get_rect(center=(350,350)))

    # Fade-in
    if fade>0 and game_state=="playing":
        cover=pygame.Surface((W,H))
        cover.fill((0,0,0))
        cover.set_alpha(int(fade))
        screen.blit(cover,(0,0))
        fade=max(0,fade-8*dt)

    # Game over
    if game_state=="gameover":
        overlay=pygame.Surface((W,H),pygame.SRCALPHA)
        overlay.fill((0,0,0,190))
        screen.blit(overlay,(0,0))

        msg=big.render("GAME OVER",True,(255,50,50))
        screen.blit(msg,msg.get_rect(center=(350,310)))

        t=font.render("COINS: "+str(score),True,GOLD)
        screen.blit(t,t.get_rect(center=(350,370)))

        t=font.render("PRESS R TO RESTART",True,WHITE)
        screen.blit(t,t.get_rect(center=(350,420)))

        t=font.render("ESC - MAIN MENU",True,WHITE)
        screen.blit(t,t.get_rect(center=(350,465)))

    pygame.display.flip()

pygame.quit()


