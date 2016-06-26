__author__ = 'brendonvillalobos'

import six
import pandas as pd
import numpy as np
from file_constants import RecFileConstants as rc, TestFileConstants as tc

def purchases_to_dict(data, delimiter='\t'):
    """
    # TODO: write description
    :param data: either pd.DataFrame of customer purhcase data or a string path to delimited file containing data
    :param delimiter: character separating values in delimited file
    :return purchase_dict: dictionary with customer ids as keys, a list of purchases as values
                            i.e. {1: ['XXXXXXX', 'YYYYYYY', ...],
                                  2: [...],
                                  ...}
    """
    # read dataframe if data is a path
    if isinstance(data, six.string_types):
        data = pd.read_csv(data, sep=delimiter)

    # list of unique customer ids
    unique_customers = data[tc.CID].unique().sort_values()
    purchase_dict = {}

    # create dictionary entry of purchases for every customer
    for customer in unique_customers:
        purchase_dict[customer] = list(data[data[tc.CID] == customer][tc.PID])

    return purchase_dict

def pid_to_indicator(rec_df, purchase_dict, row_index=0, in_place=True):
    """
    # TODO: document
    :param rec_df:
    :param purchase_dict:
    :param row_index:
    :return:
    """
    customer = rec_df[rc.CID]
    purchases = purchase_dict[customer]
    curr_vals = rec_df.ix[row_index].values
    # turns all recommendation ids into purchase indicator, leaves all other  (non-string) df values alone
    result = [rec if not isinstance(rec,six.string_types)
              else 1 if rec in purchases
              else 0
              for rec in purchases if isinstance(rec, six.string_types)]
    if in_place:
        rec_df.ix[row_index] = result
    else:
        return result

