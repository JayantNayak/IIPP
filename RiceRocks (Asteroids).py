# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started=False
rock_count=0
rock_left=12

level_speed=0
print "speed"+str(level_speed)

time_lapsed=0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward=[0,0]
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust:
            ship_thrust_sound.play()
            canvas.draw_image(self.image,[self.image_center[0]+self.image_size[0],self.image_center[1]],self.image_size,self.pos,self.image_size,self.angle)
        else:
            ship_thrust_sound.rewind()
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
    def update(self):
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        self.angle+=self.angle_vel
        self.angle=self.angle#/6.283185# so that angle aways stays within 2pi
        
        #forward direction for ship
        self.forward=angle_to_vector(self.angle)
        self.forward[0]*=.15
        self.forward[1]*=.15
        #acceleration
        if self.thrust:
            self.vel[0]+=self.forward[0]
            self.vel[1]+=self.forward[1]
        #Friction
        self.vel[0]*=.985
        self.vel[1]*=.985      
            
        #to keep the ship inside frame    
        self.pos[0]%=WIDTH
        self.pos[1]%=HEIGHT

        
    def rotate(self,rot):#helps in rotating left or right
        self.angle_vel=rot
    
    def thruster(self,thrust):#ON & OFF thruster of ship
        self.thrust=thrust
    
    def shoot(self):
        #create a new missile
        missile = Sprite([2 * WIDTH/ 3, 2 * HEIGHT / 3], [0,0], 0, 0, missile_image, missile_info, missile_sound)
        #a_missile.__init__([0,0], [0,0], 0, 0, missile_image, missile_info,missile_sound)
        forward=angle_to_vector(self.angle)
        missile.pos[0]=self.pos[0]+self.radius*forward[0]
        missile.pos[1]=self.pos[1]+self.radius*forward[1]
     
        missile.vel[0]=self.vel[0]+40*self.forward[0]
        missile.vel[1]=self.vel[1]+40*self.forward[1]
        # add the missile to missile group
        missile_group.add(missile)

    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #animation 
        if self.animated :
            
            canvas.draw_image(self.image,[self.image_center[0]+self.age*self.image_size[0],self.image_center[1]],self.image_size,self.pos,self.image_size,self.angle)

        else:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
    
    def update(self):
        #for angular rotation
        self.angle+=self.angle_vel
        #for positon
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1] 
        #to keep sprite wrapped inside frame
        self.pos[0]%=WIDTH
        self.pos[1]%=HEIGHT
        
        #increment age and check lifespan
        self.age+=1
        if self.age<self.lifespan:
            return False
        return True
    def collide(self,other_obj):
            distance=dist(self.pos,other_obj.pos)
            if distance<=(self.radius+other_obj.radius):
                return True
           #default return false if doesn't collide
            return False
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started,lives,rock_count,score,time_lapsed,level_speed,rock_left
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True 
        lives=3
        rock_count=0
        score=0
        time_lapsed=0
        level_speed=0
        rock_left=12
        soundtrack.play()
           
def draw(canvas):
    global time,lives,score,started,rock_left
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    #remaing lives
    canvas.draw_text("Score",(WIDTH-100,40),30,"White")
    canvas.draw_text(str(score),(WIDTH-100,70),30,"White")
    canvas.draw_text("Lives",(40,40),30,"White")
    canvas.draw_text(str(lives),(40,70),30,"White")
    
    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group,canvas)
    process_sprite_group(missile_group,canvas)
    process_sprite_group(explosion_group,canvas)
    
    # update ship and sprites
    my_ship.update()
    
    #check for collision
    if group_collide(rock_group,my_ship):
        lives-=1
        rock_left-=1
    
    hits=group_group_collide(missile_group,rock_group)
    if hits>0:
        score+=hits
        rock_left-=1
    #if player loses all lives or rocks lefts is 0
    if (lives==0 and started) or (rock_left == 0): 
        started = False
        soundtrack.rewind()
        for rocks in set(rock_group):
           #deleting the rocks
            rock_group.remove(rocks)
            

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
            
# timer handler that spawns a rock    
def rock_spawner():

    global rock_group,rock_count,started,time_lapsed,level_speed
    time_lapsed+=1
    if (rock_count < 12) and started:
    
        a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0, 0], 0, 0.1, asteroid_image, asteroid_info)
        
           
        #random angular velocity
        a_rock.angle_vel=random.choice([1,-1])*(random.random()%.15)
        
        #random position within screen
        a_rock.pos[0]=random.randint(0, WIDTH)
        a_rock.pos[1]=random.randint(0, HEIGHT)
        #random velocity
        a_rock.vel[0]=random.choice([1,0,-1])*random.randint(0, 2)
        a_rock.vel[1]=random.choice([1,0,-1])*random.randint(0, 2)
        # check if rock is not spawned too close to the ship
        if dist(a_rock.pos,my_ship.pos)<2*(my_ship.radius+a_rock.radius):
            pass
        else:
            rock_group.add(a_rock)
            rock_count+=1 
            
    # increase difficulty by increasing speed level of rocks
    if ((time_lapsed % 15) ==0)and started:
        
        level_speed=2+(time_lapsed//15 )
        print " my speed is : "+str(level_speed)
        for a_rock in rock_group:
            a_rock.vel[0]=random.choice([1,0,-1])*random.randint(0,level_speed)
            a_rock.vel[1]=random.choice([1,0,-1])*random.randint(0,level_speed)            
            
            
        
        
#helper function to draw groups of sprites
def process_sprite_group(group,canvas):
    for sprite in set(group):
        sprite.draw(canvas)
        if  sprite.update():
            group.remove(sprite)
            
#helper function for group collision
def  group_collide(group,other_obj):
    for sprite in set(group):
        if sprite.collide(other_obj):
            a_explode = Sprite(sprite.pos, [0, 0], 0, 0, explosion_image, explosion_info,explosion_sound )
            explosion_group.add(a_explode)
            group.remove(sprite)
            
            
            return True
    return False
#helper function for group-group collision
def group_group_collide(group1,group2):
    hits=0
    for gr1_ele in set(group1):
        if group_collide(group2,gr1_ele):
            group1.remove(gr1_ele)
            hits+=1
    return hits
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

#adding labels
label1 = frame.add_label('----GAME CONTROLS----')
label2 = frame.add_label("    Shoot:   SpaceBar")
label3 = frame.add_label("    Control: Arrow Keys")


# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group=set([])
missile_group=set([])
explosion_group=set([])

# Handler for key
def key_down(key):
    if key==simplegui.KEY_MAP["right"]:
        my_ship.rotate(.1)
        
    elif key==simplegui.KEY_MAP["left"]:
        my_ship.rotate(-.1)
        
    elif key==simplegui.KEY_MAP["up"]:
         my_ship.thruster(True)
    elif key==simplegui.KEY_MAP["down"]:
         my_ship.thruster(False)
            
    elif key==simplegui.KEY_MAP["space"]:
        
        my_ship.shoot()
        
def key_up(key):
    if key==simplegui.KEY_MAP["right"]:
        my_ship.rotate(0)
        
    elif key==simplegui.KEY_MAP["left"]:
        my_ship.rotate(0)
        
    elif key==simplegui.KEY_MAP["up"]:
         my_ship.thruster(False)
    

    
    
        
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
