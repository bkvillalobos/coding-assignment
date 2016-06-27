__author__ = 'brendonvillalobos'
from file_constants import RecFileConstants as rc, TestFileConstants as tc, OutFileConstants as oc
import calc_util as calc
import pandas as pd
import numpy as np
from datetime import datetime

class MetricCalculator():
    """
    TODO: document
    """
    data_folder = 'coding_test_data'
    out_folder = 'target'
    full_rec_filepath = '{base}/recs.txt'.format(base=data_folder)
    full_test_filepath = '{base}/test.txt'.format(base=data_folder)
    subset_rec_filepath = '{base}/rec_subset.tsv'.format(base=data_folder)
    subset_test_filepath = '{base}/bought_subset.tsv'.format(base=data_folder)
    MAX_RECS = len(rc.REC_COLUMNS)

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


    def run(self, rec_df=None, pur_df=None, delimiter='\t', save_transformed_df=False):
        """
        #TODO: document
        :param rec_df:
        :param pur_df:
        :return:
        """
        if not rec_df:
            rec_df = pd.read_csv(self.rec_filepath, sep=delimiter)
        if not pur_df:
            pur_df = pd.read_csv(self.test_filepath, sep=delimiter)

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

        if save_transformed_df:
            # saves dataframe after transformations have been applied to it, as it will be used to calculate metrics
            self._save_intermediate_df(rec_df)
        out_list =[]
        for this_num_recs in reversed(xrange(1, self.MAX_RECS + 1)):
            out_list = [self._recalculate_metrics(rec_df, this_num_recs)] + out_list
        out_df = pd.DataFrame(data=out_list, columns=(oc.NUM_RECS,oc.METRIC_ONE,oc.METRIC_TWO,oc.METRIC_THREE))
        out_df.to_csv('out.tsv', sep=delimiter, index=False)
        print out_df


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
        """
        #TODO: document
        :param num_recs:
        :return:
        """
        self.num_recs = num_recs
        # limit instance's rec column list to number of recs being considered
        self.REC_COLUMNS = rc.REC_COLUMNS[0:num_recs]

    def _recalculate_metrics(self,rec_df, this_num_recs):
        """
        Calculate the results of each metric for this number of recommendations
        :param rec_df: recommendations dataframe
        :param this_num_recs: number of recommendations to be included in this recalculation
        :return: list of output values: this number of recommendations, metric one, metric two, and metric three
        """
        metric_one =  calc.calc_metric_one(rec_df)
        metric_two = calc.calc_metric_two(rec_df, self.num_recs)
        metric_three = calc.calc_metric_three(rec_df, self.num_recs)
        # drop the next least confident recommendation
        rec_df.drop(self.REC_COLUMNS[-1], axis=1, inplace=True)
        self._set_recs(num_recs=this_num_recs - 1)
        # recalculate the total number of purchases each customer made under more restrictive recommendation set
        self.calc_total_purchases(rec_df)
        return [self.num_recs + 1, metric_one, metric_two, metric_three]

    def _save_intermediate_df(self,rec_df):
        """
        Wrapper method for saving dataframe used for metric calculations
        :param rec_df: dataframe to be saved
        :return:
        """
        curr_time = datetime.now()
        date_format='%Y%m%d_%H_%M_%S'
        dt = curr_time.strftime(date_format)
        save_path = '{base}/transformed_df_{dt}.tsv'.format(base=self.out_folder, dt=dt)
        rec_df.to_csv(save_path, sep=self.delimiter, index=False)