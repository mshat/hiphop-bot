import threading
from time import sleep
from typing import Callable, List
import validators
import PySimpleGUI as sg
from hiphop_bot.recommender_system.models.artist import ArtistModel, _Artist  # Импортируется для аннотаций
from hiphop_bot.db.abstract_model import AlreadyInTheDatabaseError


THEMES_FIELDS = ['_hard-gangsta_', '_workout_theme_', '_soft-gangsta_', '_feelings_', '_fun_', '_art_', '_conscious_']
GENRES_FIELDS = ['_alternative_', '_emo_', '_raprock_', '_electronichiphop_', '_cloud_', '_club_', '_drill_', '_grime_',
                 '_mumble_', '_phonk_', '_electronicvocal_', '_hardcore_', '_horrorcore_', '_rapcore_', '_underground_', '_popular_',
                 '_hookah_', '_pop_', '_oldschoolhardcore_', '_gangsta_', '_workout_', '_russianrap_', '_classic_',
                 '_soft_']
STREAMING_SERVICES_FIELDS = ['_spotify_', '_boom_', '_yandex_']

alternative_frame_layout = sg.Frame('Альтернатива', [[
        sg.Checkbox(text='Альтернатива', key='_alternative_'),
        sg.Checkbox(text='Эмо', key='_emo_'),
        sg.Checkbox(text='Рэп-рок', key='_raprock_')
]])

electronic_frame_layout = sg.Frame('Электронный хип-хоп', [[
        sg.Checkbox(text='Электронный хип-хоп', key='_electronichiphop_'),
        sg.Checkbox(text='Клауд', key='_cloud_'),
        sg.Checkbox(text='Клубный', key='_club_'),
        sg.Checkbox(text='Дрилл', key='_drill_'),
        sg.Checkbox(text='Грайм', key='_grime_'),
        sg.Checkbox(text='Мамбл', key='_mumble_'),
        sg.Checkbox(text='Фонк', key='_phonk_'),
        sg.Checkbox(text='Вокал', key='_electronicvocal_'),
]])

hardcore_frame_layout = sg.Frame('Хардкор', [[
        sg.Checkbox(text='Хардкор', key='_hardcore_'),
        sg.Checkbox(text='Хорроркор', key='_horrorcore_'),
        sg.Checkbox(text='Рэпкор', key='_rapcore_'),
        sg.Checkbox(text='Андеграунд', key='_underground_'),
]])

pop_frame_layout = sg.Frame('Поп-рэп', [[
        sg.Checkbox(text='Поп-рэп', key='_popular_'),
        sg.Checkbox(text='Кальянный', key='_hookah_'),
        sg.Checkbox(text='Поп', key='_pop_'),
]])


old_school_hardcore_frame_layout = sg.Frame('Олдскул хардкор', [[
        sg.Checkbox(text='Олдскул хардкор', key='_oldschoolhardcore_'),
        sg.Checkbox(text='Гангста', key='_gangsta_'),
        sg.Checkbox(text='Спортивный', key='_workout_'),
]])


russian_rap_layout = sg.Frame('Русский рэп', [[
        sg.Checkbox(text='Русский рэп', key='_russianrap_'),
        sg.Checkbox(text='Классический', key='_classic_'),
        sg.Checkbox(text='Чувства', key='_soft_'),
]])


spotify_layout = [
    sg.Frame('Spotify', [[
        sg.Text('Ссылка: '),  sg.InputText(default_text='', key='_spotify_', size=(70, 1))
    ]])
]

boom_layout = [
    sg.Frame('Boom', [[
        sg.Text('Ссылка: '),  sg.InputText(default_text='', key='_boom_', size=(70, 1))
    ]])
]

yandex_layout = [
    sg.Frame('Yandex Music', [[
        sg.Text('Ссылка: '),  sg.InputText(default_text='', key='_yandex_', size=(70, 1))
    ]])
]

