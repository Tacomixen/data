# Use the official lightweight Python image.
FROM python:3.6-slim

# Copy local code to the container image.
ENV APP_HOME /app
ENV PYTHONUNBUFFERED True
WORKDIR $APP_HOME
COPY . ./

# Install dependencies.
RUN pip install -r requirements.txt

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 app:app