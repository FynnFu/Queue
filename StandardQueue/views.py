from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.


def index(request):
    host = 'https://' + request.get_host() + '/join-the-queue/'
    context = {'host_url': host}
    return render(request, 'index.html', context)


def join_the_queue(request):
    session_id = request.session.get('id')
    if session_id is None:
        request.session['id'] = 'bar'
        session_id = request.session.get('id')
        context = {'session': True, 'id': session_id}
        return render(request, 'user_page.html', context)
    else:
        context = {'session': True, 'id': session_id}
        return render(request, 'user_page.html', context)


def leave_the_queue(request):
    del request.session['id']
    context = {'session': False}
    return render(request, 'user_page.html', context)
