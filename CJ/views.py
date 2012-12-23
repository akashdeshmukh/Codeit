from django.shortcuts import render_to_response
# importing render_to_response method


def home(request):
    return render_to_response('index.html')


def my_custom_404_view(request):
    return render_to_response('404.html')


def my_custom_error_view(request):
    return render_to_response('500.html')
