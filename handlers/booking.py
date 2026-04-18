from datetime import date

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from db.requests import get_lessons
from keyboards.booking_kb import lessons_keyboard
from keyboards.calendar_kb import get_calendar
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
@router.callback_query(BookingState.choosing_lesson,F.data.startswith("lesson:"))
async def choose_lesson(callback:CallbackQuery,state:FSMContext):
    lesson_id=int(callback.data.split(":")[1])
    await state.update_data(lesson_id=lesson_id)
    await state.set_state(BookingState.choosing_date)

    await callback.message.answer("Выберите дату:",reply_markup=get_calendar())

@router.callback_query(BookingState.choosing_lesson,F.data=="ignore")
async def ignore_calendar(callback:CallbackQuery,state:FSMContext):
    await callback.answer()

@router.callback_query(BookingState.choosing_lesson,F.data.startswith("cal_prev:"))
async def prev_calendar(callback:CallbackQuery):
    _,year,month=callback.data.split(":")
    year=int(year)
    month=int(month)
    month-=1
    if month==0:
        month=12
        year-=1
    await callback.message.edit_reply_markup(reply_markup=get_calendar(year,month))
    await callback.answer()
@router.callback_query(BookingState.choosing_lesson,F.data.startswith("cal_next:"))
async def next_calendar(callback:CallbackQuery):
    _,year,month=callback.data.split(":")
    year=int(year)
    month=int(month)
    month+=1
    if month==13:
        month=1
        year+=1
    await callback.message.edit_reply_markup(reply_markup=get_calendar(year,month))
    await callback.answer()
@router.callback_query(BookingState.choosing_date,F.data.startswith("cal_day:"))
async def start_booking(callback:CallbackQuery,state:FSMContext,session:AsyncSession):
    _, year, month,day = callback.data.split(":")
    selected_date=date(int(year),int(month),int(day))
    if not lessons:
        await callback.message.answer("Нет доступных предметов")
        await callback.answer()
        return
    await state.clear()
    await state.set_state(BookingState.choosing_lesson)
    await callback.message.answer("Выберите предмет:",reply_markup=lessons_keyboard(lessons))
    await callback.answer()