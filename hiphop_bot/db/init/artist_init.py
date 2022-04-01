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
    artist_model.add_record('25/17', 1987, 2, ['hard-gangsta', 'soft-gangsta', 'feelings', 'art', 'conscious'], 'male',
                            ['raprock', 'electronichiphop', 'russianrap'], ['spotify'],
                            ['https://open.spotify.com/artist/7bempta6uxrrkiei6jmt'], ['25/17'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('скриптонит', 1990, 4, ['soft-gangsta', 'feelings', 'fun', 'art'], 'male', ['raprock'],
                            ['spotify'], ['https://open.spotify.com/artist/3vvluxeef7sl3izjcw0g'],
                            ['скриптонит', 'скриптонита', 'скриптониту', 'скриптонитом', 'скрип', 'скрипа', 'скрипу',
                             'скрипом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('смоки мо', 1982, 1, ['hard-gangsta', 'feelings'], 'male', ['gangsta'], ['spotify'],
                            ['https://open.spotify.com/artist/6frycbkphxiybi6tffu'], ['смоки мо', 'смокимо', 'смоки'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('соня мармеладова', 1990, 1, ['soft-gangsta', 'fun'], 'male', ['grime'], ['spotify'],
                            ['https://open.spotify.com/artist/7fmhppmtr3eltoejqsb'],
                            ['соня мармеладова', 'сони мармеладовой', 'соне мармеладовой', 'соню мармеладову',
                             'соней мармеладовой'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('тимати', 1983, 1, ['soft-gangsta', 'feelings', 'fun'], 'male', ['pop', 'soft'],
                            ['spotify'], ['https://open.spotify.com/artist/3olccey7y6zte1gcfhxu'], ['тимати', 'timati'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('элджей', 1994, 1, ['soft-gangsta', 'feelings', 'fun'], 'male', ['club', 'mumble', 'pop'],
                            ['spotify'], ['https://open.spotify.com/artist/0cm90jv892oeeegb3elm'],
                            ['элджей', 'элджея', 'элджею', 'элджеем', 'элджэй', 'элджэя', 'элджэю', 'лджей', 'лджея',
                             'лджею', 'лджеем'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('баста', 1980, 1, ['hard-gangsta', 'soft-gangsta', 'feelings'], 'male',
                            ['gangsta', 'classic'], ['spotify'], ['https://open.spotify.com/artist/7as5dy4rz9jac9tgo'],
                            ['баста', 'басты', 'басте', 'басту', 'бастой'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('anacondaz', 1987, 5, ['fun', 'art'], 'male', ['raprock'], ['spotify'],
                            ['https://open.spotify.com/artist/2e7ydxnk4osy7nkhnqr'],
                            ['anacondaz', 'анакондаз', 'анакондаза', 'анакондазу', 'анакондазом', 'анакондаc',
                             'анакондаcа', 'анакондаcу', 'анакондаcом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('atl', 1989, 3, ['soft-gangsta', 'feelings', 'fun', 'art'], 'male',
                            ['electronichiphop', 'electronicvocal'], ['spotify'],
                            ['https://open.spotify.com/artist/2n6cvwo43yvjitgcpxyw'],
                            ['atl', 'атл', 'атла', 'атлу', 'атлом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('big baby tape', 2000, 1, ['soft-gangsta', 'fun'], 'male', ['mumble'], ['spotify'],
                            ['https://open.spotify.com/artist/5nmwostnfht4ldetljs'],
                            ['big baby tape', 'биг бейби тейп', 'биг бейби тейпа', 'биг бейби тейпу',
                             'биг бейби тейпом', 'биг беби тейп', 'биг беби тейпа', 'биг беби тейпу',
                             'биг беби тейпом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('boulevard depo', 1991, 1, ['feelings', 'fun', 'art'], 'male', ['alternative', 'cloud'],
                            ['spotify'], ['https://open.spotify.com/artist/7dh8w9flsy9w81ilr0x'],
                            ['boulevard depo', 'бульвар депо', 'бульвара депо', 'бульвару депо', 'бульваром депо',
                             'булевар депо', 'булевара депо', 'булевару депо', 'булеваром депо', 'бульвард депо',
                             'бульварда депо', 'бульварду депо', 'бульвардом депо', 'булевард депо', 'булеварда депо',
                             'булеварду депо', 'булевардом депо'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('alyona alyona', 1991, 1, ['hard-gangsta', 'soft-gangsta'], 'female', ['grime'],
                            ['spotify'], ['https://open.spotify.com/artist/2ic3gggmkixozp4qn'],
                            ['alyona alyona', 'алёна алёна', 'алёны алёны', 'алёне алёне', 'алёну алёну',
                             'алёной алёной', 'алена алена', 'алены алены', 'алене алене', 'алену алену',
                             'аленой аленой'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('d-man 55', 1982, 1, ['hard-gangsta', 'workout'], 'male', ['gangsta', 'workout'],
                            ['spotify'], ['https://open.spotify.com/artist/1rzc1fjy8lt02wf5rpy'],
                            ['d-man 55', 'дман 55', 'дмана 55', 'дману 55', 'дманом 55', 'диман 55', 'димана 55',
                             'диману 55', 'диманом 55', 'дман55', 'дмана55', 'дману55', 'дманом55', 'диман55',
                             'димана55', 'диману55', 'диманом55', 'д-ман 55', 'д-мана 55', 'д-ману 55', 'д-маном 55',
                             'д-ман55', 'д-мана55', 'д-ману55', 'д-маном55'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('face', 1997, 1, ['soft-gangsta', 'fun', 'conscious'], 'male', ['mumble'], ['spotify'],
                            ['https://open.spotify.com/artist/2z20q6eefm6w6piiksgt'],
                            ['face', 'фейс', 'фейса', 'фейсу', 'фейсом', 'фэйс', 'фэйса', 'фэйсу', 'фэйсом'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('gone.fludd', 1994, 1, ['soft-gangsta', 'feelings', 'fun'], 'male', ['mumble'], ['spotify'],
                            ['https://open.spotify.com/artist/0ohuvvskerzk18bvwxf'],
                            ['gone.fludd', 'gone fludd', 'гон флад', 'гон флада', 'гон фладу', 'гон фладом',
                             'гон фладд', 'гон фладда', 'гон фладду', 'гон фладдом', 'гонфлад', 'гонфлада', 'гонфладу',
                             'гонфладом', 'гонфладд', 'гонфладда', 'гонфладду', 'гонфладдом'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('guf', 1979, 1, ['hard-gangsta', 'soft-gangsta'], 'male', ['gangsta', 'classic'],
                            ['spotify'], ['https://open.spotify.com/artist/0ocydryamsdx0nsnj59w'],
                            ['guf', 'гуф', 'гуфа', 'гуфу', 'гуфом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('hammali & navai', 1992, 2, ['feelings'], 'male', ['hookah'], ['spotify'],
                            ['https://open.spotify.com/artist/6o7tsogoef5mqpiz2kcyw'],
                            ['hammali & navai', 'хамали & наваи', 'хамали и наваи', 'хамали наваи', 'хамаи & наваи',
                             'хамаи и наваи', 'хамаи наваи'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('jah khalib', 1993, 1, ['feelings'], 'male', ['hookah'], ['spotify'],
                            ['https://open.spotify.com/artist/4tjxa854ews8p5ebgcbqm'],
                            ['jah khalib', 'джа халиб', 'джа халиба', 'джа халибу', 'джа халибом', 'джа кхалиб',
                             'джа кхалиба', 'джа кхалибу', 'джа кхалибом', 'джахалиб', 'джахалиба', 'джахалибу',
                             'джахалибом', 'джакхалиб', 'джакхалиба', 'джакхалибу', 'джакхалибом'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('kizaru', 1989, 1, ['soft-gangsta', 'fun'], 'male', ['cloud'], ['spotify'],
                            ['https://open.spotify.com/artist/5nipqmgsy4aueb7kgt8a'],
                            ['kizaru', 'кизару', 'кизаре', 'кизарой', 'кизаром', 'кизара'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('krec', 1980, 1, ['soft-gangsta', 'feelings'], 'male', ['soft'], ['spotify'],
                            ['https://open.spotify.com/artist/5gz8mj85i56irsvzgxfg'],
                            ['krec', 'крек', 'крека', 'креку', 'креком'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('lizer', 1998, 1, ['feelings', 'fun'], 'male', ['emo', 'raprock', 'cloud'], ['spotify'],
                            ['https://open.spotify.com/artist/0j6g5eiocrsdlyqayw'],
                            ['lizer', 'лизер', 'лизера', 'лизеру', 'лизером', 'лиззер', 'лиззера', 'лиззеру',
                             'лиззером'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('loqiemean', 1993, 4, ['feelings', 'art'], 'male', ['raprock', 'rapcore'], ['spotify'],
                            ['https://open.spotify.com/artist/2nl6vz4knihqjyooltad'],
                            ['loqiemean', 'локимин', 'локимина', 'локимину', 'локимином', 'локимиан', 'локимиана',
                             'локимиану', 'локимианом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('miyagi', 1990, 1, ['soft-gangsta', 'feelings', 'fun', 'art'], 'male', ['hookah'],
                            ['spotify'], ['https://open.spotify.com/artist/1kmpkcybuaz8tnfejlzk'],
                            ['miyagi', 'мияги', 'миягей', 'миягем'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('mnogoznaal', 1993, 1, ['feelings', 'art'], 'male', ['cloud'], ['spotify'],
                            ['https://open.spotify.com/artist/16znqmkdzrzd8ftxen2k'],
                            ['mnogoznaal', 'многознал', 'многознала', 'многозналу', 'многозналом', 'многознаал',
                             'многознаала', 'многознаалу', 'многознаалом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('morgenshtern', 1998, 1, ['soft-gangsta', 'feelings', 'fun'], 'male', ['mumble'],
                            ['spotify'], ['https://open.spotify.com/artist/0xnkqfs2ewb3y0vsfufc'],
                            ['morgenshtern', 'моргенштерн', 'моргенштерна', 'моргенштерну', 'моргенштерном', 'морген',
                             'моргена', 'моргену', 'моргеном'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('noize mc', 1985, 4, ['feelings', 'fun', 'art', 'conscious'], 'male', ['raprock'],
                            ['spotify'], ['https://open.spotify.com/artist/69v4zooomf1tnp59yyb'],
                            ['noize mc', 'noizemc', 'нойз', 'нойза', 'нойзу', 'нойзом', 'нойз мс', 'нойза мс',
                             'нойзу мс', 'нойзом мс', 'нойзмс', 'нойзамс', 'нойзумс', 'нойзоммс', 'нойз мц', 'нойза мц',
                             'нойзу мц', 'нойзом мц', 'нойзмц', 'нойзамц', 'нойзумц', 'нойзоммц'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('oxxxymiron', 1985, 1, ['soft-gangsta', 'feelings', 'conscious'], 'male', ['grime'],
                            ['spotify'], ['https://open.spotify.com/artist/1gcoybjnua1lbvo5rlx0'],
                            ['oxxxymiron', 'оксимирон', 'оксимирона', 'оксимирону', 'оксимироном', 'окси'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('pharaoh', 1996, 1, ['soft-gangsta', 'feelings', 'fun'], 'male', ['cloud'], ['spotify'],
                            ['https://open.spotify.com/artist/1f8usyx5pbygwxf0bwdx'],
                            ['pharaoh', 'фараон', 'фараона', 'фараону', 'фараоном', 'фараох', 'фараоха', 'фараоху',
                             'фараохом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('pyrokinesis', 1995, 1, ['feelings'], 'male', ['emo', 'cloud'], ['spotify'],
                            ['https://open.spotify.com/artist/5rxthvb8jmngmsx7khd7'],
                            ['pyrokinesis', 'пирокинезис', 'пирокинезиса', 'пирокинезису', 'пирокинезисом',
                             'пирокинесис', 'пирокинесиса', 'пирокинесису', 'пирокинесисом'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('rakhim', 1998, 1, ['feelings', 'fun'], 'male', ['mumble', 'pop'], ['spotify'],
                            ['https://open.spotify.com/artist/78g8fduykcn02tsgmli3'],
                            ['rakhim', 'рахим', 'рахима', 'рахиму', 'рахимом', 'ракхим', 'ракхима', 'ракхиму',
                             'ракхимом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('ram', 1992, 1, ['hard-gangsta', 'feelings'], 'male', ['raprock', 'rapcore'], ['spotify'],
                            ['https://open.spotify.com/artist/2vi0a9r3ijmlunznhx88'],
                            ['ram', 'рэм', 'рэма', 'рэму', 'рэмом', 'рам', 'рама', 'раму', 'рамом'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('redo', 1993, 1, ['hard-gangsta', 'feelings'], 'male', ['electronichiphop', 'rapcore'],
                            ['spotify'], ['https://open.spotify.com/artist/1krpjnuxdhapazsh30tt'],
                            ['redo', 'рэдо', 'редо', 'рэдом', 'редом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('sid', 1995, 1, ['hard-gangsta'], 'male', ['rapcore'], ['spotify'],
                            ['https://open.spotify.com/artist/5yzhcgp6ozlqfxvpgphsx'],
                            ['sid', 'сид', 'сида', 'сиду', 'сидом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('slava marlow', 1999, 1, ['feelings', 'fun'], 'male',
                            ['electronichiphop', 'electronicvocal'], ['spotify'],
                            ['https://open.spotify.com/artist/55jryyk7rhvmbrvof0'],
                            ['slava marlow', 'слава мэрлоу', 'славы мэрлоу', 'славе мэрлоу', 'славой мэрлоу',
                             'слава мерлоу', 'славы мерлоу', 'славе мерлоу', 'славой мерлоу', 'слава марлоу',
                             'славы марлоу', 'славе марлоу', 'славой марлоу', 'слава марлов', 'славы марлов',
                             'славе марлов', 'славой марлов'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('t-fest', 1997, 1, ['feelings', 'fun'], 'male', ['electronicvocal', 'pop'], ['spotify'],
                            ['https://open.spotify.com/artist/01lzudgxsojt5tbhuyg'],
                            ['t-fest', 'tfest', 'ти фест', 'ти феста', 'ти фесту', 'ти фестом', 'тифест', 'тифеста',
                             'тифесту', 'тифестом', 'ти-фест', 'ти-феста', 'ти-фесту', 'ти-фестом', 'ти фэст',
                             'ти фэста', 'ти фэсту', 'ти фэстом', 'тифэст', 'тифэста', 'тифэсту', 'тифэстом', 'ти-фэст',
                             'ти-фэста', 'ти-фэсту', 'ти-фэстом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('ак-47', 1987, 2, ['hard-gangsta'], 'male', ['gangsta'], ['spotify'],
                            ['https://open.spotify.com/artist/1v662xly7vfsecwosbsb'],
                            ['ак-47', 'ак47', 'ака47', 'ak-47', 'ak47'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('грот', 1988, 1, ['hard-gangsta', 'soft-gangsta', 'feelings', 'art'], 'male', ['workout'],
                            ['spotify'], ['https://open.spotify.com/artist/6x3n6aix6d8hh0eczkhz'],
                            ['грот', 'грота', 'гроту', 'гротом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('джизус', 1997, 1, ['feelings'], 'male', ['emo', 'raprock'], ['spotify'],
                            ['https://open.spotify.com/artist/7kb4f3pktjey9jbwi6u'],
                            ['джизус', 'джизуса', 'джизусу', 'джизусом', 'джисус', 'джисуса', 'джисусу', 'джисусом'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('егор крид', 1994, 1, ['soft-gangsta', 'feelings', 'fun'], 'male', ['pop'], ['spotify'],
                            ['https://open.spotify.com/artist/2kolmbxwsgmkfavopbl'],
                            ['егор крид', 'егора крида', 'егору криду', 'егором кридом', 'крид', 'крида', 'криду',
                             'кридом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('каспийский груз', 1983, 2, ['hard-gangsta'], 'male', ['gangsta'], ['spotify'],
                            ['https://open.spotify.com/artist/5g5a3enoyfn6myylen2'],
                            ['каспийский груз', 'каспийского груза', 'каспийскому грузу', 'каспийским грузом'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('каста', 1978, 4, ['soft-gangsta', 'art', 'conscious'], 'male', ['gangsta', 'classic'],
                            ['spotify'], ['https://open.spotify.com/artist/5i37ovgant7ogiqkjsmv'],
                            ['каста', 'касты', 'касте', 'касту', 'кастой'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('кровосток', 1971, 3, ['hard-gangsta', 'soft-gangsta'], 'male', ['underground', 'gangsta'],
                            ['spotify'], ['https://open.spotify.com/artist/0ksnnf08vvpbhdxn06mr'],
                            ['кровосток', 'кровостока', 'кровостоку', 'кровостоком'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('лигалайз', 1977, 1, ['hard-gangsta', 'fun'], 'male', ['classic', 'soft'], ['spotify'],
                            ['https://open.spotify.com/artist/5ypq9lhyfefs0vr5icob'],
                            ['лигалайз', 'лигалайза', 'лигалайу', 'лигалайзом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('лсп', 1989, 3, ['feelings', 'fun', 'art'], 'male',
                            ['raprock', 'electronichiphop', 'electronicvocal'], ['spotify'],
                            ['https://open.spotify.com/artist/4h8pgxeioi7j4me1yhyx'], ['лсп', 'lsp'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('макс корж', 1988, 1, ['feelings', 'fun'], 'male', ['electronichiphop', 'electronicvocal'],
                            ['spotify'], ['https://open.spotify.com/artist/5med8c7ogk5yuey2t7'],
                            ['макс корж', 'макса коржа', 'максу коржу', 'максом коржом', 'корж', 'коржа', 'коржу',
                             'коржом'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('миша маваши', 1985, 1, ['hard-gangsta', 'workout'], 'male', ['workout'], ['spotify'],
                            ['https://open.spotify.com/artist/37wepynzuufphcguet4'],
                            ['миша маваши', 'миши маваши', 'мише маваши', 'мишу маваши', 'мишей маваши', 'маваши'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('многоточие', 1978, 1, ['feelings'], 'male', ['soft'], ['spotify'],
                            ['https://open.spotify.com/artist/1z14txuqytenmqjtkz75y'],
                            ['многоточие', 'многоточия', 'многоточию', 'многоточием'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('мукка', 1994, 1, ['feelings'], 'male', ['emo', 'raprock'], ['spotify'],
                            ['https://open.spotify.com/artist/6a1cgybfaurrwzvd2is'],
                            ['мукка', 'мукки', 'мукке', 'мукку', 'муккой', 'мука', 'муки', 'муке', 'мукой'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('овсянкин', 1984, 1, ['hard-gangsta', 'soft-gangsta'], 'male',
                            ['underground', 'russianrap'], ['spotify'],
                            ['https://open.spotify.com/artist/6a5dhhvg61qja7kmdlfs'],
                            ['овсянкин', 'овсянкина', 'овсянкину', 'овсянкином', 'овсянкиным'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('оу74', 1990, 5, ['hard-gangsta', 'soft-gangsta'], 'male', ['underground', 'russianrap'],
                            ['spotify'], ['https://open.spotify.com/artist/2oh9hrteht4vz8adywx8'],
                            ['оу74', 'оу-47', 'ou74', 'ou-74'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('паша техник', 1984, 5, ['hard-gangsta', 'fun'], 'male', ['underground', 'russianrap'],
                            ['spotify'], ['https://open.spotify.com/artist/0xbf4ezw8nrlpspaq1d'],
                            ['паша техник', 'паши техника', 'паше технику', 'пашу техника', 'пашей техником', 'техник',
                             'техника', 'технику', 'техником'], recalc_artists_pairs_proximity=False)
    artist_model.add_record('полумягкие', 1990, 2, ['hard-gangsta', 'soft-gangsta', 'fun'], 'male',
                            ['underground', 'russianrap'], ['spotify'],
                            ['https://open.spotify.com/artist/1w5lk340wjdbs7duocob'],
                            ['полумягкие', 'полумягких', 'полумягким', 'полумягкими'],
                            recalc_artists_pairs_proximity=False)
    artist_model.add_record('рем дигга', 1987, 1, ['hard-gangsta', 'soft-gangsta', 'feelings'], 'male', ['gangsta'],
                            ['spotify'], ['https://open.spotify.com/artist/2r1oelusjzxjrm8lc8f'],
                            ['рем дигга', 'рем дигги', 'рем диггу', 'рем диггой', 'рем дига', 'рем диги', 'рем дигу',
                             'рем дигой', 'рэм дигга', 'рэм дигги', 'рэм диггу', 'рэм диггой', 'рэм дига', 'рэм диги',
                             'рэм дигу', 'рэм дигой', 'ремдигга', 'ремдигги', 'ремдиггу', 'ремдиггой', 'ремдига',
                             'ремдиги', 'ремдигу', 'ремдигой', 'рэмдигга', 'рэмдигги', 'рэмдиггу', 'рэмдиггой',
                             'рэмдига', 'рэмдиги', 'рэмдигу', 'рэмдигой', 'дига', 'диги', 'диге', 'дигой', 'дигга',
                             'дигги', 'дигге', 'диггой'], recalc_artists_pairs_proximity=False)

    artist_model.recalc_artists_pairs_proximity()


if __name__ == '__main__':
    init_artist_db_table()