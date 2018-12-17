import logging
import json


logger = logging.getLogger()


class MatchResultLoggingMiddleware(object):
    """
    Create a log information for a result; matched or not matched.
    """
    def process_response(self, req, resp, resource, req_succeeded):
        """
        Log client, match and name.
        """
        raise NotImplementedError
        data = {
            "client": req.media.get('client', 'unknown'),
            "filename": req.media.get('filename', 'unknown_image'),
            "matched": resp.body.get('')
        }

        json.dumps(data)
