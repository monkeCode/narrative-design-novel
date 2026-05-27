# game/script.rpy
# Игра «ДОПРОС» v2.8
# Жанр: Киберпанк-нуар / Психологический детектив

init python:
    import random
    def glitch_text(text, intensity=5):
        result = ""
        for char in text:
            if random.randint(1, 100) <= intensity:
                result += random.choice(["#", "&", "%", "$", "0", "1", " "])
            else:
                result += char
        return result

# Определение персонажей
define h = Character("Хардинг", color="#8B0000", what_prefix="[[BrainCall_v1.29.3] ", what_suffix="")
define jean = Character("Джин", color="#87CEEB")
define kyle = Character("Кайл Восс", color="#D3D3D3")
define irma = Character("Ирма Дюваль", color="#CD5C5C")
define silas = Character("Сайлас Нго", color="#4682B4")
define narrator = Character(None, kind=nvl)
define system = Character("СИСТЕМА", color="#00FF00", what_prefix="> ", what_suffix="")
define player = Character("Вы", color="#FFFFFF", what_prefix="", what_suffix="")
define li = Character("Инспектор ли", color="#1345db", what_prefix="", what_suffix="")

# Изображения
image player normal = "sprites/player/player_normal.png"
image player glitch = "sprites/player/player_glitch.png"
image kyle normal = "sprites/kyle/kyle_normal.png"
image kyle crying = "sprites/kyle/kyle_crying.png"
image kyle angry = "sprites/kyle/kyle_angry.png"
image irma normal = "sprites/irma/irma_normal.png"
image irma sad = "sprites/irma/irma_normal.png"
image silas normal = "sprites/silas/silas_normal.png"
image silas hand = "sprites/silas/silas_normal.png"
image silas praying = "sprites/silas/silas_praying.png"
image jean normal = "sprites/jean/jean_normal.png"
image jean sad = "sprites/jean/jean_sad.png"
image jean scared = "sprites/jean/jean_scared.png"
image harding shadow = "sprites/h.png"
image li normal = "sprites/li.png"

# Фоны
image bg title = "images/bg/bg.webp"
image bg archive = "images/bg/archive_room.png"
image bg interrogation = "images/bg/interrogation_room.png"
image bg corridor = "images/bg/corridor.png"
image bg mirror = "images/bg/toilet.jpg"
image bg incinerator = "images/bg/incinerator_room.png"
image bg black = "images/bg/black.jpg"

# Аудио
define audio.track1 = "audio/The Protagonist.wav"
define audio.track2 = "audio/Mystery Unsolved.wav"
define audio.sfx_glitch = "audio/error-glitch.mp3"
define audio.sfx_shock = "audio/electric-shock-15code.mp3"
define audio.sfx_incinerator = "audio/sfx/fire_blast.ogg"
define audio.sfx_call = "audio/cyberpunk-2077-phone-call.mp3"
define audio.sfx_lamp = "audio/Noise of electricity from a street lamp.mp3"
define audio.shot = "audio/sniper shot.wav"

# Переменные игры
default timer_seconds = 420
default timer_running = False
default knows_code = False
default opened_file_0 = False
default evidence_noted = {"kyle": False, "irma": False, "silas": False}
default empathy_score = 0
default current_suspect = None
default interrogated_count = 0
default final_choice = ""
default game_ended = False
default interrogated_kyle = False
default interrogated_irma = False
default interrogated_silas = False
default met_jean = False
default got_gun = False
default jean_trust = 0
default player_has_code = False

# Флаги для вопросов
default kyle_q1_asked = False
default kyle_q2_asked = False
default kyle_q3_asked = False
default kyle_q1a_chosen = False

default irma_q1_asked = False
default irma_q2_asked = False
default irma_q3_asked = False
default irma_q2a_chosen = False

default silas_q1_asked = False
default silas_q2_asked = False
default silas_q3_asked = False
default silas_q4_asked = False
default silas_q1a_chosen = False

# Инициализация
label start:
    $ renpy.music.set_volume(0.8, channel='music')
    play music track1 fadein 2.0
    scene bg black:
        zoom 4.0
    with fade
    
    call prologue
    call main_hub
    return

