import numpy as np
class BagLearner(object):

    def __init__(self, learner, kwargs, bags, boost=False, verbose=False):
        self.learner = learner
        self.bags = bags
        self.boost = boost
        self.verbose = verbose

        self.learners = []
        for i in range(0, bags):
            self.learners.append(learner(**kwargs))

    def author(self):
        return 'vsanjeev6'

    def addEvidence(self, data_x, data_y):
        for learner in self.learners:
            # Bagging with replacement; n' = n = 321 (for Istanbul.csv)
            #random_indices is a 1-D array (321x1)
            random_indices = np.random.choice(range(data_x.shape[0]), data_x.shape[0], replace=True)
            #print("Bag Index\n", random_indices)
            random_x = data_x[random_indices]
            random_y = data_y[random_indices]
            # Train each individual learner with the new Training data
            learner.addEvidence(random_x, random_y)
        #print("Shape of bag_index", random_indices.shape)
        #print("Shape of data_x", data_x.shape)

    def query(self, points):
        predictions = []
        for learner in self.learners:
            # Query each individual learner
            predictions.append(learner.query(points))
        np_predictions = np.array(predictions)
        #print("Predictions\n", np_predictions)
        #print("Mean ; Dim", np.mean(np_predictions, axis=0), np.mean(np_predictions, axis=0).shape)
        return np.mean(np_predictions, axis=0)

    if __name__ == "__main__":
            print('not implemented')