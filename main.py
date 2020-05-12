import matplotlib
import matplotlib.pyplot as plt
from jedi.refactoring import inline
import pandas as pd
from datetime import timedelta, datetime
import numpy as np
from sklearn.linear_model import LinearRegression


def combine_state(country):
    """
    Summing the confirmed number of different states in a country into total number
    :param country: the country data with states
    :return: the combined country data
    """
    data_by_country = data[data['Country/Region'] == country]
    data_by_country = pd.DataFrame(data_by_country.groupby(['ObservationDate']).sum())
    data_by_country['ObservationDate'] = data_by_country.index
    return data_by_country


def extract_country(data, country_name):
    """
    Extract certain country from the world dataset
    :param data: the world dataset
    :param country_name: the country name that you want to extract
    :return: the extract country data

    >>> data = pd.read_csv('./data/covid_19_data.csv')
    >>> Japan = extract_country(data, 'Japan')
    >>> np.unique(Japan['Country/Region'])[0]
    'Japan'
    """
    country = data[data['Country/Region'] == country_name]
    country = country.reset_index()
    return country


def calculate_start_outbreak_date(country):
    """
    Automatically calculate when does the COVID-19 started to outbreak at the certain country
    :param country: the country data
    :return: the outbreak date
    """
    rate = 0
    i = 0
    while rate < 10:
        today = country['ObservationDate'][i]
        tomorrow = today + timedelta(1)
        tomorrow = tomorrow.strftime('%Y/%m/%d')

        today_confirmed = country['Confirmed'][country['ObservationDate'] == today]
        tomorrow_confirmed = country['Confirmed'][country['ObservationDate'] == tomorrow]

        rate = int(tomorrow_confirmed) - int(today_confirmed)
        i += 1
    return country['ObservationDate'][i]


def fit_regression(X_data, y):
    """
    Helper function of fitting regression, return score and coefficient
    :param X_data: the data that use to predict
    :param y: the response data
    :return: the score of this fit and the slope

    >>> X_data = 5
    >>> y = [1, 2, 3, 4, 5]
    >>> score, slope = fit_regression(X_data, y)
    >>> print(slope)
    1.0
    >>> print(score)
    1.0
    """
    X = [i for i in range(X_data)]
    v = np.ones((X_data, 1))
    X = np.c_[v, X]
    reg = LinearRegression().fit(X, y)
    return reg.score(X, y), reg.coef_[1]


def calculate_rate(country, start_date, end_date):
    """
    Calculate the given country's increasing rate of COVID-19 confirmed number, in the given period
    :param country: the data of the country
    :param start_date: the start date of this regression fit
    :param end_date: the end date of this regression fit
    """
    country = country[country['ObservationDate'] > start_date]
    country = country[country['ObservationDate'] <= end_date]

    score, rate = fit_regression(country.shape[0], country['Confirmed'])

    print('Accuracy:', score, '%')
    print('rate:', rate)


if __name__ == '__main__':
    # Read Data
    data = pd.read_csv('./data/covid_19_data.csv')
    # convert string into date
    data['ObservationDate'] = pd.to_datetime(data['ObservationDate'])

    #read in google trend data
    world_mask = pd.read_csv('./data/world_mask.csv')
    world_mask['天'] = pd.to_datetime(world_mask['天'])
    italy_mask = pd.read_csv('./data/italy_mask.csv')
    italy_mask['天'] = pd.to_datetime(italy_mask['天'])

    #extract different countries data
    US = combine_state('US')
    France = combine_state('France')
    Japan = extract_country(data, 'Japan')
    Italy = extract_country(data, 'Italy')
    Korea = extract_country(data, 'South Korea')
    Taiwan = extract_country(data, 'Taiwan')
    Germany = extract_country(data, 'Germany')
    UK = extract_country(data, 'UK')
    Poland = extract_country(data, 'Poland')

    germany_mask = world_mask[['天', 'masque: (法國)']]
    korea_mask = world_mask[['天', '마스크: (南韓)']]

    #Germany
    plt.figure(figsize=(10, 8))
    plt.plot(Germany['ObservationDate'], Germany['Confirmed'])
    plt.title('Germany COVID-19 confirmed number')
    plt.xlabel('date')
    plt.ylabel('confirmed number')
    plt.show()

    plt.figure(figsize=(10, 8))
    plt.plot(germany_mask['天'], germany_mask['masque: (法國)'])
    plt.title('Germany search masque(mask) google trend')
    plt.xlabel('date')
    plt.ylabel('search count')
    plt.show()

    outbreak_date = calculate_start_outbreak_date(Germany)
    print('outbreak at:', outbreak_date)

    calculate_rate(Germany, outbreak_date, '2020/04/10')
    calculate_rate(Germany, '2020/04/10', '2020/05/04')

    #Korea
    plt.figure(figsize=(10, 8))
    plt.plot(Korea['ObservationDate'], Korea['Confirmed'])
    plt.title('South Korea COVID-19 confirmed number')
    plt.xlabel('date')
    plt.ylabel('confirmed number')
    plt.show()

    plt.figure(figsize=(10, 8))
    plt.plot(korea_mask['天'], korea_mask['마스크: (南韓)'])
    plt.title('South Korea search mask google trend')
    plt.xlabel('date')
    plt.ylabel('search count')
    plt.show()

    outbreak_date = calculate_start_outbreak_date(Korea)
    print('outbreak at:', outbreak_date)

