from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import OrderForm
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()


BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
EXECUTOR_ID = os.getenv('EXECUTOR_ID')

def loader_view(request):
    return render(request, 'loader.html')


def menu_view(request):
    telegram_id = request.GET.get("telegram_id")
    if not telegram_id:
        return HttpResponse("Ошибка: telegram_id не передан", status=400)
    return render(request, "menu.html", {"telegram_id": telegram_id})



def send_telegram_message(chat_id, text, user_id=None):
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
    }

    if user_id:
        data['reply_markup'] = json.dumps({
            "inline_keyboard": [[
                {
                    "text": f"ID: {user_id}",
                    "callback_data": f"user_{user_id}"
                }
            ]]
        })

    print(f"[Telegram] Отправляем данные: {data}")

    try:
        response = requests.post(TELEGRAM_API_URL, data=data)
        response.raise_for_status()
        print("[Telegram] Сообщение успешно отправлено")
    except requests.RequestException as e:
        print(f"[Telegram] Ошибка при отправке сообщения: {e}")
        if e.response is not None:
            print(f"[Telegram] Текст ошибки: {e.response.text}")



def order_view(request):
    telegram_id = request.GET.get("telegram_id")
    cake = request.GET.get("cake")
    success = False

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            cake_display = dict(order.CAKE_CHOICES).get(order.cake_name, order.cake_name)

            message_text = (
                f"🎂 <b>Новый заказ!</b>\n\n"
                f"👤 Telegram ID клиента: <code>{order.telegram_id}</code>\n"
                f"🍰 Торт: {cake_display}\n"
                f"⚖ Вес: {order.weight} кг\n"
                f"📅 Дата доставки: {order.date}\n"
                f"tg://user?id={order.telegram_id}"
            )

            contact_url = f"tg://user?id={order.telegram_id}"

            send_telegram_message(EXECUTOR_ID, message_text)

            success = True
    else:
        form = OrderForm(initial={
            'telegram_id': telegram_id,
            'cake_name': cake,
            'weight': 1.5,
        })

    return render(request, 'order.html', {
        'form': form,
        'success': success,
        'telegram_id': telegram_id,
    })