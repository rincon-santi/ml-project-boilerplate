from google.cloud import storage
import sys
import os
import apache_beam as beam
import logging
import dvc.api
import yaml
from google.cloud import storage
import sys
import os

with dvc.api.open("docs/data_schema.yaml") as data_schema:
    DATA_SCHEMA = yaml.safe_load(data_schema)

sys.path.insert(1, '.')
from utils.src.context_management import get_source

select_cast = {'string':str,
               'int':int,
               'float':float}

def ensure_types(row):
    return {field["name"]:None if row[field["name"]] in field["none_values"] \
                    else select_cast[field["type"]](row[field["name"]]) \
                    for field in DATA_SCHEMA}

def main(argv=None):

    # Set origin and environment
    if 'ORIGIN_BUCKET' in os.environ.keys():
        origin_bucket = os.environ['ORIGIN_BUCKET']
    else:
        raise Exception('ORIGIN BUCKET ENV VARIABLE NOT FOUND')
    if 'PROJECT_ID' in os.environ.keys():
        project = os.environ['PROJECT_ID']
    else:
        raise Exception('PROJECT_ID ENV VARIABLE NOT FOUND')

    env = get_source()
    if env=='training':
        origin_folder = 'data/training'
        prefix = 'input'
        destiny_folder = 'data/raw/'
    elif env=='validation':
        origin_folder = 'data/validation'
        prefix = 'validation'
        destiny_folder = 'data/validation/'
    elif env=='test':
        origin_folder = 'data/test'
        prefix = 'validation'
        destiny_folder = 'data/validation/'
    else:
        raise Exception('Needed to specify what data to get')

    # Recovering params
    params = dvc.api.params_show(stages=['get-data'])

    # Download raw data files - must be saved in ORIGIN_BUCKET under data/training, data/validation and/or data/test paths
    storage_client = storage.Client(project=project)
    bucket = storage_client.get_bucket(origin_bucket)
    blobs = bucket.list_blobs(prefix="{origin_folder}/{prefix}".format(origin_folder=origin_folder, prefix=prefix))  # Get list of files
    for blob in blobs:
        filename = blob.name.split('/')[-1] 
        print("Downloading to {}".format(destiny_folder+filename))
        blob.download_to_filename(destiny_folder+filename)  # Download
        print("Saved")

    schema = {'namespace': params['experiment_id'].replace('.','_'),
          'name': 'Clean',
          'type': 'record',
          'fields': [{'name': field['name'], 'type': [field['type'], 'null']} \
           for field in DATA_SCHEMA]}
   
    #Save data in single file after checking types
    with beam.Pipeline() as p:
        (p 
            | 'Read' >> beam.io.ReadFromAvro('{folder}{prefix}*'.format(
                folder=destiny_folder, prefix=prefix))
            | 'EnsureTypes' >> beam.Map(ensure_types)
            | 'Write' >> beam.io.WriteToAvro(file_path_prefix='{destiny_folder}{prefix}_complete'.format(
                destiny_folder=destiny_folder, prefix=prefix), schema=schema))
   
   
if __name__ == '__main__':
  logger = logging.getLogger().setLevel(logging.INFO)
  main()