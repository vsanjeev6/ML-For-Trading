""""""
"""  		  	   		  		 			  		 			     			  	 
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  		 			  		 			     			  	 
All Rights Reserved  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Template code for CS 4646/7646  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  		 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  		 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  		 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 			  		 			     			  	 
or edited.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		  		 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  		 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 			  		 			     			  	 
GT honor code violation.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
-----do not edit anything above this line---  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Student Name: Vaishnavi Sanjeev  		  	   		  		 			  		 			     			  	 
GT User ID: vsanjeev6  		  	   		  		 			  		 			     			  	 
GT ID: 903797718 		  	   		  		 			  		 			     			  	 
"""

import random as rand
import numpy as np

class QLearner(object):
    def author(self):
        return 'vsanjeev6'

    """  		  	   		  		 			  		 			     			  	 
    This is a Q learner object.  		  	   		  		 			  		 			     			  	 

    :param num_states: The number of states to consider.  		  	   		  		 			  		 			     			  	 
    :type num_states: int  		  	   		  		 			  		 			     			  	 
    :param num_actions: The number of actions available..  		  	   		  		 			  		 			     			  	 
    :type num_actions: int  		  	   		  		 			  		 			     			  	 
    :param alpha: The learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.  		  	   		  		 			  		 			     			  	 
    :type alpha: float  		  	   		  		 			  		 			     			  	 
    :param gamma: The discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.  		  	   		  		 			  		 			     			  	 
    :type gamma: float  		  	   		  		 			  		 			     			  	 
    :param rar: Random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.  		  	   		  		 			  		 			     			  	 
    :type rar: float  		  	   		  		 			  		 			     			  	 
    :param radr: Random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.  		  	   		  		 			  		 			     			  	 
    :type radr: float  		  	   		  		 			  		 			     			  	 
    :param dyna: The number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.  		  	   		  		 			  		 			     			  	 
    :type dyna: int  		  	   		  		 			  		 			     			  	 
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 			  		 			     			  	 
    :type verbose: bool  		  	   		  		 			  		 			     			  	 
    """

    def __init__(
        self,
        num_states=100,
        num_actions=4,
        alpha=0.2,
        gamma=0.9,
        rar=0.5,
        radr=0.99,
        dyna=0,
        verbose=False,
    ):
        """  		  	   		  		 			  		 			     			  	 
        Constructor method  		  	   		  		 			  		 			     			  	 
        """
        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0

        self.num_state = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        # Initialize Q[] with all zeroes
        self.q = np.zeros((num_states, num_actions))
        self.T_prime = {}
        self.states_and_actions = {}

        if dyna > 0:
            # Init Tc with a small value to avoid divide by 0
            self.Tc = np.full((num_states, num_actions, num_states), 0.00001)
            self.R = np.zeros((num_states, num_actions))

    def querysetstate(self, s):
        """
        Update the state without updating the Q-table

        :param s: The new state
        :type s: int
        :return: The selected action
        :rtype: int
        """
        # Update the state
        self.s = s

        # Faster approach to generate random numbers than randint()
        # randint() does a lot of case-checking and parameter setting
        random = rand.random()

        # Choose the next action randomly or from Q table
        if random < self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.q[s])
        return action

    def query(self, s_prime, r):
        """
        Update the Q table and return an action

        :param s_prime: The new state
        :type s_prime: int
        :param r: The immediate reward
        :type r: float
        :return: The selected action
        :rtype: int
        """

        # Update the Q table (2-D matrix)
        self.q[self.s, self.a] = (1 - self.alpha) * self.q[self.s, self.a] + self.alpha * (r + self.gamma * np.max(self.q[s_prime]))

        # Create a dictionary of historical states (keys) and corresponding actions (values)
        self.states_and_actions.setdefault(self.s, []).append(self.a)

        # Create a dictionary of (s,a): as keys and s_prime as values
        self.T_prime = {}

        # Dyna-Q
        if self.dyna > 0:
            # Learn models Tc and R
            # Update of Tc and R is outside the Dyna loop
            self.Tc[self.s, self.a, s_prime] += 1
            self.R[self.s, self.a] = (1 - self.alpha) * self.R[self.s, self.a] + self.alpha * r

            # Hallucinate experiences
            for _ in range(self.dyna):
                self.hallucinate()

        # Faster approach to generate random numbers than randint()
        # randint() does a lot of case-checking and parameter setting
        random = rand.random()

        if random < self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.q[s_prime])

        # Update random action rate
        self.rar = self.rar * self.radr

        if self.verbose:
            print(f"s' = {s_prime}, a = {action}, r={r}")

        # Update the new state and action
        self.s = s_prime
        self.a = action
        return action

    def hallucinate(self):
        """
        For Dyna-Q:
        Hallucinate Experiences and Update the Q-table with <s,a,s',r>
        """
        # Randomly choose "s" and "a" from previously seen <s,a> pair
        s = rand.choice(list(self.states_and_actions.keys()))
        a = rand.choice(self.states_and_actions[s])

        # Infer s_prime from T_prime[]
        if (s, a) in self.T_prime:
            s_prime = self.T_prime[(s, a)]
        else:
            s_prime = np.argmax(self.Tc[s, a])
            self.T_prime[(s, a)] = s_prime

        # Expected Reward
        r = self.R[s, a]

        # Update Q Table
        self.q[s, a] = (1 - self.alpha) * self.q[s, a] + self.alpha * (r + self.gamma * np.max(self.q[s_prime]))

if __name__ == "__main__":
    print("Remember Q from Star Trek? Well, this isn't him")