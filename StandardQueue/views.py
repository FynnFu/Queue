from django.http import HttpResponse
from django.shortcuts import render, redirect
import json
from StandardQueue.forms import QueueForm
from StandardQueue.models import QueueModel


def index(request):
    session_queue = request.session.get('queue')
    if session_queue is None:
        return create_queue(request)
    else:
        host = 'https://' + request.get_host() + f'/clear_cookies/{session_queue}'
        users = json.loads(QueueModel.objects.get(name=request.session.get('queue')).ids.replace("'", '"'))
        context = {'host_url': host, 'session': True, 'name': session_queue, 'users': users['users']}
        return render(request, 'index.html', context)


def create_queue(request):
    form = QueueForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            queue = QueueModel.objects.filter(name=name)
            if len(queue) == 0:
                ids = {"users": [{"id": 0, "name": "None"}]}
                str_ids = json.dumps(ids)
                QueueModel.objects.create(name=name, password=password, ids=str_ids)
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
    try:
        if session_id is None:
            queue = QueueModel.objects.get(name=name)
            ids_old = queue.ids.replace("'", '"')
            ids = json.loads(ids_old)
            your_name = request.POST.get('your_name')
            ids['users'].append({"id": str(len(ids) + 1), "name": your_name})
            request.session['id'] = len(ids) + 1
            queue.ids = json.dumps(ids)
            queue.save(update_fields=['ids'])
            session_id = request.session.get('id')
            context = {'session': True, 'id': session_id, 'name': name}
            return render(request, 'user_page_leave.html', context)
        else:
            context = {'session': True, 'id': session_id, 'name': name}
            return render(request, 'user_page_leave.html', context)
    except QueueModel.DoesNotExist:
        context = {'error': "Срок действия QR-кода истек", 'name': name}
        return render(request, 'user_page_join.html', context)


def leave_the_queue(request, name):
    try:
        queue = QueueModel.objects.get(name=name)
        ids = json.loads(queue.ids.replace("'", '"'))
        del ids['users'][request.session['id']]
        queue.ids = str(ids)
        queue.save(update_fields=['ids'])
        del request.session['id']
        context = {'session': False, 'name': name}
        return render(request, 'user_page_join.html', context)
    except QueueModel.DoesNotExist:
        del request.session['id']
        context = {'error': "Срок действия QR-кода истек", 'name': name}
        return render(request, 'user_page_leave.html', context)
    except KeyError:
        context = {'session': False, 'name': name}
        return render(request, 'user_page_join.html', context)


def clear_cookies(request, name):
    del request.session['id']
    return redirect('join_the_queue', name=name)
