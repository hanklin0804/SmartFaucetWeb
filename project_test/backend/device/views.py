from django.shortcuts import render
from django.http import HttpResponse
# # get area's devices
# def func(request):
#     return render()

# # get 
# def func(request):
#     return render()

def set_cookie_view(request):
    response = HttpResponse('Set your lucky_number as 8')
    response.set_cookie = ('lucky_number', 8)
    return response

def get_cookie_view(request):
    if 'lucky_number' in request.COOKIES:
        return HttpResponse('Your lucky_number is {0}'.format(request.COOKIES['lucky_number']))
    else:
        return HttpResponse('No cookies.')
