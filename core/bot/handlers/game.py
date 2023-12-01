from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from sqlalchemy.ext.asyncio import AsyncSession


from core.db.methods.request import (
    get_top_games_from_db,
    get_games_info_from_db,
)

from core.bot.keyboards.inline.inline import (
    get_games_menu,
    get_games_back_menu,
    get_pagination,
)

from core.bot.keyboards.inline.callback_factory import GamesCallbackFactory


router = Router()


@router.callback_query(GamesCallbackFactory.filter())
async def get_games(
    callback: CallbackQuery, callback_data: GamesCallbackFactory, session: AsyncSession
):
    if callback_data.action == "info" or callback_data.action == "back":
        steamid_id = int(callback_data.steam_id)
        general_games_info = await get_games_info_from_db(
            steam_id=steamid_id, session=session
        )
        number_of_games, total_cost, time_in_games = general_games_info[0]
        await callback.message.answer(
            text=f"{markdown.hbold('Аккаунт ' + callback_data.steam_name)}\n"
            f"Количество: {number_of_games}\n"
            f"Общая стоимость: {total_cost}\n"
            f"Общее количество часов: {time_in_games}",
            reply_markup=get_games_menu(
                steam_id=callback_data.steam_id, steam_name=callback_data.steam_name
            ),
        )
    else:
        if callback_data.action == "time":
            all_games = await get_top_games_from_db(
                steam_id=callback_data.steam_id,
                limit=callback_data.limit,
                order=callback_data.order,
                session=session,
            )
        elif callback_data.action == "cost":
            all_games = await get_top_games_from_db(
                steam_id=callback_data.steam_id,
                limit=callback_data.limit,
                order=callback_data.order,
                session=session,
            )
        elif callback_data.action == "all":
            all_games = await get_top_games_from_db(
                steam_id=callback_data.steam_id,
                limit=callback_data.limit,
                order=callback_data.order,
                session=session,
            )
        games_list = []
        grouped_games_list = []
        for (game_id, game_name, first_game_cost, time_in_game, game_cost) in all_games:
            games_list.append(
                f"{markdown.hbold(game_name)}\n"
                f"Количество часов: {time_in_game}\n"
                f"Актуальная стоимость: {game_cost}\n"
                f"Первоначальная стоимость: {first_game_cost}\n"
                f"Ссылка на торговую площадку: "
                f"{markdown.hlink('SteamLink', f'https://store.steampowered.com/app/{game_id}')}\n\n"
            )
        for i in range(0, len(games_list), 5):
            grouped_games_list.append("".join(games_list[i : i + 5]))
        if len(games_list) <= 5:
            await callback.message.answer(
                text=f"{''.join(games_list)}",
                disable_web_page_preview=True,
                reply_markup=get_games_back_menu(
                    steam_id=callback_data.steam_id, steam_name=callback_data.steam_name
                ),
            )
        else:
            await callback.message.edit_text(
                text=f"{grouped_games_list[callback_data.page]}",
                disable_web_page_preview=True,
                reply_markup=get_pagination(
                    action="all",
                    callbackfactory=GamesCallbackFactory,
                    page=callback_data.page,
                    pages_amount=len(grouped_games_list),
                    steam_id=callback_data.steam_id,
                    steam_name=callback_data.steam_name,
                    limit=callback_data.limit,
                    order=callback_data.order,
                ),
            )
    await callback.answer()