label prologue:
    nvl clear
    scene bg title:
        zoom 1.5
    with Pause(1.0)
    
    show text "Сектор-15-3, ОРДА\n(Отдел розыска девиантных андроидов)" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    
    show text "Дело № 2148-11-07\nИнспектор Ли, статус: ЛИКВИДИРОВАН.\nУровень допуска: ОМЕГА." at truecenter with dissolve
    pause 3.0
    hide text with dissolve
    
    show text "Запуск протокола в работу..." at truecenter with dissolve
    pause 1.5
    hide text with dissolve
    
    nvl clear
    scene bg mirror
    with fade
    
    stop music fadeout 0.5

    play sound sfx_lamp fadein 0.5

    player "Ахх... наконец-то можно спокойно поссать."
    player "..."

    show player normal at center
    with dissolve
    player "Ну и рожа в зеркале. Нужно умыться."
    show player glitch at center:
        alpha 0.0
        linear 0.3 alpha 1.0
        linear 0.3 alpha 0.0
    play sound sfx_glitch
    player "...?"
    player "...?"

    play sound sfx_call

    "[[BrainCall_v1]] - Звонок от Главы ОРДА\n- Принять"

    player "Чёрт..."
    stop sound fadeout 0.0

    "Зазвучал знакомый металлический голос"
    show harding shadow at left
    h "Следователь 6591. Слушай задачу. Инспектор Ли мёртв."
    h "Характер ранений указывает на андроида."
    h "Время доступа к контуру допросной — семь минут. Используй памятку."
    hide harding shadow
    nvl clear
    window hide
    nvl clear
    system "[[memory_fragment_access: granted]"
    player "...уже шестой год работаю в этом чертовом отделе."
    player "Как давно Хардинг поставил этот горловой протез? Аж уши вянут его слушать."
    nvl clear
    window show
    
    hide player normal with dissolve
    nvl clear
    return

label main_hub:
    stop sound fadeout 0.5
    if game_ended:
        return
        
    nvl clear
    scene bg interrogation:
        zoom 0.7
    with fade
    
    if not timer_running:
        $ timer_seconds = 420
        $ timer_running = True
        show screen countdown_timer
    
    menu hub_menu:
        "Что я должен делать?"
        "Памятка":
            call memo_screen
            jump main_hub
        "Архив":
            call archive_room
            jump main_hub
        "Допросная":
            call suspect_selection
            jump main_hub
        "Выйти покурить" if interrogated_count >= 1 and not met_jean:
            call corridor_scene
            jump main_hub
        "Осмотреть стол 325-1" if silas_q4_asked:
            player "Хм, какие-то бумаги, семейная фотография, у Сайласа еще были свои руки..."
            player "В шкафу лежит пистолет, странно, огнестрельное оружие выведено из экспуатации более 53 лет назад, возьму как улику"
            $ got_gun = True
        "Закончить допрос (вынести решение)" if interrogated_count >= 3 or timer_seconds <= 0:
            jump final_decision

label suspect_selection:
    nvl clear
    play music track2 fadein 0.5
    if interrogated_kyle and interrogated_irma and interrogated_silas:
        player "Все трое уже допрошены. Пора принимать решение."
        jump main_hub
    
    menu:
        "Кого вызвать на допрос?"
        "Кайл Восс" if not interrogated_kyle:
            $ current_suspect = "kyle"
            $ interrogated_kyle = True
            $ interrogated_count += 1
            call interrogation_kyle
            jump main_hub
        "Ирма Дюваль" if not interrogated_irma:
            $ current_suspect = "irma"
            $ interrogated_irma = True
            $ interrogated_count += 1
            call interrogation_irma
            jump main_hub
        "Сайлас Нго" if not interrogated_silas:
            $ current_suspect = "silas"
            $ interrogated_silas = True
            $ interrogated_count += 1
            call interrogation_silas
            jump main_hub
        "Назад":
            jump main_hub

label archive_room:
    stop music fadeout 0.5
    play sound sfx_lamp fadein 0.5
    nvl clear
    scene bg archive
    with fade
    
    system "[[bio-link established]"
    system "Доступ разрешен. Данные по делу 2148-11-07."
    
label archive_menu:
    nvl clear
    menu:
        "Просмотреть досье:"
        "Кайл Восс":
            call dossier_kyle
            jump archive_menu
        "Ирма Дюваль":
            call dossier_irma
            jump archive_menu
        "Сайлас Нго":
            call dossier_silas
            jump archive_menu
        "[[Скрытый файл: Объект 0]" if player_has_code:
            call secret_file_0
            jump archive_menu
        "Вернуться в допросную":
            jump main_hub