artist_data_frame = sg.Frame('Artist', [
    [
        sg.Text('Имя:'), sg.InputText(key='_name_', default_text='', size=(25, 1)),
        sg.Text('Год рождения:'), sg.InputText(key='_year_of_birth_', default_text='', size=(5, 1)),
        sg.Text('Человек в группе:'), sg.InputText(key='_members_num_', default_text='1', size=(4, 1)),
    ],
    [
        sg.Text('Пол'),
        sg.Radio(text='Мужской', group_id=0, key='_male_radio_', default=True),
        sg.Radio(text='Женский', group_id=0, key='_female_radio_')
    ],
    [
        sg.Text('Темы', key='_themes_'),
        sg.Checkbox(text='hard-gangsta', key='_hard-gangsta_'),
        sg.Checkbox(text='workout', key='_workout_theme_'),
        sg.Checkbox(text='soft-gangsta', key='_soft-gangsta_'),
        sg.Checkbox(text='feelings', key='_feelings_'),
        sg.Checkbox(text='fun', key='_fun_'),
        sg.Checkbox(text='art', key='_art_'),
        sg.Checkbox(text='conscious', key='_conscious_'),
    ],
    [
        sg.Frame('Жанры', [
            [
                sg.Frame('Новая школа', [
                    [alternative_frame_layout, hardcore_frame_layout],
                    [electronic_frame_layout],
                    [pop_frame_layout]
                ]),
            ],
            [
                sg.Frame('Старая школа', [
                    [old_school_hardcore_frame_layout, russian_rap_layout]
                ])
            ]
        ])
    ],
    [
        sg.Frame('Стриминговые сервисы', [
            spotify_layout, boom_layout, yandex_layout
            ])
    ],
    [
        sg.Frame(
            'Имя на русском в разных падежах (через запятую) (по вопросам: кто? нет кого? кому? вижу кого? схожий с кем?)',
            [[sg.Multiline(default_text='', key='_aliases_', size=(98, 2))]]
        )
    ],
])

add_frame = sg.Frame('Add', [
    [sg.Button('Очистить поля ввода'), sg.Button(button_text='Добавить'), sg.Cancel()],
    [
        sg.Multiline(size=(100, 10), key='_add_output_'),
    ]
], size=(600, 200))

update_frame = sg.Frame('Update', [
    [sg.Button(button_text='Обновить')],
    [
        sg.Table(
            values=[[artist] for artist in sorted(ArtistModel().get_artist_names())],
            max_col_width=40, def_col_width=40, auto_size_columns=False, headings=['Имя'],
            justification="left", key='_artists_', enable_events=True)
    ],
    [sg.Multiline(size=(100, 4), key='_update_output_')]
])

delete_frame = sg.Frame('Delete', [
    [
        sg.Text('Имя удаляемого артиста:'), sg.InputText(key='_delete_name_', default_text='', size=(25, 1)),
    ],
    [
        sg.Button('Удалить артиста')
    ],
    [
        sg.Multiline(size=(100, 1), key='_delete_output_'),
    ]
])

action_frame = sg.Frame('Action', [[add_frame], [update_frame], [delete_frame]], size=(600, 750))

layout = [
    [artist_data_frame, action_frame]
]


