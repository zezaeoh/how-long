import logging

from functools import wraps

from django.http import HttpResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from pydantic import ValidationError as PydanticValidationError

from howlong.common import utils
from howlong.common.exceptions import ValidationError, PasswordMismatch, NotAuthError, IntegrityError, NotAllowedError, \
    InvalidArgumentError

logger = logging.getLogger(__name__)


def _print_args(args):
    for arg in args:
        if isinstance(arg, Request):
            if 'password' in arg.data:
                arg.data.pop('password')
            logger.error(arg.data)
        else:
            logger.error(arg)


def api_status_response(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        tag = 'status_response'
        try:
            result = func(*args, **kwargs)
            return Response(result, status=status.HTTP_200_OK)
        except (
            PydanticValidationError,
            ValidationError,
            InvalidArgumentError
        ) as error:
            logger.error("{}.{} error: {}".format(tag, func.__name__, error))
            _print_args(args)
            return HttpResponse(str(error), status=status.HTTP_400_BAD_REQUEST)
        except PasswordMismatch as error:
            logger.error("{}.{} error: {}".format(tag, func.__name__, error))
            _print_args(args)
            return HttpResponse(str(error), status=status.HTTP_403_FORBIDDEN)
        except NotAuthError as error:
            logger.error("{}.{} error: {}".format(tag, func.__name__, error))
            _print_args(args)
            return HttpResponse(str(error), status=status.HTTP_403_FORBIDDEN)
        except IntegrityError as error:
            logger.error("{}.{} error: {}".format(tag, func.__name__, error))
            _print_args(args)
            return HttpResponse(str(error), status=status.HTTP_404_NOT_FOUND)
        except NotAllowedError as error:
            logger.error("{}.{} error: {}".format(tag, func.__name__, error))
            _print_args(args)
            return HttpResponse(str(error), status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as error:
            logger.error("{}.{} error: {}".format(tag, func.__name__, error))
            utils.logging_traceback()
            _print_args(args)
            return HttpResponse('서버에 오류가 발생했습니다.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return decorated

