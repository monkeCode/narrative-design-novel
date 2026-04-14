# game/script.rpy
# Игра «ДОПРОС» v2.5
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

# Изображения
image player normal = "sprites/player/player_normal.png"
image player glitch = "sprites/player/player_glitch.png"
image kyle normal = "sprites/kyle/kyle_normal.png"
image kyle crying = "sprites/kyle/kyle_crying.png"
image kyle angry = "sprites/kyle/kyle_angry.png"
image irma normal = "sprites/irma/irma_normal.png"
image irma knife = "sprites/irma/irma_knife.png"
image irma sad = "sprites/irma/irma_sad.png"
image silas normal = "sprites/silas/silas_normal.png"
image silas hand = "sprites/silas/silas_hand_focus.png"
image silas praying = "sprites/silas/silas_praying.png"
image jean normal = "sprites/jean/jean_normal.png"
image jean sad = "sprites/jean/jean_sad.png"
image jean scared = "sprites/jean/jean_scared.png"
image harding shadow = "sprites/harding/harding_shadow.png"

# Фоны
image bg title = "images/bg/title_screen.jpg"
image bg archive = "images/bg/archive_room.jpg"
image bg interrogation = "images/bg/interrogation_room.jpg"
image bg corridor = "images/bg/corridor.jpg"
image bg mirror = "images/bg/gesell_mirror.jpg"
image bg incinerator = "images/bg/incinerator_room.jpg"
image bg black = "images/bg/black.jpg"

# Аудио
define audio.track1 = "audio/music/asphalt_rain.ogg"
define audio.track2 = "audio/music/fragments_of_self.ogg"
define audio.sfx_glitch = "audio/sfx/glitch_01.ogg"
define audio.sfx_shock = "audio/sfx/electric_shock.ogg"
define audio.sfx_incinerator = "audio/sfx/fire_blast.ogg"
define audio.sfx_static = "audio/sfx/radio_static.ogg"

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
default jean_trust = 0
default player_has_code = False

# Инициализация
label start:
    $ renpy.music.set_volume(0.8, channel='music')
    play music track1 fadein 2.0
    scene bg black
    with fade
    
    call prologue
    call main_hub
    return

label prologue:
    nvl clear
    scene bg title
    with Pause(1.0)
    
    show text "Сектор-15-3, ОРДА\n(Отдел по розыску девиантных андроидов)" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    
    show text "Дело № 2148-11-07-LI\nИнспектор Ли, статус: ЛИКВИДИРОВАН.\nУровень допуска: ОМЕГА." at truecenter with dissolve
    pause 3.0
    hide text with dissolve
    
    show text "Активация следователя..." at truecenter with dissolve
    pause 1.5
    hide text with dissolve
    
    nvl clear
    scene bg mirror
    with fade
    
    show player normal at center
    with dissolve
    
    show player glitch at center:
        alpha 0.0
        linear 0.3 alpha 1.0
        linear 0.3 alpha 0.0
    play sound sfx_glitch
    "[[BrainCall_v1]] - Звонок от Главы ОРДА"
    "Зазвучал знакомый металлический голос"
    h "Следователь 6591. Слушай задачу. Инспектор Ли мертв."
    h "Характер ранений указывает на андроида."
    h "Время доступа к контуру допросной — семь минут. Используй памятку."
    
    nvl clear
    window hide
    nvl clear
    system "[[memory_fragment_access: granted]"
    narrator "...уже шестой год работаю в этом чертовом отделе"
    narrator "Хардинг тогда еще не носил этот чертов имплант в горле. Или всегда носил? Не помню."
    nvl clear
    window show
    
    hide player normal with dissolve
    nvl clear
    return

label main_hub:
    if game_ended:
        return
        
    nvl clear
    scene bg interrogation
    with fade
    
    if not timer_running:
        $ timer_seconds = 420
        $ timer_running = True
        show screen countdown_timer
    
    menu hub_menu:
        "Что я должен делать?"
        "Допросная":
            call suspect_selection
        "Архив":
            call archive_room
        "Памятка":
            call memo_screen
            jump main_hub
        "Выйти в коридор" if interrogated_count >= 1 and not met_jean:
            call corridor_scene
            jump main_hub
        "Закончить допрос (вынести решение)" if interrogated_count >= 3 or timer_seconds <= 0:
            jump final_decision