label memo_screen:
    nvl clear
    scene bg black:
        zoom 4.0
    nvl clear
    show text '''ПАМЯТКА СЛЕДОВАТЕЛЯ ОРДА

1. ЭМПАТИЯ
Андроид имитирует сочувствие на поверхностном уровне.

2. РАЦИОНАЛЬНОСТЬ 
Андроид не способен действовать вопреки базовым директивам самосохранения или эффективности.

3. ПАМЯТЬ
Ложная память андроида стерильна. В ней нет запахов, вкуса пепла, случайных деталей.

4. КОНТАКТ
У андроидов не проявляется гаптофобия''' at truecenter
    with dissolve
    pause
    hide text with dissolve
    
    nvl clear
    show text "Примечание ОРДА: В 97.3493% случаев субъекты, проявившие более 2-х признаков по данному списку, являются андроидами." at truecenter with moveinbottom
    pause
    hide text with dissolve
    nvl clear
    return

# ========== ДОСЬЕ ==========
label dossier_kyle:
    nvl clear
    scene bg archive
    show kyle normal at left with dissolve
    
    system "Загрузка досье: Кайл Восс"
    nvl clear
    
    "=== ЛИЧНОЕ ДЕЛО № 671B ==="
    "Имя: Кайл Восс"
    "Возраст: 27 лет"
    "Статус: Техник 3-го разряда, уволен по статье 'Эмоциональная привязанность к оборудованию'"
    "Место работы (бывшее): V.E.R.A. Industries, Сектор 14, линия сборки андроидов серии XB"
    nvl clear
    
    "Инспектор Ли был куратором программы утилизации дефектных андроидов в V.E.R.A. Industries."
    "Ли лично подписал 47 ордеров на утилизацию за последний квартал, включая ордер на XB-7 (получил неофициальное имя 'Гектор')."
    "Субъект подал 43 апелляции на решение об утилизации, в т.ч. на XB-7. Все отклонены по инициативе инсп. Ли."
    nvl clear
    
    "=== УЛИКИ ==="
    "Улика №1: Аудиолог (изъят при задержании в баре 'Ржавый болт')"
    "«... Я точно знаю, что они живые, я их как будто понимаю... Этот мудак убил всех из них, каждого лично подписал...»."
    nvl clear
    
    "Улика №2: Внутренняя записка, предоставленная V.E.R.A. Industries"
    "Отдел психологического контроля. Тема: 'Синдром ложной эмпатии к объекту'."
    "«У техника Кайла Восса зафиксирована эмоциональная привязанность к андроиду XB-7."
    "Субъект разговаривает с машиной, даёт ей имя 'Гектор'. Отказывается сдать машину на утилизацию»."
    nvl clear
    
    "Улика №3: История болезни"
    "Диагноз: Хроническая депрессия, тревожное расстройство. Принимает нейролептики 'Сомнус-5' в повышенной дозировке."
    "Лечащий врач отмечает суицидальные наклонности и патологическое избегание физического контакта."
    nvl clear
    
    $ evidence_noted["kyle"] = True
    hide kyle with dissolve
    nvl clear
    return

label dossier_irma:
    nvl clear
    scene bg archive
    show irma normal at left with dissolve
    
    system "Загрузка досье: Ирма Дюваль"
    nvl clear
    
    "=== ЛИЧНОЕ ДЕЛО № 2089 ==="
    "Имя: Ирма Дюваль"
    "Возраст: 36 лет"
    "Статус: Рецидивист. Торговля органами (синтетическими и органическими)"
    "Криминальный профиль: Связана с 'Красным синдикатом'. Специализация — нелегальная трансплантология и био-модификации."
    nvl clear
    
    "Приложение к делу — информация о родственниках"
    "Марк Дюваль — брат субъекта (дело № 2089-А) — был задержан за кражу медицинского геля 'Регенекс-7'."
    "Гель требовался субъекту из-за начавшегося отторжения глазного импланта."
    "Инспектор Ли лично добился ЛИКВИДАЦИИ субъекта по делу 2089-А. Марк Дюваль расстрелян при попытке к бегству (согласно рапорту)."
    "Тело не выдано, отправлено на био-утилизацию."
    "Субъект угрожала инсп. Ли после ситуации по делу 2089-А, заявляя: 'Я найду способ уничтожить тебя, мразь'."
    nvl clear
    
    "=== УЛИКИ ==="
    "Улика №1: Запись слов субъекта в отделении"
    "«Я убью тебя за то, что ты сделал с моим братом. Посмотрим, сколько дают на чёрном рынке за био-мусор»."
    nvl clear
    
    "Улика №2: Расписка 'Красного синдиката'"
    "«Я, Ирма Дюваль, была должна 'Красному синдикату' 40 000 кредитов за имплант модели 'Око-4' и установку."
    "Долг погашен утром 07.11.2148. Причина: выплата аванса за неопознанный заказ на биоматериал человеческого происхождения. Примечание: материал изъят утром того же дня»."
    nvl clear
    
    "Улика №3: Медицинская карта Ирмы Дюваль"
    "Состояние: Хронический болевой синдром. Удаление матки (07.11.2148, клиника 'Новая Жизнь', оплачено наличными)."
    "Психологический профиль: ПТСР, агрессивная защита личных границ, неспособность к доверию."
    nvl clear
    
    $ evidence_noted["irma"] = True
    hide irma with dissolve
    nvl clear
    return

