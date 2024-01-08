from django.shortcuts import render

def custom_404(request, exception):
    context = {'user': request.user} if hasattr(request, 'user') else {}
    return render(request, 'errors/404.html', context, status=404)

def custom_500(request):
    context = {'user': request.user} if hasattr(request, 'user') else {}
    return render(request, 'errors/500.html', context, status=500)