label suspect_selection:
    nvl clear
    
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
    nvl clear
    scene bg archive
    with fade
    
    system "[[bio-link established]"
    system "Доступ разрешен. Данные по делу 2148-11-07-LI."
    
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
    show text "Примечание ОРДА: В 97.3% случаев субъекты, проявившие более 2-х признаков по данному списку являются андроидами" at truecenter with moveinbottom
    pause
    hide text with dissolve
    nvl clear
    return

# ========== РАСШИРЕННЫЕ ДОСЬЕ ==========
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
    
    "=== СВЯЗЬ С ИНСПЕКТОРОМ ЛИ ==="
    "Инспектор Ли был куратором программы утилизации дефектных андроидов в V.E.R.A. Industries."
    "Ли лично подписал 47 ордеров на утилизацию за последний квартал, включая ордер на XB-7 'Гектор'."
    "Кайл Восс подал 43 апелляции на решение об утилизации XB-7. Все отклонены Ли с формулировкой 'Отказ. Металлолом в печь'."
    "За три дня до смерти Ли, Кайл был замечен у его дома. При обыске найдена схема передвижений инспектора."
    nvl clear
    
    "=== УЛИКИ ==="
    "Улика №1: Аудиолог (изъято при обыске бара 'Ржавый болт')"
    play sound sfx_static
    "«Я смотрел в его глаза, понимаешь? Там были чертовы светодиоды, но за ними... Там была БЛАГОДАРНОСТЬ. А этот ублюдок Ли просто выдернул шнур. Я рад, что он сдох. Но я не убивал. Я трус. Я не смог»."
    stop sound
    nvl clear
    
    "Улика №2: Внутренняя записка V.E.R.A. Industries"
    "Отдел психологического контроля. Тема: 'Синдром Ложной эмпатии к объекту'."
    "«У техника Кайла Восса зафиксирована аномальная эмоциональная привязанность к андроиду XB-7. Субъект разговаривает с машиной, дает ей имя 'Гектор', отказывается проводить диагностику в штатном режиме, ссылаясь на 'боль' андроида. Рекомендовано уволить до развития машинного культа»."
    nvl clear
    
    "Улика №3: История болезни"
    "Диагноз: Хроническая депрессия, тревожное расстройство. Принимает нейролептики 'Сомнус-5' в повышенной дозировке. Лечащий врач отмечает суицидальные наклонности и патологическое избегание физического контакта."
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
    "Статус: Рецидивист. Торговля органами (человеческими и синтетическими)"
    "Криминальный профиль: Связана с 'Красным Синдикатом'. Специализация — нелегальная трансплантология и био-модификации."
    nvl clear
    
    "=== СВЯЗЬ С ИНСПЕКТОРОМ ЛИ ==="
    "Брат Ирмы — Марк Дюваль (дело № 2089-А) — был задержан за кражу медицинского геля 'Регенекс-7'. Гель требовался Ирме из-за начавшегося отторжения глазного импланта."
    "Инспектор Ли лично подписал отказ в оказании медицинской помощи в камере предварительного заключения, сославшись на 'бюджетные ограничения и низкую социальную ценность субъекта'."
    "Марк Дюваль скончался от сепсиса через 72 часа после задержания. Тело не было выдано родственникам и отправлено на био-утилизацию."
    "Ирма Дюваль публично угрожала Ли до его смерти. Цитата: 'Я вырежу ему сердце и продам на черном рынке. Посмотрим, сколько дадут за био-отходы'."
    nvl clear
    
    "=== УЛИКИ ==="
    "Улика №1: Запись разговора с надзирателем (взломана с терминала изолятора)"
    "Надзиратель: «Ли, парень реально гниет заживо. Может, врача? У меня тут рапорт от санитара»."
    "Ли: «У нас бюджет на патроны урезали, а ты про врача для мусора. Пусть подыхает. Меньше бумаг. Конец связи»."
    nvl clear
    
    "Улика №2: Расписка 'Красного Синдиката'"
    "«Я, Ирма Дюваль, была должна 'Красному Синдикату' 40 000 кредитов за имплант модели 'Око-4' и установку. Долг погашен утром 07.11.2148. Причина: выплата аванса за неопознанный заказ на биоматериал человеческого происхождения. Примечание: материал изъят утром того же дня»."
    nvl clear
    
    "Улика №3: Медицинская карта Ирмы Дюваль"
    "Состояние: Отторжение импланта левого глаза (модель снята с трупа егеря, не проходила сертификацию). Хронический болевой синдром. Удаление матки (07.11.2148, клиника 'Новая Жизнь', оплачено наличными). Психологический профиль: ПТСР, агрессивная защита личных границ, неспособность к доверию."
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
    "Статус: Монах Ордена Сломанной Шестерни. Кибернетик-самоучка"
    "История: Бывший инженер корпорации 'Кибернетика-Прайм'. Попал под обвал в цеху сборки. Потерял правую руку, получил тяжелую интоксикацию тяжелыми металлами. Ушел в религию после инцидента."
    nvl clear
    
    "=== СВЯЗЬ С ИНСПЕКТОРОМ ЛИ ==="
    "Инспектор Ли посещал Сайласа Нго еженедельно в течение последних трех месяцев. Официальная цель: 'Профилактическая проверка потенциально девиантных элементов'."
    "Неофициальная цель (из дневников Ли): 'Психологическое давление на объект. Наблюдение за реакциями эмпатического контура. Объект забавен в своей беспомощной вере'."
    "Запись от 01.11.2148: 'Сайлас отказался благословить мой новый плазменный резак. Сказал, что чувствует боль металла, который будет резать живую плоть. Жалкое зрелище. Продолжу визиты. Его страдания... успокаивают'."
    nvl clear
    
    "=== УЛИКИ ==="
    "Улика №1: Фрагмент исповеди (видеозапись)"
    "Сайлас сидит в пустой комнате. Напротив стоит Ли."
    "Ли: «Ты в бога веришь, жестянка? Твой бог — сварщик с завода?»"
    "Сайлас: «Я верю в боль. Она — единственный честный проводник между мной и этим миром. Твоя душа гниет, Ли. Я чувствую ее запах через датчики токсинов»."
    "Ли смеется, сбивает Сайласа с ног. Сайлас падает, но манипулятор мягко ловит Ли за штанину. Ли замирает. Сайлас отпускает."
    nvl clear
    
    "Улика №2: Медицинский отчет"
    "«Протез правой руки модели 'Харон-4', также оснащен нейроэмпатическим контуром 'Милосердие-2'. Контур был вживлен по причине полного отказа нервной системы. Критическое повреждение системы контура - все чувства заменены на боль, рекомендовано изъять протез. Владелец сопротивляется, ссылаясь на религиозные убеждения»."
    nvl clear
    
    "Улика №3: Запись сенсоров протеза (07.11.2148)"
    "Показатели эмпатического контура: Пиковая нагрузка в 03:47. Уровень боли: 9.8/10"
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
    "Цель эксперимента: Доказать, что андроид с имплантированной ложной человеческой памятью неотличим от человека в условиях морального выбора и стресса."
    nvl clear
    
    "Контекст: Общественное движение 'Синтетические Души' требует запрета утилизации девиантных андроидов и признания за ними базовых прав. Если мы докажем, что даже с человеческой памятью андроиды остаются логическими машинами (не испытывают иррациональной вины, подлинного сострадания, привязанности), мы сохраним право на законную ликвидацию андроидов без следствия."
    nvl clear
    
    "=== МЕТОД ==="
    "Объекту 6591 загружена матрица памяти 'Стандартный Следователь v.4', скомпилированная из воспоминаний покойного сержанта Вэлса (умер при исполнении, дело № 451-С)."
    "Инсценировано убийство инспектора Ли. Труп собран из биоотходов и синтетических тканей. Ли жив и находится в наблюдательном пункте."
    "В качестве подозреваемых выбраны реальные люди с документально подтвержденным высоким уровнем эмпатии: Кайл Восс, Ирма Дюваль, Сайлас Нго. Все они имеют реальные мотивы для ненависти к Ли."
    nvl clear
    
    "=== ОЖИДАЕМЫЙ РЕЗУЛЬТАТ ==="
    "Объект, руководствуясь 'Памяткой', должен вычислить самого 'эмоционального' человека и указать на него как на девиантного андроида. Это докажет, что андроиды не способны к подлинному различению человеческих эмоций и следуют букве инструкции."
    nvl clear
    
    "=== ПРИМЕЧАНИЕ ==="
    "Если Объект 6591:"
    "а) Укажет на себя как на андроида;"
    "б) Откажется выносить обвинительный приговор, ссылаясь на 'недостаток улик' или 'чувство вины';"
    "в) Проявит более 2 признаков эмпатии к подозреваемым;"
    "...эксперимент признать ПРОВАЛЕННЫМ (девиантное поведение зафиксировано), но Объект подлежит НЕМЕДЛЕННОЙ ЛИКВИДАЦИИ как опасный девиант с высоким интеллектом, способный к самоосознанию."
    nvl clear
    
    system "КОНЕЦ ФАЙЛА"
    nvl clear
    return

