from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
# # Create your views here.

    
@api_view(['POST'])
@permission_classes([AllowAny])
def get_getdevice(request):
    # TODO frontend: 
    # ip = request.data.get('ip') 
    # status = request.data.get('status')
    ip = '192.168.0.166'
    port = 5000
    url = f'http://{ip}:{port}' # /api/endpoint
    headers = {'Content-Type': 'application/json'}
    device_request_params = {
        'ip': ip,
        'status': 'hi'
    }
    # frontend: 
    # TODO ERROE
    response = requests.post(url, headers=headers, data=device_request_params)
    
    if response.status_code == 200:
        device_response_params = response.json()
        # save
        return Response({'ok':device_response_params}, status=status.HTTP_200_OK)
    else:
        return Response({'error':'error'}, status=status.HTTP_404_NOT_FOUND)
    try:
        # TODO not get error
        response = requests.post(url, headers=headers, data=device_request_params)
        
        if response.status_code == 200:
            device_response_params = response.json()
            # save
            return Response({'ok':device_response_params}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'error'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response({'error':f'{ex}'}, status=status.HTTP_404_NOT_FOUND)
    
    # request:
    # getdevice
    # response:
    # return 



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


