__author__ = 'brendonvillalobos'
from file_constants import RecFileConstants as rc, TestFileConstants as tc
import pandas as pd

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
            self.full_test_filepath = MetricCalculator.subset_test_filepath


    def run(self, rec_df=None, pur_df=None):
        """
        #TODO: document
        :param rec_df:
        :param pur_df:
        :return:
        """
        rec_df = pd.read_csv()

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