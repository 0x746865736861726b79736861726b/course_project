FROM python:3.12.4-bookworm

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install postgresql-client -y

WORKDIR /src

COPY requirements.txt /src
RUN pip install -r requirements.txt

COPY . /src

# Expose the port that the application will run on
EXPOSE 8000

# Start the application
CMD ["python", "manage.py", "runserver", "localhost:8000"]