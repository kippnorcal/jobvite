FROM python:3.7
WORKDIR /app
COPY ./.env /app/
COPY ./Pipfile* /app/
COPY dept_codes.csv /app/
RUN mkdir output
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN apt-get install -y apt-utils
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN pip install pipenv
RUN pipenv install
COPY ./*.py /app/
ENTRYPOINT ["pipenv", "run", "python", "main.py"]
 
