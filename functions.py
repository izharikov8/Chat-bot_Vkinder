import itertools
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from CONSTANTS import *


vk_personal = vk_api.VkApi(token=token_personal)
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

# Функции для общения с ботом


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


def write_msg_with_attachmt(user_id, message, attachment):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7), 'attachment': ','.join(attachment)})


def greetings(user):
    write_msg(user, greetings_text)


def repeat_bot():
    for this_event in longpoll.listen():
        if this_event.type == VkEventType.MESSAGE_NEW:
            if this_event.to_me:
                message_text = this_event.text
                return message_text, this_event.user_id


# Функции для обращения к Вконтакте


def get_user_info(user_id):
    res = vk.method('users.get', {'user_id': user_id, 'fields': 'sex, city, country'})
    sex = res[0]['sex']
    if sex == 1:
        sex_opposite = 2
    elif sex == 2:
        sex_opposite = 1
    try:
        city_title = res[0]['city']['title']
    except KeyError:
        city_title = 0
    return sex_opposite, city_title


def people_search(sex, city, age_from, age_to):
    res = vk_personal.method('users.search', {'sort': 1,
                                              'status': 6,
                                              'has_photo': 1,
                                              'sex': sex,
                                              'city': city,
                                              'age_from': age_from,
                                              'age_to': age_to,
                                              'count': 5})
    candidates = []
    prof_link = 'https://vk.com/id'
    for el in res['items']:
        if el['is_closed'] == False:
            person = [el['id'], el['first_name'], el['last_name'], str(prof_link) + str(el['id'])]
            candidates.append(person)
    return candidates


def get_candidate_photos(candidate_id):
    res = vk_personal.method('photos.get', {'owner_id': candidate_id, 'album_id': 'profile', 'extended': 1})
    data = []
    for el in res['items']:
        like_sum = el['likes']['count'] + el['comments']['count']
        owner_id = el['owner_id']
        file_id = el['id']
        temp_list = [like_sum, owner_id, file_id]
        data.append(temp_list)
        data.sort(reverse=True)
    top_list = []
    for el in itertools.islice(data, 3):
        top_list.append(f'photo{el[1]}_{el[2]}')
    return top_list


def get_city_identificator(city, country=1):
    res = vk_personal.method('database.getCities', {'country_id': country, 'q': city})
    try:
        city_id = res['items'][0]['id']
    except KeyError and IndexError:
        city_id = 0
    return city_id


def sort_candidates(info):
    candidates = []
    prof_link = 'https://vk.com/id'
    for el in info['items']:
        if el['is_closed'] == False:
            person = [el['id'], el['first_name'], el['last_name'], str(prof_link) + str(el['id'])]
            candidates.append(person)
    for candidate in candidates:
        photos = get_candidate_photos(candidate[0])
        data = []
        for el in photos['items']:
            like_sum = el['likes']['count'] + el['comments']['count']
            owner_id = el['owner_id']
            file_id = el['id']
            temp_list = [like_sum, owner_id, file_id]
            data.append(temp_list)
            data.sort(reverse=True)
        top_list = []
        for el in itertools.islice(data, 3):
            top_list.append(f'photo{el[1]}_{el[2]}')
    return top_list, candidate


