from django.contrib.auth.decorators import login_required
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
        host = 'https://' + request.get_host() + f'/clear-cookies/{session_queue}'
        users = json.loads(QueueModel.objects.get(name=request.session.get('queue')).ids)
        context = {'host_url': host, 'name': session_queue, 'users': users['users']}
        return render(request, 'index.html', context)


def create_queue(request):
    form = QueueForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            queue = QueueModel.objects.filter(name=name)
            if len(queue) == 0:
                ids = {"users": [{"id": "0", "name": "None", "visible": "None"}]}
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
    your_name = request.POST.get('your_name')
    try:
        if session_id is None:
            your_name = request.POST.get('your_name')
            if your_name is None:
                context = {'id': session_id, 'name': name}
                return render(request, 'user_page_join.html', context)
            else:
                queue = QueueModel.objects.get(name=name)
                ids = json.loads(queue.ids)
                new_id = len(ids['users'])
                ids['users'].append({"id": str(new_id), "name": your_name, "visible": "Shown"})
                request.session['id'] = new_id
                queue.ids = json.dumps(ids)
                queue.save(update_fields=['ids'])
                session_id = request.session.get('id')
                context = {'id': session_id, 'name': name, 'your_name': your_name}
                return render(request, 'user_page_leave.html', context)
        else:
            context = {'id': session_id, 'name': name, 'your_name': your_name}
            return render(request, 'user_page_leave.html', context)
    except QueueModel.DoesNotExist:
        context = {'error': "Срок действия QR-кода истек", 'name': name}
        return render(request, 'user_page_join.html', context)


# def leave_the_queue(request, name):
#     try:
#         queue = QueueModel.objects.get(name=name)
#         ids = json.loads(queue.ids)
#         for i in ids["users"]:
#             if i["id"] == str(request.session['id']):
#                 ids["users"].remove(i)
#         queue.ids = json.dumps(ids)
#         queue.save(update_fields=['ids'])
#         del request.session['id']
#         context = {'name': name}
#         return render(request, 'user_page_join.html', context)
#     except QueueModel.DoesNotExist:
#         del request.session['id']
#         context = {'error': "Срок действия QR-кода истек", 'name': name}
#         return render(request, 'user_page_leave.html', context)
#     except KeyError:
#         context = {'name': name}
#         return render(request, 'user_page_join.html', context)


def clear_cookies(request, name):
    try:
        del request.session['id']
        return redirect('join_the_queue', name=name)
    except KeyError:
        return redirect('join_the_queue', name=name)


def admin_panel(request):
    session_queue = request.session.get('queue')
    if session_queue is None:
        return redirect('create_queue')
    else:
        users = json.loads(QueueModel.objects.get(name=request.session.get('queue')).ids)
        context = {'name': session_queue, 'users': users['users']}
        return render(request, 'admin_page.html', context)


def hide_user(request, move, user_id):
    session_queue = request.session.get('queue')
    queue = QueueModel.objects.get(name=session_queue)
    ids = json.loads(queue.ids)
    for i in ids["users"]:
        if i["id"] == user_id:
            if move == "hide":
                i['visible'] = "Hidden"
            elif move == "show":
                i['visible'] = "Shown"
    queue.ids = json.dumps(ids)
    queue.save(update_fields=['ids'])
    return redirect('admin_panel')
