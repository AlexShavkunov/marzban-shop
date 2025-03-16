from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from utils import goods

def calculate_discount_percentage(price_actual, price_reference):
    if price_reference == 0:
        return 0
    return ((price_reference - price_actual) / price_reference) * 100

def get_buy_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for good in goods.get():
        # Рассчитываем месячную цену для каждого товара
        monthly_price = good['price']['ru']
        half_year_price = good['price']['half_year']
        yearly_price = good['price']['year']

        # Рассчитываем проценты
        half_year_discount = calculate_discount_percentage(half_year_price, monthly_price * 6)
        yearly_discount = calculate_discount_percentage(yearly_price, monthly_price * 12)

        # Формируем новый текст с процентами для полугода и года
        half_year_text = _("{months} месяцев - {price}₽ ({discount}%)").format(
            months=6,
            price=half_year_price,
            discount=round(half_year_discount, 2)
        )

        yearly_text = _("{months} месяцев - {price}₽ ({discount}%)").format(
            months=12,
            price=yearly_price,
            discount=round(yearly_discount, 2)
        )

        # Формируем кнопку для каждого товара
        builder.row(InlineKeyboardButton(
            text=_("{title} - {price_ru}₽").format(
                title=good['title'],
                price_ru=monthly_price
            ),
            callback_data=good['callback']
        ))

        builder.row(InlineKeyboardButton(
            text=half_year_text,
            callback_data=f"{good['callback']}_half_year"
        ))

        builder.row(InlineKeyboardButton(
            text=yearly_text,
            callback_data=f"{good['callback']}_year"
        ))

    return builder.as_markup()