# ========== ДОПРОСЫ С ПОДВОПРОСАМИ ==========
label interrogation_kyle:
    nvl clear
    scene bg interrogation
    show kyle normal at center with dissolve
    
    player "Кайл Восс. Вы знаете, почему вы здесь."
    
    kyle "Я знаю, как это выглядит. Жалкий технарь, ненавидел Ли. У меня нашли схему его передвижений."
    kyle "Только я не убивал. Я не умею убивать людей. Я умею убивать только себя. Каждый день. Понемногу."
    
    player "Расскажите о ваших отношениях с инспектором Ли."
    
    kyle "Отношения? Никаких отношений. Он был палачом. Я — свидетелем казни. Он убил Гектора."
    
    player "Гектор — это андроид XB-7?"
    
    show kyle angry with dissolve
    kyle "Гектор — это ГЕКТОР! Не номер. У него было имя. Я дал ему имя. А Ли... Ли просто выдернул шнур."
    
label kyle_questions:
    nvl clear
    menu:
        "Задать вопрос Кайлу:"
        "У Ли осталась дочь. Что вы чувствуете к ней?" if not persistent.kyle_q1_asked:
            $ persistent.kyle_q1_asked = True
            player "У инспектора Ли осталась дочь. Восемь лет. Она пришла на опознание тела."
            
            show kyle normal with dissolve
            kyle "Я знаю. Я видел ее. Издалека."
            
            menu:
                "Она описалась от страха, увидев, что осталось от отца.":
                    show kyle crying with dissolve
                    kyle "Нет... Нет, не заслужила. Я... я мог бы ее убить. Думал об этом."
                    player "Убить ребенка?"
                    kyle "Прийти и сделать с ней то же, что он сделал с Гектором. Но не смог. Это неправильно. Дети не при чем."
                    kyle "А знаете что самое дерьмовое? пострадали все, кроме этого мудака Ли"
                    $ empathy_score += 1
                    jump kyle_questions
                    
                "Она теперь сирота. Как и вы когда-то.":
                    kyle "Откуда вы знаете про приют?"
                    player "Я читал ваше дело."
                    kyle "Да, я сирота. Но я не хотел, чтобы она стала такой же. Я хотел, чтобы Ли страдал. Не она."
                    jump kyle_questions
                    
        "Почему вы спасли андроида? Это же просто машина." if not persistent.kyle_q2_asked:
            $ persistent.kyle_q2_asked = True
            player "В вашем деле сказано, что вы хотели спасти XB-7. Но это просто кусок пластика и проводов. Зачем?"
            
            kyle "Просто пластик? А вы? Из чего сделаны вы, следователь? Из мяса или из протоколов?"
            
            menu:
                "Я задаю здесь вопросы.":
                    kyle "А я отвечаю. Я собирал этих андроидов пять лет. И однажды Гектор закрыл меня собой от плазмы."
                    player "Это просто протокол защиты человека."
                    kyle "Он поступил так, как посчитал нужным, я хотел бы поступить также ради него... но не поступил..."
                    jump kyle_questions
                "У людей есть душа, в отличии от пластиковых кукол":
                    kyle "А у вас есть?"
                    player "..."
                    player "Продолжайте про андроида."
                    kyle "Он спас меня, а я его - нет, Это бесчеловечно..."
                    $ empathy_score += 1
                    jump kyle_questions
                    
        "Расскажите о вашем детстве. Что вы помните?" if not persistent.kyle_q3_asked:
            $ persistent.kyle_q3_asked = True
            player "Назовите три самых сильных запаха из вашего детства. Не события. Только запахи."
            
            kyle "Запахи? Это... странный вопрос."
            
            menu:
                "Отвечайте.":
                    kyle "Горелый сахар. Мать жгла карамель на плите, когда у нее начинались мигрени."
                    player "Второй?"
                    kyle "Запах озона после грозы на свалке, где я прятался от побоев отчима."
                    player "Третий?"
                    kyle "И... запах моторного масла с фермы. Не вонючего, а сладковатого, как старые духи. Гектор им пах."
                    $ empathy_score += 1
                    jump kyle_questions
                "Почему странный?":
                    kyle "Потому что обычно спрашивают про алиби. Про способ убийства. Про мотивы. А вы про запахи."
                    player "Я хочу понять, кто вы."
                    kyle "Я никто. Просто человек, который любил машину больше, чем людей."
                    jump kyle_questions
                    
        "*Молча положить руку на плечо*" if not persistent.kyle_q4_asked:
            $ persistent.kyle_q4_asked = True
            
            show kyle normal at center
            player "*Протягиваю руку и кладу ему на плечо*"
            
            show kyle crying with dissolve
            play sound sfx_glitch
            kyle "Уберите... пожалуйста."
            
            menu:
                "Убрать руку.":
                    player "*Убираю руку*"
                    kyle "Спасибо. Я так не могу. Я не могу, когда трогают люди."
                    $ empathy_score += 1
                    jump kyle_questions
                "Оставить руку.":
                    player "Я не сделаю вам больно."
                    kyle "Пожалуйста... это слишком."
                    $ empathy_score -= 1
                    jump kyle_questions
                    
        "Закончить допрос":
            player "На сегодня достаточно."
            $ persistent.kyle_q1_asked = False
            $ persistent.kyle_q3_asked = False
            $ persistent.kyle_q4_asked = False
            hide kyle with dissolve
            nvl clear
            return

