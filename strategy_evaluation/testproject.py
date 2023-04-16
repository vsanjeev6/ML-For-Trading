"""
Student Name: Vaishnavi Sanjeev
GT User ID: vsanjeev6
GT ID: 903797718

Code implementing testproject.py
"""

import experiment1 as exp1
import experiment2 as exp2
import ManualStrategy as ms

def author():
    return 'vsanjeev6'

def run():
    # Generates charts for Manual Strategy
    ms.test_code(symbol="JPM", sv=100000)
    # Run Experiment 1
    exp1.test_code()
    # Run Experiment 2
    exp2.test_code()

if __name__ == "__main__":
    run()
