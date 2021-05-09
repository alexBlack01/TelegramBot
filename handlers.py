from aiogram import Dispatcher, types

import main
import registration
import extra_registration
import search_user


def register_handlers_bot(dp: Dispatcher):
    dp.register_message_handler(main.say_hello, commands='start', state='*')
    dp.register_message_handler(main.check_hello, state=main.StageBot.waiting_for_check_hello)
    dp.register_message_handler(main.check_resolution, state=main.StageBot.waiting_for_check_resolution)
    dp.register_message_handler(main.choose_check_resolution, state=main.StageBot.waiting_for_choose_check_resolution)
    dp.register_message_handler(registration.registration,
                                state=registration.StageRegistration.waiting_for_registration)
    dp.register_message_handler(registration.get_name, state=registration.StageRegistration.waiting_for_name)
    dp.register_message_handler(registration.get_age, state=registration.StageRegistration.waiting_for_age)
    dp.register_message_handler(registration.get_sex, state=registration.StageRegistration.waiting_for_sex)
    dp.register_message_handler(registration.sex_chosen, state=registration.StageRegistration.waiting_for_sex_chosen)
    dp.register_message_handler(registration.get_city, state=registration.StageRegistration.waiting_for_city)
    dp.register_message_handler(registration.get_photo, state=registration.StageRegistration.waiting_for_photo,
                                content_types=[types.ContentType.PHOTO])
    dp.register_message_handler(main.choose_base_menu, state=main.StageBot.waiting_for_base_menu)
    dp.register_message_handler(extra_registration.choose_extra_registration,
                                state=extra_registration.StageExtraRegistration.waiting_for_extra_registration)
    dp.register_message_handler(extra_registration.choose_music_info,
                                state=extra_registration.StageExtraRegistration.waiting_for_get_music_info)
    dp.register_message_handler(extra_registration.choose_movie_info,
                                state=extra_registration.StageExtraRegistration.waiting_for_get_movie_info)
    dp.register_message_handler(extra_registration.choose_sex_info,
                                state=extra_registration.StageExtraRegistration.waiting_for_get_sex_info)
    dp.register_message_handler(extra_registration.choose_zodiac_info,
                                state=extra_registration.StageExtraRegistration.waiting_for_get_zodiac_info)
    dp.register_message_handler(extra_registration.choose_age_range_info,
                                state=extra_registration.StageExtraRegistration.waiting_for_get_age_range_info)
    dp.register_message_handler(search_user.regular_search_choose, state=search_user.StageSearch.waiting_for_regular_search)
