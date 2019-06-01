import requests
from logger import logger


class ApiClient:
    pimicroclimate_url = 'https://pimicroclimate.herokuapp.com/api/measurements/'

    def post_measurement(self, measurement):
        try:
            responce = requests.post(url=ApiClient.pimicroclimate_url, data=measurement)
        except Exception:
            logger.exception('trouble occured while sending measurement to server')
            return None

        if responce.status_code == 201:
            logger.info('measurement sended to server')
        else:
            logger.info('error responce from server')
        return responce
