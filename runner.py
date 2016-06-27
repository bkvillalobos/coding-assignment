__author__ = 'brendonvillalobos'
from metric_calculator import MetricCalculator
import argparse

if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Parameterize metric calculation run')
    parser.add_argument('-s', '--save', help= 'Saves intermediate processed DataFrame that is used to calculate metrics',
                        default=False)
    parser.add_argument('-rs', '--run_on_subset', help= 'runs calculations on small subset of only 20 customers',
                        default=False)
    args = parser.parse_args()
    mc = MetricCalculator(run_on_subset=args.run_on_subset)
    mc.run(save_transformed_df=args.save)