class Gui:
    def __init__(self):
        self.window = sg.Window('Artist Model Redactor', layout, font=("Helvetica, 13"), size=(1400, 770)).Finalize()
        self.window.move(self.window.CurrentLocation()[0], 0)
        self.artist_model = ArtistModel()
        self._selected_artist: str | None = None

    def _do_after_time(self, func: Callable, time: float = 1):
        sleep(time)
        func()

    def do_after_time(self, func: Callable, time: float = 1):
        thread = threading.Thread(
            target=self._do_after_time,
            args=(func, time)
        )
        thread.start()

    def highlight_field(self, field: str, time=1, warning=False, current_color=None):
        highlight_color = 'red' if not warning else 'yellow'
        if not current_color:
            current_color = self.window[field].BackgroundColor
        self.window[field].Update(background_color=highlight_color)
        self.do_after_time(lambda: self.window[field].Update(background_color=current_color), time)

    def _check_input_for_empty_values(self, values) -> bool:
        res = True
        text_fields = ['_name_', '_aliases_', '_year_of_birth_', '_members_num_']
        for field_name in text_fields:
            if values[field_name] == '':
                res = False
                self.highlight_field(field_name, current_color='#f0f3f7')

        themes_values = [values[theme] for theme in THEMES_FIELDS if values[theme]]
        if True not in themes_values:
            for field_name in THEMES_FIELDS:
                res = False
                self.highlight_field(field_name, current_color='#64778d')

        genres_values = [values[genre] for genre in GENRES_FIELDS if values[genre]]
        if True not in genres_values:
            for field_name in GENRES_FIELDS:
                res = False
                self.highlight_field(field_name, current_color='#64778d')

        if not values['_male_radio_'] and not values['_female_radio_']:
            res = False
            self.highlight_field('_male_radio_', current_color='#64778d')
            self.highlight_field('_female_radio_', current_color='#64778d')
        return res

    def _check_types(self, values) -> bool:
        int_fields = ['_year_of_birth_', '_members_num_']
        res = True
        for field_name in int_fields:
            try:
                int(values[field_name])
            except ValueError:
                self.highlight_field(field_name, current_color='#f0f3f7')
                res = False
        return res

    def validate_links(self, values) -> bool:
        res = True

        links = set([values[link_field] for link_field in STREAMING_SERVICES_FIELDS])
        if links == {''}:
            res = False
            for link_field in STREAMING_SERVICES_FIELDS:
                self.highlight_field(link_field, current_color='#f0f3f7')

        # проверка соответствия названия стриминга ссылке
        spotify_val: str = values['_spotify_']
        if spotify_val:
            if str.find(spotify_val, 'spotify') == -1:
                self.highlight_field('_spotify_', current_color='#f0f3f7')
                res = False

        yandex_val: str = values['_yandex_']
        if yandex_val:
            if str.find(yandex_val, 'yandex') == -1:
                self.highlight_field('_yandex_', current_color='#f0f3f7')
                res = False

        boom_val: str = values['_boom_']
        if boom_val:
            if str.find(boom_val, 'vk.com') == -1:  # TODO добавить проверку на мобильую boom ссылку
                self.highlight_field('_boom_', current_color='#f0f3f7')
                res = False

        # валидатор url
        if res:
            for field_name in STREAMING_SERVICES_FIELDS:
                field_value = values[field_name]
                if field_value and not validators.url(field_value):
                    self.highlight_field(field_name, warning=True, current_color='#f0f3f7')

        return res

    def validate_input(self, values) -> bool:
        res = True
        res *= self._check_input_for_empty_values(values)
        res *= self._check_types(values)
        res *= self.validate_links(values)
        return res

    def _get_artist_data(self, values):
        name = values['_name_']
        year_of_birth = values['_year_of_birth_']
        members_num = values['_members_num_']
        if values['_male_radio_']:
            gender = 'male'
        elif values['_female_radio_']:
            gender = 'female'
        themes = [theme[1:-1] for theme in THEMES_FIELDS if values[theme]]
        if 'workout_theme' in themes:
            themes.remove('workout_theme')
            themes.append('workout')
        genres = [genre[1:-1] for genre in GENRES_FIELDS if values[genre]]
        streaming_services_names = [name[1:-1] for name in STREAMING_SERVICES_FIELDS if values[name] != '']
        streaming_service_links = []
        for service_name in STREAMING_SERVICES_FIELDS:
            if values[service_name] != '':
                if service_name == '_spotify_':  # удаляю параметр в spotify ссылке
                    link = values[service_name]
                    link = link[:str.find(link, '?si=')]
                    streaming_service_links.append(link)
                else:
                    streaming_service_links.append(values[service_name])

        raw_aliases: str = values['_aliases_']
        if raw_aliases:
            raw_aliases = raw_aliases.strip()
            raw_aliases = raw_aliases.strip(',')
            raw_aliases = raw_aliases.replace('\n', ' ').replace(',,', ',')
            aliases = raw_aliases.split(',')
            aliases = [alias.strip() for alias in aliases]
            aliases = [values['_name_']] + aliases

        return name, year_of_birth, members_num, themes, gender, genres, streaming_services_names,\
               streaming_service_links, aliases

    def add_artist(self, values):
        if not self.validate_input(values):
            self.window['_add_output_'].Update(f'Не удалось добавить артиста: неверные значения полей')
            self.do_after_time(lambda: self.window['_add_output_'].Update(''), 5)
        else:
            try:
                self.artist_model.add_record(*self._get_artist_data(values))
            except AlreadyInTheDatabaseError:
                self.window['_add_output_'].Update(f'Не удалось добавить: такой артист уже есть в базе')
            except Exception as e:
                self.window['_add_output_'].Update(f'Не удалось добавить артиста: {e}')
            else:
                self.window['_add_output_'].Update('')
                self.window['_add_output_'].Update(
                    f"Артист добавлен!\n {' '.join(map(str, self._get_artist_data(values)))}")

    def update_artist(self, values):
        if not self.validate_input(values):
            self.window['_update_output_'].Update(f'Не удалось обновить артиста: неверные значения полей')
            self.do_after_time(lambda: self.window['_update_output_'].Update(''), 5)
        else:
            if not self.artist_model.get_by_name(values['_name_']):
                self.window['_update_output_'].Update(f'Не удалось обновить: артиста с таким именем нет в базе')
                return
            
            try:
                self.artist_model.add_record(*self._get_artist_data(values), update_if_exist=True)
            except Exception as e:
                self.window['_update_output_'].Update(f'Не удалось обновить артиста: {e}')
            else:
                self.window['_update_output_'].Update('')
                self.window['_update_output_'].Update(
                    f"Артист обновлён!\n {' '.join(map(str, self._get_artist_data(values)))}")

    def clean_add_tab_fields(self):
        self.window['_name_'].Update('')
        self.window['_year_of_birth_'].Update('')
        self.window['_members_num_'].Update('')
        self.window['_male_radio_'].Update(True)
        self.window['_spotify_'].Update('')
        self.window['_boom_'].Update('')
        self.window['_yandex_'].Update('')
        [self.window[theme].Update(False) for theme in THEMES_FIELDS]
        [self.window[genre].Update(False) for genre in GENRES_FIELDS]
        self.window['_aliases_'].Update('')

    def delete_artist(self, values):
        delete_artist_name = values['_delete_name_']

        if delete_artist_name == '':
            self.highlight_field('_delete_name_', current_color='#f0f3f7')
            return
        delete_artist = self.artist_model.get_by_name(delete_artist_name)
        if not delete_artist:
            self.window['_delete_name_'].Update('')
            self.window['_delete_output_'].Update('Артист не найден!')
        else:
            try:
                self.artist_model.delete(delete_artist.id)
            except Exception as e:
                self.window['_delete_output_'].Update(f'Не удалось удалить артиста: {e}')
            else:
                self.window['_delete_output_'].Update('Артист удалён!')
                self.window['_delete_name_'].Update('')

    @property
    def selected_artist(self):
        return self._selected_artist

    @selected_artist.setter
    def selected_artist(self, name: List[str]):
        assert isinstance(name, list)
        assert len(name) > 0
        assert isinstance(name[0], str)
        name = name[0]
        if self._selected_artist != name:
            self._selected_artist = name
            self.load_artist(name)

    def _load_artist_data(self, artist: _Artist):
        self.window['_name_'].Update(artist.name)
        self.window['_year_of_birth_'].Update(artist.year_of_birth)
        self.window['_members_num_'].Update(artist.group_members_number)

        if artist.gender == 'male':
            self.window['_male_radio_'].Update(True)
        else:
            self.window['_female_radio_'].Update(True)

        spotify = artist.streaming_service_links.get_link_by_streaming_name('spotify')
        yandex = artist.streaming_service_links.get_link_by_streaming_name('yandex music')
        boom = artist.streaming_service_links.get_link_by_streaming_name('boom')
        if spotify:
            self.window['_spotify_'].Update(spotify)
        if yandex:
            self.window['_yandex_'].Update(yandex)
        if boom:
            self.window['_boom_'].Update(boom)

        artist_themes = [theme.name for theme in artist.themes]
        if 'workout' in artist_themes:
            workout_index = artist_themes.index('workout')
            artist_themes[workout_index] = 'workout_theme'
        [self.window[f'_{theme}_'].Update(True) for theme in artist_themes]

        artist_genres = [genre.name for genre in artist.genres]
        [self.window[f'_{genre}_'].Update(True) for genre in artist_genres]
        self.window['_aliases_'].Update(', '.join(artist.aliases))

    def load_artist(self, name):
        self.clean_add_tab_fields()
        artist = self.artist_model.get_by_name(name)
        if artist:
            self._load_artist_data(artist)
            self.window['_update_output_'].Update(
                f'В пространство Artist загружены данные артиста {self.selected_artist}')
        else:
            self.window['_update_output_'].Update(f'Не удалось загрузить артиста {self.selected_artist}')

    def show(self):
        while True:
            event, values = self.window.read()

            if event in (sg.WIN_CLOSED, None, 'Exit', 'Cancel'):
                break
            if not event and not values:
                continue

            if event == '_artists_':
                row = values[event]
                if row:
                    self.selected_artist = self.window["_artists_"].Values[row[0]]

            if event == 'Очистить поля ввода':
                self.clean_add_tab_fields()

            if event == 'Добавить':
                self.add_artist(values)

            if event == 'Обновить':
                self.update_artist(values)

            if event == 'Удалить артиста':
                self.delete_artist(values)

        self.window.close()


gui = Gui()
gui.show()