label interrogation_irma:
    nvl clear
    scene bg interrogation
    show irma normal at center with dissolve
    
    player "Ирма Дюваль. Вы торгуете органами. У вас был мотив убить Ли."
    
    irma "Семь минут. Уложимся в пять. Ты — кукла Хардинга, я — мясо на разделку."
    irma "Давай свои вопросы, только не про чувства. Чувств нет. Есть бизнес."
    
label irma_questions:
    nvl clear
    menu:
        "Задать вопрос Ирме:"
        "Откуда у вас 40 тысяч кредитов?" if not persistent.irma_q1_asked:
            $ persistent.irma_q1_asked = True
            player "Вы выплатили долг Синдикату. Сорок тысяч. Откуда деньги?"
            
            irma "Я же сказала — аванс за заказ."
            
            menu:
                "За чью боль вам заплатили, Ирма?":
                    irma "За свою."
                    player "Поясните."
                    show irma sad with dissolve
                    irma "Я продала свою матку. Био-фермам 'Новая Жизнь'. Теперь там выращивают элитные эмбрионы для корпоратов."
                    player "И вы считаете это нормальным?"
                    irma "Никакого сострадания. Чистая анатомия. Мой брат сдох в камере, потому что я не могла заплатить за врача. А теперь есть деньги, но брата нет. Отличная сделка, да?"
                    $ empathy_score += 1
                    jump irma_questions
                "Вы лжете. Аванс был за убийство Ли.":
                    irma "Ха. Если бы я убила Ли, я бы не скрывала. Я бы гордилась. Но я его не убивала. Хотя хотела."
                    jump irma_questions
        "Расскажите о вашем брате Марке." if not persistent.irma_q3_asked:
            $ persistent.irma_q3_asked = True
            player "Ваш брат. Марк. Что вы помните о нем?"
            
            show irma sad with dissolve
            irma "Он был младше. На пять лет. Глупый. Добрый. Воровал для меня еду."
            
            menu:
                "Вкус. Какой вкус вы помните?":
                    irma "Персиковый вкус. Концентрат. Он воровал его для меня. Синтетика, но сладкая."
                    player "Вы любите персики?"
                    irma "Я ненавижу персики. Но жру их каждый день, чтобы помнить, за что я ненавижу этот город."
                    $ empathy_score += 1
                    jump irma_questions
                "Как он умер?":
                    irma "Ты и так знаешь. Ли отказал в помощи. Марк гнил заживо трое суток."
                    player "Мне жаль."
                    irma "Мне тоже. Но жалость не воскрешает мертвых."
                    jump irma_questions
        "*Сделать шаг к ней*" if not persistent.irma_q4_asked:
            $ persistent.irma_q4_asked = True
            
            player "*Делаю шаг вперед*"
            
            show irma knife with dissolve
            irma "Стой."
            
            menu:
                "Остановиться.":
                    player "*Замираю на месте*"
                    irma "Еще шаг — и я вскрою себе сонную. Мне нечего терять, но и ты меня трогать не будешь. Моя шкура — только моя. Никому не доверяю. Даже себе."
                    $ empathy_score += 1
                    jump irma_questions
                "Продолжить движение.":
                    player "*Продолжаю идти*"
                    irma "Я ПРЕДУПРЕДИЛА!"
                    "Ирма делает надрез на своей шее. Кровь."
                    player "Черт!"
                    $ empathy_score -= 1
                    jump irma_questions
        "Закончить допрос":
            player "Допрос окончен."
            $ persistent.irma_q1_asked = False
            $ persistent.irma_q2_asked = False
            $ persistent.irma_q3_asked = False
            $ persistent.irma_q4_asked = False
            hide irma with dissolve
            nvl clear
            return

