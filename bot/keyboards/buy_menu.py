from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from utils import goods

def calculate_discount_percentage(price_actual, price_reference):
    if price_reference == 0:
        return 0
    return ((price_actual - price_reference) / price_reference) * 100

def get_buy_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for good in goods.get():
        # Рассчитываем цену для полугода и года
        base_monthly_price = goods.get()[0]['price']['ru']  # Базовая цена для 1 месяца
        actual_price = good['price']['ru']

        # Вычисляем скидку для полугода и года, если это применимо
        if good['months'] == 6:
            discount_percentage = calculate_discount_percentage(actual_price, base_monthly_price * 6)
            price_text = _("{months} месяцев - {price}₽ ({discount}%)").format(
                months=good['months'],
                price=actual_price,
                discount=f"{round(discount_percentage, 2)}"
            )
        elif good['months'] == 12:
            discount_percentage = calculate_discount_percentage(actual_price, base_monthly_price * 12)
            price_text = _("{months} месяцев - {price}₽ ({discount}%)").format(
                months=good['months'],
                price=actual_price,
                discount=f"{round(discount_percentage, 2)}"
            )
        else:
            price_text = _("{months} месяц - {price}₽").format(
                months=good['months'],
                price=actual_price
            )

        # Добавляем кнопку для товара
        builder.row(InlineKeyboardButton(
            text=price_text,
            callback_data=good['callback']
        ))

    return builder.as_markup()
