from aiogram import Router, F, types
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from bot_config import database




new_recipe_router = Router()
new_recipe_router.message.filter(F.from_user.id == 1787320714)
new_recipe_router.callback_query.filter(F.from_user.id == 1787320714)

class NewRecipe(StatesGroup):
    confirm = State()
    name = State()
    recipe = State()
    image = State()
    price = State()
    category = State()

@new_recipe_router.callback_query(F.data == "new_recipe",default_state)
async def new_recipe(callback_query : CallbackQuery, state: FSMContext):
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да',callback_data= 'yes'),
                InlineKeyboardButton(text='Не',callback_data= 'no'),
            ]
        ]
    )
    await callback_query.message.answer('Вы уверены?', reply_markup=kb)
    await callback_query.answer()
    await state.set_state(NewRecipe.confirm)

@new_recipe_router.callback_query(NewRecipe.confirm,F.data == 'no')
async def cancel(callback_query : CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Отмена')
    await callback_query.answer()
    await state.clear()

@new_recipe_router.callback_query(NewRecipe.confirm,F.data == 'yes')
async def handler_confirm(callback : CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите название блюда')
    await callback.answer()
    await state.set_state(NewRecipe.name)

@new_recipe_router.message(NewRecipe.name)
async def handler_confirm(message : types.Message, state: FSMContext):
    name = message.text
    if name.isdigit():
        await message.answer('Пишите буквами')
        return
    await state.update_data(name=name)
    await message.answer('Введите рецепт')
    await state.set_state(NewRecipe.recipe)


@new_recipe_router.message(NewRecipe.recipe)
async def handler_recipe(message : Message, state: FSMContext):
    await state.update_data(recipe=message.text)
    await message.answer('Загрузите изображение')
    await state.set_state(NewRecipe.image)

@new_recipe_router.message(NewRecipe.image)
async def handler_image(message : Message, state: FSMContext):
    image = message.photo[-1].file_id
    await state.update_data(image=image)
    await message.answer('Введите цену')
    await state.set_state(NewRecipe.price)

@new_recipe_router.message(NewRecipe.price)
async def handler_price(message : Message, state: FSMContext):
    price = message.text
    if not price.isdigit():
        await message.answer('Вводите числа')
        return
    await message.answer('Введите категорию')
    await state.update_data(price=price)
    await state.set_state(NewRecipe.category)

@new_recipe_router.message(NewRecipe.category)
async def handler_category(message : Message, state: FSMContext):
    await state.update_data(category=message.text)
    data = await state.get_data()
    database.save_recipe(data)
    await message.answer('Рецепт добавлен')
    await state.clear()