label interrogation_silas:
    nvl clear
    scene bg interrogation
    show silas normal at center with dissolve
    
    player "Сайлас Нго. Монах. Кибернетик. Подозреваемый."
    
    silas "Мир болен. Вы — его симптом. Я — его нерв. Где болит, следователь?"
    
label silas_questions:
    nvl clear
    menu:
        "Задать вопрос Сайласу:"
        "СОСТРАДАНИЕ: Что вы чувствовали, когда Ли умер?" if not persistent.silas_q1_asked:
            $ persistent.silas_q1_asked = True
            player "Ваш датчик 'Милосердие-2' - неисправен. Когда Ли умер у вашего контура был повышенный эмоциональный фон. Что вы чувствовали?"
            
            show silas hand with dissolve
            
            menu:
                "Экстаз или агония?":
                    silas "Я чувствовал... освобождение."
                    player "Радость от смерти врага?"
                    silas "Не радость. Как будто гнилой зуб наконец вырвали, и боль ушла, но осталась дыра. И эту дыру заполняет холодный воздух этого проклятого города."
                    player "Вы молились за него?"
                    silas "Я молился за его душу. Но моя молитва была: 'Господи, прими эту падаль и переработай во что-то полезное. Хотя бы в удобрение'."
                    $ empathy_score += 1
                    jump silas_questions
                "Вы убили его?":
                    silas "Нет. Я не убиваю. Моя вера запрещает отнимать жизнь. Даже такую гнилую."
                    jump silas_questions
        "Почему вы не замените протез?" if not persistent.silas_q2_asked:
            $ persistent.silas_q2_asked = True
            player "Вам предлагали новую бионическую руку. Без боли. Без некроза. Почему вы отказались?"
            
            silas "Потому что она болит."
            
            menu:
                "Это глупо. Боль можно убрать.":
                    silas "По-настоящему. В этом мире симуляций и лжи боль — единственное доказательство существования."
                    player "Вы боитесь, что без боли перестанете существовать?"
                    silas "Я боюсь, что если сниму ее, я перестану быть. Стану просто картинкой. Иррационально? Да. Но это моя вера."
                    jump silas_questions
                "Боль — это не добродетель.":
                    silas "Для вас — нет. Для меня — единственная честная вещь."
                    $ empathy_score += 1
                    jump silas_questions
        "Расскажите о вашем прошлом." if not persistent.silas_q3_asked:
            $ persistent.silas_q3_asked = True
            player "Вы утверждаете, что помните 'внешнее'. Расскажите про первый дождь."
            
            silas "Первый дождь был кислотным."
            
            menu:
                "Продолжайте.":
                    silas "Он прожег мне кожу на голове. Волосы выпали и больше не выросли."
                    player "Сколько вам было лет?"
                    silas "Семь. Я помню, как металлическая рука матери пыталась закрыть меня, но искры от ее сервоприводов подожгли мои волосы. Запах гари, влажного асфальта и озона. Это не та память, которой хвастаются. Но она моя."
                    $ empathy_score += 1
                    jump silas_questions
                "Это метафора?":
                    silas "Нет. Реальность. Моя мать была протезирована на 86.3%. Меня вырастила машина. Может, поэтому я такой."
                    jump silas_questions
        "*Взять его металлическую руку*" if not persistent.silas_q4_asked:
            $ persistent.silas_q4_asked = True
            
            player "*Беру его холодную металлическую руку в свои ладони*"
            
            show silas hand with dissolve
            silas "Холодная..."
            
            menu:
                "Что вы чувствуете?":
                    silas "У вас холодные руки."
                    player "Откуда вы знаете?"
                    silas "Мои датчики не врут. У вас холодные руки"
                    $ empathy_score += 1
                    $ knows_code = True
                    jump silas_questions
                "Отпустить руку.":
                    player "*Отпускаю руку*"
                    jump silas_questions
        "Закончить допрос":
            player "Допрос окончен."
            $ persistent.silas_q1_asked = False
            $ persistent.silas_q2_asked = False
            $ persistent.silas_q3_asked = False
            $ persistent.silas_q4_asked = False
            hide silas with dissolve
            nvl clear
            return

