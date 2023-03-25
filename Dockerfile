FROM python:3.10-buster

ENV VAR1=10

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


# Install & use pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN playwright-install

WORKDIR /app
COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

