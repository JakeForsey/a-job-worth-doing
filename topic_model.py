"""
Jake Forsey
16/02/2018

Creates and saves a LDA topic model of the monster job postings
"""

import logging
import os

from gensim.corpora import Dictionary, MmCorpus
from gensim.models.ldamodel import LdaModel
import pandas as pd
from tqdm import tqdm

from lib.nlp_utils import NLTKProcessor
from lib.argument_parsers import topic_model_argument_parser


def main(n_passes, n_topics):

    # if the text has not been processed; process the text, otherwise just load it from a csv
    if not os.path.isfile('data/processed_job_descriptions.csv'):
        data_frame = pd.read_csv('data/cleansed_data.csv')

        # stemming or lemmatizing reduces word count but also makes interpreting the results more difficult
        text_processor = NLTKProcessor(stemmer=None)

        data_frame['processed_job_description'] = data_frame['job_description'].progress_apply(text_processor.process)
        data_frame = data_frame[['processed_job_description', 'uniq_id']]
        data_frame.to_csv('data/processed_job_descriptions.csv', index=False)
    else:
        data_frame = pd.read_csv('data/processed_job_descriptions.csv')

    # create a list (of word lists) of all the job descriptions
    # I'm dropping the duplicate job descriptions but this may not be suitable as there may be multiple
    #       jobs with the same description which may inform clustering
    data_frame = data_frame[['processed_job_description', 'uniq_id']].drop_duplicates()
    processed_job_descriptions = data_frame['processed_job_description'].str.split().values

    # create or load a gensim.corpora.Dictionary containing all the words in the dataset
    if not os.path.isfile('models/dictionary.dict'):
        dictionary = Dictionary(processed_job_descriptions)
        dictionary.save('models/dictionary.dict')
    else:
        dictionary = Dictionary.load('models/dictionary.dict')

    # create or load a gensim.corpora.MmCorpus 
    if not os.path.isfile('models/corpus.mm'):
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in processed_job_descriptions]
        MmCorpus.serialize('models/corpus.mm', doc_term_matrix)
    else:
        doc_term_matrix = MmCorpus('models/corpus.mm')

    # create and train a Latent Dirichlet allocation model using the monster.com job postings
    lda_model = LdaModel(doc_term_matrix, num_topics=n_topics, id2word=dictionary, passes=n_passes)

    # persist the LDAModel as a serialised file
    lda_model.save('models/lda_model_{}topics_{}passes.model'.format(n_topics, n_passes))


if __name__ == '__main__':
    arguments = topic_model_argument_parser().parse_args()

    logging.basicConfig(level=arguments.logging_level)

    # set up tqdm (pretty progress bars) for pandas
    tqdm.pandas(desc='Text processing')

    main(n_topics=arguments.n_topics,
         n_passes=arguments.n_passes)
