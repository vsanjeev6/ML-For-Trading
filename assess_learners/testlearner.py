""""""  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
Test a learner.  (c) 2015 Tucker Balch  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import math  		  	   		  		 			  		 			     			  	 
import sys
import numpy as np  		  	   		  		 			  		 			     			  	 
import time
import LinRegLearner as lrl
import DTLearner as dtl
import RTLearner as rtl
import BagLearner as bl
import InsaneLearner as it
import matplotlib.pyplot as plt

def plotting_utility_function(title,experimental_leaf_size,in_sample_rsme,out_sample_rsme,xlabel,ylabel,fig_name,label1,label2):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(range(1, experimental_leaf_size), in_sample_rsme, label=label1)
    plt.plot(range(1, experimental_leaf_size), out_sample_rsme, label=label2)
    plt.xticks(np.arange(0, experimental_leaf_size, step=5))
    plt.grid()
    plt.legend()
    plt.savefig(fig_name)
    plt.clf()

def experiment_1(train_x, train_y, test_x, test_y):
    experimental_leaf_size = 101
    in_sample_rsme = []
    out_sample_rsme = []

    for leafsize in range(1, experimental_leaf_size):
        learner = dtl.DTLearner(leaf_size=leafsize, verbose=False)
        learner.add_evidence(train_x, train_y)

        # in sample
        in_predY = learner.query(train_x)
        in_rmse = math.sqrt(((train_y - in_predY) ** 2).sum() / train_y.shape[0])

        # out sample
        out_predY = learner.query(test_x)
        out_rmse = math.sqrt(((test_y - out_predY) ** 2).sum() / test_y.shape[0])

        in_sample_rsme.append(in_rmse)
        out_sample_rsme.append(out_rmse)

    plotting_utility_function("Figure 1 - Leaf Size Vs. RMSE for DTLearner",experimental_leaf_size,in_sample_rsme,
                              out_sample_rsme, "Leaf Size", "RMSE", "Figure1.png", "In Sample", "Out Sample")

def experiment_2(train_x, train_y, test_x, test_y):
    bag_size = 50
    experimental_leaf_size = 101
    in_sample_rsme = []
    out_sample_rsme = []

    for leafsize in range(1, experimental_leaf_size):
        learner = bl.BagLearner(learner=dtl.DTLearner, kwargs={"leaf_size": leafsize}, bags=bag_size, boost=False,
                                verbose=False)
        learner.add_evidence(train_x, train_y)

        # in sample
        in_predY = learner.query(train_x)
        in_rmse = math.sqrt(((train_y - in_predY) ** 2).sum() / train_y.shape[0])

        # out sample
        out_predY = learner.query(test_x)
        out_rmse = math.sqrt(((test_y - out_predY) ** 2).sum() / test_y.shape[0])

        in_sample_rsme.append(in_rmse)
        out_sample_rsme.append(out_rmse)

    plotting_utility_function("Figure 2 - Leaf Size Vs. RMSE for DTLearner with Bagging",experimental_leaf_size,in_sample_rsme,
                              out_sample_rsme, "Leaf Size", "RMSE", "Figure2.png", "In Sample", "Out Sample")

def experiment_3_1(train_x, train_y, test_x, test_y):
    experimental_leaf_size = 101
    dt_mae_arr = np.zeros((100,25))
    rt_mae_arr = np.zeros((100,25))

    """Computing Mean Absolute Error of DT and RT """
    for i in range(25):
        for leafsize in range(1, experimental_leaf_size):
            learner = dtl.DTLearner(leaf_size=leafsize, verbose=False)
            learner.add_evidence(train_x, train_y)
            dt_predY = learner.query(test_x)
            dt_mae = np.mean(np.abs((np.asarray(test_y) - np.asarray(dt_predY))))
            dt_mae_arr[leafsize-1][i] = dt_mae

            learner = rtl.RTLearner(leaf_size=leafsize, verbose=False)
            learner.add_evidence(train_x, train_y)
            rt_predY = learner.query(test_x)
            rt_mae = np.mean(np.abs((np.asarray(test_y) - np.asarray(rt_predY))))
            rt_mae_arr[leafsize-1][i] = rt_mae

    dt_mae_mean = np.mean(dt_mae_arr, axis=1)
    rt_mae_mean = np.mean(rt_mae_arr, axis=1)

    plotting_utility_function("Figure 3.1 - Comparing Decision Tree & Random Tree using MAE", experimental_leaf_size,dt_mae_mean,
                              rt_mae_mean, "Leaf Size", "Mean Absolute Error", "Figure3_1.png", "Decision Tree", "Random Tree")

def compute_r_squared(train_x, train_y, test_x, test_y, learner):
    ss_res = 0
    ss_tot = 0

    learner.add_evidence(train_x, train_y)
    predY = learner.query(test_x)
    y_mean = np.mean(test_y)
    residuals = test_y - predY
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((test_y - y_mean)**2)
    r2 = 1 - (ss_res / ss_tot)
    return r2

def experiment_3_2(train_x, train_y, test_x, test_y):
    experimental_leaf_size = 101
    r2_dt = np.zeros((100,25))
    r2_rt = np.zeros((100,25))

    """Computing Coefficient of Determination for DT and RT """
    for i in range(25):
        for leafsize in range(1, experimental_leaf_size):
            r2_dt[leafsize-1][i] = (compute_r_squared(train_x, train_y, test_x, test_y, dtl.DTLearner(leaf_size=leafsize, verbose=False)))
            r2_rt[leafsize-1][i] = (compute_r_squared(train_x, train_y, test_x, test_y, rtl.RTLearner(leaf_size=leafsize, verbose=False)))

    r2_dt_mean = np.mean(r2_dt, axis=1)
    r2_rt_mean = np.mean(r2_rt, axis=1)

    plotting_utility_function("Figure 3.2 - Comparing Decision Tree & Random Tree using R-Squared", experimental_leaf_size,r2_dt_mean,
                              r2_rt_mean, "Leaf Size", "Coefficient of Determination", "Figure3_2.png","Decision Tree", "Random Tree")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python testlearner.py <filename>")
        sys.exit(1)
    inf = open(sys.argv[1])
    data = np.array(
        [list(map(str, s.strip().split(","))) for s in inf.readlines()]
    )

    # Strip first row (heading) and first column (date)
    if sys.argv[1] == "Data/Istanbul.csv":
        data = data[1:, 1:]
    data = data.astype('float')

    np.random.seed(903797718)
    # To ensure random 60% training set and 40% test set
    np.random.shuffle(data)

    # compute how much of the data is training and testing
    train_rows = int(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    train_x = data[:train_rows, 0:-1]
    train_y = data[:train_rows, -1]
    test_x = data[train_rows:, 0:-1]
    test_y = data[train_rows:, -1]

    #print(f"{test_x.shape}")
    #print(f"{test_y.shape}")

    experiment_1(train_x, train_y, test_x, test_y)
    experiment_2(train_x, train_y, test_x, test_y)
    experiment_3_1(train_x, train_y, test_x, test_y)
    experiment_3_2(train_x, train_y, test_x, test_y)



