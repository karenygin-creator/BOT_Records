from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def lessons_keyboard(lessons):
    return InlineKeyboardMarkup(
        inline_keyboard=[
           [ InlineKeyboardButton(text=lesson.name, callback_data=f"lesson:{lesson.id}")]
            for lesson in lessons
        ]
    )