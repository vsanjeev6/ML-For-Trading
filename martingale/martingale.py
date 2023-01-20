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
import matplotlib.pyplot as plt
  		  	   		  		 			  		 			     			  	 
def author():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    :return: The GT username of the student  		  	   		  		 			  		 			     			  	 
    :rtype: str  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    return "vsanjeev6"
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def gtid():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    :return: The GT ID of the student  		  	   		  		 			  		 			     			  	 
    :rtype: int  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    return 903797718
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
    # The probability of win is for 18 black spaces that define a win and 2 green spaces (American Roulette)
    win_prob = 18.0/38.0
    bankroll = 256
    np.random.seed(gtid())  # do this only once  		  	   		  		 			  		 			     			  	 
    #print(get_spin_result(win_prob))  # test the roulette spin

    #print(win_prob)
    figure1(win_prob, 0, bankroll)
    figure3(win_prob, 0, bankroll)
    figure4_and_5(win_prob, 1, bankroll)

def betting_strategy(win_prob, real_sim, bankroll):
    episode_winnings = 0

    #Structuring the NumPy Array hint:: Each episode consists of 1000 spins plus the initial value of 0 in the first column (1001 columns in total)
    episode_array = np.full((1001),80)

    #print(episode_array, episode_array.shape, episode_array.size)

    bet_number = 0

    while episode_winnings < 80:
        #print("while 1")
        won = False
        bet_amount = 1
        while not won:
            if bet_number >= 1001:
                #print(episode_array)
                return episode_array
            episode_array[bet_number] = episode_winnings
            bet_number += 1
            won = get_spin_result(win_prob)
            #print("while 2")
            #print("spin result", won)
            if won == True:
                episode_winnings += bet_amount
                #print("won", episode_winnings)
            else:
                episode_winnings -= bet_amount
                bet_amount *= 2
                #print("lost", episode_winnings)
                #print("bet_amt=", bet_amount)
                if real_sim:
                    if episode_winnings == -bankroll:
                        episode_array[bet_number:] = episode_winnings
                        return episode_array
                    if episode_winnings + bankroll < bet_amount:
                        bet_amount = episode_winnings + bankroll

    return episode_array

def figure1(win_prob, real_sim, bankroll):
    for i in range(10):
        cur_episode = betting_strategy(win_prob,real_sim, bankroll)
        plt.plot(cur_episode, label='Episode %s' % i)

    plotting_utility_function("Figure 1 - 10 episodes of the betting strategy",
                              [0, 300, -256, 100], "Number of Spins", "Cumulative Winnings", "figure1.png")

def figure2(win_prob, real_sim, bankroll):
    # Rows is number of episodes; columns is number of spins per episode (1000) + initial value in 1st column
    cumulative_array = np.zeros((1000,1001))

    for i in range(1000):
        cur_episode = betting_strategy(win_prob,real_sim, bankroll)
        cumulative_array[i] = cur_episode

    mean_array = np.mean(cumulative_array, axis = 0)
    std_dev_array = np.std(cumulative_array, axis = 0)
    mean_plus_std = mean_array + std_dev_array
    mean_minus_std = mean_array - std_dev_array

    plt.plot(mean_array, label="Mean")
    plt.plot(mean_plus_std, label="Mean + Standard Deviation")
    plt.plot(mean_minus_std, label="Mean - Standard Deviation")

    if real_sim == 0:
        plotting_utility_function("Figure 2 - Mean & Standard Deviations for 1000 episodes",
                                  [0, 300, -256, 100], "Number of Spins", "Cumulative Winnings", "figure2.png")
    else:
        plotting_utility_function("Figure 4 - Mean & Standard Deviations for 1000 episodes of Real Simulator",
                                  [0, 300, -256, 100], "Number of Spins", "Cumulative Winnings", "figure4.png")

    return cumulative_array,std_dev_array
def figure3(win_prob, real_sim, bankroll):
    same_cumulative_array, same_std_dev_array = figure2(win_prob, real_sim, bankroll)
    median_array = np.median(same_cumulative_array, axis=0)
    median_plus_std = median_array + same_std_dev_array
    median_minus_std = median_array - same_std_dev_array

    plt.plot(median_array, label="Median")
    plt.plot(median_plus_std, label="Median + Standard Deviation")
    plt.plot(median_minus_std, label="Median - Standard Deviation")

    if real_sim == 0:
        plotting_utility_function("Figure 3 - Median & Standard Deviations for 1000 episodes",
                                  [0, 300, -256, 100], "Number of Spins", "Cumulative Winnings", "figure3.png")
    else:
        plotting_utility_function("Figure 5 - Median & Standard Deviations for 1000 episodes of Real Simulator",
                                  [0, 300, -256, 100], "Number of Spins", "Cumulative Winnings", "figure5.png")
def figure4_and_5(win_prob, real_sim, bankroll):
    figure3(win_prob, real_sim, bankroll)

def plotting_utility_function(title,axes,xlabel,ylabel,fig_name):

    plt.title(title)
    plt.axis(axes)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(fig_name)
    plt.clf()

if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    test_code()

