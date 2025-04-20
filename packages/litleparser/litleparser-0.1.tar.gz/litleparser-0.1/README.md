# Библиотека для парсинга

Библиотека позволяет сохранять на комп html-страницы. 

Установить библиотеку:
```bash
pip install im-parsing
```

## Пример кода
```python
from imPars import Pars
p = Pars('https://google.com', './index.html')
p.get_static_page()
```

## Коротко о методах
Функция **get_static_page** принимает url страницы и сохраняет html по указанному пути. 

Функция **get_dinamic_page** с помощью библиотеки Selenium получает динамически обновляемую страницу. Это помогает когда контент на странице подгружается динамически

Обе функции сохраняют страницы по указанному пути, чтобы не долбить сайт запросами, а один раз сделать запрос, а потом уже работать с сохранёнкой

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