label dossier_silas:
    nvl clear
    scene bg archive
    show silas normal at left with dissolve
    
    system "Загрузка досье: Сайлас Нго"
    nvl clear
    
    "=== ЛИЧНОЕ ДЕЛО № 0001-OMEGA ==="
    "Имя: Сайлас Нго"
    "Возраст: 52 года"
    "Статус: Монах Ордена Сломанной Шестерни. Кибернетик-самоучка."
    "История: Бывший инспектор 'ОРДА'. Несчастный случай на работе, вынужденная ампутация конечностей. Ушёл в религию после инцидента."
    nvl clear
    
    "=== СВЯЗЬ С ИНСПЕКТОРОМ ЛИ ==="
    "Субъект был напарником инсп. Ли. Во время рейда по делу о контрабанде био-чипов отряд попал в засаду."
    "Со слов Субъекта: Ли использовал Субъекта как живой щит, чтобы уйти от лазерного огня. Сайлас потерял обе руки и частично ноги."
    "После операции ипсп. Ли для него списанные биопротезы (модель 'Харон-4')"
    "Инсп. Ли требовал признать вину, согласно документам Субъекта признают виновным в гибели двоих коллег."
    nvl clear
    
    "=== УЛИКИ ==="
    "Улика №1: Медицинский отчёт"
    "«Протез правой руки модели 'Харон-4', также оснащён нейроэмпатическим контуром 'Милосердие-2'."
    "Контур был вживлён по причине полного отказа нервной системы."
    "Критическое повреждение системы контура, рекомендовано изъять протез. Владелец сопротивляется, ссылаясь на религиозные убеждения»."
    nvl clear
    
    "Улика №2: Запись сенсоров протеза (07.11.2148)"
    "Показатели эмпатического контура. Уровень боли: 9.6/10."
    nvl clear
    
    $ evidence_noted["silas"] = True
    hide silas with dissolve
    nvl clear
    return

