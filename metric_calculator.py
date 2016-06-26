__author__ = 'brendonvillalobos'
from file_constants import RecFileConstants as rc, TestFileConstants as tc
import pandas

class MetricCalculator():
    """
    TODO: document
    """
    def __init__(self):
        self._set_recs()

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