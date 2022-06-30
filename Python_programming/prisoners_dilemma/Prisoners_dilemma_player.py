import random
class MyPlayer:
    '''Hrac hraje podle analizy'''
    def __init__(self, payoff_matrix, number_of_iterations = 1):
        #The bot will use various parameters to analyze and understand 
        # what strategy is being played against him in the first 10 turns.

        self.number_of_ierations = number_of_iterations
        self.payoff_matrix = payoff_matrix

        self.opp_weights = [0, 0]  
        self.my_weights = [0, 0]
        # These parameters will be used to count opp.'s moves

        self.memory = [None, False] 
        # Setting up the first move as "False" 
        # since i'm getting an error otherwise 

        self.coop_coop_value = payoff_matrix[0][0][0] + payoff_matrix[0][0][1]
        self.def_def_value = payoff_matrix[1][1][0] + payoff_matrix[1][1][1]
        self.coop_def_value = payoff_matrix[0][1][0] + payoff_matrix[0][1][1]
        # These parameters analyze P.M. to see what gives the most points
        # by cooperating with different strategies

        self.turn_count = 0

    def move(self):
        x = random.choice([3,5,7,11,13,17])
        # This number will be used to desync the player
        # if he realises that he is playing against himself
        # to gain the most profit for the specific scenario

        self.turn_count += 1

        if self.turn_count <= 10:
            if self.turn_count == 5: 
                return True
            else:
                return self.memory[1]
        # First 10 moves are always COOPERATE with a calculated
        # mistake on turn 5 to see how the opp. will react 
        # and to understand whether it's a tit for tat
        # or "always COOPERATE"


        else:

            if self.opp_weights[1] == 0: 
                return True
            # This scenario invokes once
            # the player has realised he's 
            # playing against "always DEFECT"

            elif self.opp_weights[0] == 0: 
                if max(self.coop_coop_value, self.coop_def_value) == self.coop_coop_value:
                    return False
                #If value of COOP. is bigger - then play COOP =)

                else:
                    return True 
            # This scenario invokes once the player has realised he's 
            # playing against "always COOP"

            
            elif self.my_weights == self.opp_weights: 
                if max(self.coop_coop_value, self.def_def_value, self.coop_def_value) == self.coop_coop_value: # If the highest value is achieved by coop. - play coop.
                    return False
                elif max(self.coop_coop_value, self.def_def_value, self.coop_def_value) == self.def_def_value: # If the highest value is achieved by def. - play def.
                    return True
                else: # it's better to desync - process
                    if self.memory[0] == self.memory[1]:
                        return random.choice([True, False])
                    else:
                        self.my_weights[0] += x
                        return self.memory[1]
            # This scenario invokes once the player has realised he
            # is playing against himself. If it's neither better to
            # always COOP nor DEFECT, the player will try to desync
            # from his doppelganger via random.choice() until suc-
            # -cessful. Once the strategy is attuned, it becomes
            # a regular TIT FOR TAT and only "else" will get invoked

            elif (self.my_weights[0]-1 == self.opp_weights[0]) and (self.my_weights[1]+1 == self.opp_weights[1]): #means i'm playing TIT FOR TAT
                if max(self.coop_coop_value, self.def_def_value, self.coop_def_value) == self.coop_coop_value: # If the highest value is achieved by COOP. - play COOP.
                    return False
                elif max(self.coop_coop_value, self.def_def_value, self.coop_def_value) == self.def_def_value: # If the highest value is achieved by DEF. - play DEF.
                    return True
                else: # else continue playing TIT FOR TAT
                    return self.memory[1]
            # This scenario invokes once the player has realised he
            # is playing against TIT FOR TAT. Scans values to see
            # what strategy is best for gaining points and sticks
            # to it.

            else:
                return self.memory[1]


    
    def record_last_moves(self, my_last_move, opponent_last_move):

        self.memory = [my_last_move, opponent_last_move]

        if opponent_last_move == True:
            self.opp_weights[0] += 1
        else:
            self.opp_weights[1] += 1

        if my_last_move == True:
            self.my_weights[0] += 1
        else:
            self.my_weights[1] += 1
        # Counting both my and opp.'s moves for later analisys 

if __name__ == "__main__":
    payoff_matrix = ( ((4,4),(1,6)) , ((6,1),(2,2)) )
    playerA = MyPlayer(payoff_matrix, 5)
    number_of_iterations = playerA.number_of_ierations
    print(playerA.payoff_matrix)
    print(playerA.number_of_ierations)
    playerA_move = playerA.move()
    print("Player A used method", playerA_move, "!")
    