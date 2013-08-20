# All the imports necessary to run this game:
import random
import os

#Global variables used in our program
cards = [(1,'2C'),(2,'3C'),(3,'4C'),(4,'5C'),(5,'6C'),(6,'7C'),(7,'8C'),
		 (8,'9C'),(9,'TC'),(10,'JC'),(11,'QC'),(12,'KC'),(13,'AC'),
		 (14,'2D'),(15,'3D'),(16,'4D'),(17,'5D'),(18,'6D'),(19,'7D'),(20,'8D'),
		 (21,'9D'),(22,'TD'),(23,'JD'),(24,'QD'),(25,'KD'),(26,'AD'),
		 (27,'2S'),(28,'3S'),(29,'4S'),(30,'5S'),(31,'6S'),(32,'7S'),(33,'8S'),
		 (34,'9S'),(35,'TS'),(36,'JS'),(37,'QS'),(38,'KS'),(39,'AS'),
		 (40,'2H'),(41,'3H'),(42,'4H'),(43,'5H'),(44,'6H'),(45,'7H'),(46,'8H'),
		 (47,'9H'),(48,'TH'),(49,'JH'),(50,'QH'),(51,'KH'),(52,'AH')]
gameplay = True
user = []
alpha = []
bravo = []
charlie = []


# Run the game
def run_game():
	user_sorted = []
	alpha_sorted = []
	bravo_sorted = []
	charlie_sorted = []
	decision = ["NA","NA","NA","NA"]
	score = [0,0,0,0,0]
	#[highest score, user score, alpha score, bravo score, charlie score]
	
	round = 1
	round_h = 1
	
	while score[0] < 100:
		alpha_decision = "NA"
		bravo_decision = "NA"
		charlie_decision = "NA"
		totem = "N"
		(user_sorted, alpha_sorted, bravo_sorted, charlie_sorted) = deck_distribute()
		# Here is the decision making loop of the game,
		# totem holder always goes first, go in clockwise fashion (U->A->B->C),
		# Keep going till 13 cards are exhausted,
		# check to make sure user can't break laws
		# run AI script when necessary, always print screen before user input
		first_play = "2C"
		first_hand = True
		hearts_broken = False
		queen_played = False
		# Run the 3 card swap phase
		(user_sorted,alpha_sorted,bravo_sorted,charlie_sorted) = swap_three(user_sorted,alpha_sorted,bravo_sorted,charlie_sorted,round_h)
		# Resort players cards
		(user_sorted,alpha_sorted,bravo_sorted,charlie_sorted) = resorting(user_sorted,alpha_sorted,bravo_sorted,charlie_sorted)
		totem = check_two(user_sorted,alpha_sorted,bravo_sorted,charlie_sorted)
		while len(user_sorted) != 0:
			for j in range(0,4):
				# NOTE: after matching with an if or elif it returns (reason for loop consistency)
				if totem == "U":
					while True:
						try:
							user_decision = "NA"
							print_screen(round,decision,score,user_sorted,first_play,hearts_broken,first_hand)
							print "Choose a card to play (input a number)"
							user_input = int(raw_input(">"))
							user_decision = user_sorted[user_input]
							if  user_sorted[user_input] == "NA":
								user_decision = "You need to input something"
							if first_hand == True:
								if "C" not in "".join(user_sorted):
									if "H" in user_sorted[user_input]:
										user_decision = "You can't play a heart on the first hand"
									if "QS" in user_sorted[user_input]:
										user_decision = "You can't play the QS on the first hand"
							if j != 0:
								if first_play[1:] in "".join(user_sorted):
									if first_play[1:] not in user_sorted[user_input]:
										user_decision = "Please choose a suit that matches the first card played"
								elif "H" in user_sorted[user_input]:
									hearts_broken = True
							if "2C" in "".join(user_sorted):
								if user_sorted[user_input] != "2C":
									user_decision = "You must play the Two of Clubs"
							if hearts_broken == False:
								if "H" in user_sorted[user_input]:
									user_decision = "The Hearts have not been broken yet"
							user_sorted.remove(user_decision)
							break
						except (TypeError, NameError, IndexError, ValueError):
							print user_decision
							raw_input("Press Enter to Continue")
					# input the decision
					decision[0] = user_decision
					# pass totem to Alpha player
					totem = "A"
					# if this player was the first card, set decision to first
					if j == 0:
						first_play = user_decision
				elif totem == "A":
					(alpha_sorted, alpha_decision, hearts_broken) = A_I(first_play,first_hand,hearts_broken,queen_played,decision,alpha_sorted)
					# input player decision
					decision[1] = alpha_decision
					# pass totem to Bravo player
					totem = "B"
					# if this player was the first card, set decision to first
					if j == 0:
						first_play = alpha_decision
				elif totem == "B":
					(bravo_sorted, bravo_decision, hearts_broken) = A_I(first_play,first_hand,hearts_broken,queen_played,decision,bravo_sorted)
					# input player decision
					decision[2] = bravo_decision
					# pass totem to Charlie player
					totem = "C"
					# if this player was the first card, set decision to first
					if j == 0:
						first_play = bravo_decision
				elif totem == "C":
					(charlie_sorted, charlie_decision, hearts_broken) = A_I(first_play,first_hand,hearts_broken,queen_played,decision,charlie_sorted)
					# input player decision
					decision[3] = charlie_decision
					# pass totem to User
					totem = "U"
					# if this player was the first card, set decision to first
					if j == 0:
						first_play = charlie_decision
			# now that all decisions have been made, decide who gets points
			print_screen(round,decision,score,user_sorted,first_play,hearts_broken,first_hand)
			print "Press anything to continue..."
			raw_input(">")
			(score, totem) = point_allocation(first_play, score, totem, decision)
			decision = ["NA","NA","NA","NA"]
			first_play = "NA"
			first_hand = False
		round += 1
		round_h += 1
		if round_h == 5:
			round_h = 1
	print_winner(score)
	score = [0,0,0,0,0]
		
	
