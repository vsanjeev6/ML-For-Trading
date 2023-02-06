import numpy as np
class DTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose

    def author(self):
        return 'vsanjeev6'

    def addEvidence(self, data_x, data_y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        data_y_transpose = np.transpose(np.array([data_y]))
        data = np.append(data_x, data_y_transpose, axis=1)
        #print("Shape of arrays", data_x.shape, data_y_transpose.shape, data.shape)
        self.tree = self.build_tree(data_x, data_y)

    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        out = []
        for point in points:
            out.append(self.get_prediction(point))
        print("Predictions")
        print(out)
        return np.asarray(out)

    def get_prediction(self, point):
        """
        @summary: Predict one query using self.tree
        @param point: numpy ndarray, one specific query.
        @return: the prediction for the one query
        """

        node = 0
        while ~np.isnan(self.tree[node][0]):
            split_value = point[int(self.tree[node][0])]

            # relative position so new_node = curr_node + offset
            if split_value <= self.tree[node][1]:
                node += int(self.tree[node][2])
            else:
                node += int(self.tree[node][3])
            print("Query Tree")
            print(self.tree[node][1])
        return self.tree[node][1]

    def best_feature_selection(self, data_x, data_y):
        best_feature_index = 0
        best_corr_val = 0

        for i in range(data_x.shape[1]):
            # Returns a 2x2 array where the diagonal elements are equal [[1,x],[x,1]]
            correlation = abs(np.corrcoef(data_x[:, i], data_y)[0, 1])
            # -1 and 1 are highly correlated, just in the opposite sense.
            # Pick the first one that satisfies this condition
            if correlation > best_corr_val:
                best_corr_val = correlation
                best_feature_index = i
        return best_feature_index

    def build_tree(self, data_x, data_y):

        # Stopping criteria
        # 1. Number of rows <= Leaf size
        if data_x.shape[0] <= self.leaf_size:
            return np.asarray([np.nan, np.mean(data_y), np.nan, np.nan])
        # 2. If all Y are the same.
        if np.all(data_y == data_y[0]):
            return np.asarray([np.nan, data_y[0], np.nan, np.nan])

        # Determine the best feature
        best_feature_index = self.best_feature_selection(data_x, data_y)
        #Median of all the rows in the best feature column
        split_val = np.median(data_x[:, best_feature_index])
        #print("Best feature Index, Split Value", best_feature_index, split_val)

        # To prevent infinite recursion due to edge case when only left sub-tree is formed
        # If the maximum value in the feature column (Xi) == split value, then all the sub nodes will be on the left
        if ((max(data_x[:, best_feature_index])) == split_val):
            return np.asarray([np.nan, np.mean(data_y), np.nan, np.nan])

        # Build left and right trees
        left_tree = self.build_tree(data_x[data_x[:, best_feature_index] <= split_val], data_y[data_x[:, best_feature_index] <= split_val])
        #print(left_tree)
        #print(left_tree.shape)
        right_tree = self.build_tree(data_x[data_x[:, best_feature_index] > split_val], data_y[data_x[:, best_feature_index] > split_val])

        #print("Left tree shape, Ndim", left_tree.shape[0], left_tree.ndim)
        # Set root node (each sub-tree is a Decision tree itself)
        # Relative node positions
        if left_tree.ndim == 1:
            root = np.asarray([best_feature_index, split_val, 1, 2]) #Need to add 1+1
        else:
            root = np.asarray([best_feature_index, split_val, 1, left_tree.shape[0] + 1])

        #Causing bound access error
        #root = np.asarray([best_feature_index, split_val, 1, left_tree.shape[0] + 1])

        # Append takes only 2 array args at a time
        return np.vstack((root, left_tree, right_tree))

    if __name__ == "__main__":
        print('not implemented')