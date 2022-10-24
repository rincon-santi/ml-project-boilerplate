import numpy as np
import pandavro
import dvc.api
import tensorflow as tf
from keras.callbacks import CSVLogger
from google.cloud import storage
import sys
import json
import os
sys.path.insert(1, '.')
import templates
from utils.src.gcloud_utils import write_to_gcs_file


params = dvc.api.params_show(stages=['train-model'])

label_column = params['label_column'] 
# Load data
data_df = pandavro.from_avro("data/features/training_features.avro").replace("None", np.NAN)
columns = len(data_df.columns)-1
data = {
    'training data': np.asarray(data_df.drop(label_column, inplace=False, axis=1)).astype('float32'),
    'labels': np.array(data_df.loc[:,label_column])
}

# Load feature schema
f = open('docs/feature_schema.json')
feature_schema = json.load(f)
f.close()

# Init and train model, remove 'model = None'
#model = {MODEL INITIATION}
#model.train(data['training data'], data['labels'])
model = None

# If continuous training enviroment, save on gcs model and feature schema
if 'AIP_MODEL_DIR' in os.environ.keys():
    tf.keras.models.save_model(model, os.environ['AIP_MODEL_DIR'])
    print('Model exported to: {}'.format(os.environ['AIP_MODEL_DIR']))
    write_to_gcs_file(os.environ['AIP_MODEL_DIR']+'/feature_schema.json', json.dumps(feature_schema))

# Save model locally
tf.keras.models.save_model(model, 'trained_model')
print('Model saved in: {}'.format('trained_model'))


