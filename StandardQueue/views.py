from django.http import HttpResponse
from django.shortcuts import render, redirect

from StandardQueue.forms import QueueForm
from StandardQueue.models import QueueModel


def index(request):
    session_queue = request.session.get('queue')
    if session_queue is None:
        return create_queue(request)
    else:
        host = 'https://' + request.get_host() + f'/join-the-queue/{session_queue}'
        context = {'host_url': host, 'session': True, 'name': session_queue}
        return render(request, 'index.html', context)


def create_queue(request):
    form = QueueForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            queue = QueueModel.objects.filter(name=name)
            if len(queue) == 0:
                QueueModel.objects.create(name=name, password=password, ids='')
                request.session['queue'] = name
                return redirect('index')
            else:
                context = {'form': form, 'error': 'Это название уже занято'}
                return render(request, 'create_queue.html', context)
    context = {'form': form}
    return render(request, 'create_queue.html', context)


def delete_queue(request):
    form = QueueForm(request.POST or None)
    if request.POST:
        queue = QueueModel.objects.get(name=request.session['queue'])
        print(form)
        if form.cleaned_data.get('password') == queue.password:
            queue.delete()
            request.session['queue'] = None
            request.POST = None
            return redirect('create_queue')
        else:
            context = {'form': form, 'error': 'Неправильный пароль'}
            return render(request, 'delete_queue.html', context)
    else:
        context = {'form': form}
        return render(request, 'delete_queue.html', context)


def join_the_queue(request, name):
    session_id = request.session.get('id')
    if session_id is None:
        queue = QueueModel.objects.get(name=name)
        ids = eval(queue.ids)
        last_id = ids[-1]
        new_id = last_id + 1
        ids.append(new_id)
        request.session['id'] = new_id
        queue.ids = str(ids)
        queue.save(update_fields=['ids'])
        session_id = request.session.get('id')
        context = {'session': True, 'id': session_id, 'name': name}
        return render(request, 'user_page.html', context)
    else:
        context = {'session': True, 'id': session_id, 'name': name}
        return render(request, 'user_page.html', context)


def leave_the_queue(request, name):
    queue = QueueModel.objects.get(name=name)
    ids = eval(queue.ids)
    ids.remove(request.session['id'])
    queue.ids = str(ids)
    queue.save(update_fields=['ids'])
    del request.session['id']
    context = {'session': False, 'name': name}
    return render(request, 'user_page.html', context)
