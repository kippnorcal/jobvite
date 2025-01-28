# jobvite
An ETL job for extracting candidate and job data from Jobvite's API.

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

# Google Cloud Storage Settings
CANDIDATES_CLOUD_FOLDER=
JOBS_CLOUD_FOLDER=
CANDIDATE_TABLE=

# Google Cloud Credentials
GOOGLE_APPLICATION_CREDENTIALS=
GBQ_PROJECT=
BUCKET=
```

### Running the Job

Regular run for new candidates. Will query Jobvite API for record updates based since the most recent timestamp in the data warehouse.

```
$ docker run -t jobvite 
```

Optionally, you can run it with start/end date arguments to pull candidates from a period of time.
```
$ docker run -t jobvite --start-date='2025-07-01' --end-date='2025-07-31'
```

## Maintenance

* No annual maintenance is required
* This connector should NOT be turned off during the summer.
