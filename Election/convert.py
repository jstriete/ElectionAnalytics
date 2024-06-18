#%%
import pandas as pd
data_xls = pd.read_excel('../Election/Unemployment.xlsx', dtype=str, index_col=None)
data_xls.to_csv('income.csv', encoding='utf-8', index=False)
# %%
