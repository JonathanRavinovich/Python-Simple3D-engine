import pygame
import math
import threading
import time

pygame.init()

class Rect:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def left_border(self):
        return Line(self.x,self.y,  self.x,self.y+self.h)

    def right_border(self):
        return Line(self.x+self.w,self.y,  self.x+self.w,self.y+self.h)

    def top(self):
        return Line(self.x,self.y,   self.x+self.w,self.y)

    def bottom(self):
        return Line(self.x,self.y+self.h,    self.x+self.w,self.y+self.h)

class Line:
    def __init__(self,x,y,x1,y1):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1

screen = pygame.display.set_mode((768,576)) # 256x192 * 3
screen2 = pygame.display.set_mode((768,576)) # 256x192 * 3
player_angle = 0
px = 300
py = 200
p_ang_l = 0
p_ang_r = 0
ang_chg = 0
speed = 0
player_view_range = 120
z = []
map = True
running = True
hold = False
fov = math.pi/6
quality = 1

walls = []

def point_line_collison(x,y,rect):
    return (rect.x <= x <= rect.x+rect.w) and (rect.y <= y <= rect.y+rect.h)

def point_line_distance(x,y,m,c):
    return abs((m*x-y+n)/math.sqrt(m**2+1))

def upd():
    global px
    global py
    global player_angle

    while running:
        px += math.cos(player_angle)*speed
        py += math.sin(player_angle)*speed
        player_angle += ang_chg
        time.sleep(0.01)

upd_t = threading.Thread(target=upd)
upd_t.start()

while running==True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                speed = 1.5
            if event.key == pygame.K_s:
                speed = -1.5
            if event.key == pygame.K_a:
                pass
            if event.key == pygame.K_d:
                pass

            if event.key == pygame.K_LEFT:
                ang_chg = -math.pi/64
            if event.key == pygame.K_RIGHT:
                ang_chg = math.pi/64

            if event.key == pygame.K_m:
                if map:
                    map = False
                else:
                    map = True

            if event.key == pygame.K_o:
                quality+=0.1
            if event.key == pygame.K_i:
                if quality>0.1:
                    quality-=0.1

            if event.key == pygame.K_l:
                fov += math.pi/128
            if event.key == pygame.K_k:
                if fov>math.pi/128:
                    fov -= math.pi/128

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                speed = 0
            if event.key == pygame.K_s:
                speed = 0
            if event.key == pygame.K_a:
                pass
            if event.key == pygame.K_d:
                pass

            if event.key == pygame.K_LEFT:
                ang_chg = 0
            if event.key == pygame.K_RIGHT:
                ang_chg = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            walls.append(Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],20,20))

        


    screen.fill((0,0,0))

    if map:
        for rect in walls:
            pygame.draw.rect(screen,(255,255,255),pygame.Rect(rect.x,rect.y,rect.w,rect.h))

    p_ang_r = player_angle - fov
    p_ang_l = player_angle + fov

    if map:
        pygame.draw.line(screen,(255,255,255),(px,py),( math.cos(p_ang_l)*25+px, math.sin(p_ang_l)*25+py))
        pygame.draw.line(screen,(255,255,255),(px,py),( math.cos(p_ang_r)*25+px, math.sin(p_ang_r)*25+py))
    else:
        tmp_angle = p_ang_l
        curr_x,curr_y = (0,0)
        angle_step = (p_ang_l - p_ang_r)/128
        check = False
        collison = False
        z = 0

        for i in range(128):
            #pygame.draw.line(screen,(100,100,100),(px,py),(math.cos(tmp_angle)*player_view_range+px,math.sin(tmp_angle)*player_view_range+py))
            check = False
            z = 0
            r = 0.5


            while r<player_view_range:
                curr_x = math.cos(tmp_angle)*r+px
                curr_y = math.sin(tmp_angle)*r+py

                for rect in walls:

                    if point_line_collison(curr_x,curr_y,rect):
                        z = r
                        check = True
                        break

                if check:
                    break

                r+=quality

            #pygame.draw.rect(screen,(255,0,0),pygame.Rect(curr_x,curr_y,1,1),10)
            #pygame.draw.line(screen,(255,255,255),(px,py),(curr_x,curr_y))

            z = z*math.cos(player_angle-tmp_angle)

            if z!=0:
                color = (0,0,0)

                if (255-z*2) >= 0:
                    color = (255-z*2,255-z*2,255-z*2)

                pygame.draw.rect(screen,color,pygame.Rect((128-i)*6,z,6,576/2))
                pygame.draw.rect(screen,color,pygame.Rect((128-i)*6,576/2,6,576/2-z))

            tmp_angle-=angle_step


    pygame.display.update()

upd_t.join()
pygame.quit()
