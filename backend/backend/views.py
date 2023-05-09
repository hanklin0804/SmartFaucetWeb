from rest_framework import status
from django.http import JsonResponse

def error(request, exception=None):
    return JsonResponse({'status': 'error in backend views'}, status=status.HTTP_404_NOT_FOUND)