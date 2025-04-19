from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from chat.models import Message, Users
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chat.ai_invoke import chat


# Create your views here.
def index(request):
    return render(request, "index.html")


def room(request, room_name):
    # 从查询参数中获取用户名
    username = request.GET.get('username')
    if not username:
        return HttpResponse("Please enter a valid username.", status=400)
    return render(request, "room.html", {"room_name": room_name, "username": username})


# 底层函数
@require_http_methods(["POST"])
def send_message_to_room(request):
    import json

    data = json.loads(request.body)
    room_name = data.get('roomName')
    username = data.get('username')
    message = data.get('message')

    # Save message to database
    Message.objects.create(content=message, room=room_name, username='AI')

    # Send message to room group
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"chat_{room_name}",
        {"type": "chat.message", "message": message}
    )
    return JsonResponse({'status': 'Message sent successfully'})


# ai调用
@require_http_methods(["POST"])
def ai_response(request):
    import json
    message_list = []

    data = json.loads(request.body)
    room_name = data.get('roomName')
    username = data.get('username')
    message = data.get('message')

    if not room_name or not message:
        return JsonResponse({'error': 'Room name and message are required'}, status=400)

    history_messages = Message.objects.filter(room=room_name).order_by('-create_time')[:10].values_list('username',
                                                                                                        'content')

    message_list.extend({"role": "user", "content": content} for username, content in history_messages)

    message_list.append({"role": "user", "content": message})

    # 调用ai函数
    ai_response = chat(message_list)

    # 数据库操作，以及同步
    Message.objects.create(content=ai_response, room=room_name, username='AI')

    # 底层逻辑
    '''
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"chat_{room_name}",
        {"type": "chat.message", "message": ai_response, "username": "AI"}
    )
    '''

    return JsonResponse({'response': ai_response})
