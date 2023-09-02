FROM python:3.11.2

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

RUN pip3 install poetry

COPY poetry.lock pyproject.toml /usr/src/app/
RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /usr/src/app/

CMD ["python", "main.py"]
