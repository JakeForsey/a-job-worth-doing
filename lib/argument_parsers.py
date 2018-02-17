"""
Jake Forsey
10/02/2018

Functions that create command line argument parsers for scripts
"""

import argparse


def explore_and_cleanse_argument_parser():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--data', type=str, default='data/monster_com-job_sample.csv',
                                 help='Path to monster job listings (.csv)')
    argument_parser.add_argument('--logging_level', type=int, default=10,
                                 help='Set the logging level, 20 for INFO, 10 for DEBUG')

    return argument_parser


def topic_model_argument_parser():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--n_topics', type=int, default=20,
                                 help='Number of topics to create')
    argument_parser.add_argument('--n_passes', type=int, default=10,
                                 help='Number of passes to make over the data')
    argument_parser.add_argument('--logging_level', type=int, default=10,
                                 help='Set the logging level, 20 for INFO, 10 for DEBUG')
    return argument_parser
