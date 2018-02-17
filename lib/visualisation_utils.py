"""
Jake Forsey
12/02/2018

Functions that visualise data
"""

import logging
import math

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import pandas as pd

plt.style.use('seaborn-white')


def plot_word_counts(data_frame, columns):
    """
    Plots the distribution of the number of words for each column in columns

    :param data_frame: <pandas.DataFrame>
    :param columns: <list> list of columns to create plots for
    :return: None
    """
    fig, axes = plt.subplots(nrows=int(math.ceil(len(columns)/2)), ncols=2)

    for axis, column in zip(axes.flatten(), columns):
        number_of_characters = data_frame[column].str.split().str.len()

        number_of_characters.hist(ax=axis, color='m', figsize=(8, 8), bins=15, alpha=0.5)

        axis.set_xlabel('No. of words in {}'.format(column))
        axis.set_ylabel('Frequency')

    plt.tight_layout()
    plt.savefig('visualisations/{}.png'.format('Word counts for columns {}'.format(', '.join(columns))))


def plot_category_balance(data_frame, column, title):
    """
    Plots the number of records in data_frame for each category in column

    :param data_frame: <pandas.DataFrame>
    :param column: <str> column name found in data_frame
    :param title: <str> title of log and plot
    :return: None
    """
    counts_series = data_frame[column].value_counts()

    logging.debug("""{}:
{}""".format(title, counts_series))

    fig, axis = plt.subplots(nrows=1, ncols=1)

    counts_series.plot(ax=axis, kind='bar', color='m', figsize=(8, 8), alpha=0.5)

    axis.set_xlabel('Category in {}'.format(column))
    axis.set_ylabel('Frequency')

    plt.tight_layout()
    plt.savefig('visualisations/{}.png'.format(title))


def plot_date_range(data_frame):
    """
    Plot the number of records in each month based on the sparse date_added column

    :param data_frame: <pandas.DataFrame>
    :return: None
    """
    fig, axis = plt.subplots(nrows=1, ncols=1)

    # plot the distribution of yearly salaries
    data_frame = pd.DataFrame({'date_added': data_frame['date_added'],
                               'count': [1 for _ in range(len(data_frame))]})
    data_frame.set_index('date_added', inplace=True)
    data_frame = data_frame['count'].resample('M').sum()

    data_frame.plot(ax=axis, color='m', alpha=0.5)

    axis.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
    axis.set_ylabel('No. of job postings/month')

    plt.tight_layout()
    plt.savefig('visualisations/Number of job postings time-series (sparse data).png')


def plot_salary_distribution(data_frame, hours_per_year):
    """
    Plot distributions of salaries in multiple combinations

    :param data_frame: <pandas.DataFrame>
    :param hours_per_year: <int> assumption for the number of hours worked in a year
    :return: None
    """
    logging.debug("""Salary statistics:
{}""".format(data_frame.describe()))

    fig, axes = plt.subplots(nrows=2, ncols=2)
    axes = axes.flatten()

    # plot the distribution of yearly salaries
    axes[0].hist(data_frame['avg_yearly_salary'].dropna().values,
                 color='b', alpha=0.5, range=(0, 200000), bins=15, label='avg_yearly_salary')

    # plot the distribution of hourly salaries
    axes[1].hist(data_frame['avg_hourly_salary'].dropna(),
                 color='m', alpha=0.5, range=(0, 100), bins=15, label='avg_hourly_salary')

    # plot the distribution of yearly salaries combined with hourly salaries after standardisation
    axes[2].hist(data_frame['avg_yearly_salary'].dropna().values,
                 color='b', alpha=0.5, range=(0, 200000), bins=15, label='avg_yearly_salary')

    axes[2].hist(data_frame['avg_hourly_salary'].dropna().apply(lambda x: x * hours_per_year),
                 color='m', alpha=0.5, range=(0, 200000), bins=15, label='avg_hourly_salary')

    # plot standardised salaries combined
    axes[3].hist(data_frame['standardised_salary'].dropna().values,
                 color='r', alpha=0.5, range=(0, 200000), bins=15, label='standardised_salary')

    axes[0].set_xlabel('Yearly salary ($)')
    axes[0].set_ylabel('Frequency')

    axes[1].set_xlabel('Hourly salary ($)')
    axes[1].set_ylabel('Frequency')

    axes[2].set_xlabel('Yearly salary ($)')
    axes[2].set_ylabel('Frequency')

    axes[3].set_xlabel('Yearly salary ($)')
    axes[3].set_ylabel('Frequency')

    plt.tight_layout()
    plt.savefig('visualisations/Salary distribution.png')