# This part of the code will create a deck and distribute to the four players
def deck_distribute():
	#Because we are calling this function multiple times lets clear what we use:
	del user[:]
	del alpha[:]
	del bravo[:]
	del charlie[:]
	
	set = cards[:]
	random.shuffle(set)
	random.shuffle(set)
	for i in range(0,13):
		user.append(set.pop())
		alpha.append(set.pop())
		bravo.append(set.pop())
		charlie.append(set.pop())
	del set[:]
	user.sort()
	u_s = [x for y, x in user]
	alpha.sort()
	a_s = [x for y, x in alpha]
	bravo.sort()
	b_s = [x for y, x in bravo]
	charlie.sort()
	c_s = [x for y, x in charlie]
	return u_s, a_s, b_s, c_s

# Check who has the two of clubs and mark them as the totem holder
def check_two(u,a,b,c):
	keyword = '2C'
	check_u = "\n".join(u)
	if keyword in check_u:
		t = "U"
			
	check_a = "\n".join(a)
	#for a in keyword:
	if keyword in check_a:
		t = "A"
			
	check_b = "\n".join(b)
	if keyword in check_b:
		t = "B"
			
	check_c = "\n".join(c)
	if keyword in check_c:
		t = "C"
	return t

#Players must pick three cards and swap
def swap_three(u_s,a_s,b_s,c_s,r):
	ua = []
	aa = []
	ba = []
	ca = []
	if r == 4:
		return u_s,a_s,b_s,c_s
	# Run a definition here for user to input 3 cards:
	(u_s,ua) = user_three_remove(u_s,r)
	# Run through each AI and have them all pick 3 cards:
	(a_s,aa) = ai_three_remove(a_s)
	(b_s,ba) = ai_three_remove(b_s)
	(c_s,ca) = ai_three_remove(c_s)
	#Now swap out the cards and let the user know what he got:
	if r == 1:
		u_s.extend(aa)
		a_s.extend(ba)
		b_s.extend(ca)
		c_s.extend(ua)
	if r == 2:
		u_s.extend(ba)
		a_s.extend(ca)
		b_s.extend(ua)
		c_s.extend(aa)
	if r == 3:
		u_s.extend(ca)
		a_s.extend(ua)
		b_s.extend(aa)
		c_s.extend(ba)
	return u_s,a_s,b_s,c_s

