__author__ = 'brendonvillalobos'

import six
import pandas as pd
import numpy as np
from file_constants import RecFileConstants as rc, TestFileConstants as tc

def purchases_to_dict(data, delimiter='\t'):
    """
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
