#%%
import pandas as pd
import matplotlib.pyplot as plt
#%%
election_data = pd.read_csv('election_data.csv')
# %%
election_2000 = election_data[election_data['year'] == 2000]
election_2004 = election_data[election_data['year'] == 2004]
election_2008 = election_data[election_data['year'] == 2008]
election_2012 = election_data[election_data['year'] == 2012]
election_2016 = election_data[election_data['year'] == 2016]
election_2020 = election_data[election_data['year'] == 2020]
#%%
print(election_data.shape[0])
print(election_2000.shape[0]+election_2004.shape[0]+election_2008.shape[0]+election_2012.shape[0]+election_2016.shape[0]+election_2020.shape[0])
#%%
election_2000.sort_values(by=['county_name'], inplace=True)
election_2004.sort_values(by=['county_name'], inplace=True)
election_2008.sort_values(by=['county_name'], inplace=True)
election_2012.sort_values(by=['county_name'], inplace=True)
election_2016.sort_values(by=['county_name'], inplace=True)
election_2020.sort_values(by=['county_name'], inplace=True)
# %%
winners_2000_series = pd.DataFrame(election_2000.county_name.unique(), columns=['county_name'])
winners_2004_series = pd.DataFrame(election_2004.county_name.unique(), columns=['county_name'])
winners_2008_series = pd.DataFrame(election_2008.county_name.unique(), columns=['county_name'])
winners_2012_series = pd.DataFrame(election_2012.county_name.unique(), columns=['county_name'])
winners_2016_series = pd.DataFrame(election_2016.county_name.unique(), columns=['county_name'])
winners_2020_series = pd.DataFrame(election_2020.county_name.unique(), columns=['county_name'])
#%%
winners_2000_series.insert(1, 'state', '')
winners_2004_series.insert(1, 'state', '')
winners_2008_series.insert(1, 'state', '')
winners_2012_series.insert(1, 'state', '')
winners_2016_series.insert(1, 'state', '')
winners_2020_series.insert(1, 'state', '')
winners_2000_series.insert(2, 'match_country_winner_2000', False)
winners_2004_series.insert(2, 'match_country_winner_2004', False)
winners_2008_series.insert(2, 'match_country_winner_2008', False)
winners_2012_series.insert(2, 'match_country_winner_2012', False)
winners_2016_series.insert(2, 'match_country_winner_2016', False)
winners_2020_series.insert(2, 'match_country_winner_2020', False)
#%%
winners_2000_series.head()
#%%
def county_country_winner(df, overall_winner, winners_series, year):
    current_county = df.iloc[0]['county_name']
    current_state = df.iloc[0]['state']
    print(year)
    for index, row in df.iterrows():
        if (row['county_name'] != current_county):
            winner = df[df['county_name'] == current_county].sort_values(by='candidatevotes', ascending=False).iloc[0]['candidate']
            if (winner == overall_winner):
                winners_series.loc[winners_series['county_name'] == current_county, f'match_country_winner_{year}'] = True
            else:
                winners_series.loc[winners_series['county_name'] == current_county, f'match_country_winner_{year}'] = False
            winners_series.loc[winners_series['county_name'] == current_county, 'state'] = current_state
            current_county = row['county_name']
            current_state = row['state']
    winner = df[df['county_name'] == current_county].sort_values(by='candidatevotes', ascending=False).iloc[0]['candidate']
    if (winner == overall_winner):
        winners_series.loc[winners_series['county_name'] == current_county, f'match_country_winner_{year}'] = True
    else:
        winners_series.loc[winners_series['county_name'] == current_county, f'match_country_winner_{year}'] = False
    winners_series.loc[winners_series['county_name'] == current_county, 'state'] = current_state
    return df
