import numpy
import json
import pandavro
import dvc.api
import sys
sys.path.insert(1, '.')
from data_to_features_function import data_to_features
from utils.src.dataframe_utils import get_schema

params = dvc.api.params_show(stages=['generate-features'])

label_column = params['label_column']

# Load data
data_df = pandavro.from_avro("data/interim/clean.avro").replace("None", numpy.NAN)
data_df_features = data_df.drop(label_column, inplace=False, axis=1)
data_df_label = data_df.loc[:,label_column]

# Generate features

data_df_features = data_to_features(data_df_features)

# Add label and save. Save feature schema.

data_df_features[label_column] = data_df_label
fields = get_schema(data_df_features)
schema = {'namespace': params['experiment_id'].replace('.','_'),
          'name': 'Clean',
          'type': 'record',
          'fields': fields}
pandavro.to_avro(file_path_or_buffer='data/features/training_features.avro', schema=schema, df=data_df_features)
with open(file='docs/feature_schema.json', mode='w') as fields_file:
    fields_file.write(json.dumps(fields))
    fields_file.close()


