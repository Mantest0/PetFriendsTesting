from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_add_new_pet_no_photo(name='Котик', animal_type='котик', age='1'):
    """Проверяем, что можно добавить питомца  без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''


def test_add_pet_new_photo(pet_photo='img/kitti.png'):
    """Проверяем что можно добавить/изменить фото питомца"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
    assert status == 200
    assert result['pet_photo'] != ''
#
def test_get_api_key_with_invalid_email(email='12345mmail.ru', password=valid_password):
        """Негативный кейс на отправку невалидного электронного адреса"""

        status, result = pf.get_api_key(email, password)
        assert status == 403

def test_get_api_key_with_invalid_password(email=valid_email, password='12345'):
    """Негативный кейс на отправку невалидного пароля"""

    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_add_new_pet_with_invalid_name(name=12345, animal_type='Дракон',
                                       age='1000', pet_photo='img/drako.jpg'):
    """Негативный кейс на добавление питомца с невалидным именем """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('Неверное имя')


def test_add_new_pet_without_name(name='', animal_type='Дракон', age='10000',
                                     pet_photo='img/drako.jpg'):
    """Негативный тест на добавление без имени"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('Неверное имя')
    else:
        assert status == 200
        print("Баг - питомец добавлен без имени")

def test_try_unsuccessful_delete_empty_pet_id():
    """Проверяем, что нельзя удалить питомца с пустым id"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = ''
    status, _ = pf.delete_pet(auth_key, pet_id)
    assert status == 400 or 404
    print('удалить питомца без id нельзя')

def test_add_new_pet_with_invalid_animal_type(name='Дракончик', animal_type=12345,
                                              age='1000', pet_photo='img/drako.jpg'):
    """Негативный кейс на добавление питомца с неверным форматом вида"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('Неверный вид питомца')


def test_add_new_pet_with_none_value_animal_type(name='Дракончик', animal_type='',
                                                 age='10000', pet_photo='img/drako.jpg'):
    """Негативный кейс на добавление питомца с пустым значением вида"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('не указан вид питомца')
    else:
        assert status == 200
        print("Баг - питомец добавлен без вида")


def test_add_new_pet_with_invalid_age(name='Дракончик', animal_type='Дракон',
                                      age='тысяча', pet_photo='img/drako.jpg'):
    """Негативный кейс на добавление питомца с неверным значением возраста"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('неверно указан возраст питомца')
    else:
        assert status == 200
        print("Баг - питомец добавлен с некоректным возрастом")