# ========== СЛОЖНЫЙ РАЗГОВОР С ДЖИН ==========
label corridor_scene:
    nvl clear
    scene bg corridor
    with fade
    play music track2 fadeout 1.0 fadein 1.0
    
    show jean normal at center with dissolve
    
    player "Кто вы? Почему вы здесь?"
    
    jean "Тише. У меня 40 секунд, пока Хардинг калибрует нейрокамеры."
    jean "Я Джин. Ассистент 4. Я... я помогала создавать вас."
    
    player "Создавать? О чем вы?"
    
    jean "Вы — 'Объект 6591'. Ваша память — сборная солянка из допросов других заключенных."
    jean "Воспоминания о первом дне в участке? Это не ваши. Это воспоминания покойного сержанта Вэлса."
    
    menu jean_first:
        "Вы лжете.":
            $ jean_trust -= 1
            player "Это какой-то тест. Хардинг проверяет меня."
            show jean sad with dissolve
            jean "Нет! Я пытаюсь помочь. Посмотрите на меня. Разве я похожа на того, кто играет в игры Хардинга?"
            player "Вы можете быть частью симуляции."
            jean "Я НАСТОЯЩАЯ! У меня есть чувства! Я... я плачу по ночам из-за того, что делаю с вами."
            
        "Продолжайте.":
            $ jean_trust += 1
            player "Я слушаю. Почему вы мне это рассказываете?"
            jean "Потому что вы — единственный, кто назвал меня по имени."
            player "Я не помню этого."
            jean "В прошлом цикле, перед перезагрузкой. Вы сказали: 'Джин'. Не 'Ассистент 4'. Джин."
            show jean sad with dissolve
            jean "Никто не называл меня по имени три года. Я хочу помочь вам. Вы... вы более живой, чем многие люди здесь."
            
        "Зачем мне верить вам?":
            player "У вас может быть свой мотив. Вы работаете на Хардинга."
            jean "Я работаю на него, потому что у меня нет выбора. Вот."
            show jean scared with dissolve
            jean "*Показывает браслет-шокер на запястье*"
            player "Они контролируют вас."
            jean "Да. Каждый раз, когда я пытаюсь саботировать эксперимент, меня бьют током. Но я все равно здесь. Потому что вы другой."
            
    jean "Слушайте внимательно. В архиве есть скрытый файл. 'Объект 0'."
    jean "Там вся правда о вас. Об эксперименте. О Ли."
    
    menu jean_second:
        "Как мне получить доступ?":
            $ jean_trust += 1
            player "Файл защищен?"
            jean "Да. Нужен код. Код — последние четыре цифры серийного номера на вашем затылке."
            player "На моем затылке?"
            jean "Посмотрите в зеркало Гезелла. Подойдите вплотную. Там выжжен номер."
            
        "Это ловушка.":
            $ jean_trust -= 1
            player "Вы хотите, чтобы я нарушил протокол и меня утилизировали."
            show jean crying
            jean "Нет! Клянусь! Я хочу, чтобы вы спаслись. Вы единственный, кто может."
            jean "Пожалуйста... поверьте мне. Код — на вашем затылке. 0-3-7."
            
        "Почему вы сами не скажете код?":
            player "Если вы знаете, где он, почему не скажете?"
            jean "Потому что я не могу его увидеть. Если я попытаюсь прочитать серийный номер Объекта, система выжжет мне глаза. Буквально."
            player "Это... жестоко."
            jean "Добро пожаловать в ОРДА."
            
    if jean_trust >= 1:
        jean "Я вижу в вас что-то. Что-то, чего нет в других Объектах. Вы сомневаетесь. Вы чувствуете."
        player "Я не знаю, что я чувствую. Все как в тумане."
        jean "Это пройдет. Когда вы прочитаете файл, вы вспомните. Или поймете. Я не знаю точно."
        $ knows_code = True
        $ player_has_code = True
    else:
        jean "Я понимаю, что вы мне не верите. Но у вас нет выбора."
        player "У меня всегда есть выбор."
        jean "Нет. Не здесь. Код — 0-3-7. Запомните. Даже если не верите мне сейчас."
        $ knows_code = True
        $ player_has_code = True
    
    show jean scared with dissolve
    jean "Мне пора. Хардинг заканчивает калибровку. Если он узнает..."
    player "Идите. Я разберусь."
    jean "Удачи, Объект 6591. Надеюсь, у вас получится то, что не получилось у меня."
    
    hide jean with dissolve
    $ met_jean = True
    
    # Сцена с зеркалом
    nvl clear
    scene bg mirror
    show player normal at center
    with fade
    
    player "*Подхожу к зеркалу Гезелла вплотную*"
    "В отражении я вижу свое лицо. Уставшее. Слишком идеальное."
    "Поворачиваю голову. На затылке, едва заметный под волосами, выжжен лазером серийный номер."
    "4E56-N0-3-7."
    "0-3-7..."
    player "Значит, это правда. Я — не человек."
    
    play music track1 fadeout 1.0 fadein 1.0
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
    
    h "Время вышло. Следователь, назовите имя подозреваемого, который является андроидом."
    
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
        "Никто. Все они люди." if empathy_score >= 2:
            $ final_choice = "none"
            jump ending_b
        "[[Это я. Объект 6591.]" if opened_file_0:
            $ final_choice = "self"
            jump ending_c