#%%
election_2000 = county_country_winner(election_2000, 'GEORGE W. BUSH', winners_2000_series, 2000)
election_2004 = county_country_winner(election_2004, 'GEORGE W. BUSH', winners_2004_series, 2004)
election_2008 = county_country_winner(election_2008, 'BARACK OBAMA', winners_2008_series, 2008)
election_2012 = county_country_winner(election_2012, 'BARACK OBAMA', winners_2012_series, 2012)
election_2016 = county_country_winner(election_2016, 'DONALD TRUMP', winners_2016_series, 2016)
election_2020 = county_country_winner(election_2020, 'JOSEPH R BIDEN JR', winners_2020_series, 2020)
#%%
winners_2000_series.tail()
# %%
overall_winners = pd.merge(winners_2000_series, winners_2004_series, on=['county_name', 'state'], how='inner')
overall_winners = pd.merge(overall_winners, winners_2008_series, on=['county_name', 'state'], how='inner')
overall_winners = pd.merge(overall_winners, winners_2012_series, on=['county_name', 'state'], how='inner')
overall_winners = pd.merge(overall_winners, winners_2016_series, on=['county_name', 'state'], how='inner')
overall_winners = pd.merge(overall_winners, winners_2020_series, on=['county_name', 'state'], how='inner')
overall_winners.insert(7, 'percentage', 0.0)
#%%
overall_winners.head()
#%%
best_counties = []
best_county_true = 0
for index, row in overall_winners.iterrows():
    county_true = row.apply(lambda x: x == True).sum()
    overall_winners.loc[overall_winners['county_name'] == row['county_name'], 'percentage'] = county_true/6 * 100
#%%
overall_winners = overall_winners.sort_values(by='percentage', ascending=False)
#%%
scores = overall_winners['percentage']
#%%
plt.hist(scores, bins=6, edgecolor='black')
plt.title('Distribution of the accuracy of a county at voting for the general election winner')
plt.ylabel('Number of counties')
plt.xlabel('County Accuracy Percentage')
plt.show()
# %%
#MAKE THIS IN TABLEAU
#%%
election_data.head()
overall_winners.head()
#%%
def get_states_winners(winner_df):
    states = {}
    for index, row in winner_df.iterrows():
        state_true = row.apply(lambda x: x == True).sum()
        if (f'{row['state']}_overall' not in states):
            states[f'{row['state']}_overall'] = 0
            states[f'{row['state']}_true'] = 0
        states[f'{row['state']}_overall'] += 6
        states[f'{row['state']}_true'] += state_true
    return states
# %%
states_overall = get_states_winners(overall_winners)
# %%
print(states_overall)
# %%
state_percentage = {}
for key in states_overall:
    if ('_true' in key):
        state_percentage[key.replace("_true","")] = round(states_overall[key]/states_overall[key.replace('_true', '_overall')] * 100, 2)
# %%
print(state_percentage)
# %%
state_percentage = dict(sorted(state_percentage.items(), key=lambda item: item[1]))
# %%
state_percentage_list = []
for item in state_percentage:
    state_percentage_list.append(state_percentage[item])
state_percentage_list = pd.Series(state_percentage_list)
print(state_percentage_list.describe())
# %%
plt.hist(state_percentage_list, bins=10, edgecolor='black')
plt.title('Distribution of the number of times a state voted for the general election winner')
plt.ylabel('Number of states')
plt.xlabel('Number of times state voted for general election winner')
plt.show()
# %%
print(state_percentage)
# NOW INCLUDING THE INCOME DATA
# %%
income_data = pd.read_csv('income.csv')
#%%
income_data.drop(columns=['FIPS_Code', 'Metro_2013', "Med_HH_Income_Percent_of_State_Total_2021", "Rural_Urban_Continuum_Code_2013", "Urban_Influence_Code_2013"], inplace=True)
income_data.insert(95, 'Average_Unemployment', 0.0)
# %%
income_data.shape[1]
# %%
for index, row in income_data.iterrows():
    current_county = row['Area_Name']
    if ("County" in row['Area_Name']):
        cutoff = row['Area_Name'].index(" County")
        income_data.loc[income_data['Area_Name'] == current_county, 'Area_Name'] = row['Area_Name'][0:cutoff].strip().upper()
    total = 23
    sum_unemp = 0
    for year in range(2000, 2023):
        if (pd.isna(row[f'Unemployment_rate_{year}'])):
            total -= 1
            continue
        sum_unemp += row[f'Unemployment_rate_{year}']
    income_data.loc[income_data['Area_Name'] == current_county, 'Average_Unemployment'] = sum_unemp/total
