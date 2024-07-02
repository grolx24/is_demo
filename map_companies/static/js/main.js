document.addEventListener('DOMContentLoaded', function () {
    // Инициализация карты
    ymaps.ready(init);
    function init() {
        let myMap = new ymaps.Map("map", {
            center: [60, 30.3], // Координаты  спб
            zoom: 10
        });

        let clusterer = new ymaps.Clusterer({
            clusterDisableClickZoom: true,
            clusterOpenBalloonOnClick: true,
            clusterBalloonContentLayout: 'cluster#balloonCarousel',
            clusterBalloonPanelMaxMapArea: 0,
            clusterBalloonContentLayoutWidth: 300,
            clusterBalloonContentLayoutHeight: 'auto',
            clusterBalloonPagerSize: 5
        });

        fetch('companies/')
            .then(response => response.json())
            .then(companies => {
                let geoObjectsPromises = companies.map(company => {
                    return ymaps.geocode(company.address).then(res => {
                        return new ymaps.Placemark(res.geoObjects.get(0).geometry.getCoordinates(), {
                            balloonContentHeader: `<strong>${company.name}</strong>`,
                            balloonContentBody: company.address,
                            clusterCaption: company.name
                        });
                    });
                });
                // Добавление меток на карту
                Promise.all(geoObjectsPromises).then(geoObjects => {
                    clusterer.add(geoObjects);
                    myMap.geoObjects.add(clusterer);
                });
            })
            .catch(error => console.error('Error fetching companies:', error));
    }
});