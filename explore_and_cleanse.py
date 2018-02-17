"""
Data exploration and cleansing script for the 'US jobs on Monster.com' data found at:
https://www.kaggle.com/residentmario/exploring-monster-com-job-postings/data
"""

import logging

import pandas as pd

from lib.argument_parsers import explore_and_cleanse_argument_parser
from lib import cleansing_utils
from lib import visualisation_utils

# assumptions used to standardise hourly salaries
HOURS_PER_WEEK = 40
WEEKS_PER_YEAR = 52
WEEKS_VACATION_PER_YEAR = 5

HOURS_WORKED_PER_YEAR = HOURS_PER_WEEK * (WEEKS_PER_YEAR - WEEKS_VACATION_PER_YEAR)


def main(data):
    """
    Loads the raw data (--data) and produces a cleansed data set (data/cleansed_data.csv) also creates
    relevant logs and visualisations

    :param data: <str> file path to monster job listings
    :return: None
    """

    logging.info('Loading csv: {}'.format(data))
    data_frame = pd.read_csv(data)
    logging.info('Number of rows in data: {}'.format(len(data)))

    # log some basic data quality metrics
    logging.debug("""No. of non-null records:
{}""".format(data_frame.count()))

    logging.debug("""No. of unique values:
{}""".format(data_frame.nunique()))

    # drop the columns which only contain a single value (country, country_code etc.)
    data_frame = cleansing_utils.drop_uniform_columns(data_frame)

    # drop all the rows (but one) where the id and url are the only differentiating columns
    data_frame = cleansing_utils.drop_duplicate_rows(data_frame)

    # plot the number of words in the key text columns
    visualisation_utils.plot_word_counts(data_frame, columns=['job_description', 'job_title',
                                                              'job_type', 'sector',
                                                              'location', 'organization'])

    # format dates uniformly
    #   input is a string         [format = %m/%d/%Y with and without zero padding]
    #   output is datetime object [default format = %d/%m/%Y with zero padding]
    # TODO consider creating cleansing_utils function for logging
    data_frame['date_added'] = pd.to_datetime(data_frame['date_added'], format='%m/%d/%Y')
    visualisation_utils.plot_date_range(data_frame)

    logging.info('First date: {}'.format(data_frame['date_added'].min()))
    logging.info('Last date: {}'.format(data_frame['date_added'].max()))

    # aggregate job_type column to 'Full Time', 'Part Time' or 'Other'
    data_frame = cleansing_utils.standardise_job_type(data_frame)
    visualisation_utils.plot_category_balance(data_frame, 'job_type', 'Cleansed job_type balance')

    # extract salary ranges and save the mid points of the range, also create a
    # standardised salary column using an hours per year assumption
    data_frame = cleansing_utils.standardise_salaries(data_frame, HOURS_WORKED_PER_YEAR)
    visualisation_utils.plot_salary_distribution(data_frame, HOURS_WORKED_PER_YEAR)

    data_frame.to_csv('data/cleansed_data.csv', index=False)


if __name__ == '__main__':

    arguments = explore_and_cleanse_argument_parser().parse_args()
    logging.basicConfig(level=arguments.logging_level)

    main(data=arguments.data)
