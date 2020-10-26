FROM python:3.8-alpine
USER root
WORKDIR /usr/src/app
COPY main.py Pipfile Pipfile.lock ./
RUN pip install pipenv && \
    pipenv install --deploy --system
CMD ["python", "main.py"]