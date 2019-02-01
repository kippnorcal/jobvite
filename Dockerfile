FROM python:3
WORKDIR /app
COPY ./.env /app/
COPY ./Pipfile* /app/
RUN mkdir output
RUN pip install pipenv
RUN pipenv install
COPY ./*.py /app/
CMD ["pipenv", "run", "python", "main.py"]
