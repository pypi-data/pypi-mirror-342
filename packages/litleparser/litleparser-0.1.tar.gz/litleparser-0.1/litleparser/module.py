from requests import get, RequestException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep

class Pars:
    '''Модуль для парсинга статических и динамических страниц'''

    def __init__(self, url, pathToSaveFile, writeMethod='w'):
        """Конструктор"""
        self.url = url
        self.pathToSaveFile = pathToSaveFile
        self.writeMethod = writeMethod

    def get_static_page(self):
        '''Получаем статическую страницу'''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }
        try:
            # Отправляем запрос
            req = get(self.url, headers=headers)
            req.raise_for_status()  # Проверка на ошибки HTTP

            # Записываем данные
            if self.writeMethod == 'w':
                src = req.text
                with open(self.pathToSaveFile, self.writeMethod, encoding='utf-8') as file:
                    file.write(src)
            elif self.writeMethod == 'wb':
                src = req.content
                with open(self.pathToSaveFile, self.writeMethod) as file:
                    file.write(src)
            else:
                raise ValueError("Неподдерживаемый метод записи: {}".format(self.writeMethod))

        # Обрабатываем ошибки
        except RequestException as e:
            print(f"Ошибка при запросе: {e}")
        except IOError as e:
            print(f"Ошибка при записи в файл: {e}")
        except Exception as e:
            print('Ошибка:')
            print(e)


    def get_dinamic_page(self, closeWindow:bool=1):
        '''Функция для получения динамической страницы'''


        # Устанавливаем опции для Chrome WebDriver
        options = Options()
        if closeWindow:
            options.add_argument('--headless')
        # открываем браузер
        with webdriver.Chrome(options=options) as driver:
            driver.get(self.url)
            # Прокручиваем страницу до самого низа
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                # Прокручиваем до низа страницы
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Ждем загрузки страницы
                sleep(2)
                # Вычисляем новую высоту страницы
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            # Получаем HTML-код страницы
            html_content = driver.page_source
            # Сохраняем HTML-код в файл
            with open(self.pathToSaveFile, "w", encoding="utf-8") as file:
                file.write(html_content)