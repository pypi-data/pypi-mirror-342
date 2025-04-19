from django.shortcuts import render


def server_error(request):
    response = render(request, '500.html', context={})
    response.status_code = 500

    return response
