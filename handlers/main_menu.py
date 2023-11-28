from vkbottle.bot import Message
from config import labeler, state_dispenser
from keyboards import main_keyboard


@labeler.message(payload={'menu': 'menu'})
async def menu(message: Message):
    await message.answer(
        'Ну вот! Ты снова в меню)',
        keyboard=main_keyboard
    )
    await state_dispenser.delete(message.peer_id)
