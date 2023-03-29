from django.shortcuts import render
from django.views import View
# from page.services import Class 
# from account.views import account_login

def login_view(request):
    return render(request, 'page/login.html')

def signup_view(request):
    return render(request, 'page/signup.html')

def logout_view(request):
    return render(request, 'page/logout.html')

# def account_login_view(request):
#     template_name = 'login.html'
#     data = account_login(request)
#     return render(request, template_name, data)

# def account_signup_view(request):
#     template_name = 'register.html'
#     return render(request, template_name, {})
# def account_modify_view(request):
#     pass

# def account_profile_view(request):
#    template_name = 'profile.html'
#    return render(request, template_name, {})

# def 



# def example_create_view(request, pk):
#   template_name = 'form.html'
#   form_class = FormExample
  
#   form = form_class
  
#   if request.method == 'POST':
#     form = form_class(request.POST)
#     if form.is_valid():
#       form.save()
#       return HttpResponseRedirect(reverse('list-view'))
  
#   return render(request, template_name, {'form': form})