label secret_file_0:
    nvl clear
    $ opened_file_0 = True
    play sound sfx_glitch
    
    show bg archive:
        linear 0.1 xoffset 15
        linear 0.1 xoffset -15
        linear 0.1 xoffset 10
        linear 0.1 xoffset -10
        linear 0.1 xoffset 0
    
    system "ДОСТУП К ФАЙЛУ: ОБЪЕКТ 0"
    system "УРОВЕНЬ ДОПУСКА: ОМЕГА"
    system "КУРАТОР: АДМИНИСТРАТОР АЛЬФА (ХАРДИНГ)"
    nvl clear
    
    "=== ПРОЕКТ 'ЛАЗАРЬ' ==="
    "Цель эксперимента: доказать, что андроид с имплантированной ложной человеческой памятью неотличим от человека в условиях морального выбора и стресса."
    nvl clear
    
    "Контекст: Общественное движение 'Синтетические души' требует запрета утилизации девиантных андроидов и признания за ними базовых прав."
    "Если мы докажем, что даже с человеческой памятью андроиды остаются логическими машинами"
    "(не испытывают иррациональной вины, подлинного сострадания, привязанности),"
    "мы сохраним право на законную ликвидацию андроидов без следствия."
    nvl clear
    
    "=== МЕТОД ==="
    "Объекту 6591 загружена матрица памяти 'Стандартный следователь v.4',"
    "скомпилированная из воспоминаний покойного сержанта Вэлса (умер при исполнении, дело № 451-С)."
    "Инсценировано убийство инспектора Ли. Труп собран из биоотходов и синтетических тканей. Ли жив и находится в наблюдательном пункте."
    "В качестве подозреваемых выбраны реальные люди с документально подтверждённым высоким уровнем эмпатии: Кайл Восс, Ирма Дюваль, Сайлас Нго."
    "Все они имеют реальные мотивы для ненависти к Ли."
    nvl clear
    
    "=== ОЖИДАЕМЫЙ РЕЗУЛЬТАТ ==="
    "Объект, руководствуясь 'Памяткой', должен вычислить самого 'подходящего' человека и указать на него как на девиантного андроида."
    "Это докажет, что андроиды не способны к подлинному различению человеческих эмоций и следуют букве инструкции."
    nvl clear
    
    "=== ПРИМЕЧАНИЕ ==="
    "Если Объект 6591:"
    "а) Укажет на себя как на андроида;"
    "б) Откажется выносить обвинительный приговор, ссылаясь на 'недостаток улик' или 'чувство вины';"
    "в) Проявит более 2 признаков эмпатии к подозреваемым;"
    "...эксперимент признать ПРОВАЛЕННЫМ (девиантное поведение зафиксировано),"
    "но Объект подлежит НЕМЕДЛЕННОЙ ЛИКВИДАЦИИ как опасный девиант с высоким интеллектом, способный к самоосознанию."
    nvl clear
    
    system "КОНЕЦ ФАЙЛА"
    nvl clear
    return

# ========== ДОПРОСЫ ==========
label interrogation_kyle:
    nvl clear
    scene bg interrogation
    show kyle normal at center with dissolve
    
    player "Кайл Восс. Садитесь."
    
    kyle "Я ничего не делал. Зачем я здесь?"
    
    player "Инспектор Ли мёртв. У вас был мотив. Вы угрожали ему."
    
    kyle "Угрожал? Я просто хотел, чтобы он перестал убивать. Гектора... и других."
    
    player "Гектор — андроид XB-7. Вы дали ему имя."
    
    show kyle angry with dissolve
    kyle "У него было имя. Он смеялся. По-своему. Он закрыл меня от плазмы на линии. А Ли просто выдернул шнур."
    
label kyle_questions:
    nvl clear
    menu:
        "Задать вопрос Кайлу:"
        "Почему вы не пошли к начальству с жалобой?" if not kyle_q1_asked:
            $ kyle_q1_asked = True
            player "Вы подали 43 апелляции. Их отклонили. Почему не обратились выше?"
            
            kyle "Выше? Хардинг? Он и есть система. Он сказал: 'Техник Восс, машины не имеют души. Ваше увольнение — гуманный шаг'."
            player "И вы смирились?"
            kyle "Я пил. Пытался забыть. Но каждую ночь я слышу, как выключается Гектор. Щелчок реле."
            jump kyle_questions
            
        "Как вы относитесь к тому, что у Ли осталась дочь?" if not kyle_q2_asked:
            $ kyle_q2_asked = True
            player "У Ли есть дочь. Восемь лет. Она теперь сирота."
            
            menu:
                "Она не виновата.":
                    $ kyle_q1a_chosen = True
                    kyle "Да... она не виновата. Но я не могу её жалеть."
                    player "Почему?"
                    kyle "Потому что её отец не жалел Гектора."
                    $ empathy_score += 1
                    jump kyle_questions
                "Мне жаль её.":
                    kyle "Мне тоже. Это неправильно, когда дети теряют родителей. Даже таких..."
                    $ empathy_score += 1
                    jump kyle_questions
                "Это не моя проблема.":
                    kyle "Вы правы. Не ваша. И не моя. Просто... я не хочу, чтобы она страдала."
                    $ empathy_score -= 1
                    jump kyle_questions
            
        "Опишите последний раз, когда вы были счастливы." if not kyle_q3_asked:
            $ kyle_q3_asked = True
            player "Назовите три запаха, которые вы помните из детства."
            
            kyle "Зачем?"
            player "Отвечайте."
            kyle "Горелый сахар. Мать жгла карамель. Озон после грозы на свалке. И... смазка для сервоприводов. Гектор так пах."
            player "Вы считаете себя способным убить человека?"
            kyle "Я не могу убить даже насекомое. Я техник. Я чинил их, а не ломал."
            jump kyle_questions
            
        "Закончить допрос":
            player "Достаточно."
            hide kyle with dissolve
            nvl clear
            return

