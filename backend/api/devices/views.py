from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
import requests

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# # Create your views here.

# rest_framework
from api.devices.models import RpiModel, TapModel, WeekStatisticsModel
from api.devices.serializers import RpiSerializer, TapSerializer, RpiTapSerializer, WeekSerializer
from rest_framework import viewsets

from rest_framework import mixins
from django.contrib.auth.decorators import permission_required, login_required
from rest_framework import permissions

from django.contrib.auth.models import Group
class GroupPermission(permissions.BasePermission): 
    """
        
    """
    def has_permission(self, request, view):
        # return request.user.groups.filter(name='Managers').exists()
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if request.user and request.user.is_authenticated:
            group_manager = Group.objects.get(name='Managers')
            if request.method == 'POST' and (not group_manager in request.user.groups.all()):
                return False
            if request.method == 'DELETE' and (not group_manager in request.user.groups.all()):
                return False      
            return True
        return False



class WeekViewSet(viewsets.ModelViewSet):
    queryset = WeekStatisticsModel.objects.all()
    serializer_class = WeekSerializer



# GET, PUT, PATCH
# @login_required
# @permission_required('api.accounts.view')
class RpiViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [GroupPermission] # login and jwt verify >/token/ login and jwt ???   
    queryset = RpiModel.objects.all()
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RpiTapSerializer
        else:
            return RpiSerializer
        
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
class TapViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_class = [GroupPermission]

    queryset = TapModel.objects.all()
    serializer_class = TapSerializer


# TODO
# class ControlViewSet(viewsets.ModelViewSet):
#     # read fe, write db,send by go mqtt
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [GroupPermission]
#     querset = TapModel
#     serializer_class = TapControlSerializer

# @permission_classes([AllowAny])
# class DeviceViewSet(viewsets.ModelViewSet):
#     queryset = DeviceModel.objects.all()
#     serializer_class = DeviceSerializer 


# TODO ERROR
# def retrieve(self, request, *args, **kwargs): # one 
#     queryset = RpiModel.objects.all()
#     serializer  = RpiTapSerializer
#     return Response(serializer.data)


#     queryset = self.filter_queryset(self.get_queryset())

#     page = self.paginate_queryset(queryset)
#     if page is not None:
#         serializer = self.get_serializer(page, many=True)
#         return self.get_paginated_response(serializer.data)

#     serializer = self.get_serializer(queryset, many=True)
#     return Response(serializer.data)
    # return super().list(request, *args, **kwargs)

# def get_permissions(self):
#     return [ManagersGroup()]

# permission_classes = [AllowAny]
# authentication_classes = []






# from rest_framework.response import Response
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
# class TapViewSet(mixins.RetrieveModelMixin,
#                     mixins.ListModelMixin,
#                     mixins.UpdateModelMixin,
#                     viewsets.GenericViewSet):
#     queryset = TapModel.objects.all()
#     serializer_class = TapSerializer 
#     # def perform_authentication(self, request):
#     #     return self.request.user.groups.filter(name='Managers')
#     def list(self, request, *args, **kwargs):
#         return Response({'data': str(self.request.user.groups.all()), 'data1': str(self.request.user.groups.filter(name='Managers').exists()), 'data2': str(self.request.user.groups.filter(name='Engineers').exists())})






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
    
 





