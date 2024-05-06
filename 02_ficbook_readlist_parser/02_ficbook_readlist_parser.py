'''
# Выгрузка аналитики прочитанных работ с Книги Фанфиков

Для получения списка прочитанных работ необходимо выполнить следующие шаги:

1. Открыть сайт Книги Фанфиков (https://ficbook.net/)
2. Войти в свою учетную запись
3. Перейти на страницу "Кабинет читателя" -> "Прочитанные работы"
4. Выгрузить данные на указанном количестве страниц
'''

'''
## Решение задачи
### Шаг 1. Установка необходимых библиотек
'''
# !pip install undetected-chromedriver

# Импорты для работы с временем
import time
import datetime

# Импорты для работы с данными
import pandas as pd
import re

# Импорты для управления браузером и взаимодействия с веб-страницами
import undetected_chromedriver as uc  # Незамеченный драйвер Chrome
from selenium.webdriver.common.by import By  # Для выбора элементов на веб-странице
from selenium.webdriver.support.ui import WebDriverWait  # Для ожидания появления элементов
from selenium.webdriver.support import expected_conditions as EC  # Для ожидаемых условий
from selenium.webdriver.common.keys import Keys  # Для ввода клавиш на веб-страницах

# Импорты для управления программой и выхода из нее
import sys

'''
### Шаг 2. Подготовка к выполнению задачи, создание необходимых функций
'''


# Вход в учетную запись и переход на страницу прочитанного
def login_and_continue(url, username, password):
    options = uc.ChromeOptions()
    options.headless = False
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })

    driver = uc.Chrome(use_subprocess=True, options=options)

    # Открытие страницы
    driver.get(url)

    # Ожидание появления кнопки "Вход" в течение 10 секунд
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Вход"))
    )

    # Нажатие на кнопку "Вход"
    login_button.click()

    # Ожидание появления формы ввода логина и пароля
    login_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "login-form"))
    )

    # Заполнение полей логина и пароля
    username_field = login_form.find_element(By.ID, "username")
    password_field = login_form.find_element(By.ID, "password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Отправка формы с помощью кнопки "Войти"
    password_field.send_keys(Keys.ENTER)

    # Находим элемент с именем пользователя на странице и нажимаем на него
    username_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '" + username + "')]"))
    )

    username_element.click()

    # Находим элемент "Кабинет читателя" в выпадающем меню и нажимаем на него
    cabinet_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Кабинет читателя"))
    )

    cabinet_button.click()

    # Находим элемент "Прочитанные работы" в подсписке и нажимаем на него
    read_works_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Прочитанные работы"))
    )

    read_works_button.click()

    # Возвращаем объект driver, чтобы можно было продолжить работу с ним
    return driver


# Создание таблицы с данными фанфиков на текущей странице
def get_fanfics(driver):
    # Создаем пустые списки для данных
    names = []
    authors = []
    pages = []
    fandoms = []
    dates = []
    # Находим все элементы, содержащие информацию о фанфиках
    fanfic_elements = driver.find_elements(By.XPATH, '//div[@class="js-toggle-description"]')

    # Итерируемся по каждому элементу и извлекаем информацию
    for element in fanfic_elements:
        name_element = WebDriverWait(element, 10).until(
            EC.visibility_of_element_located((By.XPATH, './/h3[@class="fanfic-inline-title"]/a')))
        name = name_element.text
        author_elements = element.find_elements(By.XPATH, './/span[@class="author word-break"]/a')
        author = ', '.join([author.text for author in author_elements])
        pages_element = None
        try:
            pages_element = element.find_element(By.XPATH,
                                                 './/dl[@class="fanfic-inline-info"]/dd[contains(text(), "страниц")]')
        except:
            pass
        if pages_element:
            pages_text = pages_element.text
            # Используем регулярное выражение для поиска числа
            pages_match = re.search(r'\b\d+\b', pages_text)
            if pages_match:
                pages_number = int(pages_match.group())
            else:
                pages_number = None
        else:
            pages_number = None

        fandom = element.find_element(By.XPATH, './/dl[@class="fanfic-inline-info"]/dd/a').text
        date_element = element.find_element(By.XPATH, './/div[@class="read-notification"]//span[@title]')
        date = date_element.get_attribute("title")

        names.append(name)
        authors.append(author)
        pages.append(pages_number)
        fandoms.append(fandom)
        dates.append(date)

    # Создаем датафрейм
    df = pd.DataFrame({
        'Name': names,
        'Author': authors,
        'Pages': pages,
        'Fandom': fandoms,
        'Date': dates
    })

    return df


'''
### Шаг 3. Подготовка и сбор данных
'''
try:
    url = "https://ficbook.net/"

    username = str(input('Введите логин:'))
    password = str(input('Введите пароль:'))
    end_page = int(input('Сколько страниц надо выгрузить:'))

    driver = login_and_continue(url, username, password)

    df = get_fanfics(driver)
    for i in range(1, end_page):
        # Переход на следующую страницу
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="page-arrow page-arrow-next"]/a')))
        next_button.click()
        time.sleep(2)
        # Получаем данные с текущей страницы
        current_page_df = get_fanfics(driver)

        # Объединяем данные с предыдущими страницами
        df = pd.concat([df, current_page_df], ignore_index=True)

    '''
    ### Шаг 4. Сохранение полученных результатов и завершение программы
    '''
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    df.to_excel('Readlist_ficbook_{}_{}.xlsx'.format(username, current_date), index=False)
finally:
    # Закрытие браузера
    driver.quit()
    # Завершение работы программы
    sys.exit()