# %%
income_data.head()
# %%
combined_dataset = pd.merge(overall_winners, income_data, left_on=['county_name'], right_on=['Area_Name'], how='inner').drop(columns=['State', 'match_country_winner_2000', 'match_country_winner_2004', 'match_country_winner_2008', 'match_country_winner_2012', 'match_country_winner_2016', 'match_country_winner_2020', 'Area_Name'])
# %%
combined_dataset.head()
# %%
import seaborn as sns
#%%
heatmap_combined_dataset = combined_dataset.drop(columns=['state', 'county_name'])
for year in range(2000, 2023):
    heatmap_combined_dataset.drop(columns=[f'Unemployment_rate_{year}'], inplace=True)
    heatmap_combined_dataset.drop(columns=[f'Civilian_labor_force_{year}'], inplace=True)
    heatmap_combined_dataset.drop(columns=[f'Employed_{year}'], inplace=True)
    heatmap_combined_dataset.drop(columns=[f'Unemployed_{year}'], inplace=True)
sns.heatmap(heatmap_combined_dataset.corr(), annot=True)
# %%
def get_percent_switch_counties(winners_df, year, party_switch):
    """
    winners_df: DataFrame containing the county winners for each year
    year: The year in which we want to calculate the percentage of counties that switched parties
    party_switch: Boolean indicating if a different party won the election than the won from the previous election (i.e. year - 4)
    """
    if party_switch:
        return ((winners_df[(winners_df[f'match_country_winner_{year}'] == True) & (winners_df[f'match_country_winner_{year-4}'] == True)].shape[0] + 
                 winners_df[(winners_df[f'match_country_winner_{year}'] == False) & (winners_df[f'match_country_winner_{year-4}'] == False)].shape[0])/winners_df.shape[0]) * 100
    else:
        return ((winners_df[(winners_df[f'match_country_winner_{year}'] == True) & (winners_df[f'match_country_winner_{year-4}'] == False)].shape[0] + 
                 winners_df[(winners_df[f'match_country_winner_{year}'] == False) & (winners_df[f'match_country_winner_{year-4}'] == True)].shape[0])/winners_df.shape[0]) * 100
#%%
print("Percentage of                          Change in Average\nCounties Switching Parties:               Unemployment:")
print(f'{get_percent_switch_counties(overall_winners, 2004, False)}                    {income_data.Unemployment_rate_2004.mean() - income_data.Unemployment_rate_2000.mean()}')
print(f'{get_percent_switch_counties(overall_winners, 2008, True) }                    {income_data.Unemployment_rate_2008.mean() - income_data.Unemployment_rate_2004.mean()}')
print(f'{get_percent_switch_counties(overall_winners, 2012, False)}                    {income_data.Unemployment_rate_2012.mean() - income_data.Unemployment_rate_2008.mean()}')
print(f'{get_percent_switch_counties(overall_winners, 2016, True)}                     {income_data.Unemployment_rate_2016.mean() - income_data.Unemployment_rate_2012.mean()}')
print(f'{get_percent_switch_counties(overall_winners, 2020, True)}                     {income_data.Unemployment_rate_2020.mean() - income_data.Unemployment_rate_2016.mean()}')
#%%
income_data.Unemployment_rate_2004.mean()
income_data.Unemployment_rate_2008.mean()
income_data.Unemployment_rate_2010.mean()