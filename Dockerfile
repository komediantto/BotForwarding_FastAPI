FROM python:3

WORKDIR /BotForwarding

COPY poetry.lock pyproject.toml /BotForwarding/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

WORKDIR /usr

# Немножко патчим sqladmin под мою задачу
COPY sqladmin_patch/list.html sqladmin_patch/login.html /usr/local/lib/python3.11/site-packages/sqladmin/templates/
COPY sqladmin_patch/application.py /usr/local/lib/python3.11/site-packages/sqladmin/

WORKDIR /BotForwarding

ENV PYTHONPATH=/BotForwarding:${PYTHONPATH}

COPY . /BotForwarding/
