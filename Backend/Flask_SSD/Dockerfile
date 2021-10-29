# Use an official PyTorch runtime as a parent image
FROM python:3.7
FROM pytorch/pytorch

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple --user

# Run when the container launches
CMD ["python", "app.py"]