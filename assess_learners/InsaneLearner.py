import BagLearner as bl
import LinRegLearner as lrl
class InsaneLearner(object):
    def __init__(self, verbose=False):
        self.learners = []
        for i in range(0, 20):
            self.learners.append(bl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=20, boost=False, verbose=False))
    def author(self):
        return 'vsanjeev6'
    def add_evidence(self, data_x, data_y):
        for learner in self.learners:
            learner.add_evidence(data_x, data_y)
    def query(self, points):
        predictions = []
        for learner in self.learners:
            predictions.append(learner.query(points))
        return sum(predictions)/len(predictions)
    if __name__ == "__main__":
        print('not implemented')