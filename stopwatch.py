# template for "Stopwatch: The Game"
import simplegui
# define global variables
last_digit=0
x=0
y=0
interval=100
#time in 10th seconds
time=0
#Boolean Variable
score=False
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D

def format(t):
    global last_digit
    temp="00000"+str(t)
    
    #finding the tenth of second here it is last digit
    tenth_seconds=temp[-1]
    
    # assigning value to last digit
    last_digit=int(tenth_seconds)
    #print last_digit
    #finding the remaing seconds values 
    # i.e from begining to previous of last digit
    remain_seconds=temp[0:-1]
    
    #Finding the actual seconds
    s=int(remain_seconds[0:])
    seconds=s%60
    
    #Finding the actual minutes
    minutes=(int(remain_seconds))/60
    
    #check if seconds is in single digit return this
    if(seconds<=9):
       return str(minutes) + ":" + "0"+str(seconds) + "." + tenth_seconds
 
    #if seconds is in double digit return this
    return str(minutes) + ":" + str(seconds) + "." + tenth_seconds

def attempt():
    return str(x)+"/"+str(y)
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global score
    score=True
    timer.start()
def stop():
    timer.stop()
    global x,y,last_digit,score
    if score:
        score=False
        if(last_digit==0):
            x=x+1
            y=y+1
        else:
            y=y+1
    else:
        score=False
        
def reset():
    timer.stop()
    global time,x,y,last_digit
    time=0
    x=0
    y=0
    last_digit=0
    
    

# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time=time+1
    
    
    

# define draw handler
def draw(canvas):
    canvas.draw_text(format(time),[140,170],60,"Blue")
    canvas.draw_text(attempt(),[300,70],30,"Green")
# create frame
frame=simplegui.create_frame("Stopwatch: The Game",400,300)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("Start",start,200)
frame.add_button("Stop",stop,200)
frame.add_button("Reset",reset,200)
timer=simplegui.create_timer(interval,tick)

# start frame
frame.start()

# Please remember to review the grading rubric
