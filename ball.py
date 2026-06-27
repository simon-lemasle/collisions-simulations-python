import pygame, math

pygame.init()

screen_size = (1200,700)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Physics Simulation")

clock = pygame.time.Clock()

center = (screen_size[0]/2,screen_size[1]/2)


### creates a new particule
class particule:
    def __init__(self,x,y,vx=0,vy=0,radius=40):
        self.x , self.y = x , y
        self.vx , self.vy = vx , vy
        self.radius = radius

p1 = particule(center[0],center[1])
p2 = particule(100,100)
particules = [p1,p2]


elasticity = -0.7

#ring 
# ring_radius = 200
# ring_wall_width = 20


g = 800 #pixels/s^2


dragging_particule = None

def distance(A,B):
    return math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos() ### get mouse position


    dt = clock.tick(60)/1000      #### ∆t between frames

    for event in pygame.event.get():
        ## quit
        if event.type == pygame.QUIT:
            running = False

        ## drag the ball
        if event.type == pygame.MOUSEBUTTONDOWN:
            for p in particules:
                if distance(mouse_pos,(p.x,p.y)) < p.radius:
                    dragging_particule = p
                    p.vx,p.vy = 0,0

        ## drop the ball
        if event.type == pygame.MOUSEBUTTONUP:
            dragging_particule = None
        
        ## adds a particule
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                particules.append(particule(mouse_pos[0],mouse_pos[1]))
    
    screen.fill((0,0,0))

    for p in particules: ##### check every particules of the simulation

        if p == dragging_particule:  #### check if we are dragging a particule
            p.vx = (mouse_pos[0] - p.x)/dt
            p.vy = (mouse_pos[1] - p.y)/dt
            p.x,p.y = mouse_pos
            pygame.draw.circle(screen,(35, 236, 250),(p.x,p.y),p.radius)
            



        else: #### apply newtonian gravity
            p.vy += g*dt   ### gravity.     g is positive here because of the inversion of the y axis of the screen

            #update position
            p.x += p.vx*dt
            p.y += p.vy*dt

            ### collision
            if p.y + p.radius > screen_size[1]:
                p.y = screen_size[1] - p.radius
                p.vy *= elasticity
            if p.y - p.radius < 0:
                p.y = p.radius
                p.vy *= elasticity
            if p.x + p.radius > screen_size[0]:
                p.x = screen_size[0] - p.radius
                p.vx *= elasticity
            if p.x - p.radius < 0:
                p.x = p.radius
                p.vx *= elasticity

            ## collision between particules 
            for part in particules:
                if part != p:
                    if distance((p.x,p.y),(part.x,part.y)) < p.radius + part.radius:
                        p.x -= p.vx*dt
                        p.y -= p.vy*dt
                        part.x -= part.vx*dt
                        part.y -= part.vy*dt
                        p.vx *= elasticity
                        p.vy *= elasticity
                        part.vx *= elasticity
                        part.vy *= elasticity
                        
                        
            # if radius + ring_radius + ring_wall_width > distance((x,y),center) + radius >= ring_radius - ring_wall_width:
            #     x -= vx*dt
            #     y -= vy*dt
            #     vx *= elasticity
            #     vy *= elasticity
            

            # pygame.draw.circle(screen,(255,255,255),center,ring_radius,ring_wall_width) ### ring
            
            pygame.draw.circle(screen,(35, 236, 250),(p.x,p.y),p.radius)



    pygame.display.update()

pygame.quit()

