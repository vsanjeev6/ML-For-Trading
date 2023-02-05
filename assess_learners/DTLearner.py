import numpy as np

class DTLearner(object):

    #Constructor
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        #pass == return None

    def author(self):
        return "vsanjeev6"

    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        self.tree = self.build_tree(data_x,data_y)
        if self.verbose:
            print("DTLearner")
            print("Tree Shape" + str(self.tree.shape))
            print(self.tree)


    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        return (self.model_coefs[:-1] * points).sum(axis=1) + self.model_coefs[
            -1
        ]

    def build_tree(self, data_x, data_y):

        best_feature_index = 0
        best_corr_val = 0

        #Stopping criteria
        if data_x.shape[0] <= self.leaf_size:
            return np.asarray([-1, np.mean(data_y), np.nan, np.nan])
        if (all(y==data_y[0]) for y in data_y):
            return np.asarray([-1, np.mean(data_y), np.nan, np.nan])

        #Determine the best feature to split on based on correlation of Xi with Y
        for i in range(data_x.shape[1]):
            correlation = np.corrcoef(data_x[:,i],data_y)
            correlation = abs(correlation[0,1])
            if correlation > best_corr_val:
                best_corr_val = correlation
                best_feature_index = i

        #Computing the split value
        split_val = np.median(data_x[:,best_feature_index])

        #Build left and right trees
        left_tree = self.build_tree(data_x[data_x[:,best_feature_index] <= split_val])
        right_tree = self.build_tree(data_x[data_x[:,best_feature_index] > split_val])

        #Set root node (each sub-tree is a Decision tree itself)
        root = np.asarray([best_feature_index, split_val, 1, left_tree.shape[0] + 1])

        return np.append(root, left_tree, right_tree)


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")