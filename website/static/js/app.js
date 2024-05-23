// 'use strict';
// /**
//  * 
//  * @param {NodeList} elements 
//  * @param {string} eventType 
//  * @param {*} callback 
//  */

const fetchData = function (input, callback) {
    // 检查城市是否在允许的城市列表中
    const taiwanCities = [
        '台北市', '新北市', '桃園市', '台中市', '台南市', '高雄市',
        '基隆市', '新竹市', '嘉義市',
        '新竹縣', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣',
        '屏東縣', '宜蘭縣', '花蓮縣', '台東縣', '澎湖縣',
        '金門縣', '連江縣'
    ];
    
    // if (taiwanCities.includes(city)) {
    //     // 如果城市在列表中，直接将城市传递给回调函数
    //     callback(city);
    // } else {
    //     // 如果城市不在列表中，可以选择执行一些其他操作或者什么都不做
    //     // console.error(`City '${city}' is not allowed.`);
    // }

    let result = [];
    if (input.length) {
        const regex = new RegExp(input.split('').join('.*')); // 將輸入的字串轉換成正規表達式
        result = taiwanCities.filter(city => regex.test(city));
        
        // callback all results
        callback(result);
    }
}

const addEventOnElements = function (elements, eventType, callback) {
    for (const element of elements) element.addEventListener(eventType, callback);
}

const searchView = document.querySelector("[data-search-view]");
const searchTogglers = document.querySelectorAll("[data-search-toggler]");

const toggleSearch = () => searchView.classList.toggle("active");
addEventOnElements(searchTogglers, "click", toggleSearch);


// SEARCH INTEGRATION
const searchField = document.querySelector("[data-search-field]");
const searchResult = document.querySelector("[data-search-result]");

let searchTimeout = null;
const searchTimeoutDuration = 500;

searchField.addEventListener("input", function() {
    searchTimeout ?? clearTimeout(searchTimeout);

    if (!searchField.value) {
        searchResult.classList.remove("active");
        searchResult.innerHTML = "";
        searchField.classList.remove("searching");
    } else {
        searchField.classList.add("searching");
    }


    if(searchField.value) {
        searchTimeout = setTimeout(() => {
            fetchData(searchField.value, function (cities) {
                searchField.classList.remove("searching");
                searchResult.classList.add("active");

                searchResult.innerHTML =`
                    <ul class="view-list" data-search-list></ul>
                `;
                const searchList = searchResult.querySelector("[data-search-list]");

                if (cities.length === 0) {

                    const searchItem = document.createElement("li");
                    searchItem.classList.add("view-item");
                    searchItem.classList.add("noResultItem");
                    searchItem.innerHTML = `
                            <div>
                                <p class="item-title noResult">查無結果</p>
                            </div>
                    `;
                    searchList.appendChild(searchItem);

                } else {

                    cities.forEach(city => {
                        const searchItem = document.createElement("li");
                        searchItem.classList.add("view-item");
                        searchItem.innerHTML = `
                            <span class="m-icon">location_on</span>
                            <div>
                                <p class="item-title">${city}</p>
                                <p class="label-2 item-subtitle">台灣</p>
                            </div>
                            <a href="/weather?&city=${encodeURIComponent(city)}&date=d0" class="item-link has-state" data-search-toggler></a>
                        `;
                        searchList.appendChild(searchItem);
                    });
                }
            });
        }, searchTimeoutDuration);
    }

});


const getLocation = () => {
    // const btn = document.querySelector("[data-current-location-btn]");

    const success = (position) => {
        const { latitude, longitude } = position.coords;
        console.log(latitude, longitude);

        // change url to /location-weather?lat=xxx&lon=xxx&date=d0
        window.location.href = `/location-weather?lat=${latitude}&lon=${longitude}&date=d0`;
    }

    const error = () => { 
        console.error("Unable to retrieve your location");
    }

    navigator.geolocation.getCurrentPosition(success, error);



    // if (navigator.geolocation) {
    //     navigator.geolocation.getCurrentPosition(showPosition);
    // } else {
    //     console.error("Geolocation is not supported by this browser.");
    // }
}

document.querySelector("[data-current-location-btn]").addEventListener("click", getLocation);


// PRELOADER

window.addEventListener('load', () => {
    document.getElementById('preloader__container').classList.add("preloader__container--hidden");
    document.getElementById('preloader__container').addEventListener('transitionend', () => {
        document.body.removeChild(document.getElementById('preloader__container'));
    });
});