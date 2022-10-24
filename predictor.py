import pandas
import numpy as np
import os
import yaml
import json
import logging

from google.cloud.aiplatform.constants import prediction
from google.cloud.aiplatform.utils import prediction_utils
from google.cloud.aiplatform.prediction.predictor import Predictor
import tensorflow as tf

from src.features.data_to_features_function import data_to_features

f = open('params/data-params.yaml')
params = yaml.safe_load(f)
f.close()


class MyPredictor(Predictor):

    def __init__(self):
        return

    def load(self, artifacts_uri: str) -> None:
        """Loads the model artifact.
        Args:
            artifacts_uri (str):
                Required. The value of the environment variable AIP_STORAGE_URI.
        Raises:
            ValueError: If there's no required model files provided in the artifacts
                uri.
        """
        prediction_utils.download_model_artifacts(artifacts_uri)
        """Load model in self._model, for example:
        if os.path.exists('{saved_model.pb}'):
            self._model = tf.keras.models.load_model('.')
            logging.info("Loaded model")
        else:
            valid_filenames = [
                'saved_model.pb'
            ]
            raise ValueError(
                f"One of the following model files must be provided: {valid_filenames}."
            )
        """
        self._model = None
        """Load feature schema in self._feature_schema, for example:
        if os.path.exists('feature_schema.json'):
            f = open('feature_schema.json')
            self._feature_schema = json.load(f)
            f.close()
        else:
            raise ValueError(
                f"Feature schema 'feature_schema.json' must be provided"
            )
        """
        self._feature_schema = None

    def preprocess(self, prediction_input: dict) -> pandas.DataFrame:
        """Converts the request body to a numpy array before prediction.
        Args:
            prediction_input (dict):
                Required. The prediction input that needs to be preprocessed.
        Returns:
            The preprocessed prediction input.
        """
        instances = prediction_input["instances"]
        instances_pandas = pandas.DataFrame(instances)
        features_raw = data_to_features(instances_pandas)
        features = features_raw.reindex(columns=[field["name"] for field in self._feature_schema if field["name"]!="CLICKS"])
        for field in [field["name"] for field in self._feature_schema if field["name"]!="CLICKS" and field["name"] not in features_raw.columns]:
            features[field].fillna(value=0, inplace=True)
        return features

    def predict(self, instances: pandas.DataFrame) -> pandas.DataFrame:
        """Performs prediction.
        Args:
            instances (pandas.DataFrame):
                Required. The instance(s) used for performing prediction.
        Returns:
            Prediction results.
        """
        return self._model.predict(np.asarray(instances).astype('float32'))

    def postprocess(self, prediction_results: pandas.DataFrame) -> dict:
        """Converts numpy array to a dict.
        Args:
            prediction_results (pandas.DataFrame):
                Required. The prediction results.
        Returns:
            The postprocessed prediction results.
        """
        return {"predictions": prediction_results.tolist()}