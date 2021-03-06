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
    unique_customers = data[tc.CID].unique()
    unique_customers.sort()
    purchase_dict = {}

    # create dictionary entry of purchases for every customer
    for customer in unique_customers:
        purchase_dict[customer] = list(data[data[tc.CID] == customer][tc.PID])

    return purchase_dict

def calc_purs_not_recommended(rec_df, purchase_dict, row_index=0, in_place=True):
    """
    # TODO: document
    :param rec_df:
    :param purchase_dict:
    :param row_index:
    :param in_place:
    :return:
    """
    customer = rec_df.loc[row_index,rc.CID]
    if customer in purchase_dict:
        purchases = purchase_dict[customer]
        curr_vals = rec_df.ix[row_index].values
        purchases_recommended = sum([1 if rec in purchases else 0 for rec in curr_vals if isinstance(rec, six.string_types)])
        total_purchases = len(purchases)
        result = total_purchases - purchases_recommended
    else:
        # if a customer is not in the purchase dictionary, then they have made zero purchases
        result = 0
    if in_place:
        rec_df.loc[row_index, rc.NOT_RECD] = result
    else:
        return result

def pid_to_indicator(rec_df, purchase_dict, row_index=0, in_place=True):
    """
    # TODO: document
    :param rec_df:
    :param purchase_dict:
    :param row_index:
    :param in_place:
    :return:
    """
    customer = rec_df.loc[row_index, rc.CID]
    purchases = purchase_dict[customer]
    curr_vals = rec_df.ix[row_index].values
    # turns all recommendation ids into purchase indicator, leaves all other  (non-string) df values alone
    result = [rec if not isinstance(rec,six.string_types)
              else 1 if rec in purchases
              else 0
              for rec in curr_vals]
    if in_place:
        rec_df.ix[row_index] = result
    else:
        return result

def calc_metric_one(rec_df):
    """
    Calculates the proportion of customers who purchased at least one recommendation
    # TODO: document
    :param rec_df:
    :return:
    """
    num_customers = len(rec_df[rc.CID].unique())
    who_purchased_rec = len(rec_df[rec_df[rc.TOTAL_PUR] > rec_df[rc.NOT_RECD]])
    return float(who_purchased_rec) / num_customers

def calc_metric_two(rec_df, num_recs):
    """
    Calculates precision (number of purchased recommendations / number of given recommendations)
    #TODO: document
    :param rec_df:
    :return:
    """
    # number of recommended purchases = total purchases - number of purchases not recommended
    num_customers = len(rec_df[rc.CID].unique())
    purchased_recs = sum(rec_df[rc.TOTAL_PUR]) - sum(rec_df[rc.NOT_RECD])
    return float(purchased_recs) / (num_recs*num_customers)

def calc_metric_three(rec_df, num_recs):
    """
    Calculates recall (number of purchased recommendations / number of purchases)
    #TODO: document
    :param rec_df:
    :param num_recs:
    :return:
    """
    total_purchased = sum(rec_df[rc.TOTAL_PUR])
     # number of recommended purchases = total purchases - number of purchases not recommended
    purchased_recs = total_purchased - sum(rec_df[rc.NOT_RECD])
    return float(purchased_recs) / total_purchased


