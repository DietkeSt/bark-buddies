from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Service, AvailableTime
from .forms import CommentForm


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
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


    def post(self, request, slug, *args, **kwargs):
        queryset = Service.objects.filter(status=1)
        service = get_object_or_404(queryset, slug=slug)
        comments = service.comments.filter(
            approved=True).order_by('created_on')
        liked = False
        if service.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.service = service
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "service_detail.html",
            {
                "service": service,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )
