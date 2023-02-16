""""""  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
template for generating data to fool learners (c) 2016 Tucker Balch  		  	   		  		 			  		 			     			  	 
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
  		  	   		  		 			  		 			     			  	 
import math  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import numpy as np  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
# this function should return a dataset (X and Y) that will work  		  	   		  		 			  		 			     			  	 
# better for linear regression than decision trees  		  	   		  		 			  		 			     			  	 
def best_4_lin_reg(seed=1489683273):
    """  		  	   		  		 			  		 			     			  	 
    Returns data that performs significantly better with LinRegLearner than DTLearner.  		  	   		  		 			  		 			     			  	 
    The data set should include from 2 to 10 columns in X, and one column in Y.  		  	   		  		 			  		 			     			  	 
    The data should contain from 10 (minimum) to 1000 (maximum) rows.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param seed: The random seed for your data generation.  		  	   		  		 			  		 			     			  	 
    :type seed: int  		  	   		  		 			  		 			     			  	 
    :return: Returns data that performs significantly better with LinRegLearner than DTLearner.  		  	   		  		 			  		 			     			  	 
    :rtype: numpy.ndarray  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    np.random.seed(seed)
    # Generate features randomly
    X_rows = np.random.randint(10, 1001)
    X_columns = np.random.randint(2, 11)
    x = np.random.random((X_rows, X_columns))

    # Y is linearly related to X
    y = np.mean(x,axis = 1)

    #print("Linear Regression Dataset")
    #print(x,y, np.shape(x), np.shape(y))
    return x, y  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def best_4_dt(seed=1489683273):
    """  		  	   		  		 			  		 			     			  	 
    Returns data that performs significantly better with DTLearner than LinRegLearner.  		  	   		  		 			  		 			     			  	 
    The data set should include from 2 to 10 columns in X, and one column in Y.  		  	   		  		 			  		 			     			  	 
    The data should contain from 10 (minimum) to 1000 (maximum) rows.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param seed: The random seed for your data generation.  		  	   		  		 			  		 			     			  	 
    :type seed: int  		  	   		  		 			  		 			     			  	 
    :return: Returns data that performs significantly better with DTLearner than LinRegLearner.  		  	   		  		 			  		 			     			  	 
    :rtype: numpy.ndarray  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    np.random.seed(seed)  		  	   		  		 			  		 			     			  	 
    # Generate features randomly
    X_rows = np.random.randint(10, 1001)
    X_columns = np.random.randint(2, 11)
    x = np.random.random((X_rows, X_columns))

    # Decision Trees deal with non-linear data batter
    sums = np.sum(x, axis=1)
    powers = np.arange(0, x.shape[1])
    y_temp = np.power((5*x), powers+1) * np.power((3*x), powers+1)
    y = np.sum(y_temp, axis=1)

    #print(sums, np.shape(sums))
    #print("Decision Tree Dataset")
    #print(y, np.shape(x), np.shape(y))
    return x, y

  		  	   		  		 			  		 			     			  	 
def author():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    :return: The GT username of the student  		  	   		  		 			  		 			     			  	 
    :rtype: str  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    return "vsanjeev6"  # Change this to your user ID
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
if __name__ == "__main__":
    x_lin, y_lin = best_4_lin_reg(seed=1489683273)
    x_dt, y_dt = best_4_dt(seed=1489683273)
    if np.array_equal(x_lin, x_dt):
        pass
        #print("Same-sies")
    else:
        pass
        #print("ERROR")
