import logging
import requests
from os import getenv
from requests.compat import urlencode


class JobviteAPI:
    """Interface for accessing the Jobvite v2 API.

        args:
            api_key (str): stored in environment as 'JOBVITE_API_KEY'
            api_Secret (str): stored in environment as 'JOBVITE_API_SECRET'

        example:
            >>> jv = JobviteAPI(environ['JOBVITE_API_KEY'], environ['JOBVITE_API_SECRET'])

    """

    ENDPOINT = "https://api.jobvite.com/api/v2"

    def __init__(self, api_key=None, api_secret=None, logger=None):
        self.api_key = api_key if api_key else getenv("JOBVITE_API_KEY")
        self.api_secret = api_secret if api_secret else getenv("JOBVITE_API_SECRET")
        self.logger = logger if logger else logging.getLogger()

    @property
    def request_credentials(self):
        return {"x-jvi-api": self.api_key, "x-jvi-sc": self.api_secret}

    @property
    def candidates_endpoint(self):
        return f"{self.ENDPOINT}/candidate"

    @property
    def jobs_endpoint(self):
        return f"{self.ENDPOINT}/job"

    def _get(self, endpoint, **params):
        params = params.copy()
        self.logger.debug(
            'requesting: "{}?{}"'.format(endpoint, urlencode(params, doseq=True))
        )

        # As of 10/1/2023, credentials have to be passed through headers
        response = requests.get(endpoint, params=params, headers=self.request_credentials)
        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()

    def jobs(self, batch_size=100, limit=None, **params):
        """Fetch jobs from Jobvite API.

        This API will stream jobs from the Jobvite API as a generator, making multiple requests until all
        job meeting the filters are returned.

        Args:
            batch_size (int): number of jobs to fetch in each request.
            limit (int): stop fetching jobs after a limit is reached. this is primarily for testing.
            **params: additional args that may be passed into the Jobvite API.

        Yields:
            dict: job JSON converted to objects.

        Examples:
            >>> jv.jobs(batch_size=500, start_date='2018-12-20')
            >>> jv.jobs(limit=30)

        Todo:
            * implement wflowstate filter (if necessary).
            * Investigate datetime filters.
        """
        params = params.copy()

        params["count"] = batch_size
        if limit and limit < batch_size:
            params["count"] = limit

        if batch_size > 500:
            raise ValueError('Batch size cannot be greater than "500"')

        return self._stream(
            self.jobs_endpoint,
            params,
            batch_size=batch_size,
            limit=limit,
            items_key="requisitions",
        )

    def candidates(self, start_date=None, end_date=None, batch_size=100, limit=None, **params):
        """Fetch candidates from Jobvite API.

        This API will stream candidates from the Jobvite API as a generator, making multiple requests until all
        candidates meeting the filters are returned.

        Args:
            start_date (str): filter results by start date >= 'yyyy-MM-dd'.
            end_date (str): filter results by end date <= 'yyyy-MM-dd'.
            batch_size (int): number of candidates to fetch in each request.
            limit (int): stop fetching candidates after a limit is reached. this is primarily for testing.
            **params: additional args that may be passed into the Jobvite API.

        Yields:
            dict: candidate JSON converted to objects.

        Examples:
            >>> jv.candidates(batch_size=500, start_date='2018-12-20', end_date='2019-03-30')
            >>> jv.candidates(limit=30)

        Todo:
            * implement wflowstate filter (if necessary).
            * Investigate datetime filters.
        """
        params = params.copy()
        params["datestart"] = start_date
        params["dateend"] = end_date
        params["dateFormat"] = "yyyy-MM-dd"
        params["count"] = batch_size
        if limit and limit < batch_size:
            params["count"] = limit

        if batch_size > 500:
            raise ValueError('Batch size cannot be greater than "500"')

        return self._stream(
            self.candidates_endpoint,
            params,
            batch_size=batch_size,
            limit=limit,
            items_key="candidates",
        )

    def _stream(self, endpoint, params, batch_size=100, limit=None, items_key=None):
        start = 0
        collected_items = 0
        while True:
            params["start"] = start
            r = self._get(endpoint, **params)
            data = r.json()
            for c in data[items_key]:
                collected_items += 1
                yield c

            num_items = len(data[items_key])
            if num_items < batch_size or (limit and collected_items >= limit):
                break
            else:
                start += batch_size