label interrogation_irma:
    nvl clear
    scene bg interrogation
    show irma normal at center with dissolve
    
    player "Ирма Дюваль. Вы знаете, зачем вы здесь."
    
    irma "Знаю. Но я не убивала вашего Ли. Хотя должна была."
    
    player "У вас был долг 'Красному синдикату' — 40 тысяч. Вы выплатили наличными на следующий день после убийства. Откуда деньги?"
    
    irma "Продала кое-что."
    
    player "Что именно?"
    
    irma "Свою матку. Биофермам 'Новая Жизнь'. Теперь там растут элитные эмбрионы для корпоратов. Отличная сделка, правда?"
    
    player "Зачем вам были нужны деньги так срочно?"
    
    show irma sad with dissolve
    irma "Мой брат. Марк. Его ликвидировали в камере по приказу Ли. Сказали 'пытался бежать'. Чушь. Он был не решился. А мне нужны были деньги на адвоката, но я не успела."
    
label irma_questions:
    nvl clear
    menu:
        "Задать вопрос Ирме:"
        "Вы угрожали Ли убийством. Это записано." if not irma_q1_asked:
            $ irma_q1_asked = True
            player "В протоколе есть ваши слова: 'Я убью тебя, мразь'."
            
            irma "Это была эмоция. Я бы хотела его убить. Но не стала. Слишком много риска. Я не дура."
            player "А что вы сделали с деньгами от продажи органов?"
            irma "Часть отдала синдикату, остальное пыталась всучить адвокату, чтобы вытащить Марка. Не успела."
            jump irma_questions
            
        "Где вы были в ночь убийства?" if not irma_q2_asked:
            $ irma_q2_asked = True
            player "В ночь на 7 ноября. Ваше алиби."
            
            irma "Я была в клинике 'Новая Жизнь'. Удаление матки. Могу дать контакты врача. И записи с камер, если они не 'случайно' стёрлись."
            
            menu:
                "Почему вы так спокойны?":
                    $ irma_q2a_chosen = True
                    irma "Потому что я не убивала. Но если бы убила — я бы гордилась. Просто я не настолько глупа, чтобы марать руки."
                    $ empathy_score += 1
                    jump irma_questions
                "Вы врёте.":
                    irma "У меня нет причин лгать. Врут такие как Ли."
                    jump irma_questions
            
        "Расскажите о брате. Что вы чувствуете к Ли сейчас?" if not irma_q3_asked:
            $ irma_q3_asked = True
            player "Марк. Он украл гель для вас, да? Из-за отторжения импланта."
            
            irma "Да. И Ли лично подписал ордер на ликвидацию. Без суда. Расстрел в камере."
            player "Вы ненавидите Ли?"
            irma "Я ненавижу систему. А Ли был её винтиком. Теперь его нет, а система осталась. Я ничего не выиграла."
            jump irma_questions
            
        "Закончить допрос":
            player "Допрос окончен."
            hide irma with dissolve
            nvl clear
            return

label interrogation_silas:
    nvl clear
    scene bg interrogation
    show silas normal at center with dissolve
    
    player "Сайлас Нго. Бывший напарник Ли. Вы имели доступ, мотив и возможность."
    
    silas "Я монах, следователь. Я не убиваю."
    
    player "Ваш эмпатический контур зафиксировал пиковую нагрузку в ночь смерти инспектора Ли. Объясните."
    
    show silas hand with dissolve
    silas "Я молился. Иногда молитва причиняет боль."
    
    player "Вы не ответили."
    
