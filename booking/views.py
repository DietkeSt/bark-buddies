from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Service


class ServiceList(generic.ListView):
    model = Service
    queryset = Service.objects.filter(status=1).order_by('title')
    template_name = 'index.html'


class ServiceDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Service.objects.filter(status=1)
        service = get_object_or_404(queryset, slug=slug)
        comments = service.comments.filter(
            approved=True).order_by('created_on')
        liked = False
        if service.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "service_detail.html",
            {
                "service": service,
                "comments": comments,
                "liked": liked
            }
        )
