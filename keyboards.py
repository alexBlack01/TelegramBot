import yes as yes
from emoji import emojize
from typing import NamedTuple

keys_for_resolution = [emojize(':white_check_mark:', use_aliases=True),
                       emojize(':no_entry_sign:', use_aliases=True)]

keys_for_sex = [emojize(':woman:', use_aliases=True),
                emojize(':man:', use_aliases=True)]

key_no_sex = emojize(':couple:', use_aliases=True)

key_save_and_cancel = [emojize(':white_check_mark:', use_aliases=True),
                       emojize(':back:', use_aliases=True)]

keys_for_extra_registration = [emojize(':musical_note:', use_aliases=True),
                               emojize(':movie_camera:', use_aliases=True),
                               emojize(':couple:', use_aliases=True),
                               emojize(':aries:', use_aliases=True),
                               emojize(':older_man:', use_aliases=True)]

keys_zodiac = [emojize(':aries:', use_aliases=True),
               emojize(':taurus:', use_aliases=True),
               emojize(':gemini:', use_aliases=True),
               emojize(':cancer:', use_aliases=True),
               emojize(':leo:', use_aliases=True),
               emojize(':virgo:', use_aliases=True),
               emojize(':libra:', use_aliases=True),
               emojize(':scorpius:', use_aliases=True),
               emojize(':sagittarius:', use_aliases=True),
               emojize(':capricorn:', use_aliases=True),
               emojize(':aquarius:', use_aliases=True),
               emojize(':pisces:', use_aliases=True)]

keys_music = [emojize(':guitar:', use_aliases=True),
              emojize(':microphone:', use_aliases=True),
              emojize(':headphones:', use_aliases=True),
              emojize(':violin:', use_aliases=True),
              emojize(':drum:', use_aliases=True),
              emojize(':musical_score:', use_aliases=True),
              emojize(':saxophone:', use_aliases=True),
              emojize(':banjo:', use_aliases=True)]

keys_movie = [emojize(':ghost:', use_aliases=True),
              emojize(':alien:', use_aliases=True),
              emojize(':dancer:', use_aliases=True),
              emojize(':boom:', use_aliases=True),
              emojize(':detective:', use_aliases=True),
              emojize(':books:', use_aliases=True),
              emojize(':gun:', use_aliases=True),
              emojize(':baby_bottle:', use_aliases=True),
              emojize(':european_castle:', use_aliases=True)]

keys_solution = [emojize(':thumbsup:', use_aliases=True),
                 emojize(':thumbsdown:', use_aliases=True),
                 emojize(':sleeping:', use_aliases=True),
                 emojize(':gear:', use_aliases=True)]

keys_base_menu = [emojize(':thumbsup:', use_aliases=True),
                 emojize(':thumbsdown:', use_aliases=True),
                 emojize(':sleeping:', use_aliases=True),
                 emojize(':gear:', use_aliases=True)]