def user_three_remove(u,r):
	a = []
	passing = ""
	if r == 1:
		passing = "Alpha"
	if r == 2:
		passing = "Bravo"
	if r == 3:
		passing = "Charlie"
	for x in range(0,3):
		cards_count = len(u)
		print """\n\n\n\n\n\n
.--------------------------------------------------------------------.
|                                                                    |
|   _|_|_|                                  _|                       |
|   _|    _|    _|_|_|    _|_|_|    _|_|_|      _|_|_|      _|_|_|   |
|   _|_|_|    _|    _|  _|_|      _|_|      _|  _|    _|  _|    _|   |
|   _|        _|    _|      _|_|      _|_|  _|  _|    _|  _|    _|   |
|   _|          _|_|_|  _|_|_|    _|_|_|    _|  _|    _|    _|_|_|   |
|                                                               _|   |
|                                                           _|_|     |
|                                                                    |
|   _|_|_|    _|                                                     |
|   _|    _|  _|_|_|      _|_|_|    _|_|_|    _|_|                   |
|   _|_|_|    _|    _|  _|    _|  _|_|      _|_|_|_|                 |
|   _|        _|    _|  _|    _|      _|_|  _|                       |
|   _|        _|    _|    _|_|_|  _|_|_|      _|_|_|                 |
|                                                                    |
`--------------------------------------------------------------------'
		
"""
		first,second,third ="","",""
		for i in range(0,cards_count):
			first += "   %d    " % i
		print first
		print ".-----. " * (cards_count)
		for j in range(0,cards_count):
			second += "|   %s| " % u[j]
		print second
		print "|     | " * (cards_count)
		print "| CTO | " * (cards_count)
		print "|     | " * (cards_count)
		for k in range(0,cards_count):
			third += "|%s   | " % u[k]
		print third
		print "`-----' " * (cards_count)
		print "Choose a card to pass to player %s:" % passing
		while True:
			try:
				user_input = int(raw_input("> "))
				a.append(u[user_input])
				u.remove(u[user_input])
				break
			except (TypeError, NameError, IndexError, ValueError):
				print "That is not a valid input..."
				raw_input("Press Enter to Continue")
	return u,a

def ai_three_remove(s):
	a = []
	for x in range(0,3):
		# Strategic move here, if you have a lot of spades than you know you can effectively use the queen, so keep it and other spades
		if "".join(s).count("S") < 6 and "QS" in "".join(s):
			a.append("QS")
			s.remove("QS")
		elif "".join(s).count("S") < 6 and "AS" in "".join(s):
			a.append("AS")
			s.remove("AS")
		elif "".join(s).count("S") < 6 and "KS" in "".join(s):
			a.append("KS")
			s.remove("KS")
		#Now we remove cards based on count, if only 2 diamonds, get rid of highest value first
		else:
			C = [x for x in s if "C" in x]
			D = [x for x in s if "D" in x]
			H = [x for x in s if "H" in x]
			suit_array = [C,D,H]
			while len(min(suit_array, key=len)) == 0:
				suit_array.remove(min(suit_array))
			decision = min(suit_array, key=len)
			decision = decision[-1]
			a.append(decision)
			s.remove(decision)
	return s,a
			
