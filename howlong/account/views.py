from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request

from howlong.account import services
from howlong.common.decorators import api_status_response


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@api_status_response
def login_with_kakao(request: Request):
    return services.login(request.query_params, services.LoginType.Kakao)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@api_status_response
def login_with_naver(request):
    return services.login(request.query_params, services.LoginType.Naver)
