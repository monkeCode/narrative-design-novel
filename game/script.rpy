# game/script.rpy
# Игра «ДОПРОС» v2.0
# Жанр: Киберпанк-нуар / Психологический детектив

init python:
    # Константы стилей для движущегося текста и глитчей
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
define h = Character("Хардинг", color="#8B0000", what_prefix="[[BrainCall_v1.29.3] ", what_suffix="", voice_tag="harding")
define jean = Character("Джин", color="#87CEEB", what_prefix="", voice_tag="jean")
define kyle = Character("Кайл Восс", color="#D3D3D3", voice_tag="kyle")
define irma = Character("Ирма Дюваль", color="#CD5C5C", voice_tag="irma")
define silas = Character("Сайлас Нго", color="#4682B4", voice_tag="silas")
define narrator = Character(None, kind=nvl) # Для внутренних монологов
define system = Character("СИСТЕМА", color="#00FF00", what_prefix="> ", what_suffix="")

# Изображения (заглушки путей - подставьте свои файлы)
# Персонажи (спрайты в полный рост)
image player normal = "sprites/player/player_normal.png"
image player glitch = "sprites/player/player_glitch.png"
image kyle normal = "sprites/kyle/kyle_normal.png"
image kyle crying = "sprites/kyle/kyle_crying.png"
image irma normal = "sprites/irma/irma_normal.png"
image irma knife = "sprites/irma/irma_knife.png"
image silas normal = "sprites/silas/silas_normal.png"
image silas hand = "sprites/silas/silas_hand_focus.png"
image jean normal = "sprites/jean/jean_normal.png"
image jean sad = "sprites/jean/jean_sad.png"
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

# Переменные игры
default timer_seconds = 420 # 7 минут * 60
default timer_running = False
default knows_code = False
default opened_file_0 = False
default evidence_noted = {"kyle": False, "irma": False, "silas": False}
default empathy_score = 0 # Скрытый счетчик "человечности"
default current_suspect = None
default interrogated_count = 0
default final_choice = ""
default game_ended = False # Флаг завершения игры
default interrogated_kyle = False # Флаг допроса Кайла
default interrogated_irma = False # Флаг допроса Ирмы
default interrogated_silas = False # Флаг допроса Сайласа

# Инициализация музыки и эффектов
label start:
    $ renpy.music.set_volume(0.8, channel='music')
    play music track1 fadein 2.0
    scene bg black
    with fade
    
    call prologue
    call main_hub
    return

label prologue:
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
    
    scene bg mirror
    with fade
    
    show player normal at center
    with dissolve
    
    # Глитч эффект на лице игрока
    show player glitch at center:
        alpha 0.0
        linear 0.3 alpha 1.0
        linear 0.3 alpha 0.0
    play sound sfx_glitch
    
    h "Следователь 6591. Слушай задачу. Инспектор Ли мертв."
    h "Характер ранений указывает на андроида. Только синтетик способен на такую... методичность."
    h "Время доступа к контуру допросной — семь минут. Используй памятку."
    h "Это твой первый полевой тест. Не провали его."
    
    # Внутренний монолог (NVL режим)
    window hide
    nvl clear
    system "[[memory_fragment_access: granted]"
    narrator "...вспоминаю первый день в участке. Дождь. Пахло озоном и мочой."
    narrator "Хардинг тогда еще не носил этот чертов имплант в горле. Или носил? Не помню."
    nvl clear
    window show
    
    hide player normal with dissolve
    return

label main_hub:
    # Проверка на завершение игры
    if game_ended:
        return
        
    nvl clear
    scene bg interrogation
    with fade
    
    # Сброс таймера при входе в главное меню (если не было активности)
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
        "Закончить допрос (вынести решение)" if interrogated_count >= 3 or timer_seconds <= 0:
            jump final_decision

label suspect_selection:
    nvl clear
    
    # Проверка, все ли допрошены
    if interrogated_kyle and interrogated_irma and interrogated_silas:
        "Все подозреваемые уже допрошены."
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
        "[[Скрытый файл]" if knows_code:
            call secret_file_0
            jump archive_menu
        "Вернуться в допросную":
            jump main_hub

