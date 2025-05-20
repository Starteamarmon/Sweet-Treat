import os
import sys
from dotenv import load_dotenv
from tortoise import Tortoise
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
import asyncio
from models import User, Order
from tortoise.exceptions import DoesNotExist

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cake_ordering.settings')
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(project_dir)
cake_creator_id = os.getenv('EXECUTOR_ID')

import django
django.setup()


async def init():
    await Tortoise.init(
        db_url="sqlite://database.db",
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()


build_cake_keyboard = [
    [
        InlineKeyboardButton("Выбрать корж", callback_data='select_crust'),
        InlineKeyboardButton("Выбрать начинку", callback_data='select_filling'),
    ],
    [
        InlineKeyboardButton("Назад", callback_data='back_to_main'),
    ],
    [
        InlineKeyboardButton("Заказать ещё", callback_data='back_to_main'),
    ],
    [
        InlineKeyboardButton('Заказать',callback_data='weight_cake')
    ]
]


build_cake_base = [
    [
        InlineKeyboardButton('Ванильный',callback_data='vanilla_base')
    ],
    [
        InlineKeyboardButton('Шоколадный',callback_data='chocolate_base')
    ],
    [
        InlineKeyboardButton('Красный бархат',callback_data='red_velvet_base')
    ],
    [
        InlineKeyboardButton('Медовый',callback_data='honey_base')
    ],
    [
        InlineKeyboardButton('Маковый',callback_data='poppy_seed_base')
    ],
    [
        InlineKeyboardButton('Назад',callback_data='back_to_main')
    ],
]


cake_cream = [
    [
        InlineKeyboardButton('Сметанно-сливочный',callback_data='sour_cream')
    ],
    [
        InlineKeyboardButton('Творожно-сливочный(крем-чиз)',callback_data='cream_cheese')
    ],
    [
        InlineKeyboardButton('Ганаш с молочныйм шоколадом',callback_data='Milk_Chocolate_Ganache')
    ],
    [
        InlineKeyboardButton('Ганаш с белым шоколадом',callback_data='white_Chocolate_Ganache')
    ],
    [
        InlineKeyboardButton('Ганаш с темным шоколадом',callback_data='black_Chocolate_Ganache')
    ],
    [
        InlineKeyboardButton('Творожно-сливочный крем со сгущеным молоком',callback_data='sour_cream_2')
    ]
]


cake_filling = [
    [
        InlineKeyboardButton('Ягодная',callback_data='berry_filling')
    ],
    [
        InlineKeyboardButton('Муссовая',callback_data='mousse_filling')
    ],
    [
        InlineKeyboardButton('Ганаш',callback_data='ganache_filling')
    ],
    [
        InlineKeyboardButton('Карамель',callback_data='caramel_filling')
    ]
]
ccaramel_filling = [
    [
        InlineKeyboardButton('Карамель',callback_data='caramel_filling_ok')
    ],
    [
        InlineKeyboardButton('Карамель-арахис',callback_data='caramel_peanuts')
    ],
    [
        InlineKeyboardButton('Карамель-грецкий орех',callback_data='caramel_walnut')
    ],
    [
        InlineKeyboardButton('Карамель-банан',callback_data='caramel_banana')
    ]
]
berry_filling = [
    [
        InlineKeyboardButton('Малиновый конфитюр',callback_data='raspberry_jam')
    ],
    [
        InlineKeyboardButton('Клубничный конфитюр',callback_data='strawberry_jam')
    ],
    [
        InlineKeyboardButton('Вишневый конфитюр',callback_data='cherry_jam')
    ],
    [
        InlineKeyboardButton('Смородиновый конфитюр',callback_data='currant_Jam')
    ],
    [
        InlineKeyboardButton('Ягодный конфитюр(микс)',callback_data='mix_jam')
    ],
]

mousse_filling = [
    [
        InlineKeyboardButton('Шоколадный мусс',callback_data='chocolate_mousse')
    ],
    [
        InlineKeyboardButton('Карамельный мусс',callback_data='caramel_mousse')
    ],
    [
        InlineKeyboardButton('Ягодный мусс',callback_data='berry_mousse')
    ]
]


final_coating = [
    [
        InlineKeyboardButton('Ганаш на белом шоколаде',callback_data='final_coating_white_ganache')
    ],
    [
        InlineKeyboardButton('Ганаш на молочном шоколаде',callback_data='final_coating_milk_ganache')
    ],
    [
        InlineKeyboardButton('Крем-чиз',callback_data='final_cream_cheese')
    ],
]

chocolate_mousse = [
    [
        InlineKeyboardButton('Мусс на молочном шоколаде',callback_data='milk_chocolate_mousse')
    ],
    [
        InlineKeyboardButton('Мусс на белом шоколаде',callback_data='white_chocolate_mousse')
    ],
    [
        InlineKeyboardButton('Мусс на тёмном шоколаде',callback_data='black_chocolate_mousse')
    ],
]

berry_mousse = [
    [
        InlineKeyboardButton('Малина',callback_data='raspberry_mousse')
    ],
    [
        InlineKeyboardButton('Клубника',callback_data='strawberry_mousse')
    ],
    [
        InlineKeyboardButton('Вишня',callback_data='cerry_mousse')
    ],
    [
        InlineKeyboardButton('Cмородина',callback_data='currant_mousse')
    ],
    [
        InlineKeyboardButton('Cмесь ягод (микс)',callback_data='mix_mousse')
    ],
]

ganache_filling = [
    [
        InlineKeyboardButton('Ганаш на белом шоколаде',callback_data='ganache_filling_white')
    ],
    [
        InlineKeyboardButton('Ганаш на молочном шоколаде',callback_data='ganache_filling_milk')
    ],
    [
        InlineKeyboardButton('Ганаш на тёмном шоколаде',callback_data='ganache_filling_black')
    ],
]
cake_build_final = [
    [
        InlineKeyboardButton('Да/Заказать',callback_data='YES')
    ],
    [
        InlineKeyboardButton('Нет/Главное меню',callback_data='back_to_main')
    ]
]


build_cake_reply_markup = InlineKeyboardMarkup(build_cake_keyboard)
mousse_filling_markup = InlineKeyboardMarkup(mousse_filling)
berry_filling_markup = InlineKeyboardMarkup(berry_filling)
cake_filling_markup = InlineKeyboardMarkup(cake_filling)
ganache_filling_markup = InlineKeyboardMarkup(ganache_filling)
caramel_filling_markup = InlineKeyboardMarkup(ccaramel_filling)
berry_mousse_markup = InlineKeyboardMarkup(berry_mousse)
chocolate_mousse_markup = InlineKeyboardMarkup(chocolate_mousse)
cake_cream_markup = InlineKeyboardMarkup(cake_cream)
build_cake_base_markup=InlineKeyboardMarkup(build_cake_base)
final_coating_markup = InlineKeyboardMarkup(final_coating)
cake_build_final_markup = InlineKeyboardMarkup(cake_build_final)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    url = f"https://127.0.0.1:8000/orders/loader/?telegram_id={telegram_id}"
    first_level_keyboard = [
    [
        InlineKeyboardButton("Выбрать торт", web_app=WebAppInfo(url=url)),
        InlineKeyboardButton("Собрать 🍰", callback_data='build_cake'),
    ],
    ]
    first_level_reply_markup = InlineKeyboardMarkup(first_level_keyboard)
    try:
        user = await User.get(chat_id=telegram_id)
        await update.message.reply_text(
            text=f'Привет, {user.name}!\nХочешь выбрать торт или собрать?',
            reply_markup=first_level_reply_markup
        )
    except DoesNotExist:
        user = await User.create(
            chat_id=telegram_id,
            name=update.effective_user.full_name,
        )
        
        await update.message.reply_text(f'Привет!{update.effective_user.full_name} Хочешь выбрать торт или собрать? :', reply_markup=first_level_reply_markup)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query 
    telegram_id = query.from_user.id
    url = f"https://127.0.0.1:8000/orders/loader/?telegram_id={telegram_id}"
    first_level_keyboard = [
        [
            InlineKeyboardButton("Выбрать торт", web_app=WebAppInfo(url=url)),
            InlineKeyboardButton("Собрать 🍰", callback_data='build_cake'),
        ],
    ]
    first_level_reply_markup = InlineKeyboardMarkup(first_level_keyboard)

    await query.message.edit_text(
        text='Хочешь выбрать торт или собрать?',
        reply_markup=first_level_reply_markup
    )

async def create_order_from_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from orders.models import Order
    message = update.message.text
    try:
        cake_name, weight, telegram_id = message.split()
        weight = float(weight)
        telegram_id = int(telegram_id)
        order = Order(
            telegram_id=telegram_id,
            cake_name=cake_name,
            weight=weight,
        )
        order.save()
        await update.message.reply_text('Заказ создан!')
    except:
        chat_id = update.effective_chat.id
        user = await User.get(chat_id=chat_id)
        context.user_data['cake_build']['вес'] = float(update.message.text)
        order_summary = (
                f"Ваш заказ, {user.name}!\n\n"
                f"Вы выбрали торт:\n"
                f"• Корж: {context.user_data['cake_build']['корж']}\n"
                f"• Крем: {context.user_data['cake_build']['крем']}\n"
                f"• Начинка: {context.user_data['cake_build']['начинка']}\n"
                f"• Покрытие: {context.user_data['cake_build']['покрытие']}\n"
                f"• Вес: {context.user_data['cake_build']['вес']} кг.\n"
            )
        await update.message.reply_text(order_summary,reply_markup=cake_build_final_markup)
        context.user_data['waiting_quantity_build_cake'] = False


async def send_message_creator(context:ContextTypes.DEFAULT_TYPE, message:str,reply_markup):
    await context.bot.send_message(chat_id=cake_creator_id, text=message,reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query 
    telegram_id = query.from_user.id
    chat_id = update.effective_chat.id
    user = await User.get(chat_id=chat_id)
    query = update.callback_query
    await query.answer()


    if query.data == "user_orders":
        user_orders = await Order.filter(user=user)
        

    elif query.data == 'build_cake':
        context.user_data['cake_build'] = {
        'корж': None,
        'начинка': None,
        'крем': None,
        'покрытие': None,
        'вес': 0.0
        }
        await query.edit_message_text(text='Выберите корж:', reply_markup=build_cake_base_markup)
    
    elif query.data == 'vanilla_base':
        context.user_data['cake_build']['корж'] = "Ванильный"
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nВыберите крем:",reply_markup=cake_cream_markup)  
    elif query.data == 'red_velvet_base':
        context.user_data['cake_build']['корж'] = "Красный бархат"
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nВыберите крем:",reply_markup=cake_cream_markup)       
    elif query.data == 'honey_base':
        context.user_data['cake_build']['корж'] = "Медовый"
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nВыберите крем:",reply_markup=cake_cream_markup)         
    elif query.data == 'poppy_seed_base':
        context.user_data['cake_build']['корж'] = "Маковый"
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nВыберите крем:",reply_markup=cake_cream_markup) 
    elif query.data == 'chocolate_base':
        context.user_data['cake_build']['корж'] = "Шоколадный"
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nВыберите крем:",reply_markup=cake_cream_markup) 

    elif query.data == 'sour_cream':
        context.user_data['cake_build']['крем'] = 'Сметанно-сливочный'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nВыберите начинку:",reply_markup=cake_filling_markup)           
    elif query.data == 'cream_cheese':
        context.user_data['cake_build']['крем'] = 'Творожно-сливочный(крем-чиз'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nВыберите начинку:",reply_markup=cake_filling_markup)            
    elif query.data == 'Milk_Chocolate_Ganache':
        context.user_data['cake_build']['крем'] = 'Ганаш с молочныйм шоколадом'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nВыберите начинку:",reply_markup=cake_filling_markup)             
    elif query.data == 'white_Chocolate_Ganache':
        context.user_data['cake_build']['крем'] = 'Ганаш с белым шоколадом'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nВыберите начинку:",reply_markup=cake_filling_markup)     
    elif query.data == 'black_Chocolate_Ganache':
        context.user_data['cake_build']['крем'] = 'Ганаш с темным шоколадом'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nВыберите начинку:",reply_markup=cake_filling_markup)          
    elif query.data == 'sour_cream_2':
        context.user_data['cake_build']['крем'] = 'Творожно-сливочный крем со сгущеным молоком'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nВыберите начинку:",reply_markup=cake_filling_markup)

    elif query.data == 'mousse_filling':
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nВыберите начинку:",reply_markup=mousse_filling_markup)
    elif query.data == 'berry_filling':
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nВыберите начинку:",reply_markup=berry_filling_markup)
    elif query.data == 'chocolate_mousse':
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nВыберите начинку:", reply_markup=chocolate_mousse_markup)
    elif query.data == 'ganache_filling':
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nВыберите начинку:",reply_markup=ganache_filling_markup)
    elif query.data == 'caramel_filling':
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nВыберите начинку:",reply_markup=caramel_filling_markup)

    elif query.data == 'caramel_filling_ok':
        context.user_data['cake_build']['начинка'] = 'Карамель'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'caramel_peanuts':
        context.user_data['cake_build']['начинка'] = 'Карамель-арахис'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'caramel_walnut':
        context.user_data['cake_build']['начинка'] = 'Карамель-грецкий орех'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'caramel_banana':
        context.user_data['cake_build']['начинка'] = 'Карамель-банан'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)

    elif query.data == 'ganache_filling_white':
        context.user_data['cake_build']['начинка'] = 'Ганаш на белом шоколаде'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'ganache_filling_milk':
        context.user_data['cake_build']['начинка'] = 'Ганаш на молочном шоколаде'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'ganache_filling_black':
        context.user_data['cake_build']['начинка'] = 'Ганаш на тёмном шоколаде'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)

    elif query.data == 'raspberry_jam':
        context.user_data['cake_build']['начинка'] = 'Малиновый конфитюр'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'strawberry_jam':
        context.user_data['cake_build']['начинка'] = 'Клубничный конфитюр'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'cherry_jam':
        context.user_data['cake_build']['начинка'] = 'Вишневый конфитюр'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'currant_Jam':
        context.user_data['cake_build']['начинка'] = 'Смородиновый конфитюр'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'mix_jam':
        context.user_data['cake_build']['начинка'] = 'Ягодный конфитюр(микс)'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)    

    elif query.data == 'milk_chocolate_mousse':
        context.user_data['cake_build']['начинка'] = 'мусс на молочном шоколаде'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'white_chocolate_mousse':
        context.user_data['cake_build']['начинка'] = 'мусс на белом шоколаде'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'black_chocolate_mousse':
        context.user_data['cake_build']['начинка'] = 'мусс на тёмном шоколаде'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    
    elif query.data == 'berry_mousse':
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nВыберите ягодный мусс:",reply_markup=berry_mousse_markup)

    elif query.data == 'raspberry_mousse':
        context.user_data['cake_build']['начинка'] = 'мусс: Малина'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'strawberry_mousse':
        context.user_data['cake_build']['начинка'] = 'мусс: Клубника'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'cerry_mousse':
        context.user_data['cake_build']['начинка'] = 'мусс: Вишня'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'currant_mousse':
        context.user_data['cake_build']['начинка'] = 'мусс: Cмородина'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    elif query.data == 'mix_mousse':
        context.user_data['cake_build']['начинка'] = 'мусс: Cмесь ягод (микс)'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)

    elif query.data == 'caramel_mousse':
        context.user_data['cake_build']['начинка'] = 'мусс: Карамельный'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nВыберите финальное покрытие:",reply_markup=final_coating_markup)
    
    elif query.data == 'final_coating_white_ganache':
        context.user_data['cake_build']['покрытие'] = 'Ганаш на белом шоколаде'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nФинальное покрытие: {context.user_data['cake_build']['покрытие']}\nВведите вес торта в килограммах:")
        context.user_data['waiting_quantity_build_cake'] = True
    elif query.data == 'final_coating_milk_ganache':
        context.user_data['cake_build']['покрытие'] = 'Ганаш на молочном шоколаде'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nФинальное покрытие: {context.user_data['cake_build']['покрытие']}\nВведите вес торта в килограммах:")
        context.user_data['waiting_quantity_build_cake'] = True  
    elif query.data == 'final_cream_cheese':
        context.user_data['cake_build']['покрытие'] = 'Крем-чиз'
        await query.edit_message_text(f"Основа: {context.user_data['cake_build']['корж']}\nКрем: {context.user_data['cake_build']['крем']}\nНачинка: {context.user_data['cake_build']['начинка']}\nФинальное покрытие: {context.user_data['cake_build']['покрытие']}\nВведите вес торта в килограммах:")
        context.user_data['waiting_quantity_build_cake'] = True



    elif query.data == 'back_to_main':
        await menu(update,context)
    
    elif query.data == 'YES':        
        order_summary = (
                f"\n• Корж: {context.user_data['cake_build']['корж']}\n"
                f"• Крем: {context.user_data['cake_build']['крем']}\n"
                f"• Начинка: {context.user_data['cake_build']['начинка']}\n"
                f"• Покрытие: {context.user_data['cake_build']['покрытие']}\n"
                f"• Вес: {context.user_data['cake_build']['вес']} кг\n"
            )
        await Order.create(user=user,order=order_summary)
        keyboard = [
            [InlineKeyboardButton('Связаться с клиетном', url=f'tg://user?id=')]
        ]
        await send_message_creator(context,f'Новый заказ на торт: {order_summary}, от пользователя {user.chat_id}\n tg://user?id={telegram_id}',reply_markup=InlineKeyboardMarkup(keyboard))
        # await send_message_creator(context,f'Новый заказ на торт: {order_summary}, от пользователя {user.chat_id}',reply_markup=InlineKeyboardMarkup(keyboard))
        await query.edit_message_text(text=f'{user.name}, спасибо за заказ!🤗\nМы Вам перезвоним в течении получаса🕖📲',reply_markup=InlineKeyboardMarkup([build_cake_keyboard[-2]]))





