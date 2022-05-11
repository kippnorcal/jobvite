FROM python:3.7
WORKDIR /app
COPY ./.env /app/
COPY ./Pipfile* /app/
COPY dept_codes.csv /app/
RUN mkdir output
RUN wget https://packages.microsoft.com/debian/10/prod/pool/main/m/msodbcsql17/msodbcsql17_17.9.1.1-1_amd64.deb
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y unixodbc unixodbc-dev
RUN pip install pipenv
RUN pipenv install
RUN yes | dpkg -i msodbcsql17_17.9.1.1-1_amd64.deb
COPY ./*.py /app/
ENTRYPOINT ["pipenv", "run", "python", "main.py"]
 