#Now that the user gets cards from another player, they are at the end, let us fix this:
def resorting(u_s,a_s,b_s,c_s):
	u_n = []
	a_n = []
	b_n = []
	c_n = []
	for x,y in enumerate(cards):
		if y[1] in "".join(u_s):
			u_n.append(cards[x])
	u = [x for y, x in u_n]
	for x,y in enumerate(cards):
		if y[1] in "".join(a_s):
			a_n.append(cards[x])
	a = [x for y, x in a_n]
	for x,y in enumerate(cards):
		if y[1] in "".join(b_s):
			b_n.append(cards[x])
	b = [x for y, x in b_n]
	for x,y in enumerate(cards):
		if y[1] in "".join(c_s):
			c_n.append(cards[x])
	c = [x for y, x in c_n]
	return u,a,b,c

# A_I input
def A_I(f_p,f_h,h_b,q_p,d,i_s):
	# Make a decision based upon what would be best for player/rules
	# first_play,first_hand,hearts_broken,queen_played,decision,charlie_sorted
	decision = "NA"
	
	# before checking anything else, if its the first hand ever, limits to clubs or
	# highest spade if king or ace than goes diamonds
	if f_h == True:
		if "2C" in "".join(i_s):
			decision = i_s[0]
		elif "C" in "".join(i_s):
			update_sorted = [x for x in i_s if "C" in x]
			decision = update_sorted[-1]
		else:
			if ("KS" in "".join(i_s) or "AS" in "".join(i_s)):
				update_sorted = [x for x in i_s if "S" in x]
				decision = update_sorted[-1]
			elif "D" in "".join(i_s):
				update_sorted = [x for x in i_s if "D" in x]
				decision = update_sorted[-1]
			elif "S" in "".join(i_s):
				update_sorted = [x for x in i_s if "S" in x]
				if "QS" in "".join(update_sorted):
					update_sorted.remove('QS')
				decision = update_sorted[-1]
			else:
				decision = i_s[-1]
	# IS the first card played a club?
	elif "C" in "".join(f_p):
		decision = card_to_play("C",f_p,i_s,d)
		
	# IS the first card played a Diamond?				
	elif "D" in "".join(f_p):
		decision = card_to_play("D",f_p,i_s,d)
		
	# IS the first card played a Spade?
	elif "S" in "".join(f_p):
		decision = card_to_play("S",f_p,i_s,d)

	# IS the first card played a Heart?
	elif "H" in "".join(f_p):
		decision = card_to_play("H",f_p,i_s,d)
	
	# This means no ones played a card yet, free reign
	else:
		C = [x for x in i_s if "C" in x]
		D = [x for x in i_s if "D" in x]
		S = [x for x in i_s if "S" in x]
		H = [x for x in i_s if "H" in x]
		suit_number = [len(C),len(D),len(S),len(H)]
		if "S" in "".join(i_s):	
			if ("QS" not in "".join(i_s) and "KS" not in "".join(i_s) and "AS" not in "".join(i_s)):
				decision = S[0]
			else:
				decision = i_s[0]
		else:
			decision = i_s[0]
			
			
	if "H" in decision:
		h_b = True
	i_s.remove(decision)
	return i_s, decision, h_b

# Point system
def point_allocation(f_p,s,t,d):
#score = point_allocation(first_play, score, totem, decision)
	points = 0
	# Here is where the cards battle out
	for suit in d:
		if "H" in suit:
			points += 1
		if "QS" in suit:
			points += 13
	#Add up the points
	for n,i in enumerate(d):
		if f_p[1:] not in i:
			d[n] = "00"
	updated_d = [x[:-1] for x in d]
	for n,i in enumerate(updated_d):
		if "T" in i:
			updated_d[n] = "10"
		elif "J" in i:
			updated_d[n] = "11"
		elif "Q" in i:
			updated_d[n] = "12"
		elif "K" in i:
			updated_d[n] = "13"
		elif "A" in i:
			updated_d[n] = "14"
	updated_d = map(int, updated_d)
	max_index = updated_d.index(max(updated_d))
	if max_index == 0:
		t = "U"
	elif max_index == 1:
		t = "A"
	elif max_index == 2:
		t = "B"
	elif max_index == 3:
		t = "C"
	s[max_index + 1] += points
	s[0] = max(s)
	return s, t

