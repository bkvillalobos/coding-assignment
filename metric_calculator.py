__author__ = 'brendonvillalobos'
from file_constants import RecFileConstants as rc, TestFileConstants as tc
import calc_util as calc
import pandas as pd
import numpy as np

class MetricCalculator():
    """
    TODO: document
    """
    data_folder = 'coding_test_data'
    full_rec_filepath = '{base}/recs.txt'.format(base=data_folder)
    full_test_filepath = '{base}/test.txt'.format(base=data_folder)
    subset_rec_filepath = '{base}/rec_subset.tsv'.format(base=data_folder)
    subset_test_filepath = '{base}/bought_subset.tsv'.format(base=data_folder)

    def __init__(self, rec_path=full_rec_filepath, test_path=full_test_filepath, run_on_subset=False):
        """
        #TODO: document
        :param rec_path:
        :param test_path:
        :param run_on_subset:
        :return:
        """
        self._set_recs()
        # run calculations on subset of data I created, much quicker and easier to inspect the results
        if run_on_subset:
            self.rec_filepath = MetricCalculator.subset_rec_filepath
            self.test_filepath = MetricCalculator.subset_test_filepath


    def run(self, rec_df=None, pur_df=None):
        """
        #TODO: document
        :param rec_df:
        :param pur_df:
        :return:
        """
        if not rec_df:
            rec_df = pd.read_csv(self.rec_filepath)
        if not pur_df:
            pur_df = pd.read_csv(self.test_filepath)

        # create dictionary of every purchase each customer has made
        pur_dict = calc.purchases_to_dict(pur_df)
        del pur_df

        # add columns to rec_df for number of purchases that weren't recommended, and total number of purchases
        rec_df[rc.NOT_RECD] = np.nan
        rec_df[rc.TOTAL_PUR] = np.nan

        # iterate through rows of recommendations dataframe
        # can be done as an apply function, but a for loop is much less expensive computationally
        for ix in rec_df.index:
            # calculate the number of purchases that weren't recommended for this customer
            calc.calc_purs_not_recommended(rec_df=rec_df, purchase_dict=pur_dict, row_index=ix)
            # this customer's recommendations' product ids into indicator: 1 = they bought it, 0 = they didn't
            calc.pid_to_indicator(rec_df=rec_df, purchase_dict=pur_dict, row_index=ix)
        del pur_dict

        # calculate the total number of purchases each customer made
        self.calc_total_purchases(rec_df)

        # calculate the results of each metric for this number of recommendations
        print self.num_recs
        print calc.calc_metric_one(rec_df)
        print calc.calc_metric_two(rec_df, self.num_recs)
        print calc.calc_metric_three(rec_df, self.num_recs)


    def calc_total_purchases(self, rec_df, in_palce=True):
        """
        #TODO: document
        :param rec_df:
        :param in_palce:
        :return:
        """
        purchase_columns = self.REC_COLUMNS + [rc.NOT_RECD]
        result = rec_df[purchase_columns].sum(axis=1)
        if in_palce:
            rec_df[rc.TOTAL_PUR] = result
        else:
            return result

    def _set_recs(self, num_recs=10):
        self.num_recs = num_recs
        # limit instance's rec column list to number of recs being considered
        self.REC_COLUMNS = rc.REC_COLUMNS[0:num_recs]