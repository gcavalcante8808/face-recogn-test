import logging
import json
import time
import logbook


default_logger = logbook.Logger()
default_handler = logbook.StderrHandler(level='INFO', format_string='{record.message}')

logger = logging.getLogger()


class MatchResultLoggingMiddleware(object):
    def process_request(self, req, resp):
        """
        Start the Timer.
        """
        req.start_time = time.time()

    """
    Create a log information for a result; matched or not matched.
    """
    def process_response(self, req, resp, resource, req_succeeded):
        """
        Log client, match and name.
        """
        elapsed = time.time() - req.start_time
        data = {
            "channel": "falconapp",
            "client": req.media.get('client', 'unknown'),
            "filename": req.media.get('filename', 'unknown_image'),
            "matched": json.loads(resp.body).get("matched"),
            "person": json.loads(resp.body).get("person"),
            "elapsed_time": elapsed
        }
        #
        with default_handler.applicationbound():
                default_logger.info(json.dumps(data))
