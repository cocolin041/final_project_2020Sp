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

    US = combine_state('US')
    France = combine_state('France')
    Japan = extract_country(data, 'Japan')
    Italy = extract_country(data, 'Italy')
    Korea = extract_country(data, 'South Korea')
    Taiwan = extract_country(data, 'Taiwan')
    Germany = extract_country(data, 'Germany')
    UK = extract_country(data, 'UK')
    Poland = extract_country(data, 'Poland')

    #Germany
    plt.figure(figsize=(10, 8))
    plt.plot(Germany['ObservationDate'], Germany['Confirmed'])
    plt.show()

    outbreak_date = calculate_start_outbreak_date(Germany)
    print('outbreak at:', outbreak_date)

    calculate_rate(Germany, outbreak_date, '2020/04/10')
    calculate_rate(Germany, '2020/04/10', '2020/05/04')

    #US
    plt.figure(figsize=(10, 8))
    plt.plot(US.index, US['Confirmed'])
    plt.show()

    outbreak_date = calculate_start_outbreak_date(US)
    print('outbreak at:', outbreak_date)

    #Italy
    plt.figure(figsize=(10, 8))
    plt.plot(Italy['ObservationDate'], Italy['Confirmed'])
    plt.show()

    outbreak_date = calculate_start_outbreak_date(Italy)
    print('outbreak at:', outbreak_date)

    #Korea
    plt.figure(figsize=(10, 8))
    plt.plot(Korea['ObservationDate'], Korea['Confirmed'])
    plt.show()

    outbreak_date = calculate_start_outbreak_date(Korea)
    print('outbreak at:', outbreak_date)

    #Taiwan
    plt.figure(figsize=(10, 8))
    plt.plot(Taiwan['ObservationDate'], Taiwan['Confirmed'])
    plt.show()

    outbreak_date = calculate_start_outbreak_date(Taiwan)
    print('outbreak at:', outbreak_date)

    #France
    plt.figure(figsize=(10, 8))
    plt.plot(France['ObservationDate'], France['Confirmed'])
    plt.show()

    outbreak_date = calculate_start_outbreak_date(France)
    print('outbreak at:', outbreak_date)