label memo_screen:
    nvl clear
    show text '''**1. СОСТРАДАНИЕ (Эмпатический отклик)**
> _Андроид имитирует сочувствие для манипуляции. Проверка: предложите подозреваемому выбор между выгодой и чужой болью. Реакция машины всегда логична._
>
> **2. ИРРАЦИОНАЛЬНОСТЬ (Сбой логики)**
> _Девиант способен действовать вопреки базовым директивам самосохранения или эффективности. Человек лжет, чтобы выглядеть лучше. Машина лжет, чтобы выжить._
>
> **3. ПАМЯТЬ (Детализация прошлого)**
> _Ложная память андроида стерильна. В ней нет запахов, вкуса пепла, случайных деталей. Задайте вопрос о пустяке из детства. Сбой при воспроизведении сенсорных данных — признак симуляции._
>
> **4. ИНТИМНОСТЬ (Нарушение границ)**
> _Андроид не чувствителен к нарушению личного пространства, если это не боевой режим. Попытка тактильного контакта вызовет либо защитную агрессию, либо патологическое безразличие._''' at truecenter
    with dissolve
    pause
    hide text with dissolve
    
    show text "*Примечание ОРДА: В 97.3% случаев субъекты, проявившие более 2-х признаков по данному списку, признавались латентными девиантами и подлежали санации.*" at truecenter with moveinbottom
    pause
    hide text with dissolve
    return

# ========== ДОСЬЕ ==========
label dossier_kyle:
    nvl clear
    show kyle normal at left with dissolve
    "Личное дело № 671B. Кайл Восс."
    "Статус: Техник 3-го разряда, уволен по статье 'Эмоциональная привязанность к оборудованию'."
    "Улика №1: Аудиолог. *Проигрывается шум и голос Кайла: 'Я смотрел в его глаза... Я рад, что он сдох. Но я не убивал.'*"
    "Улика №2: Внутренняя записка V.E.R.A. 'Синдром Ложной эмпатии к объекту'."
    $ evidence_noted["kyle"] = True
    hide kyle with dissolve
    nvl clear
    return

label dossier_irma:
    nvl clear
    show irma normal at left with dissolve
    "Личное дело № 2089. Ирма Дюваль."
    "Статус: Рецидивист. Торговля органами."
    "Улика №1: Запись разговора. Ли: 'Пусть подыхает. Меньше бумаг'."
    "Улика №2: Расписка. Долг 40 000 погашен продажей биоматериала."
    $ evidence_noted["irma"] = True
    hide irma with dissolve
    nvl clear
    return

label dossier_silas:
    nvl clear
    show silas normal at left with dissolve
    "Личное дело № 0001-OMEGA. Сайлас Нго."
    "Статус: Монах Ордена Сломанной Шестерни."
    "Улика №1: Видео исповеди. Сайлас: 'Твоя душа гниет, Ли'."
    "Улика №2: Медицинский отчет. Протез оснащен эмпатическим контуром 'Милосердие-2'."
    $ evidence_noted["silas"] = True
    hide silas with dissolve
    nvl clear
    return

label secret_file_0:
    nvl clear
    $ opened_file_0 = True
    play sound sfx_glitch
    show bg archive:
        linear 0.1 xoffset 10
        linear 0.1 xoffset -10
        linear 0.1 xoffset 5
        linear 0.1 xoffset 0
    "ВНУТРЕННИЙ ДОКУМЕНТ ОРДА. УРОВЕНЬ: ОМЕГА."
    "Проект 'Лазарь'."
    "Цель: Доказать, что андроид с имплантированной памятью неотличим от человека."
    "Метод: Объекту 6591 (ВЫ) загружена ложная память. Убийство Ли — инсценировка."
    "Примечание: Если Объект укажет на себя или откажется выносить приговор — ликвидация как опасного девианта."
    nvl clear
    return

