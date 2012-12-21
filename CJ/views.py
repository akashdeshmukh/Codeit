from django.shortcuts import render_to_response
# importing render_to_response method

def home(request):
    return render_to_response('index.html')
