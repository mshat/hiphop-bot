from hiphop_bot.recommender_system.models.artist import ArtistModel


def init_artist_db_table():
    artist_model = ArtistModel()

    if len(artist_model.get_all()) == 0:
        print('Добавляю артистов в базу...')
        _add_artists(artist_model)
        print('Артисты добавлены в БД!')
    else:
        print(f'В базе {len(artist_model.get_all())} артистов')


def _add_artists(artist_model):
    artist_model.add_record('25/17', 1987, 2, ['hard-gangsta', 'soft-gangsta', 'feelings', 'art', 'conscious'], 'male', ['raprock', 'electronichiphop', 'russianrap'], ['spotify'], ['https://open.spotify.com/artist/7bempta6uxrrkiei6jmt'], ['25/17'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('anacondaz', 1987, 5, ['fun', 'art'], 'male', ['raprock'], ['spotify'], ['https://open.spotify.com/artist/2e7ydxnk4osy7nkhnqrof'], ['anacondaz', 'анакондаз', 'анакондазу', 'анакондаза'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('скриптонит', 1990, 4, ['soft-gangsta', 'feelings', 'fun', 'art'], 'male', ['raprock'], ['spotify'], ['https://open.spotify.com/artist/3vvluxeef7sl3izjcw0gi'], ['скриптонита', 'скриптонит', 'скриптоните', 'скриптониту'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('каспийский груз', 1983, 2, ['hard-gangsta'], 'male', ['gangsta'], ['spotify'], ['https://open.spotify.com/artist/5g5a3enoyfn6myylen21'], ['каспийский груз', 'каспийского груза', 'каспийском грузе', 'каспийскому грузу'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('loqiemean', 1993, 4, ['feelings', 'art'], 'male', ['raprock', 'rapcore'], ['spotify'], ['https://open.spotify.com/artist/2nl6vz4knihqjyooltadc'], ['локимина', 'loqiemean', 'локимину', 'локимин', 'локимине'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('pharaoh', 1996, 1, ['soft-gangsta', 'feelings', 'fun'], 'male', ['cloud'], ['spotify'], ['https://open.spotify.com/artist/1f8usyx5pbygwxf0bwdxw'], ['фараоне', 'фараон', 'фараону', 'pharaoh', 'фараона'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('d-man 55', 1982, 1, ['hard-gangsta', 'workout'], 'male', ['gangsta', 'workout'], ['spotify'], ['https://open.spotify.com/artist/1rzc1fjy8lt02wf5rpyl'], ['d-man 55', 'димане 55', 'димана 55', 'диман55', 'диман 55'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('mnogoznaal', 1993, 1, ['feelings', 'art'], 'male', ['cloud'], ['spotify'], ['https://open.spotify.com/artist/16znqmkdzrzd8ftxen2ku'], ['многознаале', 'многознаал', 'многознала', 'многознал', 'многозналу', 'mnogoznaal', 'многознаала', 'многознаалу', 'многознале'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('kizaru', 1989, 1, ['soft-gangsta', 'fun'], 'male', ['cloud'], ['spotify'], ['https://open.spotify.com/artist/5nipqmgsy4aueb7kgt8av'], ['кизаре', 'кизару', 'kizaru'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('лсп', 1989, 3, ['feelings', 'fun', 'art'], 'male', ['raprock', 'electronichiphop', 'electronicvocal'], ['spotify'], ['https://open.spotify.com/artist/4h8pgxeioi7j4me1yhyxl'], ['лсп'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('atl', 1989, 3, ['soft-gangsta', 'feelings', 'fun', 'art'], 'male', ['electronichiphop', 'electronicvocal'], ['spotify'], ['https://open.spotify.com/artist/2n6cvwo43yvjitgcpxywr'], ['атла', 'атл', 'atl'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('миша маваши', 1985, 1, ['hard-gangsta', 'workout'], 'male', ['workout'], ['spotify'], ['https://open.spotify.com/artist/37wepynzuufphcguet4j'], ['миша маваши', 'мишу маваши', 'миши маваши', 'мише маваши'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('oxxxymiron', 1985, 1, ['soft-gangsta', 'feelings', 'conscious'], 'male', ['grime'], ['spotify'], ['https://open.spotify.com/artist/1gcoybjnua1lbvo5rlx0j'], ['оксимироне', 'оксимирону', 'oxxxymiron', 'оксимирон', 'оксимирона'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('morgenshtern', 1998, 1, ['soft-gangsta', 'feelings', 'fun'], 'male', ['mumble'], ['spotify'], ['https://open.spotify.com/artist/0xnkqfs2ewb3y0vsfufc5'], ['моргенштерну', 'morgenshtern', 'моргенштерна', 'моргенштерн', 'моргенштерне'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('face', 1997, 1, ['soft-gangsta', 'fun', 'conscious'], 'male', ['mumble'], ['spotify'], ['https://open.spotify.com/artist/2z20q6eefm6w6piiksgtb'], ['фейс', 'фэйе', 'фэйсу', 'face', 'фэйса', 'фейса', 'фейсе', 'фэйс', 'фейсу'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('элджей', 1994, 1, ['soft-gangsta', 'feelings', 'fun'], 'male', ['club', 'mumble', 'pop'], ['spotify'], ['https://open.spotify.com/artist/0cm90jv892oeeegb3elmv'], ['элджея', 'элджей', 'элджее', 'элджею'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('ram', 1992, 1, ['hard-gangsta', 'feelings'], 'male', ['raprock', 'rapcore'], ['spotify'], ['https://open.spotify.com/artist/2vi0a9r3ijmlunznhx88b'], ['рэм', 'рэму', 'рэма', 'рэме', 'ram'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('redo', 1993, 1, ['hard-gangsta', 'feelings'], 'male', ['electronichiphop', 'rapcore'], ['spotify'], ['https://open.spotify.com/artist/1krpjnuxdhapazsh30tt1'], ['рэдо', 'редо', 'redo'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('полумягкие', 1990, 2, ['hard-gangsta', 'soft-gangsta', 'fun'], 'male', ['underground', 'russianrap'], ['spotify'], ['https://open.spotify.com/artist/1w5lk340wjdbs7duocobs'], ['полумягкие', 'полумягким', 'полумягких'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('оу74', 1990, 5, ['hard-gangsta', 'soft-gangsta'], 'male', ['underground', 'russianrap'], ['spotify'], ['https://open.spotify.com/artist/2oh9hrteht4vz8adywx8y'], ['оу74'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('овсянкин', 1984, 1, ['hard-gangsta', 'soft-gangsta'], 'male', ['underground', 'russianrap'], ['spotify'], ['https://open.spotify.com/artist/6a5dhhvg61qja7kmdlfsq'], ['овсянкине', 'овсянкина', 'овсянкин', 'овсянкину'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('miyagi', 1990, 1, ['soft-gangsta', 'feelings', 'fun', 'art'], 'male', ['hookah'], ['spotify'], ['https://open.spotify.com/artist/1kmpkcybuaz8tnfejlzkj'], ['miyagi', 'мияги'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('rakhim', 1998, 1, ['feelings', 'fun'], 'male', ['mumble', 'pop'], ['spotify'], ['https://open.spotify.com/artist/78g8fduykcn02tsgmli3q'], ['рахиме', 'рахим', 'рахиму', 'рахима', 'rakhim'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('тимати', 1983, 1, ['soft-gangsta', 'feelings', 'fun'], 'male', ['pop', 'soft'], ['spotify'], ['https://open.spotify.com/artist/3olccey7y6zte1gcfhxuw'], ['тимати'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('pyrokinesis', 1995, 1, ['feelings'], 'male', ['emo', 'cloud'], ['spotify'], ['https://open.spotify.com/artist/5rxthvb8jmngmsx7khd77'], ['пирокинезису', 'pyrokinesis', 'пирокинезисе', 'пирокинезиса', 'пирокинезис'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('кровосток', 1971, 3, ['hard-gangsta', 'soft-gangsta'], 'male', ['underground', 'gangsta'], ['spotify'], ['https://open.spotify.com/artist/0ksnnf08vvpbhdxn06mry'], ['кровостоку', 'кровосток', 'кровостоке', 'кровостока'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('ак-47', 1987, 2, ['hard-gangsta'], 'male', ['gangsta'], ['spotify'], ['https://open.spotify.com/artist/1v662xly7vfsecwosbsbt'], ['ак-47'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('грот', 1988, 1, ['hard-gangsta', 'soft-gangsta', 'feelings', 'art'], 'male', ['workout'], ['spotify'], ['https://open.spotify.com/artist/6x3n6aix6d8hh0eczkhzv'], ['гроту', 'грот', 'гроте', 'грота'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('guf', 1979, 1, ['hard-gangsta', 'soft-gangsta'], 'male', ['gangsta', 'classic'], ['spotify'], ['https://open.spotify.com/artist/0ocydryamsdx0nsnj59w1'], ['гуф', 'guf', 'гуфа', 'гуфе', 'гуфу'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('баста', 1980, 1, ['hard-gangsta', 'soft-gangsta', 'feelings'], 'male', ['gangsta', 'classic', 'soft'], ['spotify'], ['https://open.spotify.com/artist/7as5dy4rz9jac9tgotrj9'], ['басту', 'баста', 'басте', 'басты'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('каста', 1978, 4, ['soft-gangsta', 'art', 'conscious'], 'male', ['gangsta', 'classic'], ['spotify'], ['https://open.spotify.com/artist/5i37ovgant7ogiqkjsmvr'], ['каста', 'касту', 'касте', 'касты'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('лигалайз', 1977, 1, ['hard-gangsta', 'fun'], 'male', ['classic', 'soft'], ['spotify'], ['https://open.spotify.com/artist/5ypq9lhyfefs0vr5icob7'], ['лигалайза', 'лигалайзе', 'лигалайз', 'лигалайзу'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('krec', 1980, 1, ['soft-gangsta', 'feelings'], 'male', ['soft'], ['spotify'], ['https://open.spotify.com/artist/5gz8mj85i56irsvzgxfgg'], ['креку', 'креке', 'крек', 'krec', 'крека'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('slava marlow', 1999, 1, ['feelings', 'fun'], 'male', ['electronichiphop', 'electronicvocal'], ['spotify'], ['https://open.spotify.com/artist/55jryyk7rhvmbrvof0n'], ['славы мэрлоу', 'slava marlow', 'славе мэрлоу', 'слава мэрлоу', 'славу мэрлоу'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('noize mc', 1985, 4, ['feelings', 'fun', 'art', 'conscious'], 'male', ['raprock'], ['spotify'], ['https://open.spotify.com/artist/69v4zooomf1tnp59yyb1'], ['нойз мс', 'нойзе мс', 'нойз', 'нойза', 'noizemc', 'noize mc', 'нойзе', 'нойзу', 'нойзу мс', 'нойза мс'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('boulevard depo', 1991, 1, ['feelings', 'fun', 'art'], 'male', ['alternative', 'cloud'], ['spotify'], ['https://open.spotify.com/artist/7dh8w9flsy9w81ilr0xx'], ['бульвар депо', 'бульвару депо', 'бульвара депо', 'бульваре депо', 'boulevard depo'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('макс корж', 1988, 1, ['feelings', 'fun'], 'male', ['alternative', 'electronichiphop', 'electronicvocal'], ['spotify'], ['https://open.spotify.com/artist/5med8c7ogk5yuey2t7zz'], ['макса коржа', 'максе корже', 'макс корж', 'максу коржу'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('соня мармеладова', 1990, 1, ['soft-gangsta', 'fun'], 'male', ['grime'], ['spotify'], ['https://open.spotify.com/artist/7fmhppmtr3eltoejqsbk'], ['соню мармеладову', 'сони мармеладовой', 'соне мармеладовой', 'соня мармеладова'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('alyona alyona', 1991, 1, ['hard-gangsta', 'soft-gangsta'], 'female', ['grime'], ['spotify'], ['https://open.spotify.com/artist/2ic3gggmkixozp4qnaks'], ['алёны алёны', 'алёна алёна', 'алена алена', 'алёну алёну', 'алёне алёне', 'алену алену', 'алене алене', 'alyona alyona'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('gone.fludd', 1994, 1, ['soft-gangsta', 'feelings', 'fun'], 'male', ['mumble'], ['spotify'], ['https://open.spotify.com/artist/0ohuvvskerzk18bvwxfe'], ['гон флад', 'гон флада', 'гон фладе', 'гон фладду', 'гон фладда', 'гон фладде', 'gone.fludd', 'гон фладу', 'гон фладд', 'gone fludd'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('big baby tape', 2000, 1, ['soft-gangsta', 'fun'], 'male', ['mumble'], ['spotify'], ['https://open.spotify.com/artist/5nmwostnfht4ldetljsw'], ['биг бэйби тэйпу', 'биг бэйби тэйп', 'биг бэйби тейп', 'биг бейби тэйпа', 'биг бэйби тэйпе', 'биг бейби тэйпе', 'биг бейби тейпе', 'биг бэйби тейпу', 'биг бэйби тейпа', 'биг бейби тэйп', 'биг бейби тейпа', 'биг бэйби тейпе', 'биг бейби тейп', 'биг бэйби тэйпа', 'биг бейби тейпу', 'big baby tape', 'биг бейби тэйпу'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('паша техник', 1984, 5, ['hard-gangsta', 'fun'], 'male', ['underground', 'russianrap'], ['spotify'], ['https://open.spotify.com/artist/0xbf4ezw8nrlpspaq1d5'], ['паше технику', 'паше технике', 'паши техника', 'пашу техника', 'паша техник'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('sid', 1995, 1, ['hard-gangsta'], 'male', ['rapcore'], ['spotify'], ['https://open.spotify.com/artist/5yzhcgp6ozlqfxvpgphsxe'], ['sid', 'сид', 'сида', 'сиду', 'сиде'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('jah khalib', 1993, 1, ['feelings'], 'male', ['hookah'], ['spotify'], ['https://open.spotify.com/artist/4tjxa854ews8p5ebgcbqmv'], ['jah khalib', 'джа халиб', 'джа халибе', 'джа халиба', 'джа халибу'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('hammali & navai', 1992, 2, ['feelings'], 'male', ['hookah'], ['spotify'], ['https://open.spotify.com/artist/6o7tsogoef5mqpiz2kcywe'], ['hammali & navai', 'хамали & наваи', 'хамали и наваи'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('многоточие', 1978, 1, ['feelings'], 'male', ['soft'], ['spotify'], ['https://open.spotify.com/artist/1z14txuqytenmqjtkz75yu'], ['многоточие', 'многоточия', 'многоточию', 'многоточии'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('егор крид', 1994, 1, ['soft-gangsta', 'feelings', 'fun'], 'male', ['pop'], ['spotify'], ['https://open.spotify.com/artist/2kolmbxwsgmkfavopblp'], ['егора крида', 'егору криду', 'егор крид', 'егоре криде'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('t-fest', 1997, 1, ['feelings', 'fun'], 'male', ['electronicvocal', 'pop'], ['spotify'], ['https://open.spotify.com/artist/01lzudgxsojt5tbhuygb'], ['t-fest', 'ти-фест', 'ти-фесту', 'ти феста', 'ти фест', 'ти-феста', 'ти-фесте', 'ти фесте', 'тифесту'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('lizer', 1998, 1, ['feelings', 'fun'], 'male', ['emo', 'raprock', 'cloud'], ['spotify'], ['https://open.spotify.com/artist/0j6g5eiocrsdlyqaywt'], ['лизера', 'лизере', 'лизеру', 'lizer', 'лизер'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('смоки мо', 1982, 1, ['hard-gangsta', 'feelings'], 'male', ['gangsta'], ['spotify'], ['https://open.spotify.com/artist/6frycbkphxiybi6tffum'], ['смокимо', 'смоки мо'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('мукка', 1994, 1, ['feelings'], 'male', ['emo', 'raprock'], ['spotify'], ['https://open.spotify.com/artist/6a1cgybfaurrwzvd2iss'], ['мукка', 'мукки', 'мукку', 'мукке', 'мукк'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('джизус', 1997, 1, ['feelings'], 'male', ['emo', 'raprock'], ['spotify'], ['https://open.spotify.com/artist/7kb4f3pktjey9jbwi6uj'], ['джизуса', 'джизус', 'джизусу'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('рем дигга', 1987, 1, ['hard-gangsta', 'soft-gangsta', 'feelings'], 'male', ['gangsta'], ['spotify'], ['https://open.spotify.com/artist/2r1oelusjzxjrm8lc8fj'], ['рем дигги', 'рем дигга', 'ремдигга', 'рем диггу', 'рем дигге'], recalc_artists_pairs_proximity=False)

    artist_model.recalc_artists_pairs_proximity()


if __name__ == '__main__':
    init_artist_db_table()