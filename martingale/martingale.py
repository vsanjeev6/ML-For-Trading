""""""  		  	   		  		 			  		 			     			  	 
"""Assess a betting strategy.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
  		  	   		  		 			  		 			     			  	 
import numpy as np  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def author():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    :return: The GT username of the student  		  	   		  		 			  		 			     			  	 
    :rtype: str  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    return "vsanjeev6"  # replace tb34 with your Georgia Tech username.
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def gtid():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    :return: The GT ID of the student  		  	   		  		 			  		 			     			  	 
    :rtype: int  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    return 903797718  # replace with your GT ID number
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def get_spin_result(win_prob):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param win_prob: The probability of winning  		  	   		  		 			  		 			     			  	 
    :type win_prob: float  		  	   		  		 			  		 			     			  	 
    :return: The result of the spin.  		  	   		  		 			  		 			     			  	 
    :rtype: bool  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    result = False  		  	   		  		 			  		 			     			  	 
    if np.random.random() <= win_prob:  		  	   		  		 			  		 			     			  	 
        result = True  		  	   		  		 			  		 			     			  	 
    return result  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def test_code():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Method to test your code  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    win_prob = 0.60  # set appropriately to the probability of a win  		  	   		  		 			  		 			     			  	 
    np.random.seed(gtid())  # do this only once  		  	   		  		 			  		 			     			  	 
    print(get_spin_result(win_prob))  # test the roulette spin  		  	   		  		 			  		 			     			  	 
    # add your code here to implement the experiments
    betting_strategy(win_prob)
  		  	   		  		 			  		 			     			  	 

def betting_strategy(win_prob):
    episode_winnings = 0

    while episode_winnings < 80:
        won = False
        bet_amount = 1
        while not won:
            #wager on black?
            won = get_spin_result(win_prob)
            print("spin result", won)
            if won == True:
                episode_winnings += bet_amount
                print("won", episode_winnings)
            else:
                episode_winnings -= bet_amount
                bet_amount *= 2
                print("lost", episode_winnings)
                print("bet_amt", bet_amount)





if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    test_code()

