# Руководство пользователя приложения

Приветствуем тебя, пользователь нашего приложения для взаимодействия с такси
`"Довезем, если повезет"`!

##  Архитектура проекта

В нашем проекте содержатся только классы, отвечающие за бизнес-логику,
вот список базовых файлов:

+ `Car` (автомобиль и информация о нем)
+ `User` и его потомки `Driver` и `Passenger` (общий пользователь, водитель и пассажир)
+ `Offer` (предложение поездки, которое поступает от пассажира)
+ `Trip` (сама поездка, основной класс программы)
+ `Report` (отзыв о водителе, который может оставить пассажир, или наоборот)
+ `Payment` (оплата поездки, реализован паттерн `Цепочка ответственности` чтобы устроить 
нужный пассажиру порядок попыток оплаты поездки)
+ `Map` (содержит логику работы с картой, рассчет пути между двумя точками, реализован 
алгоритм Дийкстры для поиска кратчайшего пути с учетом препятствий и пробок)

Немного про вспомогательные, но важные классы:

+ `Manager` (инкапсулирует статические методы для работы со списком 
(добавление, удаление поиск))
+ `OfferManager` (занимается обработкой всего, что связано с созданием, удалением, 
поиском офферов, реализован паттерн `Строитель` для создание оффера и `Наблюдатель` 
для рассылки офферов водителям)
+ `TripManager` (занимается обработкой жизненного цикла поездки,
реализован паттерн `Состояние` для перехода между состояниями 
Ожидание -> Поездка -> Оплата -> Окончание)

## Цикл работы такси

1. Пассажир создает оффер 
2. Он рассылается доступным водителям
3. Один из водителей соглашается на этот оффер
4. Создается поездка
5. Происходит переход поездки между состояниями Ожидание -> Поездка -> Оплата -> Окончание
6. Пассажир осуществляет оплату удобным ему способом (иначе получает репорт от водителя)
7. Заканчивается поездка, цикл окончен

<img src="./taxi.svg" alt="UML-diagram">