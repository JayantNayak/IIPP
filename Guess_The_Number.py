# Testing template for "Guess the number"

#############################

######################
# Student should add code for "Guess the number" here


# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console


import simplegui
import random
import math

#initialize global variables in the code
num_remain=7
num_secret=0
num_range=100
remain=0

#helper functions to initialise the game
def new_game():
    global num_range,num_secret,remain,num_remain
    remain=num_remain
    num_secret=random.choice(range(0, num_range))
    print "New game. Range is from 0 to ",num_range
    print "Number of remaining guesses is " , remain
    print" "
#define callback functons for control panel
def range100():
    global num_range,num_remain
    num_remain=7
    num_range=100
    new_game()
    
def range1000():
    global num_range,num_remain
    num_remain=10
    num_range=1000
    new_game()
    
    
def get_input(guess):
    my_guess=int(guess)
    global num_secret,num_remain,remain
    
    print" "
    print "Guess was ",my_guess
    
    remain=remain-1
  
    print "Number of remaining guesses is " , remain
        
    if (my_guess > num_secret)and(remain > 0):
        print"Lower!"
    if (my_guess < num_secret)and(remain > 0):
        print"Higher!"
    if (my_guess==num_secret)and(remain >= 0):
        print "Correct!"
        print  " "
        new_game()
    if(remain==0):
        print "You ran out of guesses.  The number was ",num_secret
        print  " "
        new_game()
       
        

    
#create window(S)
f=simplegui.create_frame("Guess the number",200,200)

#create control elements for window
f.add_button("Range is [0,100)",range100,200)
f.add_button("Range is [0,1000)",range1000,200)
f.add_input("Enter a  guess",get_input,200)


new_game()

# start handlers for created window and exit code

