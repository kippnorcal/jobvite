# jobvite_connector
An ETL service job for staging Jobvite candidate and job data

## Dependencies:

* Python3.7
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)
* [Docker](https://www.docker.com/)
* [Black](https://github.com/ambv/black)
* [Pre-commit](https://pre-commit.com/)

## Getting Started

### Setup Environment

1. Clone this repo

```
$ git clone https://github.com/kipp-bayarea/jobvite_connector.git
```

2. Install Pipenv

```
$ pip install pipenv
$ pipenv install
```

3. Install developer dependencies

```
$ pip install black
$ pip install pre-commit
$ pre-commit install
```

4. Install Docker

* **Mac**: [https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/)
* **Linux**: [https://docs.docker.com/install/linux/docker-ce/debian/](https://docs.docker.com/install/linux/docker-ce/debian/)
* **Windows**: [https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/)

5. Build Docker Image

```
$ docker build -t jobvite .
```

6. Create .env file with project secrets

```
JOBVITE_API_KEY=
JOBVITE_API_SECRET=
GMAIL_USER=
GMAIL_PWD=
SLACK_EMAIL=
SERVER_IP=
DB=
USER=
PWD=
```

### Running the Job

Run in detached mode (runs as background process) with the output folder mapped to the host directory.

```
$ docker run -d -v ${PWD}/output:/app/output --name=jobvite jobvite 
```

Optionally, you can run it with a date argument to pull more than just yesterday's candidates.

```
$ docker run -d -v ${PWD}/output:/app/output --name=jobvite jobvite "2019-03-14"
```


### Testing

To execute tests, run:
* `pipenv run pytest`
