"""
Author: Aymone Jeanne Kouame
Date Released: 04/16/2025
Last Updated: 04/18/2025  
"""

import os
import subprocess
import sys

from google.cloud import bigquery
client = bigquery.Client()

def README():

    print("""
gc_temp_tables lets you easily create and query temporary tables within Google Cloud environments. 
The user can work within a session and use an external table. The typical steps are:

    - Initiate a session with `create_bq_session()`.

    - If using an external table obtain the external table configurations with `get_external_table_config().

    - Create a temporary table using `create_temp_table(query)`. 

    - Query a temporary table using `query_temp_table()`.

    - Delete un-needed temporary table using `drop_temp_table()`.

More information, including a code snippet, at: https://github.com/AymoneKouame/data-science-utilities/blob/main/README.md#1---package-gc_temp_tables

""")

def create_bq_session():
    job_config = bigquery.QueryJobConfig(create_session = True) 
    query_job = client.query("""SELECT 1""", job_config = job_config)
    session_id = query_job.session_info.session_id
    print(f'''Session initiated. Session ID = {session_id}''')
          
    return session_id

def get_external_table_config(filename_in_bucket
                              , bucket_directory = None, bucket =  None, schema = None):
    
    if bucket == None:  bucket = os.getenv('WORKSPACE_BUCKET')
    if bucket_directory == None:  bucket_directory = ''
        
    ext = filename_in_bucket.split('.')[1].upper()
    external_table_config = bigquery.ExternalConfig(ext)
    external_table_config.source_uris = f'{bucket}/{bucket_directory}/{filename_in_bucket}'.replace('//','/').replace('gs:/','gs://')
    
    if schema == None: external_table_config.autodetect = True 
    else: external_table_config.schema = schema
   
    external_table_config.options.skip_leading_rows = 1
    
    return external_table_config

def create_temp_table(query, dataset = None, ext_table_def_dic = {}, session_id = None):
    
    if dataset == None: dataset = os.getenv('WORKSPACE_CDR')
    
    if session_id == None:
        job_config = bigquery.QueryJobConfig(default_dataset=dataset, table_definitions = ext_table_def_dic)
    
    else:
        job_config = bigquery.QueryJobConfig(
                    default_dataset=dataset
                    , connection_properties=[bigquery.ConnectionProperty("session_id", session_id)]
                    , table_definitions = ext_table_def_dic)
        
    query_job = client.query(query, job_config = job_config)  # API request
    results = query_job.result()
    
    t = query_job.created
    print(f'Temp table(s) created on {t}.')    
    return results

def query_temp_table(query, dataset = None, ext_table_def_dic = {}, session_id = None):
    
    if dataset == None: dataset = os.getenv('WORKSPACE_CDR')
    
    if session_id == None:
        job_config = bigquery.QueryJobConfig(default_dataset=dataset, table_definitions = ext_table_def_dic)

    else:
        job_config = bigquery.QueryJobConfig(
                    default_dataset=dataset
                    , connection_properties=[bigquery.ConnectionProperty("session_id", session_id)]
                    , table_definitions = ext_table_def_dic)
        
    query_job = client.query(query, job_config = job_config)
    df = query_job.result().to_dataframe()

    return df

def drop_temp_table(temp_table, session_id = None):
    
    if session_id == None: query_job = client.query(f'''DROP TABLE {temp_table}''')

    else:
        job_config = bigquery.QueryJobConfig(
            connection_properties=[bigquery.ConnectionProperty("session_id", session_id)])
        query_job = client.query(f'''DROP TABLE {temp_table}''', job_config = job_config)
        
    query_job.result()
    print(f'''Temp table {temp_table} deleted.''')

    return df