import json

THEMES = ['hard-gangsta', 'workout', 'soft-gangsta', 'feelings', 'fun', 'art', 'conscious']

# сначала старые, неагрессивные, непопулярные сейчас
# soft classic gangsta workout
# grime rapcore underground
# cloud electro vocal raprock emo mumble
# pop hookah

ARTISTS = [
    'Лигалайз', 'Многоточие', 'KREC',  # soft
    'Guf', 'Баста', 'Каста',  # classic
    'АК-47', 'Каспийский груз', 'Кровосток', 'The Chemodan', 'Смоки МО', 'Рем Дигга',  # gangsta
    'Миша Маваши', 'D-MAN 55', 'Грот',  # workout
    'Oxxxymiron', 'Соня Мармеладова', 'Alyona Alyona',  # grime
    'SID', 'REDO', 'RAM',  # rapcore
    'Полумягкие', 'ОУ74', 'Паша Техник', 'Овсянкин',  # underground
    'PHARAOH', 'Boulevard Depo', 'Mnogoznaal', 'Kizaru',  # cloud
    'ЛСП', 'ATL', 'Макс Корж', 'Slava Marlow',  # electro vocal
    'Скриптонит', 'Noize MC', 'Loqiemean', 'anacondaz', '25/17',  # RapRock
    'LIZER', 'Джизус', 'МУККА', 'lizer', # emo
    'Face', 'GONE.Fludd', 'Big Baby Tape', 'Элджей', 'Morgenshtern',  # mumble
    'Rakhim', 'Егор Крид', 'Тимати', 'Pyrokinesis', 'T-Fest',  # pop
    'MiyaGi', 'Jah Khalib', 'HammAli & Navai'  # hookah
]

ARTISTS = list(map(str.lower, ARTISTS))

GENRES = ['hiphop', 'battlerap', 'freestyle', 'regular', 'hiphopmusic', 'newschool', 'alternative', 'emo', 'raprock', 'electronichiphop', 'cloud', 'club', 'drill', 'electronicvocal', 'grime', 'mumble', 'phonk', 'hardcore', 'horrorcore', 'rapcore', 'underground', 'popular', 'hookah', 'pop', 'oldschool', 'oldschoolhardcore', 'gangsta', 'workout', 'russianrap', 'classic', 'soft']

leafs = ['Freestyle', 'Regular', 'Emo', 'RapRock', 'Cloud', 'Club', 'Drill', 'ElectronicVocal', 'Grime', 'Mumble', 'Phonk', 'Hardcore', 'Horrorcore', 'Underground', 'Hookah', 'Pop', 'Gangsta', 'WorkOut', 'Classic', 'Soft']
leafs = list(map(str.lower, leafs))




