import json
from functools import wraps
from Osdental.InternalHttp.Request import CustomRequest
from Osdental.InternalHttp.Response import CustomResponse
from Osdental.Exception.ControlledException import OSDException
from Osdental.Utils.Logger import logger
from Osdental.Utils.Code import APP_ERROR
from Osdental.Utils.Message import UNEXPECTED_ERROR

def handle_audit_and_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            _, info = args[:2] 
            request = info.context.get('request')
            headers = info.context.get('headers')
            if request:
                CustomRequest(request)

            response = await func(*args, **kwargs)
            CustomResponse(content=json.dumps(response), headers=headers)
            return response

        except OSDException as ex:
            logger.warning(f'Controlled server error: {str(ex.error)}')
            return ex.get_response()
        except Exception as e:
            logger.error(f'Unexpected server error: {str(e)}')            
            ex = OSDException(message=UNEXPECTED_ERROR, error=str(e), status_code=APP_ERROR, headers=headers)
            return ex.get_response()

    return wrapper