# Common Card decision to pick the best card of that suit, you may have 5 cards that beat the highest card played so play the highest that still beats it:
def best_lowest(card_type,dec,updated_sorted):
	decision = "NA"
	update_d = [x[:-1] for x in dec if card_type in x]
	for m,j in enumerate(update_d):
		if j == "T":
			update_d[m] = "10"
		elif j == "J":
			update_d[m] = "11"
		elif j == "Q":
			update_d[m] = "12"
		elif j == "K":
			update_d[m] = "13"
		elif j == "A":
			update_d[m] = "14"
	update_d = map(int, update_d)
	update_d = max(update_d)

	updated_i_s = [x[:-1] for x in updated_sorted]
	for n,i in enumerate(updated_i_s):
		if i == "T":
			updated_i_s[n] = "10"
		elif i == "J":
			updated_i_s[n] = "11"
		elif i == "Q":
			updated_i_s[n] = "12"
		elif i == "K":
			updated_i_s[n] = "13"
		elif i == "A":
			updated_i_s[n] = "14"
	updated_i_s = map(int, updated_i_s)

	for x in range(0,len(updated_i_s)):
		if updated_i_s[x] < update_d:
			decision = updated_i_s[x]
	decision = str(decision)
	updated_i_s = map(str, updated_i_s)
	if decision == "NA":
		decision = updated_i_s[-1]

	if decision == "10":
		decision = "T"
	elif decision == "11":
		decision = "J"
	elif decision == "12":
		decision = "Q"
	elif decision == "13":
		decision = "K"
	elif decision == "14":
		decision = "A"
	decision = decision + card_type
	return decision

# After a suit has been played, this the deciding factor on which card to choose as an AI:
def card_to_play (suit, f_p, i_s, d):
	if suit in "".join(i_s):
		update_sorted = [x for x in i_s if suit in x]
		last_flag = d.count("NA")
		if last_flag == 1:
			if "H" in "".join(d) or "QS" in "".join(d):
				#Play lowest card IF it beats the lowest diamond
				decision = best_lowest(suit,d,update_sorted)
			else:
				#Otherwise play the highest diamond value because you are getting no points
				decision = update_sorted[-1]
		else:
			#Play lowest card because we have unknowns, no reason to gamble
			decision = update_sorted[0]
	else:
		#if player has the "QS" play it
		if "QS" in i_s:
			decision = "QS"
		#if player has a card higher than "QS" and Queen of Spades has not been played
		elif "KS" in i_s or "AS" in i_s:
			update_decision = [x for x in i_s if "S" in x]
			decision = update_decision[-1]
		#Just play highest card or if any of the suits are 2 or less and are safe to play, play them
		#make sure to check that hearts are allowed to be played...
		else:
			check_clubs = [x for x in i_s if "C" in x]
			check_hearts = [x for x in i_s if "H" in x]
			if len(check_clubs) < 3 and len(check_clubs) != 0:
				decision = check_clubs[-1]
			elif len(check_hearts) != 0:
				decision = check_hearts[-1]
			else:
				decision = i_s[-1]
	return decision

