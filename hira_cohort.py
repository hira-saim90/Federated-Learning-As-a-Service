import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

import missingno as msno
from textwrap import wrap
import matplotlib.pyplot as plt


class Cohort:
    def _init_():
      transaction_df = pd.read_excel('/content/federated-learning-as-a-service1/Cohort_data.xlsx')
# View data
      transaction_df.head()
      msno.bar(transaction_df)
# Inspect missing values in the dataset
      print(transaction_df.isnull().values.sum())
# Replace the ' 's with NaN
      transaction_df = transaction_df.replace(" ",np.NaN)
# Impute the missing values with mean imputation
      transaction_df = transaction_df.fillna(transaction_df.mean())
# Count the number of NaNs in the dataset to verify
      print(transaction_df.isnull().values.sum())
      print(transaction_df.info())
      for col in transaction_df.columns:
    # Check if the column is of object type
          if transaction_df[col].dtypes == 'object':
        # Impute with the most frequent value
              transaction_df[col] = transaction_df[col].fillna(transaction_df[col].value_counts().index[0])

# Count the number of NaNs in the dataset and print the counts to verify
      print(transaction_df.isnull().values.sum())
      msno.bar(transaction_df)
      transaction_df.info()
# A function that will parse the date Time based cohort:  1 day of month
# def get_month(x): return dt.datetime(x.year, x.month, 1) 
# Create transaction_date column based on month and store in TransactionMonth
      transaction_df['TransactionMonth'] = transaction_df['Task_id']
# Grouping by customer_id and select the InvoiceMonth value
      grouping = transaction_df.groupby('Client_id')['TransactionMonth'] 
# Assigning a minimum InvoiceMonth value to the dataset
      transaction_df['CohortMonth'] = grouping.transform('min')
# printing top 5 rows
      print(transaction_df.head())
#  Get the  difference in years
#       years_diff = transcation_year - cohort_year
# # Calculate difference in months
#       months_diff = transaction_month - cohort_month
      # transaction_df['CohortIndex'] = years_diff * 12 + months_diff  + 1 
      # print(transaction_df.head(5))
# Counting daily active user from each chort
      grouping = transaction_df.groupby(['CohortMonth', 'CohortIndex'])
# Counting number of unique customer Id's falling in each group of CohortMonth and CohortIndex
      cohort_data = grouping['Client_id'].apply(pd.Series.nunique)
      cohort_data = cohort_data.reset_index()
 # Assigning column names to the dataframe created above
      cohort_counts = cohort_data.pivot(index='CohortMonth',
                                 columns ='CohortIndex',
                                 values = 'Client_id')
# Printing top 5 rows of Dataframe
      cohort_data.head()
      print(cohort_counts.round(1))
      cohort_sizes = cohort_counts.iloc[:,0]
      retention = cohort_counts.divide(cohort_sizes, axis=0)
# Coverting the retention rate into percentage and Rounding off.
      retention.round(3)*100
# retention.index = retention.index.strftime('%Y-%m')
      retention.index
      pf=retention.head(5)
      pf.plot(kind="bar")
      plt.xlabel('Task Id')
      plt.ylabel('Cohort Index')
