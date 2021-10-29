# Deploy a backend application for Faster RCNN using Flask

## Before using the code

Please download the model weights from [Google Drive](https://drive.google.com/drive/folders/14uIo6juLHrEoN5igBduw5euhsr1Geh9C). Download the 'models' folder, put it into the 'faster-rcnn.pytorch' folder and unzip it.

## Running the backend server
Launch your application locally on your computer (in local virtual environment or in Docker):
```console
# Run the server locally
pip install -r requirements.txt

cd faster-rcnn.pytorch/lib
python setup.py build develop

cd ../..
python main.py
```
```console
# Build docker image
docker build -t faster_rcnn_flask:latest .
docker builder prune -y

# Run docker container
docker run -d -p 5000:5000 faster_rcnn_flask:latest

# Upload docker image to personal account
docker image tag faster_rcnn_flask:latest username/flask_yolov5:latest
docker image push username/flask_yolov5:latest
docker system prune -y
```

# Credits:
The Faster RCNN model was cloned from https://github.com/jwyang/faster-rcnn.pytorch/tree/pytorch-1.0, with some modifications.
