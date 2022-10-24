from google.cloud import aiplatform
from google.cloud.aiplatform.prediction import LocalModel
import os

from predictor import MyPredictor

aiplatform.init(project=os.environ["PROJECT_ID"], location="europe-west1", staging_bucket=os.environ["STAGING_BUCKET"])

# Build and push serving image
local_model = LocalModel.build_cpr_model('.', os.environ["DEPLOY_IMAGE"], 
                                        predictor=MyPredictor, requirements_path="requirements_predictor.txt")
local_model.push_image()


# Start training job
job = aiplatform.CustomContainerTrainingJob(
    display_name=os.environ['JOB_DISPLAY_NAME'],
    container_uri=os.environ["TRAIN_IMAGE"],
    command=["bash", "app/vertex.sh"],
    model_serving_container_image_uri=os.environ["DEPLOY_IMAGE"],
)
model = job.run(
        model_display_name=os.environ['MODEL_DISPLAY_NAME'],
        replica_count=1,
        machine_type=os.environ["MACHINE_TYPE"],
        environment_variables={"ORIGIN_BUCKET":os.environ["ORIGIN_BUCKET"],
                                "PROJECT_ID":os.environ["PROJECT_ID"],
                                "VAL_SOURCE":"validation"},
        accelerator_count=0,
    )