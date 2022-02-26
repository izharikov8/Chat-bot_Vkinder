import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from functions import *
from db import *


if __name__ == '__main__':
    while True:
        msg, id_user = repeat_bot()
        if msg:
            greetings(id_user)
            current_id_user = check_db_user(id_user)
            if current_id_user == None:
                register_user(id_user)
                current_id_user = check_db_user(id_user)
            msg, id_user = repeat_bot()
            if msg == 'start':
                sex_opposite, city_title = get_user_info(id_user)
                if city_title == 0:
                    write_msg(id_user, 'В каком городе ищем? (пример: Москва / Тверь): ')
                    msg, id_user = repeat_bot()
                    city_title = msg
                city_id = get_city_identificator(city_title)
                write_msg(id_user, 'Введите минимальный возраст (от 18) для поиска: ')
                msg, id_user = repeat_bot()
                min_age = msg
                if int(min_age) < 18:
                    write_msg(id_user, 'У нас всё по закону! Выставлен минимальный возраст - 18 лет!')
                    min_age = 18
                write_msg(id_user, 'Введите максимальный возраст (до 99) для поиска: ')
                msg, id_user = repeat_bot()
                max_age = msg
                if int(max_age) >= 100:
                    write_msg(id_user, 'Таких здесь точно нет! Выставлен максимальный возраст - 99 лет!')
                    max_age = 99
                candidates = people_search(sex_opposite, city_id, min_age, max_age)
                for candidate in candidates:
                    prospect_id = int(candidate[0])
                    checked_prospect = check_db_prospect(prospect_id)
                    current_id_user = check_db_user(id_user)
                    if checked_prospect == None:
                        add_user(candidate[0], candidate[1], candidate[2], candidate[3], current_id_user.id)
                        link = candidate[3]
                        photos = get_candidate_photos(candidate[0])
                        write_msg_with_attachmt(id_user, link, photos)
                        write_msg(id_user, 'Продолжить поиск - 1\n'
                                           'Выход / Начать поиск сначала - 2')
                        msg, id_user = repeat_bot()
                        if msg == '1':
                            continue
                        elif msg == '2':
                            write_msg(id_user, 'Благодарим за использование нашего бота!\n'
                                               'Для перезапуска и поиска по новым параметрам введите любой текст!')
                            break
                        else:
                            write_msg(id_user, 'Неизвестная команда! Введите любой текст для перезапуска бота!')
                            break
                    else:
                        continue
                write_msg(id_user, 'Вы просмотрели все подобранные профили!\n'
                                   'Введите любой текст для перезапуска бота!')
