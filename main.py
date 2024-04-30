import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

register_matplotlib_converters()
## build dataframes for each data file
df_tesla = pd.read_csv('TESLA Search Trend vs Price.csv')
df_unemployment = pd.read_csv('UE Benefits Search vs UE Rate 2004-19.csv')
df_btc_search = pd.read_csv('Bitcoin Search Trend.csv')
df_btc_price = pd.read_csv('Daily Bitcoin Price.csv')

## check out details of each dataframe 
print(df_tesla.shape)
print(df_tesla)
print(df_tesla.columns)
## find day with highest searches
max_tsla_websearch = df_tesla['TSLA_WEB_SEARCH'].idxmax()
print(df_tesla.loc[max_tsla_websearch])
print(df_tesla.describe())
print(f'Largest value for Tesla in Web Search: {df_tesla.TSLA_WEB_SEARCH.max()}')
print(f'Smallest value for Tesla in Web Search: {df_tesla.TSLA_WEB_SEARCH.min()}')

print(df_unemployment.shape)
print(df_unemployment.columns)
max_ue_websearch = df_unemployment["UE_BENEFITS_WEB_SEARCH"].idxmax()
print(df_unemployment.loc[max_ue_websearch])
print(df_unemployment.describe())
print('Largest value for "Unemployemnt Benefits" '
      f'in Web Search: {df_unemployment.UE_BENEFITS_WEB_SEARCH.max()}')


print(df_btc_search.shape)
print(df_btc_search.columns)
btc_websearch = df_btc_search["BTC_NEWS_SEARCH"].idxmax()
print(df_btc_search.loc[btc_websearch])
print(df_btc_search.describe())
print('Largest value for "Unemployemnt Benefits" '
      f'in Web Search: {df_btc_search.BTC_NEWS_SEARCH.max()}')


print(df_btc_price.shape)
print(df_btc_price.columns)
print(df_btc_search.describe())

## check to see if any of the dataframes have junk data -- these ones are fine
print(f'Missing values for Tesla?: {df_tesla.isna().values.any()}')
print(f'Missing values for U/E?: {df_unemployment.isna().values.any()}')
print(f'Missing values for BTC Search?: {df_btc_search.isna().values.any()}')

## however, the price data for BTC is incomplete
print(f'Missing values for BTC price?: {df_btc_price.isna().values.any()}')

## showing howmany days have missing data
print(f'Number of missing values: {df_btc_price.isna().values.sum()}')
## showing which date has missing data
print(df_btc_price[df_btc_price.CLOSE.isna()])
## update the dataframe to drop the dates with junk data
df_btc_price = df_btc_price.dropna()

## update the date columns to datetime objects
df_tesla['MONTH'] = pd.to_datetime(df_tesla['MONTH'])
print(df_tesla)
df_unemployment['MONTH'] = pd.to_datetime(df_unemployment['MONTH'])
print(df_unemployment)
df_btc_search['MONTH'] = pd.to_datetime(df_btc_search['MONTH'])
print(df_btc_search)
df_btc_price["DATE"] = pd.to_datetime(df_btc_price["DATE"])
print(df_btc_price)
## check to see if the str became a date time object in the date column
print(df_btc_price.DATE.head())

## resample the data to only show the closing at the end of the month instead of daily data points
df_btc_monthly = df_btc_price.resample('M', on="DATE").last()
print(df_btc_monthly)
## resample to show the average over the month instead of the closing
df_btc_monthly = df_btc_price.resample('M', on="DATE").mean()
print(df_btc_monthly)


# Create locators for ticks on the time axis
years = mdates.YearLocator()
months = mdates.MonthLocator()
year_fmt = mdates.DateFormatter('%Y')

# define a graph for the tsla stock price
plt.figure(figsize=(14,8), dpi=120)
plt.title("Tesla Web Search and Stock Price", fontsize=18)
## increasese the font size and rotate the lables
plt.xticks(fintsize=14, rotation=45)

ax1 = plt.gca() ## get the current axis for lefthand y axis
ax2 = ax1.twinx() ## create duplicate for the right hand y axis

ax1.set_ylabel("TSLA Stock Price", color="#E6232E", fontsize=14)
ax2.set_ylabel("Search Trend", color="skyblue", fontsize=14)
## set minimum and maximum values for both x and y axis
ax1.set_ylim([0, 600])
ax1.set_xlim([df_tesla['MONTH'].min(), df_tesla['MONTH'].max()])

ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color="#E6232E", linewidth=3)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color="skyblue", linewidth=3)

