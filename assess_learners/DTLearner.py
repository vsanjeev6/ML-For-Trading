import numpy as np
class DTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose

    def author(self):
        return 'vsanjeev6'

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        self.tree = self.build_tree(dataX, dataY)
        if self.verbose:
            print("DTLearner")
            print("tree shape: " + str(self.tree.shape))
            print("tree details below")
            print(self.tree)

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @return: the estimated values according to the saved model.
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

    def get_best_feature(self, data_x, data_y):
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

    def build_tree(self, dataX, dataY):
        """
        @summary: build the decision tree
        @param dataX: numpy ndarray, features of trainning data
        @param dataY: numpy ndarray, labels of tranning data
        @return: numpy ndarray, decision tree in tabular format
        """

        # aggregated all the data left into a leaf if leaf_size or fewer entries left
        if dataX.shape[0] <= self.leaf_size:
            return np.asarray([np.nan, np.mean(dataY), np.nan, np.nan])

        if np.all(np.isclose(dataY, dataY[0])):
            return np.asarray([np.nan, dataY[0], np.nan, np.nan])

        feature_index = self.get_best_feature(dataX, dataY)
        split_val = np.median(dataX[:, feature_index])
        print("Best Feature index", feature_index)
        print("Split Val", split_val)

        left_mask = dataX[:, feature_index] <= split_val
        # make a leaf to prevent infinite recursion
        if np.all(np.isclose(left_mask, left_mask[0])):
            return np.asarray([np.nan, np.mean(dataY), np.nan, np.nan])

        right_mask = np.logical_not(left_mask)

        """
        # not correct! we should not delete a column becasue we can ask it again
        dataX = np.delete(dataX, feature_index, 1)
        """

        left_tree = self.build_tree(dataX[left_mask], dataY[left_mask])

        #print("++++++++")
        #print(left_tree)
        #print(left_tree.shape)

        right_tree = self.build_tree(dataX[right_mask], dataY[right_mask])

        if left_tree.ndim == 1:
            root = np.asarray([feature_index, split_val, 1, 2])
        else:
            root = np.asarray([feature_index, split_val, 1, left_tree.shape[0] + 1])

        return np.row_stack((root, left_tree, right_tree))

    if __name__ == "__main__":
        print('not implemented')