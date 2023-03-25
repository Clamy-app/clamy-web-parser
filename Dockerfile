FROM mcr.microsoft.com/playwright/python:v1.21.0-focal

# Install & use pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system
RUN playwright install

WORKDIR /app
COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

