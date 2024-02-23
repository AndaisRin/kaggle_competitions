"""
# Тестовое задание для Гринатома

## Условия задачи:
1. Открыть https://www.moex.com;
2. Перейти по следующим элементам: Меню -> Срочный рынок -> Индикативные курсы;
3. В выпадающем списке выбрать валюты: USD/RUB - Доллар США к российскому рублю;
4. Сформировать данные за предыдущий месяц;
5. Скопировать данные в Excel;
    Столбцы в Excel:
    - (A) Дата USD/RUB – Дата
    - (B) Курс USD/RUB – Значение из Курс основного клиринга
    - (C) Время USD/RUB – Время из Курс основного клиринга
6. Повторить шаги для валют JPY/RUB - Японская йена к российскому рублю;
7. Скопировать данные в Excel;
    Столбцы в Excel:
    - (D) Дата JPY/RUB – Дата
    - (E) Курс JPY/RUB – Значение из Курс основного клиринга
    - (F) Время JPY/RUB – Время из Курс основного клиринга
8. Для каждой строки полученного файла поделить курс USD/RUB на JPY/RUB, полученное значение записать в ячейку (G) Результат;
9. Выровнять – автоширина;
10. Формат чисел – финансовый;
11. Проверить, что автосумма в Excel распознает ячейки как числовой формат;
12. Направить итоговый файл отчета себе на почту;
13. В письме указать количество строк в Excel в правильном склонении.
"""

"""
## Решение задачи

### Шаг 1. Установка необходимых библиотек
"""
# !pip install selenium
# !pip install openpyxl
# Модуль сокрытия предупреждений
import warnings

warnings.filterwarnings("ignore")

# Модули для работы с временем
import time  # для работы с временем

# Модули для работы с данными
import pandas as pd

# Модули для управления браузером и взаимодействия с веб-страницами
from selenium import webdriver  # для управления браузером
from selenium.webdriver.chrome.service import Service  # для настройки сервиса ChromeDriver
from selenium.webdriver.common.by import By  # для выбора элементов на веб-странице
from selenium.webdriver.chrome.options import Options  # для установки опций браузера Chrome
from selenium.webdriver.support.ui import WebDriverWait  # для ожидания появления элементов
from selenium.webdriver.support import expected_conditions as EC  # для ожидаемых условий

# Модули для работы с регулярными выражениями и файлами Excel
from openpyxl import load_workbook  # для загрузки книги Excel
from openpyxl.styles import NamedStyle  # для именованных стилей в Excel

# Модули для отправки почтовых сообщений
import smtplib  # для отправки почтовых сообщений
from email.mime.multipart import MIMEMultipart  # для создания многочастных сообщений
from email.mime.text import MIMEText  # для создания текстовых сообщений
from email.mime.application import MIMEApplication  # для создания прикрепленных файлов

# Модули для работы с переменными окружения
import os  # для работы с переменными окружения

"""
### Шаг 2. Подготовка к выполнению задачи, создание необходимых функций
"""
# Функция получения таблицы о курсах валют
def create_table(currency):
    table_rows = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr')))
    data = []
    for row in table_rows:
        row_data = [cell.text for cell in row.find_elements(By.XPATH, "./td")]
        data.append(row_data)

    # Создаем датафрейм
    df = pd.DataFrame(data, columns=["Дата {}".format(currency),
                                     "Курс {} промежуточного клиринга значение".format(currency),
                                     "Курс {} промежуточного клиринга время".format(currency),
                                     "Курс {} основного клиринга значение".format(currency),
                                     "Курс {} основного клиринга время".format(currency)])
    df = df.filter(regex='^(?!.*промежуточного).*$')
    # Переименовываем столбцы
    df = df.rename(columns={
        "Курс {} основного клиринга значение".format(currency): "Курс {}".format(currency),
        "Курс {} основного клиринга время".format(currency): "Время {}".format(currency)
    })
    return df


# Функция для создания корректного текста письма
def create_email_text(num_rows):
    # Определение правильного склонения для слова "строка"
    if num_rows % 10 == 1 and num_rows % 100 != 11:
        rows_text = "строка"
    elif 2 <= num_rows % 10 <= 4 and (num_rows % 100 < 10 or num_rows % 100 >= 20):
        rows_text = "строки"
    else:
        rows_text = "строк"
    return "Добрый день!\n\nОтчет о файле currency_data.xlsx, он содержит {} {}.\n\nС уважением, Екатерина и её бот.".format(
        num_rows, rows_text)


