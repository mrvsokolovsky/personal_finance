# Скрипт для учета покупок

Основная идея программы заключается в том, чтобы считать qr-код с чека через камеру вашего устройства. 
На этом qr-коде закодирована налоговая информация, которая передается операторам фискальных данных (ОФД).
Эти данные с помощью модуля Selenium передаются на сайт проверки чеков, который, в свою очередь, получив данные ОФД может вернуть данные о покупках, содержащихся в загруженном фискальном чеке.
Эти данные затем парсятся с помощью того же Selenium и добавляются в заранее созданную базу данных. В данный момент всё работает из консоли, в будущем планируется создать пользовательский интерфейс (скорее всего, в вебе).

P.S. Код будет дорабатываться, поэтому буду рад предложениям и pull-request'ам.