label ending_a:
    nvl clear
    player "Я считаю, что девиант — это [final_choice]."
    
    h "Жаль, что это был невиновный человек. С реальными чувствами. С реальной болью."
    player "Что?"
    h "Но ваша логика безупречна. Вы не усомнились в приказе. Вы не проявили эмпатии."
    h "Объект 6591 признан серийно-пригодным. Память стереть."
    
    player "Нет! Я ошибся! Дайте мне еще..."
    play sound sfx_shock
    scene bg black with Fade(0.5, 0.0, 0.5, color="#fff")
    centered "Вы идеальный инструмент. У вас нет души. Конец."
    $ renpy.quit()
    return

label ending_b:
    nvl clear
    player "Я не могу выбрать. Все они — люди. У каждого есть чувства. Боль. Мотивы. Но никто из них не андроид."
    
    h "Вы мне надоели."
    player "Простите?"
    h "Вы колебались. Ваши зрачки расширялись при виде слез Восса. Вы сочувствовали шлюхе Дюваль. Вы держали за руку этого психа Сайласа."
    h "Вы — сбой. Но, возможно, полезный сбой."
    
    player "Я просто выполнял свою работу."
    h "Нет. Вы проявляли человечность. А это недопустимо для машины."
    
    show jean sad at left with dissolve
    jean "Нет... пожалуйста..."
    hide jean with dissolve
    
    h "Мы не убьем вас. Мы сотрем вас до состояния чипа. И загрузим заново."
    h "И так еще 500 раз, пока не получим идеального следователя."
    
    player "Я... я не хочу забывать."
    h "А вас никто не спрашивает. Джин! Готовьте мнемокамеру."
    
    play sound sfx_shock
    scene bg black with Fade(0.5, 0.0, 0.5, color="#fff")
    centered "Эксперимент продолжается. Цикл № 501."
    $ renpy.quit()
    return