"""
### Шаг 3. Подготовка и сбор данных
"""
# Запускаем браузер
options = Options()
options.add_experimental_option("excludeSwitches", ['enable-logging'])
options.add_argument("user-agent=[Chrome/122.0.6261.58]")
service = Service('D:\\Python_Data\\competitions_projects\\11_greenatom_rpa\\resourse\\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
print("Начинаем работу парсера")

# URL и XPath для поискового поля
url = 'https://www.moex.com/'
search = '//input[@id="moex-search-input"]'
indicative_text = "Индикативные курсы"

# Открываем браузер и увеличиваем окно до максимального размера
driver.get(url)
driver.maximize_window()

# Находим и вводим текст в поисковое поле
search_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, search)))
search_field.click()
search_field.send_keys(indicative_text)

# Находим ссылку на индикативные курсы и проверяем её текст
try:
    indicative_courses_link = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, '//a[@itemprop="item"]')))
    indicative_courses_text = indicative_courses_link[2].text
    print(indicative_courses_text)
    try:
        assert indicative_courses_text == indicative_text
        print(f"Клик по ссылке: {indicative_courses_text}")
        indicative_courses_link[2].click()
        accept_terms = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//a[@data-dismiss="modal"]')))
        accept_terms.click()
        time.sleep(5)
    except AssertionError:
        print("Текст элемента не соответствует")
except:
    print("Ссылка на индикативные курсы не найдена")

# Выводим сообщение об успешном завершении
print('Страница USD/RUB успешно найдена')

df_usd = create_table('USD/RUB')

# Сохранение датафрейма в файл Excel
df_usd.to_excel("currency_data.xlsx", index=False)
print('Создаем файл Excel для USD')

# Сохраняем текущий URL
current_url = driver.current_url

# Меняем текущий URL для смены валюты
new_url = current_url.replace("USD", "JPY")
driver.get(new_url)

print('Страница JPY/RUB успешно найдена')

df_jpy = create_table('JPY/RUB')

# Закрываем браузер
driver.quit()
print('Закрываем браузер')

to_update = {"Sheet1": df_jpy}

# Добавляем данные о йенах на текущий лист в файл Excel
with pd.ExcelWriter('currency_data.xlsx', mode='a', if_sheet_exists='overlay') as excel_writer:
    for sheet, append_df in to_update.items():
        sheet_df = pd.read_excel('currency_data.xlsx', sheet_name=sheet)
        if not append_df.empty:
            sheet_df = pd.concat([sheet_df, append_df], axis=1)
        sheet_df.to_excel(excel_writer, sheet, index=False)
print('Обновляем файл Excel, добавляя информацию о JPY')

# Удаляем переменные df, to_update и другие ненужные датафреймы из памяти программы
del df_usd, df_jpy, to_update, sheet_df, append_df

"""
### Шаг 4. Обработка данных
"""
# Чтение данных из созданного файла
df = pd.read_excel('currency_data.xlsx')

# Вычисление значения в новом столбце
df['Результат'] = df['Курс USD/RUB'] / df['Курс JPY/RUB']

# Сохранение обновленных данных в файл
df.to_excel('currency_data.xlsx', index=False)

"""
### Шаг 5. Настройки отображения Excel-файла
"""
# Загрузка файла
file_name = "currency_data.xlsx"
workbook = load_workbook(file_name)

# Получение активного листа
sheet = workbook.active

# Выравнивание по автоширине
for column_cells in sheet.columns:
    max_length = 0
    for cell in column_cells:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        except:
            pass
    adjusted_width = (max_length + 2) * 1.2
    sheet.column_dimensions[cell.column_letter].width = adjusted_width

# Применение формата чисел "Финансовый"
financial_style = NamedStyle(name='financial', number_format='#,##0.00')
for column in sheet.columns:
    for cell in column:
        if isinstance(cell.value, (int, float)):
            cell.style = financial_style

# Сохранение изменений в файл
workbook.save(file_name)
print('Файл Excel приведен в заданный вид')

"""
### Шаг 6. Формирование письма
"""
# Получение почты и пароля для отправки из переменной среды
email_login = os.getenv('email')
password = os.getenv('password')

# Формирование текста письма
email_text = create_email_text(df.shape[0])

# Создание сообщения
msg = MIMEMultipart()
msg['From'] = email_login
msg['To'] = email_login
msg['Subject'] = 'Отчет'

# Добавление текста письма
msg.attach(MIMEText(email_text, 'plain'))

# Добавление файла вложения
with open('currency_data.xlsx', 'rb') as file:
    attachment = MIMEApplication(file.read(), Name='currency_data.xlsx')
    attachment['Content-Disposition'] = f'attachment; filename={"currency_data.xlsx"}'
    msg.attach(attachment)

# Отправка письма
with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as server:
    server.login(email_login, password)
    server.send_message(msg)

print('Письмо отправлено на указанную в переменной среды почту')
print('Задание выполнено успешно')
