FROM python:3.8.7-slim-buster
COPY requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY . /app
WORKDIR /app

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION python
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port", "8501"]



