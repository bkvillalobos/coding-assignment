__author__ = 'brendonvillalobos'

class RecFileConstants:
    """
    #TODO: document
    """
    # file column names, only needs to be changed here if they ever change
    CID = 'customer_id'
    ONE ='1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    NOT_RECD = 'num_purs_not_recommended'
    TOTAL_PUR = 'total_purchased'
    REC_COLUMNS = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN]

    def __init__(self, num_recs=10):
        # limit instance's rec column list to number of recs being considered
        self.REC_COLUMNS = RecFileConstants.REC_COLUMNS[0:num_recs]

class TestFileConstants:
    """
    #TODO: document
    """
    CID = 'customer_id'
    PID = 'product_id'