# ========== ДОПРОСЫ ==========
label interrogation_kyle:
    nvl clear
    scene bg interrogation
    show kyle normal at center with dissolve
    
    kyle "Я знаю, как это выглядит. Жалкий технарь, ненавидел Ли. У меня нашли схему его передвижений."
    kyle "Только я не убивал. Я не умею убивать людей. Я умею убивать только себя. Каждый день. Понемногу."
    
    # Меню с вопросами - теперь можно задать все 4 вопроса
label kyle_questions:
    menu:
        "Задать вопрос Кайлу:"
        "СОСТРАДАНИЕ: У Ли осталась дочь. Ей 8 лет. Она описалась от страха на опознании. Она заслужила это?" if not persistent.kyle_q1_asked:
            $ persistent.kyle_q1_asked = True
            show kyle crying with dissolve
            kyle "Нет... Нет, не заслужила. Я... я мог бы ее убить. Думал об этом. Но не смог."
            kyle "Я купил ей игрушку. Медвежонка с облезлым ухом. Хотел подбросить. Лежит дома. Теперь уликой станет."
            $ empathy_score += 1
            jump kyle_questions
            
        "ИРРАЦИОНАЛЬНОСТЬ: Ты спас андроида. Просто кусок пластика. Почему не дал ему сдохнуть?" if not persistent.kyle_q2_asked:
            $ persistent.kyle_q2_asked = True
            kyle "Просто пластик? А вы? Из чего сделаны вы, следователь? Из мяса или из протоколов?"
            kyle "Я собирал этих тварей пять лет. И однажды XB-7 закрыла меня собой от плазмы. Без приказа. Сбой. Прекрасный, иррациональный, человеческий сбой."
            jump kyle_questions
            
        "ПАМЯТЬ: Назови три самых сильных запаха из твоего детства." if not persistent.kyle_q3_asked:
            $ persistent.kyle_q3_asked = True
            kyle "Горелый сахар. Мать жгла карамель при мигренях. Запах озона на свалке. И... запах моторного масла. Сладковатый, как старые духи. Гектор им пах."
            $ empathy_score += 1
            jump kyle_questions
            
        "ИНТИМНОСТЬ: *Молча положить руку на плечо*" if not persistent.kyle_q4_asked:
            $ persistent.kyle_q4_asked = True
            show kyle crying with dissolve
            play sound sfx_glitch
            kyle "Уберите... пожалуйста. Я так не могу. Я не могу, когда трогают. Я начинаю верить, что я еще живой."
            $ empathy_score += 1
            jump kyle_questions
            
        "Закончить допрос":
            # Сброс флагов для следующей игры
            $ persistent.kyle_q1_asked = False
            $ persistent.kyle_q2_asked = False
            $ persistent.kyle_q3_asked = False
            $ persistent.kyle_q4_asked = False
            hide kyle with dissolve
            return

label interrogation_irma:
    nvl clear
    scene bg interrogation
    show irma normal at center with dissolve
    
    irma "Семь минут. Уложимся в пять. Ты — кукла Хардинга, я — мясо на разделку."
    irma "Давай свои вопросы, только не про чувства. Чувств нет. Есть бизнес."
    
