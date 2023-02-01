FROM python:3.7
ARG DIR  
ENV PYTHONPATH=/code
COPY $DIR/requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
COPY $DIR /code
WORKDIR /code
CMD ["python", "main.py"]
