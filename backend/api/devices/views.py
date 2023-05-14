from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
import requests

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# # Create your views here.

# rest_framework
from api.devices.models import RpiModel, TapModel
from api.devices.serializers import RpiSerializer, TapSerializer
from rest_framework import viewsets

from rest_framework import mixins
from django.contrib.auth.decorators import permission_required, login_required
from rest_framework import permissions
from rest_framework_simplejwt import authentication

class EngineersGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.groups.filter(name='Engineers').exists()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ManagersGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Managers').exists()
from django.contrib.auth.models import Group
class GroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            group1 = Group.objects.get(name='Managers')
            group2 = Group.objects.get(name='Engineers')

            if request.method == 'POST' and group1 in request.user.groups.all():
                return True
            
            if request.method == 'DELETE' and group1 in request.user.groups.all():
                return True
    
            
        return False


# GET, PUT, PATCH
# @login_required
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
# @permission_required('api.accounts.view')
class RpiViewSet(viewsets.ModelViewSet):
    permission_classes = [GroupPermission]

    # authentication_classes = [authentication.JWTAuthentication]
    queryset = RpiModel.objects.all()
    serializer_class = RpiSerializer
    # def get_permissions(self):
    #     return [ManagersGroup()]

    # permission_classes = [AllowAny]
    # authentication_classes = []

from rest_framework.response import Response
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
class TapViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = TapModel.objects.all()
    serializer_class = TapSerializer 
    # def perform_authentication(self, request):
    #     return self.request.user.groups.filter(name='Managers')
    def list(self, request, *args, **kwargs):
        return Response({'data': str(self.request.user.groups.all()), 'data1': str(self.request.user.groups.filter(name='Managers').exists()), 'data2': str(self.request.user.groups.filter(name='Engineers').exists())})



# @permission_classes([AllowAny])
# class DeviceViewSet(viewsets.ModelViewSet):
#     queryset = DeviceModel.objects.all()
#     serializer_class = DeviceSerializer 


# TODO test socket
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def get_getdevice(request):
#     # TODO frontend: 
#     # ip = request.data.get('ip') 
#     # status = request.data.get('status')
#     ip = '192.168.0.166'
#     port = 5000
#     url = f'http://{ip}:{port}' # /api/endpoint
#     headers = {'Content-Type': 'application/json'}
#     device_request_params = {
#         'ip': ip,
#         'status': 'hi'
#     }
#     # frontend: 
#     # TODO ERROE
#     response = requests.post(url, headers=headers, data=device_request_params)
    
#     if response.status_code == 200:
#         device_response_params = response.json()
#         # save
#         return Response({'ok':device_response_params}, status=status.HTTP_200_OK)
#     else:
#         return Response({'error':'error'}, status=status.HTTP_404_NOT_FOUND)
#     try:
#         # TODO not get error
#         response = requests.post(url, headers=headers, data=device_request_params)
        
#         if response.status_code == 200:
#             device_response_params = response.json()
#             # save
#             return Response({'ok':device_response_params}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error':'error'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as ex:
#         return Response({'error':f'{ex}'}, status=status.HTTP_404_NOT_FOUND)
    
 




# def which_irduty(requst):
#     pass
#     # frontend: 
#     # get para
#     # request:
#     # para=para
#     # response:
#     # return command pass/fail
#     return

# def set_powersave(request):
#     pass
#     # frontend: 
#     # get command
#     # request:
#     # command=command
#     # response:
#     # return command pass/fail ???
#     return 

# def set_feedtime(request):
#     pass
#     return

# def set_feedcntlimit(request):
#     pass
#     # frontend: 
#     # get command
#     # request:
#     # command=command
#     # response:
#     # return command pass
#     return

# def set_feedcntmax(requset):
#     pass
#     # frontend: 
#     # get para
#     # request:
#     # para=para
#     # response:
#     # return feedcntmax pass
#     return


# def set_amountlimit(request):
#     pass
#     # frontend: 
#     # get command
#     # request:
#     # command=command
#     # response:
#     # return command pass
#     return

# def set_amountcapacityunit(requset):
#     pass
#     # frontend: 
#     # get para
#     # request:
#     # para=para
#     # response:
#     # return capacity pass
#     return


# def set_powerwarn(request):
#     pass
#     # frontend: 
#     # get command
#     # request:
#     # command=command
#     # response:
#     # return command pass
#     return

# def set_powerwarnvolt(requset):
#     pass
#     # frontend: 
#     # get para
#     # request:
#     # para=para
#     # response:
#     # return warnvolt pass
#     return

# def set_powerfail(request):
#     pass
#     # frontend: 
#     # get command
#     # request:
#     # command=command
#     # response:
#     # return command pass
#     return

# def set_powerfailvolt(requset):
#     pass
#     # frontend: 
#     # get para
#     # request:
#     # para=para
#     # response:
#     # return powerfailvolt pass
#     return


# def set_leakdet(request):
#     pass
#     # frontend: 
#     # get command
#     # request:
#     # command=command
#     # response:
#     # return command pass
#     return

# def set_leakdet_duty(requset):
#     pass
#     # frontend: 
#     # get para
#     # request:
#     # para=para
#     # response:
#     # return leakdetduty pass
#     return

# def set_leakdet_keep(requset):
#     pass
#     # frontend: 
#     # get para
#     # request:
#     # para=para
#     # response:
#     # return leakdetkeep pass
#     return

# def set_leakdet_time(requset):
#     pass
#     # frontend: 
#     # get para
#     # request:
#     # para=para
#     # response:
#     # return leakdettime pass
#     return


