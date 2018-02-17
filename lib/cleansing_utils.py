"""
Jake Forsey
11/02/2018

Functions to filter, aggregate and standardise data
"""

import logging

import numpy as np
import pandas as pd


def drop_uniform_columns(data_frame):
    """
    Drops all columns of a pandas.DataFrame which contain only a
    single value as these columns can add no value to data analysis

    :param data_frame: <pandas.DataFrame>
    :return: <pandas.DataFrame>
    """
    # save all the original columns
    original_columns = set(data_frame.columns)

    # delete all the columns where there is only a single value
    data_frame = data_frame.loc[:, data_frame.nunique() != 1]

    logging.warning('Deleting columns: {}'.format(original_columns - set(data_frame.columns)))

    return data_frame


def drop_duplicate_rows(data_frame, columns_to_ignore=('page_url', 'uniq_id')):
    """
    Drop records which have duplicated content

    :param data_frame: <pandas.DataFrame>
    :param columns_to_ignore: <list> list of columns to ignore when assess duplication
    :return: <pandas.DataFrame>
    """
    # save the number of records before dropping duplications
    original_number_of_records = len(data_frame)

    logging.info('Dropping duplicate records ignoring columns: {}'.format(columns_to_ignore))

    # drop records if they only differentiating columns are columnes_to_ignore
    data_frame = data_frame.drop_duplicates(subset=list(set(data_frame.columns) - set(columns_to_ignore)))

    logging.warning('Duplicate records dropped: {}'.format(original_number_of_records - len(data_frame)))

    return data_frame


def standardise_job_type(data_frame):

    def aggregate_job_types(job_type):
        # if the job type is null then return null
        if pd.isnull(job_type):
            return job_type

        if 'Full Time' in job_type:
            aggregated_job_type = 'Full Time'
        elif 'Part Time' in job_type:
            aggregated_job_type = 'Part Time'
        else:
            aggregated_job_type = 'Other'

        return aggregated_job_type

    data_frame['job_type'] = data_frame['job_type'].map(aggregate_job_types)

    return data_frame


def standardise_salaries(data_frame, hours_per_year):
    """
    Parse out the minimum, maximum salary to calculate average salary for the job postings

    Code based on Aleksey Bilogur's code found here:
        https://www.kaggle.com/residentmario/exploring-monster-com-job-postings/notebook

    :param data_frame: <pandas.DataFrame>
    :param hours_per_year: <int> assumption for the number of hours worked in a year
    :return: <pandas.DataFrame> updated with 2 new columns (avg_yearly_salary, avg_hourly_salary)
    """
    def map_avg_yearly_salary(salary):
        if pd.isnull(salary):
            return np.nan

        elif "/year" in salary:
            salary = salary.split("/year")[0].replace("$", " ").strip()
            if "-" in salary:
                min_salary, max_salary = salary.split("-")[0:2]
                try:
                    min_salary = float(min_salary.replace(",", "").strip())
                    max_salary = float(max_salary.replace(",", "").strip())
                except:
                    return np.nan
                return min_salary + (max_salary - min_salary) / 2

    def map_avg_hourly_salary(salary):
        if pd.isnull(salary):
            return np.nan

        elif "/hour" in salary:
            salary = salary.split("/hour")[0].replace("$", " ").strip()
            if "-" in salary:
                min_salary, max_salary = salary.split("-")[0:2]
                try:
                    min_salary = float(min_salary.replace(",", "").strip())
                    max_salary = float(max_salary.replace(",", "").strip())
                except:
                    return np.nan

                return min_salary + (max_salary - min_salary) / 2

    def combine_salaries(salaries, hours_per_year):
        yearly_salary = salaries[0]
        hourly_salary = salaries[1]

        if pd.isnull(yearly_salary) and pd.isnull(hourly_salary):
            return np.nan
        elif not pd.isnull(yearly_salary):
            return yearly_salary
        elif not pd.isnull(hourly_salary):
            return hourly_salary * hours_per_year

    data_frame['avg_yearly_salary'] = data_frame['salary'].map(map_avg_yearly_salary)
    data_frame['avg_hourly_salary'] = data_frame['salary'].map(map_avg_hourly_salary)

    # combine the yearly and hourly salaries based on working hour assumptions
    data_frame['standardised_salary'] = data_frame[['avg_yearly_salary', 'avg_hourly_salary']].apply(combine_salaries,
                                                                                                     args=(hours_per_year, ),
                                                                                                     axis=1)

    return data_frame
