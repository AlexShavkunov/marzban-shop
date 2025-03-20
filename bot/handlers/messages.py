from aiogram import Router, F
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from .commands import start
from keyboards import get_buy_menu_keyboard, get_back_keyboard, get_main_menu_keyboard, get_subscription_keyboard
from db.methods import can_get_test_sub, update_test_subscription_state, get_marzban_profile_db
from utils import marzban_api
import glv

router = Router(name="messages-router")

@router.message(F.text == __("Join 🚀"))
async def buy(message: Message):
    await message.answer(_("Choose the appropriate tariff ⭐"), reply_markup=get_buy_menu_keyboard())

@router.message(F.text == __("My subscription 🎯"))
async def profile(message: Message):
    user = await marzban_api.get_marzban_profile(message.from_user.id)
    if user is None:
        await message.answer(_("Your profile is not active at the moment.\n️\nYou can choose \"2 hours free 🎁\" or \"Join 🚀\"."), reply_markup=get_main_menu_keyboard())
        return
    subscription_text = _("Subscription page — <a href=\"{link}\">Follow the link</a>").format(
        link=glv.config['PANEL_GLOBAL'] + user['subscription_url']
    )
    await message.answer(subscription_text, reply_markup=get_back_keyboard())

@router.message(F.text == __("Frequent questions 📚"))
async def information(message: Message):
    faq_text = (
        f"{_('FAQ:')}\n\n"
        f"{_('1. A subscription is a way to authorize and get the latest server configurations. Some apps can update configurations automatically, but not all of them. If your internet stops working, try updating the subscription manually in the app.')}\n\n"
        f"{_('2. Are there connection limits? Yes, there are. You can connect from a maximum of 4 unique IP addresses. If the limit is exceeded, you need to disconnect one of your devices or wait for the connection list to update.')}\n\n"
        f"{_('3. Why do I see that access is disabled? If you see that access is disabled, it may mean that the connection limit has been exceeded. Make sure you are using no more than 4 unique IP addresses and disconnect any extra devices.')}\n\n"
        f"{_('4. What should I do if configurations don’t add automatically? Try copying and pasting your subscription link manually.')}"
    )

    await message.answer(faq_text, reply_markup=get_back_keyboard())

@router.message(F.text == __("Support 💙"))
async def support(message: Message):
    await message.answer(
        _("Follow the <a href=\"{link}\">link</a> and ask us a question. We are always happy to help 🤗").format(
            link=glv.config['SUPPORT_LINK']),
        reply_markup=get_back_keyboard())

@router.message(F.text == __("2 hours free 🎁"))
async def test_subscription(message: Message):
    result = await can_get_test_sub(message.from_user.id)
    if result:
        await message.answer(
            _("Your subscription is available in the \"My subscription 🎯\" section."),
            reply_markup=get_main_menu_keyboard())
        return
    await message.answer(_("Wait, the test subscription is being generated"))
    result = await get_marzban_profile_db(message.from_user.id)
    result = await marzban_api.generate_test_subscription(result.vpn_id)
    await update_test_subscription_state(message.from_user.id)
    await message.answer(
        _("Thank you for choice 💙\n️\nAccess granted! <a href=\"{link}\">Subscription and instructions</a> inside ✅\n\nYour subscription is purchased and available in \"My subscription 🎯\".").format(
            link=glv.config['PANEL_GLOBAL'] + result['subscription_url']
        ),
        reply_markup=get_main_menu_keyboard()
    )

@router.message(F.text == __("⏪ Back"))
async def start_text(message: Message):
    await start(message)

def register_messages(dp: Dispatcher):
    dp.include_router(router)