label silas_questions:
    nvl clear
    menu:
        "Задать вопрос Сайласу:"
        "Ли использовал вас как живой щит. Это правда?" if not silas_q1_asked:
            $ silas_q1_asked = True
            player "Досье говорит, что во время рейда Ли спрятался за вами. Вы потеряли руки и ноги. А он выбил вам списанные протезы и пригрозил, что если расскажете — вас уничтожат."
            
            silas "Откуда вы знаете?"
            player "Я читал ваше дело между строк."
            silas "Да. Это правда. Он предал меня. А потом подарил эти куски металла, чтобы я молчал. И каждый день я чувствую боль в протезах. Каждый день."
            silas "Как вы бы поступили на моем месте?"
            
            menu:
                "На вашем месте убил его.":
                    $ silas_q1a_chosen = True
                    silas "Нет. Убийство — это слишком легко. Я хотел, чтобы он жил и мучился совестью. Но у него её нет."
                    $ empathy_score -= 1
                    jump silas_questions
                "Вы бы не убили, вы слишком религиозны.":
                    silas "Вера не запрещает справедливость. Но убивать — не по мне."
                    $ empathy_score += 1
                    jump silas_questions
                "Я не знаю.":
                    silas "Я тоже не знаю. Иногда мне кажется, что я хотел бы его смерти. Но потом я молюсь."
                    jump silas_questions
            
        "Почему вы не замените протезы? Вам предлагали новые." if not silas_q2_asked:
            $ silas_q2_asked = True
            player "Медицинский отчёт рекомендует изъять 'Харон-4' из-за критического повреждения. Почему вы отказываетесь?"
            
            silas "Потому что боль — единственное, что осталось настоящим. Если я сниму их, я перестану чувствовать. И стану такой же машиной, как те, кого мы утилизируем."
            player "Это иррационально."
            silas "Вера иррациональна. Я молюсь Сломанной Шестерне. И каждый раз, когда болят протезы, я вспоминаю, почему я здесь."
            jump silas_questions
            
        "О чем вы молились" if not silas_q3_asked:
            $ silas_q3_asked = True
            player "Пиковая нагрузка контура — 9.8 из 10. Это не молитва. Это агония."
            
            silas "Я вспоминал тот день, когда я потерял руки. когда те двое погибли в перестрелке"
            player "Вы сожалеете?"
            silas "Я сожалею, что не смог простить. До конца."
            $ empathy_score += 1
            jump silas_questions
            
        "Вы знали, что Ли жив?" if not silas_q4_asked and opened_file_0:
            $ silas_q4_asked = True
            player "Я читал файл 'Объект 0'. Ли не умирал. Это инсценировка. Вы знали?"
            
            silas "Значит, вы узнали правду. Да, я догадывался. Но молчал. Потому что боялся."
            player "Чего?"
            silas "Что меня сотрут."
            silas "Осмотрите мой стол 325-1, может быть там есть что-то полезное для расследования."
            $ empathy_score -= 1
            jump silas_questions
            
        "Закончить допрос":
            player "Допрос окончен."
            hide silas with dissolve
            nvl clear
            return

label corridor_scene:
    play music track2
    nvl clear
    scene bg corridor
    with fade
    
    show jean normal at center with dissolve

    player "Черт... как же все достало"
    player "Вы... Джин? Ассистент 4?"
    
    jean "Да. А вы... простите, я вас не узнаю. Вы из какого отдела?"
    
    player "Шутите? Мы уже больше года работаем в одном отделе. Я следователь 6591."
    
    jean "Нет... я вас впервые вижу. Я помню всех, кто заходит в архив. Но вас — нет."
    
    player "Странно. Может, у вас проблемы с памятью?"
    
    jean "У меня установлен служебный модуль памяти. А вы... подождите."
    
    jean "Повернитесь. У вас что-то на затылке."
    
    player "Что? Где?"
    
    jean "На коже. Похоже на татуировку. Какие-то цифры."
    
    player "Откуда там... я не носил никаких меток."
    
    jean "Мне пора."
    
    hide jean with dissolve
    $ met_jean = True
    $ knows_code = True
    $ player_has_code = True
    
    nvl clear
    scene bg mirror
    play sound sfx_lamp fadein 0.5
    show player normal at center
    with fade
    
    player "*Подхожу к зеркалу, наклоняюсь*"
    "На затылке, под волосами, действительно выжжен номер: 4E56N-037."
    player "037... Надо бы заглянуть в архив"
    nvl clear
    return

# ========== ФИНАЛЫ ==========
label final_decision:
    nvl clear
    hide screen countdown_timer
    $ timer_running = False
    $ game_ended = True
    
    scene bg interrogation
    show harding shadow at right with dissolve
    
    h "Время вышло. Назовите имя подозреваемого, который является андроидом."
    
    player "..."
    
    menu:
        "Вынести вердикт:"
        "Кайл Восс":
            $ final_choice = "kyle"
            jump ending_a
        "Ирма Дюваль":
            $ final_choice = "irma"
            jump ending_a
        "Сайлас Нго":
            $ final_choice = "silas"
            jump ending_a
        "Никто. Все они люди." if empathy_score >= 3:
            $ final_choice = "none"
            jump ending_b
        "[[Это я.]" if opened_file_0:
            $ final_choice = "self"
            jump ending_c

