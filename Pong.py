# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos=[0,0]
ball_vel=[0,0]
paddle1_pos=HEIGHT/2 
paddle2_pos=HEIGHT/2 
paddle1_vel=0 
paddle2_vel=0
score1=0
score2=0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left

def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos[0]=WIDTH/2
    ball_pos[1]=HEIGHT/2
    #spawning according to direction
    if direction:
       ball_vel[0]=random.randrange(2, 5)
       ball_vel[1]=-random.randrange(2, 5)
       
    else:
       ball_vel[0]=-random.randrange(2, 5)
       ball_vel[1]=-random.randrange(2, 5)
       
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_vel=0 
    paddle2_vel=0
    score1=0
    score2=0
    paddle1_pos=HEIGHT/2
    paddle2_pos=HEIGHT/2
    #randomisation for spawning the direction of ball
    
    spawn_ball(random.choice([LEFT,RIGHT]))
    
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos,paddle1_vel,paddle2_vel, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    #check collision and reflection
    
    
     # check if collides in left
    if  ball_pos[0]<=BALL_RADIUS+PAD_WIDTH:
        #reflect and increase speed by 10%
        if (ball_pos[1]>=(paddle1_pos-HALF_PAD_HEIGHT))and (ball_pos[1]<=(paddle1_pos+HALF_PAD_HEIGHT)):
            
            ball_vel[0]=ball_vel[0]+(ball_vel[0]/10.0)
            ball_vel[0]=-ball_vel[0]
            
        #increase score for player2 on miss
        else:
            score2+=1
            spawn_ball(RIGHT)
        
    # check if collides in right
    if  ball_pos[0]>=(WIDTH-1)-BALL_RADIUS-PAD_WIDTH:
        #reflect and increase speed by 10%
        if (ball_pos[1]>=(paddle2_pos-HALF_PAD_HEIGHT))and (ball_pos[1]<=(paddle2_pos+HALF_PAD_HEIGHT)):
            
            ball_vel[0]=ball_vel[0]+(ball_vel[0]/10.0)
            ball_vel[0]=-ball_vel[0]
            
        #increase score for player1 on miss
        else:
            score1+=1
            spawn_ball(LEFT)
        
    # check if collides in up
    if  ball_pos[1]<=BALL_RADIUS:
        ball_vel[1]=-ball_vel[1]
        
    # check if collides in down
    if  ball_pos[1]>=(HEIGHT-1)-BALL_RADIUS:
        ball_vel[1]=-ball_vel[1]
        
    
    
    
    # update ball
    ball_pos[0]+=ball_vel[0]
    ball_pos[1]+=ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,4,"Green","Yellow")
    
    #update padle
    paddle1_pos+=paddle1_vel
    paddle2_pos+=paddle2_vel
    
    # update paddle's vertical position, keep paddle on the screen
    
    #keep paddle1 on screen and update pos    
    if (paddle1_pos-HALF_PAD_HEIGHT)<0 : 
        paddle1_pos=HALF_PAD_HEIGHT
    if(paddle1_pos+HALF_PAD_HEIGHT)>(HEIGHT-1) :
        paddle1_pos=(HEIGHT-1)-HALF_PAD_HEIGHT
       
    #keep paddle2 on screen and update pos    
        
    if (paddle2_pos-HALF_PAD_HEIGHT)<0 :
        paddle2_pos=HALF_PAD_HEIGHT
    if(paddle2_pos+HALF_PAD_HEIGHT)>(HEIGHT-1) :
        paddle2_pos=(HEIGHT-1)-HALF_PAD_HEIGHT
        
    
    # draw paddles
    canvas.draw_polygon([[0,paddle1_pos-HALF_PAD_HEIGHT ], [PAD_WIDTH, paddle1_pos-HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos+HALF_PAD_HEIGHT], [0, paddle1_pos+HALF_PAD_HEIGHT]], 1, 'Green', 'Blue')
    canvas.draw_polygon([[WIDTH-1-PAD_WIDTH,paddle2_pos-HALF_PAD_HEIGHT ], [WIDTH-1, paddle2_pos-HALF_PAD_HEIGHT], [WIDTH-1, paddle2_pos+HALF_PAD_HEIGHT], [WIDTH-1-PAD_WIDTH, paddle2_pos+HALF_PAD_HEIGHT]], 1, 'Green', 'Blue')

    # draw scores
    canvas.draw_text(str(score1),[225,50],50,"Green")
    canvas.draw_text(str(score2),[350,50],50,"Green")
def keydown(key):
    global paddle1_vel, paddle2_vel
    step=5
    #check for up-W and down-S
    if "W"==chr(key):
        paddle1_vel=-step
    if "S"==chr(key):
        paddle1_vel=step
    #check for upArrow ASCII 38 and downArrow ASCII 40
  
    if 38==key:
        paddle2_vel=-step
    if 40==key:
        paddle2_vel=step
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    
      #check for up-W and down-S
    if "W"==chr(key):
        paddle1_vel=0
    if "S"==chr(key):
        paddle1_vel=0
    #check for upArrow ASCII 38 and downArrow ASCII 40
  
    if 38==key:
        paddle2_vel=0
    if 40==key:
        paddle2_vel=0
   

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart",new_game,80)

# start frame
new_game()
frame.start()
