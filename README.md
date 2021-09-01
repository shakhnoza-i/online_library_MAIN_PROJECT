Онлайн библиотеки c базой книг, где по каждой книге можно оставлять отзыв. ОнлайнБиблиотека предоставляет различный уровень доступа(разрешений) для разных типов пользователей (администратор, авторизованный пользователь, неавторизованный пользователь)


Стек:
Python 
Django
Django Rest Framework
Django-Filter


Общий функционал проекта:

- Registration, Login, Logout - через Токен авторизацию
- ОнлайнБиблиотека может содержать множество книг.
- Одна книга может находиться только в Одной определенной ОнлайнБиблиотеке.
- У одной книги может быть множество отзывов.
- Отзывы могут оставлять только зарегистрированные пользователи.
- Один пользователь может оставлять только один отзыв на одну книгу.
- Только сам пользователь (или администратор) может редактировать или удалять свой отзыв. Остальные пользователи могут только читать.
- Из общего списка ОнлайнБиблиотек доступны ссылки на книги, которые содержаться в ОнлайнБиблиотеке.
- Для списка книг поддерживается нумерация. По умолчанию 10 книг на страницу. Также пользователь может задать этот параметр самостоятельно. Максимум 20 книг на страницу.
- Поддерживается поиск и фильтрация по названию книги, рейтингу и описанию.
- Unit-testing основных модулей
