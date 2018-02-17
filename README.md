# a-job-worth-doing
An analysis of 22,000 online Monster.com job postings.

Raw data and further discussion around it can be found: https://www.kaggle.com/PromptCloudHQ/us-jobs-on-monstercom

**explore_and_cleanse.py**
* count the number of nulls
* count the number of unique values in each field
* drop columns with 1 unique value
* drop duplicate rows
* standardise the following fields:
  * date_added
  * salary
  * job_type
* plot basic visualisations

**topic_model.py**
* process text
* create and persist objects for unsupervise topic modelling:
  * lda_model.model
  * dictionary.dict
  * coprus.mm
  
**LDA-Model-Visualisation-And-Classification.ipynb**
* Load and visualse a trained topic model
* Name each topic
* Classify job descriptions
* Further analysis using the results of the model