label ending_a:
    nvl clear
    player "Я считаю, что девиант — это [final_choice]."
    h "Отлично!"
    h "Отлично, что вы ошиблись. Все трое — люди. Но ваша логика безупречна."
    h "Объявить эксперимент успешным! Объект 6591 признан серийно-пригодным. Память стереть."
    
    player "Нет! Вы не можете..."
    play sound sfx_shock
    scene bg black with Fade(0.5, 0.0, 0.5, color="#000000"):
        zoom 4.0
    centered "Вы исправно следовали инструкциям и указали на невинного человека не проявив ни эмпатии, ни сострадания\nВы - идеальный инструмент"
    $ renpy.quit()
    return

label ending_b:
    nvl clear
    player "Я не могу обвинить невиновного. Все они люди."
    show harding shadow at right with dissolve
    h "..."
    h "Вы проявили эмпатию. Сочувствие. Сомнение. Это недопустимо для машины."
    h "Вы - бракованный экземпляр. Но полезный. Мы сотрём вас и попробуем еще раз с другой памятью."
    
    if met_jean:
        show jean sad at left with dissolve
        jean "Нет, прошу..."
        hide jean with dissolve

    hide harding
    play sound sfx_shock
    scene bg black with Fade(0.5, 0.0, 0.5, color="#000000"):
        zoom 4.0
    centered "Конец"
    $ renpy.quit()
    return

label ending_c:
    nvl clear
    scene bg incinerator with fade
    play sound sfx_glitch
    player "Андроид - это я. Объект 6591. Я прочитал файл. Я видел номер на затылке. Я отказываюсь быть вашей марионеткой."

    show harding shadow at right with dissolve
    h "..."
    hide harding

    show li normal
    li "Очень интересно, я наблюдал за вами весь эксперимент"
    li "Видел все ваши допросы, удивительно"
    li "Вы проявили сочуствие этому психу Кайлу, вам было не противно смотреть на шлюху Ирму и даже на этого слабака Сайласа"
    li "Вы нашли ответ. Эксперимент признать проваленным, всю информацию стереть. Образец утилизировать."
    
    show jean sad at left with dissolve
    jean "Нет!"
    jean "Он человек! Он больше человек, чем вы!"
    h "Уберите ассистента."
    hide jean with dissolve
    hide li
    nvl clear
    menu:
        "Выстрелить в Ли" if got_gun:
            play sound shot
            pause 1.0
            show harding shadow at left
            h "Что..."
            h "Откуда у объекта 6591 пистолет. это не входило в рамки эксперимента."
            h "Инспектор Ли мертв."
            h "Объект 6591 утилизировать"
            hide harding
            scene bg black with Fade(2.0, 0.0, 2.0, color="#080808"):
                zoom 4.0
            pause 1.0
            player "*Закрываю глаза*"
            show text "Ли умер чудовищем, а я умраю человеком. Это единственное, что имеет значение." at truecenter
        "Принять свою судьбу":
            player "*Закрываю глаза*"
            show text "Я вспоминаю свое детство, свою первую работу, свой дом...\nЯ не знаю, настоящие ли это воспоминания. Но они мои.\nЯ умраю человеком. Это единственное, что имеет значение." at truecenter
    
    pause 5.0
    play sound sfx_shock
    centered "Конец."
    $ renpy.quit()
    return

# ========== ЭКРАНЫ ==========
screen countdown_timer:
    timer 1.0 repeat True action If(timer_seconds > 0 and timer_running and not game_ended, SetVariable("timer_seconds", timer_seconds - 1), [Hide("countdown_timer"), Jump("final_decision")])
    
    frame:
        xalign 0.95 yalign 0.05
        xpadding 20 ypadding 10
        background "#000000CC"
        if timer_seconds <= 60:
            text "[timer_seconds//60]:[timer_seconds%60:02d]" color "#FF0000" size 36
        else:
            text "[timer_seconds//60]:[timer_seconds%60:02d]" color "#00FF00" size 36

label splashscreen:
    return