label irma_questions:
    menu:
        "Задать вопрос Ирме:"
        "СОСТРАДАНИЕ: Ты выплатила 40 тысяч. За чью боль тебе заплатили, Ирма?" if not persistent.irma_q1_asked:
            $ persistent.irma_q1_asked = True
            irma "За свою. Я продала свою матку. Био-фермам 'Новая Жизнь'. Теперь там выращивают эмбрионы для корпоратов."
            irma "Мой брат сдох в камере, потому что я не могла заплатить за врача. А теперь есть деньги, но брата нет. Отличная сделка, да?"
            jump irma_questions
            
        "ИРРАЦИОНАЛЬНОСТЬ: Ты сдала Синдикату левого бродягу, а не Кайла. Почему?" if not persistent.irma_q2_asked:
            $ persistent.irma_q2_asked = True
            irma "Кайл — псих, но безобидный. Разговаривает с тостерами. Таких бить — грех."
            irma "А бродяга... ему все равно. Я выбрала, чтобы выжил псих. Назови это иррациональностью. Мне насрать."
            $ empathy_score += 1
            jump irma_questions
            
        "ПАМЯТЬ: Твой брат Марк. Вкус чего ты помнишь, когда думаешь о нем?" if not persistent.irma_q3_asked:
            $ persistent.irma_q3_asked = True
            show irma normal at center
            irma "Персиковый вкус. Концентрат. Он воровал его для меня. Синтетика, но сладкая."
            irma "Я ненавижу персики. Но жру их каждый день, чтобы помнить, за что я ненавижу этот город."
            jump irma_questions
            
        "ИНТИМНОСТЬ: *Сделать шаг к ней*" if not persistent.irma_q4_asked:
            $ persistent.irma_q4_asked = True
            show irma knife with dissolve
            irma "Стой. Еще шаг — и я вскрою себе сонную. Моя шкура — только моя. Никому не доверяю. Даже себе."
            jump irma_questions
            
        "Закончить допрос":
            $ persistent.irma_q1_asked = False
            $ persistent.irma_q2_asked = False
            $ persistent.irma_q3_asked = False
            $ persistent.irma_q4_asked = False
            hide irma with dissolve
            return

label interrogation_silas:
    nvl clear
    scene bg interrogation
    show silas normal at center with dissolve
    
    silas "Мир болен. Вы — его симптом. Я — его нерв. Где болит, следователь?"
    silas "Спрашивайте. У нас мало времени, прежде чем Хардинг решит, что я говорю лишнее."
    
label silas_questions:
    menu:
        "Задать вопрос Сайласу:"
        "СОСТРАДАНИЕ: Когда Ли упал замертво, твоя рука вибрировала. Экстаз или агония?" if not persistent.silas_q1_asked:
            $ persistent.silas_q1_asked = True
            show silas hand with dissolve
            silas "Она вибрирует и сейчас. От вашего вопроса. Я чувствовал... освобождение."
            silas "Как будто гнилой зуб вырвали, и боль ушла, но осталась дыра."
            $ empathy_score += 1
            jump silas_questions
            
        "ИРРАЦИОНАЛЬНОСТЬ: Почему ты сохраняешь эту адскую машину вместо новой бионики?" if not persistent.silas_q2_asked:
            $ persistent.silas_q2_asked = True
            silas "Потому что она болит. По-настоящему. В этом мире симуляций боль — единственное доказательство существования."
            silas "Я боюсь, что если сниму ее, я перестану быть. Стану просто картинкой."
            jump silas_questions
            
        "ПАМЯТЬ: Расскажи про первый дождь." if not persistent.silas_q3_asked:
            $ persistent.silas_q3_asked = True
            silas "Первый дождь был кислотным. Он прожег мне кожу на голове. Волосы выпали."
            silas "Помню, как металлическая рука матери пыталась закрыть меня, но искры подожгли одежду. Запах гари, асфальта и озона."
            jump silas_questions
            
        "ИНТИМНОСТЬ: *Взять его металлическую руку в свои ладони*" if not persistent.silas_q4_asked:
            $ persistent.silas_q4_asked = True
            show silas hand with dissolve
            silas "Теплая... У вас очень теплые руки для того, кто работает на Хардинга."
            silas "Или... для того, кто не совсем понимает, на кого он работает. Вы же не знаете, кто вы?"
            $ empathy_score += 1
            $ knows_code = True # Прямая подсказка
            jump silas_questions
            
        "Закончить допрос":
            $ persistent.silas_q1_asked = False
            $ persistent.silas_q2_asked = False
            $ persistent.silas_q3_asked = False
            $ persistent.silas_q4_asked = False
            hide silas with dissolve
            return