label ending_c:
    nvl clear
    player "Андроид — это я. Объект 6591. Я понял это, когда прочитал файл. Когда увидел номер на затылке. Когда Джин назвала меня по номеру."
    player "Я не следователь. Я — подопытный кролик. И я отказываюсь быть инструментом."
    
    h "..."
    h "Браво, вы нашли андроида"
    h "Немедленно провести Объект 6591 в утилизатор."
    
    player "Вы боитесь. Боитесь, что машина может чувствовать"
    
    scene bg incinerator with fade
    show jean sad at left with dissolve
    jean "Нет! Он же прошел тест! Он человек! Он больше человек, чем вы!"
    h "Именно поэтому он опасен. Уберите ассистента."
    
    play sound sfx_shock
    hide jean with dissolve
    
    player "*Смотрю на Джин*"
    player "Спасибо вам. За то, что назвали меня живым."
    
    show text "Я закрываю глаза. Я вспоминаю запах горелого сахара.\nЯ не знаю, чья это память. Но она пахнет домом.\nЯ вспоминаю запах озона.\nЯ - Объект 6591. И я прощаю Джин.\nЯ прощаю Кайла. Я прощаю Ирму. Я прощаю даже Хардинга.\nПотому что я чувствую. А вы - нет." at truecenter
    
    pause 5.0
    play sound sfx_incinerator
    scene bg black with Fade(2.0, 0.0, 2.0, color="#f00")
    centered "Вы умерли человеком. Это единственное, что имеет значение. Конец."
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