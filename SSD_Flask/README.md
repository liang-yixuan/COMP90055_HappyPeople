# Deploy a backend application for SSD using Flask

## Instructions before using code

Please download the model weights from [Google Drive](https://drive.google.com/drive/folders/1U2nyjNXI8JqtxtaFizSVIsiI5WHE0c6M?usp=sharing) and place them into the 'model_data' folder (See below).<br>
Then you need to edit the voc_classes.txt file in model_data with the categories you need to detect

The Structure:<br>
SSD_Flask<br>
├─ Dockerfile<br>
├─ app.py<br>
├─ model_data<br>
│    ├─ age_1.pth<br>
│    ├─ emotion_1.pth<br>
│    ├─ gender_1.pth<br>
│    ├─ race_1.pth<br>
│    └─ voc_classes.txt<br>
├─ nets<br>
│    ├─ ssd.py<br>
│    ├─ ssd_layers.py<br>
│    ├─ ssd_training.py<br>
│    └─ vgg.py<br>
├─ requirements.txt<br>
├─ ssd_2.py<br>
├─ utils<br>
│    ├─ box_utils.py<br>
│    ├─ config.py<br>
│    └─ dataloader.py<br>
└─ voc_annotation.py<br>

## Instructions for running the code

Launch your application locally on your computer (in local virtual environment or in Docker): 
```console
# LOCAL NEW VIRTUAL ENV
pip install -r requirements.txt
python app.py
```

```console
# DOCKER
# building docker image
docker image build -t ssd:latest .

# running docker container (interactively, deleted when exit)
docker run --rm -it -p 5000:5000 ssd:latest

# uploading docker image to personal account
docker image tag ssd:latest USRNAME/ssd:latest
docker image push USRNAME/ssd:latest
docker system prune
```

Once started, your application should be available on http://localhost:5000.


## Credit:
This repo is build on https://github.com/bubbliiiing/ssd-pytorch