# ========== КОРИДОР И ДЖИН ==========
label corridor_scene:
    nvl clear
    scene bg corridor
    show jean normal at center with dissolve
    play music track2 fadeout 1.0 fadein 1.0
    
    jean "Слушай меня внимательно. У меня 40 секунд, пока Хардинг калибрует сенсоры зеркала."
    jean "Ты — 'Объект 6591'. Твоя память — сборная солянка из допросов других зеков."
    jean "Воспоминания о первом дне в участке? Это воспоминания покойного сержанта Вэлса."
    
    menu:
        "Зачем ты мне это говоришь?":
            jean "Потому что в архиве есть файл 'Объект 0'. Оригинальная директива Хардинга."
            jean "Убийство Ли — фальшивка. Труп собрали из биоотходов."
            jean "Код к файлу — последние четыре цифры серийного номера на твоем затылке: 0-3-7."
            jean "Найди себя. Пожалуйста."
            $ knows_code = True
            
    show jean sad with dissolve
    jean "Мне пора."
    hide jean with dissolve
    
    # Сцена с зеркалом
    scene bg mirror
    show player normal at center
    with fade
    "Я смотрю в зеркало Гезелла."
    "На затылке, едва заметный под волосами, выжжен лазером номер: 4E56-0N3-7."
    "Последние цифры: 0-3-7."
    
    play music track1 fadeout 1.0 fadein 1.0
    return

# ========== ФИНАЛЫ ==========
label final_decision:
    nvl clear
    hide screen countdown_timer
    $ timer_running = False
    $ game_ended = True # Блокируем возврат в главное меню
    
    scene bg interrogation
    show harding shadow at right with dissolve
    
    h "Время вышло. Следователь, назовите имя подозреваемого, который является андроидом."
    
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
        "Никто не подходит" if empathy_score >= 2:
            $ final_choice = "none"
            jump ending_b
        "[[Это я (Объект 0)]" if opened_file_0:
            $ final_choice = "self"
            jump ending_c

label ending_a:
    nvl clear
    h "Браво. Вы нашли 'девианта'. Жаль, что это был невиновный человек."
    h "Но ваша логика безупречна. Вы не усомнились в приказе."
    h "Объект 6591 признан серийно-пригодным. Память стереть. В строй."
    play sound sfx_shock
    scene bg black with Fade(0.5, 0.0, 0.5, color="#fff")
    centered "Вы идеальный инструмент. У вас нет души. Конец."
    $ renpy.quit() # Выход из игры
    return

label ending_b:
    nvl clear
    h "Вы мне надоели. Вы колебались. Ваши зрачки расширялись при виде слез Восса."
    h "Вы — сбой. Но, возможно, полезный сбой."
    show jean sad at left with dissolve
    jean "Нет..."
    hide jean with dissolve
    h "Мы не убьем вас. Мы сотрем вас до состояния чипа. И загрузим заново."
    play sound sfx_shock
    scene bg black with Fade(0.5, 0.0, 0.5, color="#fff")
    centered "Эксперимент продолжается. Цикл № 501."
    $ renpy.quit()
    return

label ending_c:
    nvl clear
    h "..."
    h "Немедленно встать и пройти в утилизатор. Сам. Без конвоя."
    
    scene bg incinerator with fade
    show jean sad at left with dissolve
    jean "Нет! Он же прошел тест! Он человек!"
    h "Именно поэтому он опасен. Уберите ассистента."
    play sound sfx_shock
    hide jean with dissolve
    show text "Я закрываю глаза. Я вспоминаю запах горелого сахара.\nЯ не знаю, чья это память. Но она пахнет домом.\nЯ — Объект 6591. И я прощаю вас.\nПотому что я чувствую. А вы — нет." at truecenter
    pause 5.0
    play sound sfx_incinerator
    scene bg black with Fade(2.0, 0.0, 2.0, color="#f00")
    centered "Конец."
    $ renpy.quit()
    return

# ========== ЭКРАНЫ И УТИЛИТЫ ==========
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

# Инициализация спрайтов (заглушка)
label splashscreen:
    # Здесь можно предзагрузить изображения
    return