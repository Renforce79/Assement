import pandas as pd

class test_dataframe:
    def __init__(self, df, n):
        self.df = df
        self.n = n
    
    def test(self):
        # Define the critical columns that cannot have null values
        critical_cols = ['Ad group ID', 'Ad ID', 'Customer','Gregorian date', 'Account number']

        # Verify that the critical columns do not have null values
        nulls = self.df[critical_cols].isnull().sum().sum()
        if nulls > 0:
            raise ValueError('Error: The dataframe has {} null values in the critical columns'.format(nulls))

        # Verify that the number of columns does not exceed 36
        num_cols = len(self.df.columns)
        if num_cols > self.n:
            raise ValueError('Error: The dataframe has {} columns, which exceeds the maximum limit of 36'.format(num_cols))


