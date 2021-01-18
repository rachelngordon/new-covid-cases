import pandas as pd
import matplotlib.pyplot as plt

# read in the csv file
covid_data=pd.read_csv('owid-covid-data.csv')

# Visualize the total number of new cases by month (through and including October 2020) over time by continent. 
## side by side bar chart

# creates a list of continent names and a dictionary of months and their number of days for January through October
continents=['Asia','Europe','Africa','North America','South America','Australia']
jan_oct={'01':31, '02':28, '03':31, '04':30, '05':31, '06':30, '07':31, '08':31, '09':30, '10':31}

# function to create a new dataframe for a given continent
def continent_df(continent):
    continent_df=covid_data[covid_data.continent.isin([continent])]
    return continent_df

# calculates the total new cases in a given month for a given dataframe
def monthly_new_cases(df, month, num_days):
    month_dates=pd.date_range(month+'/01/2020', periods=num_days, freq='D')
    month_dates=month_dates.strftime('%Y-%m-%d')
    month=df[df.date.isin(month_dates)]
    new_cases=month['new_cases'].sum()
    return new_cases

# creates a list of monthly new cases on a given continent for January through October
def continent_cases(continent):
    continent_cases=[]
    for month in jan_oct:
        continent_cases.append(monthly_new_cases(continent_df(continent), month, jan_oct[month]))
    return continent_cases

# list of month names for use in dataframe indices and labeling x-axis 
month_names=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# creates a dictionary for continents and their list of monthly new cases
continent_data={continent:continent_cases(continent) for continent in continents}

# creates a pandas dataframe from the dictionary of continents and their monthly new cases with the month names from January through October as the indices
plot1data=pd.DataFrame(
    continent_data,
    index=month_names[0:10]
)

# plots the dataframe with title and axis labels and saves it to a png file
fig=plt.figure()
plot=plot1data.plot(kind="bar")
plot.set_title("New Cases Per Month By Continent")
plot.set_xlabel("Month")
plot.set_ylabel("# New Cases")
plt.savefig('Plot1.png', dpi=400, bbox_inches='tight')

# Visualize the contribution of each country to the monthly number of new cases for European countries (through and including October 2020).
## stacked bar chart

# creates a dataframe for covid data in Europe
Europe=continent_df('Europe')

# list of European countries being considered
European_countries=["Italy", "France", "Spain", "United Kingdom", "Russia", "Other"]

# function to create a new dataframe for a given country or "Other", which includes all European countries not listed in European_countries
def country_df(country):
    if country == "Other":
        country_df=Europe[~Europe.location.isin(European_countries)]
    else:
        country_df=covid_data[covid_data.location.isin([country])]
    return country_df

# function to calculate monthly cases for a given country
def country_cases(country):
    country_cases=[]
    for month in jan_oct:
        country_cases.append(monthly_new_cases(country_df(country), month, jan_oct[month]))
    return country_cases

# creates a dictionary for countries and their list of monthly new cases
countries_data={country:country_cases(country) for country in European_countries}

# creates a pandas dataframe from the dictionary of countries and their monthly new cases with the month names from January through October as the indices
plot2data=pd.DataFrame(
    countries_data,
    index=month_names[0:10]
)

# plots the dataframe with title and axis labels and saves it to a png file
fig=plt.figure()
plot=plot2data.plot(kind="bar", stacked=True)
plot.set_title("Monthly New Cases for European Countries")
plot.set_xlabel("Month")
plot.set_ylabel("# New Cases")
plt.savefig('Plot2.png', dpi=400, bbox_inches='tight')

# Visualize the daily number of new cases relative to their individual populations over time for Sweden, Norway, Denmark, and Finland.
## line graph

# list of Sweden and neighboring countries
Sweden_neighbors=['Sweden', 'Norway', 'Denmark', 'Finland']

# function to calculate the ratio of daily new cases to total population in millions
def daily_country_cases(country):
    country_data=covid_data[covid_data.location.isin([country])]
    # resets the index so that indices of each dataframe are the same when plotting
    country_data=country_data.reset_index(drop=True)
    cases_ratio=country_data['new_cases']/(country_data['population']/1000000)
    return cases_ratio

# creates a figure for plotting the data
fig=plt.figure()
ax=fig.subplots()

# plots each dataframe for daily new cases as a separate line in a separate color
for country in Sweden_neighbors:
    plt.plot(daily_country_cases(country), linestyle='solid')

# creates a key with the list of countries
ax.legend(Sweden_neighbors, loc='best')

# title and axis labels
ax.set_title("Daily New Cases Over Time for Sweden, Norway, Denmark, and Finland")
ax.set_xlabel("# Days Since 12/31/2020")
ax.set_ylabel("# New Cases Divided by Total Population in Millions")

# saves the plot to a png file
plt.savefig('Plot3.png', dpi=400, bbox_inches='tight')