## add in the appropriate ticks
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(year_fmt)
ax1.xaxis.set_minor_locator(months)

plt.show()

## bitcoin data graphed

# Create locators for ticks on the time axis
years = mdates.YearLocator()
months = mdates.MonthLocator()
year_fmt = mdates.DateFormatter('%Y')

plt.figure(figsize=(14,8), dpi=120)
plt.title('Bitcoin News Search vs Resampled Price', fontsize=18)

    # Increase the size and rotate the labels on the x-axis
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('BTC Price', color='#E6232E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

    # Set the minimum and maximum values on the axes
ax1.set_ylim(bottom=0, top=1600)
ax1.set_xlim([df_btc_monthly.index.min(), df_btc_monthly.index.max()])

## Updating the linestyle and adding markers
ax1.plot(df_btc_monthly.index, df_btc_monthly.CLOSE, color='#E6232E', linewidth=3, linestyle='--')
ax2.plot(df_btc_monthly.index, df_btc_search.BTC_NEWS_SEARCH, color='skyblue', linewidth=3, marker='o')
## add in the appropriate ticks
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(year_fmt)
ax1.xaxis.set_minor_locator(months)
plt.show()


## unemployment search vs rate graph adding the grid
# Create locators for ticks on the time axis
years = mdates.YearLocator()
months = mdates.MonthLocator()
year_fmt = mdates.DateFormatter('%Y')

plt.figure(figsize=(14,8), dpi=120)
plt.title('Monthly Search of "Unemployment Benefits" in US vs U/E Rate', fontsize=18)

    # Increase the size and rotate the labels on the x-axis
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

    # Set the minimum and maximum values on the axes
ax1.set_ylim(bottom=3, top=11)
ax1.set_xlim([df_unemployment.MONTH.min(), df_unemployment.MONTH.max()])

ax1.grid(color="grey", linestyle="--")

## Updating the linestyle and adding markers
ax1.plot(df_unemployment.MONTH, df_unemployment.UNRATE, color='purple', linewidth=3, linestyle='--')
ax2.plot(df_unemployment.MONTH, df_unemployment.UE_BENEFITS_WEB_SEARCH, color='skyblue', linewidth=3)
## add in the appropriate ticks
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(year_fmt)
ax1.xaxis.set_minor_locator(months)
plt.show()

## unemployment rates with Rolling average

plt.figure(figsize=(14,8), dpi=120)
plt.title('Rolling Monthly US "Unemployment Benefits" Web Searches vs UNRATE', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)
     
ax1 = plt.gca()
ax2 = ax1.twinx()
     
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(year_fmt)
ax1.xaxis.set_minor_locator(months)
     
ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=16)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=16)
     
ax1.set_ylim(bottom=3, top=10.5)
ax1.set_xlim([df_unemployment.MONTH[0], df_unemployment.MONTH.max()])
     
    # Calculate the rolling average over a 6 month window
roll_df = df_unemployment[['UE_BENEFITS_WEB_SEARCH', 'UNRATE']].rolling(window=6).mean()
     
ax1.plot(df_unemployment.MONTH, roll_df.UNRATE, 'purple', linewidth=3, linestyle='-.')
ax2.plot(df_unemployment.MONTH, roll_df.UE_BENEFITS_WEB_SEARCH, 'skyblue', linewidth=3)
     
plt.show()


## unemployment rates in only 2020
df_ue_2020 = pd.read_csv('UE Benefits Search vs UE Rate 2004-20.csv')
df_ue_2020.MONTH = pd.to_datetime(df_ue_2020.MONTH)

plt.figure(figsize=(14,8), dpi=120)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)
plt.title("Monthly Search in US of 'Unemployment Benefits' and US U/E Rate in 2020", fontsize=18)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel("FRED U/E Rate", color='purple', fontsize=16)
ax2.set_ylabel("Search Trend", color='skyblue', fontsize=16)

ax1.set_xlim([df_ue_2020.MONTH.min(), df_ue_2020.MONTH.max()])

ax1.plot(df_ue_2020.MONTH, df_ue_2020.UNRATE, color='purple', linewidth=3)
ax2.plot(df_ue_2020.MONTH, df_ue_2020.UE_BENEFITS_WEB_SEARCH, color='skyblue', linewidth=3)
plt.show()