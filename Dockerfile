FROM python:3.9-slim-buster

# Update and install AWS CLI in a single RUN command
RUN apt update -y && apt install -y awscli curl

WORKDIR /app

COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port that Streamlit will run on
EXPOSE 8080

# Healthcheck command
HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health || exit 1

# Set the entrypoint for the container
ENTRYPOINT ["streamlit", "run", "finalapp.py", "--server.port=8080", "--server.address=0.0.0.0"]
