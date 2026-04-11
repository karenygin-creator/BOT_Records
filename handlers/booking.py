from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from db.requests import get_lessons
from keyboards.booking_kb import lessons_keyboard
from states.booking_state import BookingState

router=Router()
@router.callback_query(F.data=="start_booking")
async def start_booking(callback:CallbackQuery,state:FSMContext,session:AsyncSession):
    lessons=await get_lessons(session)
    if not lessons:
        await callback.message.answer("Нет доступных предметов")
        await callback.answer()
        return
    await state.clear()
    await state.set_state(BookingState.choosing_lesson)
    await callback.message.answer("Выберите предмет:",reply_markup=lessons_keyboard(lessons))
    await callback.answer()