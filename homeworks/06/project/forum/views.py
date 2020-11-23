from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Message, User

from collections import deque


@api_view(['GET', 'PUT'])
def handle_all_forum(request):
    if request.method == 'GET':
        return get_all_forum()
    elif request.method == 'PUT':
        return put_root_message(request)


@api_view(['GET', 'PUT', 'POST', 'DELETE'])
def handle_one_message(request, id_):
    if request.method == 'GET':
        return get_message(id_)
    elif request.method == 'PUT':
        return put_message(request, id_)
    elif request.method == 'POST':
        return edit_message(request, id_)
    elif request.method == 'DELETE':
        return delete_message(id_)


def get_all_forum():
    forum = []
    mes2replies = {}
    d = deque()
    for cur in Message.objects.filter(reply=None):
        cur_dict = {
            'id': cur.id,
            'username': User.objects.get(id=cur.user_id.id).name,
            'text': cur.text,
            'replies': []
        }
        forum.append(cur_dict)
        mes2replies[cur.id] = cur_dict['replies']
        for e in Message.objects.filter(reply=cur.id):
            d.append(e)

    while len(d) > 0:
        cur = d.popleft()
        cur_dict = {
            'id': cur.id,
            'username': User.objects.get(id=cur.user_id.id).name,
            'text': cur.text,
            'replies': []
        }
        mes2replies[cur_dict['id']] = cur_dict['replies']
        mes2replies[cur.reply].append(cur_dict)
        for e in Message.objects.filter(reply=cur.id):
            d.append(e)

    return Response(forum)


def get_message(id_):
    mes2replies = {}
    d = deque()
    try:
        root = Message.objects.get(id=id_)
    except Message.DoesNotExist:
        res = f'Message does not exist id={id_}'
        return Response(res, status=404)
    forum = {
        'id': root.id,
        'username': User.objects.get(id=root.user_id.id).name,
        'text': root.text,
        'replies': []
    }
    mes2replies[root.id] = forum['replies']
    for e in Message.objects.filter(reply=root.id):
        d.append(e)

    while len(d) > 0:
        cur = d.popleft()
        cur_dict = {
            'id': cur.id,
            'username': User.objects.get(id=cur.user_id.id).name,
            'text': cur.text,
            'replies': []
        }
        mes2replies[cur_dict['id']] = cur_dict['replies']
        mes2replies[cur.reply].append(cur_dict)
        for e in Message.objects.filter(reply=cur.id):
            d.append(e)

    return Response(forum)


def put_root_message(request):
    try:
        User.objects.get(name=request.data['username'])
    except User.DoesNotExist:
        t = User(name=request.data['username'])
        t.save()
    new_message = Message(
        user_id=User.objects.get(name=request.data['username']),
        text=request.data['text'],
        reply=None
    )
    new_message.save()
    return Response()


def put_message(request, id_):
    try:
        message = Message.objects.get(id=id_)
    except Message.DoesNotExist:
        res = f'Message does not exist id={id_}'
        return Response(res, status=404)
    try:
        User.objects.get(name=request.data['username'])
    except User.DoesNotExist:
        t = User(name=request.data['username'])
        t.save()
    new_message = Message(
        user_id=User.objects.get(name=request.data['username']),
        text=request.data['text'],
        reply=id_
    )
    new_message.save()
    return Response()


def edit_message(request, id_):
    try:
        message = Message.objects.get(id=id_)
    except Message.DoesNotExist:
        res = f'Message does not exist id={id_}'
        return Response(res, status=404)
    message.text = request.data['text']
    message.save()
    return Response()


def delete_message(id_):
    try:
        message = Message.objects.get(id=id_)
    except Message.DoesNotExist:
        res = f'Message does not exist id={id_}'
        return Response(res, status=404)
    d = deque()
    for e in Message.objects.filter(reply=message.id):
        d.append(e)
    message.delete()

    while len(d) > 0:
        cur = d.popleft()
        for e in Message.objects.filter(reply=cur.id):
            d.append(e)
        cur.delete()

    return Response()
