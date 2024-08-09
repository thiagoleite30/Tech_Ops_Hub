from django.shortcuts import render

# Create your views here.
def index(request):
 return render(request, 'apps/move_gpos/index.html')


def request(request):
 return render(request, 'apps/move_gpos/request.html')