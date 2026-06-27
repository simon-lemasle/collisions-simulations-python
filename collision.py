import pygame
import math

pygame.init()

## SCREEN 
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Collision simulations")

dt = 1/60
g = 800



class Objects:
    def __init__(self,x,y,vx,vy,mass=1,radius=50,color=(255,255,255),elasticity=0.8):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.radius = radius
        self.color = color
        self.elasticity = elasticity


        self.ay = g

    def distance(self,other):
        return math.sqrt((self.x - other.x)**2+(self.y - other.y)**2)

    def draw(self):
        pygame.draw.circle(SCREEN,self.color,(self.x,self.y),self.radius)

    def orientation(self,theta):
        self.ax = math.cos(theta) * g
        self.ay = math.sin(theta) * g

    def collision(self,other):

        ## Impulse of the collision
        v_rel = [self.vx - other.vx,self.vy - other.vy]
        if math.sqrt((self.x - other.x)**2 + (self.y - other.y )**2) < 0.00001:
            return
        n = [(self.x - other.x)/math.sqrt((self.x - other.x)**2 + (self.y - other.y )**2),(self.y - other.y)/math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)]

        v_rel_dot_n = v_rel[0]*n[0]+v_rel[1]*n[1]

        J = -(1 + min(self.elasticity,other.elasticity) ) * v_rel_dot_n / ( (1 / self.mass)+(1 / other.mass) )


        
        self.vx += J * n[0] / self.mass
        self.vy += J * n[1] / self.mass
        other.vx -= J * n[0] / other.mass
        other.vy -= J * n[1] / other.mass


    def update_position(self,objects):
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        self.x += self.vx * dt
        self.y += self.vy * dt
        
        ## ## collisions with other objects
        for obj in objects:
             if obj != self:
                  distance = self.distance(obj)
                  legal_distance = obj.radius + self.radius
                  if distance < legal_distance:
                        penetration = legal_distance - distance
                        if distance > 0.00001 :
                            A = self.x,self.y
                            B = obj.x , obj.y
                            self.collision(obj)
                            self.x += (A[0] - B[0]) * penetration / (distance * 2)
                            obj.x -= (A[0] - B[0]) * penetration / (distance * 2)
                            self.y += (A[1] - B[1]) * penetration / (distance * 2)
                            obj.y -= (A[1] - B[1]) * penetration / (distance * 2)

                        


        ## collisions with edges of the screen
        if self.x + self.radius > WIDTH:
                self.x = WIDTH - self.radius
                self.vx *= -self.elasticity
        if self.x - self.radius < 0:
                self.x = self.radius
                self.vx *= -self.elasticity
        if self.y - self.radius < 0:
                self.y = self.radius
                self.vy *= -self.elasticity
        if self.y + self.radius > HEIGHT:
                self.y = HEIGHT - self.radius
                self.vy *= -self.elasticity


def main():
    clock = pygame.time.Clock()

    b1 = Objects(600,400,1200,1200)
    b2 = Objects(200,600,-1200,1200)


    objects = [b1,b2]

    orientation = math.pi / 2
    
    dragging = None

    running = True
    while running:
        clock.tick(60)
        SCREEN.fill((0,0,0))

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in objects:
                    if math.sqrt((obj.x - mouse_pos[0])**2+(obj.y - mouse_pos[1])**2) < obj.radius:
                        dragging = obj
                        obj.vx , obj.vy = 0 , 0

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for i in range (5):
                        objects.append(Objects(mouse_pos[0],mouse_pos[1],0,0 ))
                        print(len(objects))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    orientation -= math.pi / 45
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    orientation += math.pi / 45

        for obj in objects:
            if dragging == obj:
                obj.vx = (mouse_pos[0] - obj.x)/dt
                obj.vy = (mouse_pos[1] - obj.y)/dt
                obj.x,obj.y = mouse_pos
            else:
                obj.orientation(orientation)
                obj.update_position(objects)
            obj.draw()

        pygame.display.update()
        


main()
pygame.quit()