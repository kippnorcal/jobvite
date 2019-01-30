# jobvite_connector
An ETL service job for staging Jobvite candidate data


### Jobvite API

Initializing the Jobvite API object:
```python
api_key = environ.get('JOBVITE_API_KEY'),
api_secret = environ.get('JOBVITE_API_SECRET')
jv = JobviteAPI(api_key, api_secret)
```

The `jv.candidates()` method returns a generator to iterate over candidates.  Here are some sample arguments for getting results:

* `jv.candidates(batch_size=500, modified_date='2018-12-20')`
* `jv.candidates(limit=30):`


### Environment Setup

.env file:
```
JOBVITE_API_KEY=
JOBVITE_API_SECRET=
```
