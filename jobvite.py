import logging
import requests
from requests.compat import urlencode


class JobviteAPI:
    """Interface for accessing the Jobvite v2 API.

        args:
            api_key (str): stored in environment as 'JOBVITE_API_KEY'
            api_Secret (str): stored in environment as 'JOBVITE_API_SECRET'

        example:
            >>> jv = JobviteAPI(environ['JOBVITE_API_KEY'], environ['JOBVITE_API_SECRET'])

    """

    ENDPOINT = 'https://api.jobvite.com/api/v2'

    def __init__(self, api_key, api_secret, logger=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.logger = logger if logger else logging.getLogger()


    @property
    def default_request_params(self):
        return {
                'api': self.api_key,
                'sc': self.api_secret,
            }


    @property
    def candidates_endpoint(self):
        return f'{self.ENDPOINT}/candidate'


    def _get(self, endpoint, **params):
        params = params.copy()
        self.logger.debug('requesting: "{}?{}"'.format(endpoint, urlencode(params, doseq=True)))
        
        for k, v in self.default_request_params.items():
            if k not in params:
                params[k] = v

        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()


    def candidates(self, modified_date=None, batch_size=100, limit=None, **params):
        """Fetch candidates from Jobvite API.

        This API will stream candidates from the Jobvite API as a generator, making multiple requests until all
        candidates meeting the filters are returned.

        Args:
            modified_date (str): filter results by modified date >= 'yyyy-MM-dd'.
            batch_size (int): number of candidates to fetch in each request.
            limit (int): stop fetching candidates after a limit is reached. this is primarily for testing.
            **params: additional args that may be passed into the Jobvite API.

        Yields:
            dict: candidate JSON converted to objects.

        Examples:
            >>> jv.candidates(batch_size=500, modified_date='2018-12-20')
            >>> jv.candidates(limit=30)

        Todo:
            * implement wflowstate filter (if necessary).
            * Investigate datetime filters.
        """
        params = params.copy()
        if modified_date:
            params['startdate'] = modified_date
            params['dateFormat'] = 'yyyy-MM-dd'

        if limit < batch_size:
            params['count'] = limit

        if batch_size > 500:
            raise ValueError('Batch size cannot be greater than "500"')

        params['count'] = batch_size

        return self._stream(self.candidates_endpoint, params, batch_size=batch_size, limit=limit, items_key='candidates')


    def _stream(self, endpoint, params, batch_size=100, limit=None, items_key=None):
        start = 0
        collected_items = 0
        while True:
            params['start'] = start
            r = self._get(endpoint, **params)
            data = r.json()
            for c in data[items_key]:
                collected_items +=1
                yield c

            num_items = len(data[items_key])
            if num_items < batch_size or collected_items >= limit:
                break
            else:
                start += batch_size
                
