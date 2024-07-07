document.addEventListener('DOMContentLoaded', function () {
    // Инициализация карты
    ymaps.ready(init);

    function init() {
        let myMap = new ymaps.Map("map", {
            center: [60, 30.3], // Координаты спб
            zoom: 10
        });

        // Координаты углов квадрата
        const topLeft = [60.3, 29.7];
        const bottomRight = [59.5, 30.99];
        const startPoint = [59.83, 30.4]; // 60.052110, 30.423710

        // Количество точек (30 x 30 = 900)
        const numPoints = 40;
        const latStep = (topLeft[0] - bottomRight[0]) / (numPoints);
        const lonStep = (bottomRight[1] - topLeft[1]) / (numPoints);

        // Создаем коллекцию геообъектов
        let geoObjects = new ymaps.GeoObjectCollection();

        // Генерация точек внутри квадрата
        for (let i = 0; i < numPoints; i++) {
            for (let j = 0; j < numPoints; j++) {
                const lat = bottomRight[0] + i * latStep;
                const lon = topLeft[1] + j * lonStep;
                const point = [lat, lon];

                // Построение маршрута и вывод времени в пути в консоль
                let multiRoute = new ymaps.multiRouter.MultiRoute({
                    referencePoints: [point, startPoint],
                    params: { routingMode: 'masstransit' } // Использование общественного транспорта
                }, {
                    // Опции маршрута
                    wayPointStartIconColor: "blue",
                    wayPointFinishIconColor: "red",
                    routeStrokeColor: "0000ffff"
                });

                multiRoute.model.events.add('requestsuccess', function() {
                    // Получаем маршруты
                    let routes = multiRoute.getRoutes();
                    if (routes.getLength() > 0) {
                        let route = routes.get(0);
                        let routeTimeText = route.properties.get('duration').text;

                        let routeTimeParts = routeTimeText.split(/\s+/);
                        let routeTimeMinutes = 0;

                        // Обработка времени маршрута
                        if (routeTimeParts.includes("ч")) {
                            let hoursIndex = routeTimeParts.indexOf("ч") - 1;
                            let hours = parseInt(routeTimeParts[hoursIndex]);
                            let minutesIndex = routeTimeParts.indexOf("мин") - 1;
                            let minutes = parseInt(routeTimeParts[minutesIndex]);
                            routeTimeMinutes = hours * 60 + minutes;
                        } else {
                            routeTimeMinutes = parseInt(routeTimeParts[routeTimeParts.length - 2]);
                        }

                        console.log(`${lat}, ${lon}:`, routeTimeMinutes);

                        // Определяем цвет метки в зависимости от времени маршрута
                        let color = "blue"; // значение по умолчанию
                        if (routeTimeMinutes < 30) {
                            color = "green";
                        } else if (routeTimeMinutes < 45) {
                            color = "yellow";
                        } else if (routeTimeMinutes < 60) {
                            color = "red";
                        } else if (routeTimeMinutes < 75) {
                            color = "black";
                        }

                        // Если время в пути меньше 75 минут, добавляем метку
                        if (routeTimeMinutes < 75) {
                            let placemark = new ymaps.Placemark(point, {
                                balloonContent: `${point}: ${routeTimeText}`
                            }, {
                                preset: `islands#${color}DotIcon` // используем цветную метку
                            });
                            geoObjects.add(placemark);
                        }
                    }
                });
            }
        }
        // Добавляем все созданные геообъекты на карту
        myMap.geoObjects.add(geoObjects);
    }
});
