# A simulation of the Chinese-Japanese dice game 'Chinchirorin'
# See /doc for explanations of rules and game mechanics
# Authored by il-dedischado (B.T. Coyne) November 2013, USA
import random
import time

# Game variables
active = 1                                          # If 1 primary program loop remains active
debug_msgs = 1                                      # Debug messages active
current_banker = 2                                  # Player 2 is default banker
stacks = [1500, 1500, 1500, 1500, 1500]             # All players start with same cashmoney
solvent = [True, True, True, True, True]            # Becomes false if the player busts
neutral_bet = 0                                     # Carry-over bet from banker push
current_round = 0                                   # Increments at the beginning of every round
#cheaters = [False, False, False, False, False]     # Players which have 4-5-6 dice
player_names = ["Player 1", "Player 2", "Player 3", # Names of current players
"Player 4", "Player 5"]

# Rule variables - see /doc/rules
#instant_kills = 1                                  # Whether the game is being played with 'instant kills'
#2nd_bets = 0                                       # Whether the game will have a 2nd round of bets after bank rolls
#table_debts = 0                                    # Whether insolvent players get a line of credit
#call_out_cheaters = 0                              # Players can call bullshit on cheating rolls w/ risks
#random_cheaters = 0                                # Random NPC players will cheat
#pg13 = 0                                           # Game is played for valueless chips and not money, profanity free

# Round variables
current_player = -1                                 # Set to the banker and then moves clockwise around table
minimum_bet = 0                                     # Raised to the banker's bet during betting phase
table_bets = [0, 0, 0, 0, 0]                        # Bets placed by each player during betting phase
point_set = 0                                       # Point that must be beaten
highest_doubles = 0                                 # Value of the doubles for breaking ties
current_rerolls = 0                                 # How many rolls the current player has taken
current_dice = [0, 0, 0]                            # The current roll of the dice

# Class declarations

# class Player:
# TODO: Refactor to use player classes

# Function declarations

def debug_msg(message):
    """Prints a debug message if we have debug messages turned on, and writes it to the debug log"""
    if (debug_msgs == 1):
        print "#DEBUG: %s" % message
    # Write to file
    
def do_roll(silent=0):
    """Rolls three dice and immediately reports their results."""
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice3 = random.randint(1, 6)
    if (silent == 0): # Roll silently without reporting the results of the roll.
        print dice1
        print dice2
        print dice3
    current_dice = [dice1, dice2, dice3]

def player_places_bet(restart=0):
    """Player is prompted to bet and places money on the table."""
    if (restart == 0):
        print "So what'll you bet, hotshot?"
    print "Enter your bet ($%d-$%d)" % (minimum_bet, stacks[0]) 
    bet = input(">")
    if (bet > stacks[0]):
        print "You don't have that much money."
        player_places_bet(1)
    elif (bet < minimum_bet):
        print "You must bet equal to or less than the banker."
        player_places_bet(1)
    else:
        stacks[0] = stacks[0] - bet
        table_bets[0] = table_bets[0] + bet
        print "You place a bet of $%d." % bet
    
def npc_places_bet(which):
    """NPC is prompted to bet and places money on the table.
    Provisional formula is:
    Random 1-200 roll on the multiplier table (see /doc)
    Random 1-5 roll on the multiplicand table
    """
    if (which != 0):
        # Determine random bet
        multiplier = random.randint(1, 200)
        multiplicand = random.randint(1, 5)
        sum = multiplier * multiplicand
        debug_msg(player_names[which] + " is placing a bet of $" + str(sum))
        # Make sure he has enough cash (makes him reconsider if cautious)
        if (stacks[which] < sum):
            sum = stacks[which]
            debug_msg("Bet was reduced to $"+str(sum)+ ": lack of funds")
        # Then we actually place the bet
        stacks[which] = stacks[which] - sum
        table_bets[which] = table_bets[which] + sum
        # Handle messaging
        print "%s has placed a bet of $%d" % (player_names[which], sum)
        if (which == current_banker):
            minimum_bet = sum
    else:
        npc_places_bet(current_player)

def betting_cycle():
    """Cycles through all players in the game, making them all place bets."""
    current_player = current_banker
    for x in range(0, 5):
        which = current_player
        current_player = current_player + 1
        if (current_player > 4):
            current_player = 0
        elif (current_player != 0):
            debug_msg(player_names[which] + " is betting.")
            npc_places_bet(which)
            time.sleep(2)
        elif (current_player == 0):
            debug_msg("Human player is betting.")
            player_places_bet()
        else:
            debug_msg("Broke out of betting_cycle() loop -- invalid player selected")
            break
    else:
        # Betting cycle is over
        print "All bets processed!"
    
def report_state():
    """Report the state of gameplay: point to beat, current round,
    amount of money each player has, amount of bet money on the table, et cetera. """
    if (point_set != 0):
        print "The point to beat is %d, with double %d." % (point_set, highest_doubles)
    print "It's round %d." % current_round
    print "%s has $%d, %s has $%d, %s has $%d, %s has $%d, %s has $%d." % (player_names[0], stacks[0], player_names[1], stacks[1], player_names[2], stacks[2], player_names[3], stacks[3], player_names[4], stacks[4])
    print "$%d belongs to %s, $%d to %s, $%d to %s, $%d to %s, $%d to %s, and $%d in neutral bets.\nThe total pot is $%d." % (table_bets[0], player_names[0], table_bets[1], player_names[1], table_bets[2], player_names[2], table_bets[3], player_names[3], table_bets[4], player_names[4], neutral_bet, table_bets[0]+table_bets[1]+table_bets[2]+table_bets[3]+table_bets[4]+neutral_bet)

def knockout_npc(which):
    """Knock an NPC out of the game when they lose."""
    if (solvent[which] is False):
        pass
    else:
        print "%s has gone bankrupt! -Loss Message Placeholder-" % player_names[which]
        solvent[which] = False
        stacks[which] = 0
        table_bets[which] = 0
        
def rotate_banker():
    """Rotate banker status clockwise around the table, skipping insolvent players"""
    global current_banker # Apparently not implicit in the function body
    debug_msg("It's the end of " + player_names[current_banker] + " turn as banker.")
    current_banker = current_banker + 1
    if (current_banker > 4):
        current_banker = 0
    if (solvent[current_banker] == False):
        debug_msg("Passing " + player_names[current_banker] + " as banker because he's insolvent")
        rotate_banker()
    else:
        print "%s is now the Banker." % player_names[current_banker]
       
def game_loop():
    global current_round
    current_round = current_round + 1
    current_player = current_banker
    betting_cycle()
    
# Primary program loop
# while (active == 1):    
game_loop()
report_state()