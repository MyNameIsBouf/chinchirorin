# A simulation of the Chinese-Japanese dice game 'Chinchirorin'
# See /doc for explanation of rules and implementation
# Authored by il-dedischado (B.T. Coyne) November 2013, USA
import random

# Game variables
current_banker = 1 # Player 2 is default banker
stacks = [1500, 1500, 1500, 1500, 1500] # All players start with same cashmoney
solvent = [True, True, True, True, True] # Becomes false if the player busts
neutral_bet = 0 # Carry-over bet from banker push
current_round = 0 # Increments at the beginning of every round
#cheaters = [False, False, False, False, False] # Players which have 4-5-6 dice

# Rule variables - see /doc/rules
#instant_kills = 1 # Whether the game is being played with 'instant kills'
#2nd_bets = 0 # Whether the game will have a 2nd round of bets after bank rolls
#table_debts = 0 # Whether insolvent players get a line of credit
#call_out_cheaters = 0 # Players can call bullshit on cheating rolls w/ risks
#random_cheaters = 0 # Random NPC players will cheat
#pg13 = 0 # Game is played for valueless chips and not money, profanity free

# Round variables
current_player = -1 # Set to the banker and then moves clockwise around table
minimum_bet = 0 # Raised to the banker's bet during betting phase
table_bets = [0, 0, 0, 0, 0] # Bets placed by each player during betting phase
point_set = 0 # Point that must be beaten
highest_doubles = 0 # Value of the doubles for breaking ties
current_rerolls = 0 # How many rolls the current player has taken
current_dice = [0, 0, 0] # The current roll of the dice

random.seed()

# Rolls dice for a player
def do_roll():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice3 = random.randint(1, 6)
    print dice1
    print dice2
    print dice3
    current_dice = [dice1, dice2, dice3]
# Player wins from a dice roll

# Player instantly loses from a dice roll

# Player asked if they want to re-roll

# NPC decides if it wants to reroll
    
do_roll()
for x in (current_dice)
    print x