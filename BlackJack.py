# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
               

        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card=[]
        
        pass	# create Hand object
        

    def __str__(self):
        s=""
        for c in self.card:
            s+=str(c)+" "
        return "Hand contains "+s
        pass	# return a string representation of a hand

    def add_card(self, card):
        self.card.append(card)
        
        pass	# add a card object to a hand

    def get_value(self):
        flag_aces=False
        hand_value=0
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        for mycard in self.card:
            hand_value+=int(VALUES[mycard.rank]) 
            if mycard.rank=='A':
                flag_aces=True
        if not flag_aces:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
            
        
        #print hand_value
        pass	# compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards
        step=0
        for hcard in self.card:
            hcard.draw(canvas,[pos[0]+step,pos[1]])
            step+=100
            
         
# define deck class 
class Deck:
    def __init__(self):
        self.card=[]
        for suit in SUITS:
            for rank in RANKS:
                self.card.append(Card(suit, rank))
        
        pass	# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.card)

    def deal_card(self):
        # deal a card object from the deck
        return self.card.pop()
    
    def __str__(self):
        s=""
        for card in self.card:
            s+=str(card) + " "
            
        return "Deck contains : "+s	# return a string representing the deck




#define event handlers for buttons
def deal():
    global outcome, in_play,my_deck,dealer_hand,player_hand,score
    
    # your code goes here
    my_deck=Deck()
    dealer_hand=Hand()
    player_hand=Hand()
    #shuffling deck
    print my_deck
    my_deck.shuffle()
    print my_deck
    
    #passing cards to player_hand then dealer_hand and alternate
    player_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    
    player_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    
    print "Player's cards :"+str(player_hand)
    print "Dealer's cards :"+str(dealer_hand)
    
    print "cards in deck : "
    print my_deck
    print "card "+str(player_hand)+" Player Score : "+ str(player_hand.get_value())
    print "card "+str(dealer_hand)+"Dealer Score : "+str(dealer_hand.get_value())

    outcome=""
    #Code for if player leaves in middle of round
    if in_play:
        score-=1
        outcome="You lost the round"
    else:
        in_play=True

def hit():
    global in_play,outcome,score
    # replace with your code below
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
    
    if in_play:
        player_hand.add_card(my_deck.deal_card())
        
        print "card "+str(player_hand)+" Player Score : "+ str(player_hand.get_value())
    
    if not in_play and player_hand.get_value()>21:
        outcome="You are already bust"
        
    if  in_play and (player_hand.get_value()>21):
        in_play=False
        outcome="You went bust and loose"
        score-=1
        print "player "+str(player_hand.get_value())+outcome
   
    
    print outcome
    
    
       
def stand():
    global in_play,outcome,score
    pass	# replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score
    
    if  (player_hand.get_value()>21):#check if player is bust
        outcome="You are already bust"
        
    while in_play and (dealer_hand.get_value()<17):
        dealer_hand.add_card(my_deck.deal_card())
        
    print "card "+str(dealer_hand)+"Dealer Score : "+str(dealer_hand.get_value())
    
    if in_play and player_hand.get_value()<=dealer_hand.get_value()and(dealer_hand.get_value()<=21):
        outcome=" You Lose !!"
        score-=1
        in_play=False
    elif in_play and (player_hand.get_value()<=21):
        outcome="You Win !!"
        score+=1
        in_play=False
        
        
    print outcome
# draw handler    
def draw(canvas):
    global dealer_hand,player_hand,outcome,in_play
    # test to make sure that card.draw works, replace with your code below
    
    dealer_hand.draw(canvas, [50,200])
    player_hand.draw(canvas,[50,425])
    canvas.draw_text(outcome, (250, 150), 30, 'White')
    canvas.draw_text("Blackjack", (190, 100), 40, 'LightBlue')
    canvas.draw_text("Score : "+str(score), (450, 75), 30, 'Red')
    canvas.draw_text("Dealer", (50, 150), 30, 'Black')
    canvas.draw_text("Player", (50, 400), 30, 'Black')
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER , CARD_BACK_SIZE, [86,250], CARD_BACK_SIZE)
        canvas.draw_text("Hit or stand ?", (250, 350), 30, 'yellow')
        
    else:
        canvas.draw_text("New deal ?", (250, 350), 30, 'yellow')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric