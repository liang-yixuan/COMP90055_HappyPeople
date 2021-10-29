FROM pytorch/pytorch:1.7.1-cuda11.0-cudnn8-runtime

WORKDIR /workspace

ADD . /workspace

RUN apt-get update && apt-get install build-essential -y

RUN apt install -y libgl1-mesa-glx

RUN apt-get install -y libglib2.0-0

RUN apt-get install -y gfortran

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN cd faster-rcnn.pytorch/lib/ && python setup.py build develop

CMD [ "python" , "/workspace/main.py" ]

ENV HOME=/workspace