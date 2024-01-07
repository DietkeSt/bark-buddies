from booking.models import Service


def services_processor(request):
    services = Service.objects.all()
    return {'services': services}


def add_published_services_to_context(request):
    published_services = Service.objects.filter(status=1)
    return {'published_services': published_services}
