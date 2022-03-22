from typing import List
from hiphop_bot.recommender_system import config


class RawGeneralProximity:
    """
    Класс используется для хранения результатов вычисления мер близости после их расчёта.
    Далее его объекты передаются в метод обновления таблиы пар близости артистов в базе данных.
    В рекомендательной системе для хранения загруженных из бд данных о
    близости пар артистов ДОЛЖЕН ИСПОЛЬЗОВАТЬСЯ ДРУГОЙ КЛАСС
    """
    _gender_proximity: float
    _theme_proximity: float
    _year_of_birth_proximity: float
    _members_num_proximity: float
    _genre_proximity: float

    def __init__(
            self,
            gender_proximity: float,
            theme_proximity: float,
            year_of_birth_proximity: float,
            members_num_proximity: float,
            genre_proximity: float):
        self._gender_proximity = gender_proximity
        self._theme_proximity = theme_proximity
        self._year_of_birth_proximity = year_of_birth_proximity
        self._members_num_proximity = members_num_proximity
        self._genre_proximity = genre_proximity
        self._max_general_proximity = None
        self._min_general_proximity = None

    @property
    def gender_proximity(self) -> float:
        return self._gender_proximity * config.GENDER_PROXIMITY_MEASURE_WEIGHT

    @property
    def theme_proximity(self) -> float:
        return self._theme_proximity * config.THEME_PROXIMITY_MEASURE_WEIGHT

    @property
    def year_of_birth_proximity(self) -> float:
        return self._year_of_birth_proximity * config.YEAR_OF_BIRTH_PROXIMITY_MEASURE_WEIGHT

    @property
    def members_num_proximity(self) -> float:
        return self._members_num_proximity * config.MEMBERS_NUM_PROXIMITY_MEASURE_WEIGHT

    @property
    def genre_proximity(self) -> float:
        return self._genre_proximity * config.GENRE_PROXIMITY_MEASURE_WEIGHT

    @property
    def general_proximity(self) -> float:
        general_proximity = self.genre_proximity + self.theme_proximity + self.year_of_birth_proximity + \
               self.members_num_proximity + self.genre_proximity
        if not (self._max_general_proximity is None) and not (self._min_general_proximity is None):
            general_proximity = self._normalize_value(general_proximity, min_value=self._min_general_proximity,
                                                      max_value=self._max_general_proximity)
        return general_proximity

    @property
    def proximities_list(self) -> List[float]:
        return [self._gender_proximity, self._theme_proximity, self._year_of_birth_proximity,
                self._members_num_proximity, self._genre_proximity]

    def _normalize_value(self, value, min_value: float, max_value: float) -> float:
        if value < min_value:
            return 0
        value -= min_value
        value /= (max_value - min_value)
        return value

    def normalize_gender_proximity(self, min_value: float, max_value: float):
        self._gender_proximity = self._normalize_value(self.gender_proximity, min_value=min_value, max_value=max_value)
        return

    def normalize_theme_proximity(self, min_value: float, max_value: float):
        self._theme_proximity = self._normalize_value(self.theme_proximity, min_value=min_value, max_value=max_value)
        return

    def normalize_year_of_birth_proximity(self, min_value: float, max_value: float):
        self._year_of_birth_proximity = self._normalize_value(
            self.year_of_birth_proximity, min_value=min_value, max_value=max_value)
        return

    def normalize_members_num_proximity(self, min_value: float, max_value: float):
        self._members_num_proximity = self._normalize_value(
            self.members_num_proximity, min_value=min_value, max_value=max_value)
        return

    def normalize_genre_proximity(self, min_value: float, max_value: float):
        self._genre_proximity = self._normalize_value(self.genre_proximity, min_value=min_value, max_value=max_value)

    def normalize_general_proximity(self, min_value: float, max_value: float):
        self._min_general_proximity = min_value
        self._max_general_proximity = max_value