from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
import requests
# # Create your views here.



def get_getdevice(request):
    pass
    ip = '192.168.1.1'
    port = 1234
    # url = f'http://{ip}/api/endpoint'
    # frontend: 
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # save
            return Response({'ok':'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'error'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'error':'error'}, status=status.HTTP_404_NOT_FOUND)
    
    # request:
    # getdevice
    # response:
    # return 

    return

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