# Printing the screen to visualize whats happening
def print_screen(r,d,s,u_s,f_p,h_b,f_h):
	#Structure that user sees
	os.system('clear')
	q = ""
	if len(str(r)) == 1:
		q = " "
	p = ["","","",""]
	#make sure points system works for the spacing
	for x in range(0,4):
		if len(str(s[x+1])) == 1:
			p[x] = "  "
		elif len(str(s[x+1])) == 2:
			p[x] = " "
	cards_count = len(u_s)
	print """\n\n\n\n\n\n\n\n
	.----------------------------------------.
	| Round %d %s      |        HEARTS         |
	`----------------------------------------'
	.---------------Card Field---------------.
	| You:     %s                            |
	| Alpha:   %s                            |
	| Bravo:   %s                            |
	| Charlie: %s                            |
	|-----------------HEARTS-----------------|
	| User's points:     %r %s                |
	| Alphas's points:   %r %s                |
	| Bravo's points:    %r %s                |
	| Charlie's points:  %r %s                |
	`----------------------------------------'
	Hand:
	""" % (r, q, d[0], d[1], d[2], d[3], s[1], p[0], s[2], p[1], s[3], p[2], s[4], p[3])
	first, second, can_use, third = "","","",""
	for i in range(0,cards_count):
		first += "   %d    " % i
	print first
	print ".-----. " * (cards_count)
	for j in range(0,cards_count):
		second += "|   %s| " % u_s[j]
	print second
	print "|     | " * (cards_count)
	if f_h == True and "C" not in "".join(u_s):
		for k in range(0,cards_count):
			if "H" in u_s[k] or "QS" in u_s[k]:
				can_use += "|     | "
			else:
				can_use += "| CTO | "
	elif "2C" in "".join(u_s):
		can_use += "| CTO | "
		can_use += "|     | " * (cards_count - 1)
	elif f_p == "NA":
		for k in range(0,cards_count):
			if h_b == False and "H" in u_s[k]:
				can_use += "|     | "
			else:
				can_use += "| CTO | "
	else:
		for k in range(0,cards_count):
			if f_p[1:] in u_s[k] or f_p[1:] not in "".join(u_s):
				can_use += "| CTO | "
			else:
				can_use += "|     | "
	print can_use
	print "|     | " * (cards_count)
	for k in range(0,cards_count):
		third += "|%s   | " % u_s[k]
	print third
	print "`-----' " * (cards_count)

def print_winner(s):
	win = s.index(min(s))
	if win == 1:
		winner = "User!          "
	elif win == 2:
		winner = "Player Alpha!  "
	elif win == 3:
		winner = "Player Bravo!  "
	elif win == 4:
		winner = "Player Charlie!"
	print """
.---------------------------------------------------.
|    .--------------------------------------------. |
|   ( THE WINNER IS: %s               )|
|    `--------------------------------------------' |
|       |                                           |
|        `.                                         |
|          `.  . --- .                              |
|             /        \                            |
|            |  O  _  O |                           |
|            |  ./   \. |                           |
|            /  `-._.-'  \                          |
|          .' /         \ `.                        |
|      .-~.-~/           \~-.~-.                    |
|  .-~ ~    |             |    ~ ~-.                |
|  `- .     |             |     . -'                |
|       ~ - |             | - ~                     |
|           \             /                         |
|         ___\           /___                       |
|         ~;_  >- . . -<  _i~                       |
|            `'         `'                          |
|                                                   |
`---------------------------------------------------'
""" % winner
	raw_input("> ")
# This is the start of the game, built on function calls	
while gameplay == True:
	print """\n\n\n\n
.---------------------------------------------------.
|                                                   |
|    _    _                 _                       |
|   | |  | |               | |                      |
|   | |__| | ___  __ _ _ __| |_ ___                 |
|   |  __  |/ _ \/ _` | '__| __/ __|                |
|   | |  | |  __/ (_| | |  | |_\__ \                |
|   |_|  |_|\___|\__,_|_|   \__|___/                |
|                                                   |
|                      |\_/|,,_____,~~`             |
| 'P' - Play           (.".)~~     )`~}}            |
|                       \o/\ /---~\\ ~}}             |
| 'Q' - Quit              _//    _// ~}             |
`---------------------------------------------------'
"""
	user_input = raw_input("> ")
	if (user_input != 'P' and user_input != 'p'):
		print "Thanks for playing, bye!"
		gameplay = False
	else:
		run_game()