async def echo(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    telegram_id = update.message.from_user.id
    url = f"https://127.0.0.1:8000/orders/loader/?telegram_id={telegram_id}"
    first_level_keyboard = [
    [
        InlineKeyboardButton("Выбрать торт", web_app=WebAppInfo(url=url)),
        InlineKeyboardButton("Собрать 🍰", callback_data='build_cake'),
    ],
    ]
    first_level_reply_markup = InlineKeyboardMarkup(first_level_keyboard)
    


    if context.user_data.get('waiting_quantity_build_cake'):
        user = await User.get(chat_id=chat_id)
        context.user_data['cake_build']['вес'] = float(update.message.text)
        order_summary = (
                f"Ваш заказ, {user.name}!\n\n"
                f"Вы выбрали торт:\n"
                f"• Корж: {context.user_data['cake_build']['корж']}\n"
                f"• Крем: {context.user_data['cake_build']['крем']}\n"
                f"• Начинка: {context.user_data['cake_build']['начинка']}\n"
                f"• Покрытие: {context.user_data['cake_build']['покрытие']}\n"
                f"• Вес: {context.user_data['cake_build']['вес']} кг.\n"
            )
        await update.message.reply_text(order_summary,reply_markup=cake_build_final_markup)
        context.user_data['waiting_quantity_build_cake'] = False

    else:
        await update.message.reply_text("юзай команды")


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, create_order_from_message))

    echo_handler = MessageHandler(None, echo)
    button_handler = CallbackQueryHandler(button)
    application.add_handler(echo_handler)
    application.add_handler(button_handler)

    application.run_polling()

if __name__ == '__main__':
    main()




