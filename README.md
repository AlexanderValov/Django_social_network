# Django_social_network
Приложение, которое даёт пользователям возможность делиться фотографиями и картинками, которые они нашли в интернете.

На сайте реализован следющий функционал:

1. Система авторизации, также через VK; 
----------
2. Система регистрации;
----------
3. Система смены пароля, сброса пароля через e-mail (При регистрации указывается e-mail, при сбросе указывается тот же e-mail, если совпадают, то на него придёт сообщение с ссылкой на восстановление пароля);
----------
4. Личный кабинет, возможность изменения данных ЛК, возможность привязывать картинку к профилю, если картинки нет, будет стоять стандартная (пока не во всех вкладках);
----------
5. Создан JavaScript-букмарклет для доступа через сайт к содержимому других сайтов (возможность сохранять картинки с других сайтов на этом);
----------
6. Реализаваны AJAX-запросы с jQuery;
----------
7. Постраничный вывод с помощью AJAX и Paginator;
----------
8. Создан собственный декоратор для проверки типа запроса (@ajax_required);
----------
9. Создано отношений «многие ко многим»;
----------
10. Реализована возможность ставить like к опубликованным картинкам;
----------
11. Защита от межсайтовых запросов в AJAX;
----------
12. Создано превью изображений с помощью sorl-thumbnail;
----------
13. Добавлена возможность смотреть всех зарегистрированных (активных) пользвателей;
----------
14. По умолчанию всем пользователям присваивается стандартная картинка профиля, если они не выберут другую, будет отображаться она;
----------
15. Добавлена кнопка FOLLOW и UNFOLLOW у пользователей для возможности подписываться на новости (новостная лента ещё не доработана);
----------
16. Добавлена активность в новостную ленту, построничный вывод новостей (по 5 шт (пока без AJAX)), что входит в активность: 

  - пользователь добавил картинку в закладки;
  - пользователь лайкнул изображение;
  - пользователь создал аккаунт;
  - пользователь подписался на обновления;
  
----------
17. Возможность переходить из превью картинки в профиль пользователей, которые поставили лайк;
----------
18. Устранение дублирования новостей в ленте;
----------
19. Убрана ссылка на подписку в профиле авторизованного пользователя;
----------
20. Оптимизированы запросы дя связанных объектов с использованием select_related() и prefetch_related();
----------
21. Добавлен счётчик просмотров изображений с помощью Redis;
----------
22. Добавлена возможность сортировки по title, date, total likes (Не доработан);
----------
P.S. В файле requirements.txt очень много ненужных приложений, пока нет желания чистить. 
P.S.S. В коде много комментариев, это сделано специально для лучшего усвоения материала. Сайт реализован по книге Меле Антонио "Django 2 в примерах"
