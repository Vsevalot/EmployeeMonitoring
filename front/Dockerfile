FROM python:3.11.2

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["python", "main.py"]