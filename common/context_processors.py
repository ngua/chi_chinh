from django.conf import settings


def channel_url(request):
    return {
        'channel_url': settings.CHANNEL_URL
    }


def sub_url(request):
    return {
        'sub_url': settings.SUBSCRIBE_URL
    }
