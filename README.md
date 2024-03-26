# jobvite
An ETL service job for staging Jobvite candidate and job data

## Dependencies:

* Python3
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)
* [Docker](https://www.docker.com/))

## Getting Started

### Setup Environment

1. Clone this repo

```
$ git clone https://github.com/kippnorcal/jobvite.git
```

2. Install Pipenv

```
$ pip install pipenv
$ pipenv install
```

3. Install Docker

* **Mac**: [https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/)
* **Linux**: [https://docs.docker.com/install/linux/docker-ce/debian/](https://docs.docker.com/install/linux/docker-ce/debian/)
* **Windows**: [https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/)

4. Build Docker Image

```
$ docker build -t jobvite .
```
If you get back an error then try the following command instead (this will likely happen if you are using a newer Macbook with an M1 chip):

docker build -t jobvite . --no-cache --platform linux/amd64

5. Create .env file with project secrets

```
JOBVITE_API_KEY=
JOBVITE_API_SECRET=

# Mailgun & email notification variables
MG_DOMAIN=
MG_API_URL=
MG_API_KEY=
FROM_ADDRESS=
TO_ADDRESS=

DB_SERVER=
DB=
DB_USER=
DB_PWD=
DB_SCHEMA=
```

### Running the Job

Run for yesterdays candidates.

```
$ docker run -t jobvite 
```

Optionally, you can run it with start/end date arguments to pull more than just yesterday's candidates.
```
$ docker run -it jobvite --start-date='2019-07-01' --end-date='2019-07-31'
```


### Testing

To execute tests, run:
* `pipenv run pytest`

## Maintenance

* No annual maintenance is required
* This connector should NOT be turned off during the summer.
