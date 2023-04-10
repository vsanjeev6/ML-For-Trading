import experiment1 as ex1
import experiment2 as ex2
import ManualStrategy as ms

def author():
    return "pcometti3"  # replace tb34 with your Georgia Tech username

def run():
    ms.test_code(symbol="JPM", sv=100000)
    ex1.test_code()
    ex2.test_code()

if __name__ == "__main__":
    run()
