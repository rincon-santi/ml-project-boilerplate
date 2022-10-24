FROM tensorflow/tensorflow
COPY . ./app
RUN pip install --no-cache-dir -r ./app/requirements.txt