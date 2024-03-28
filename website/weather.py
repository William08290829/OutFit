import datetime as dt
from datetime import datetime, date, timedelta, time
# pip install requests
import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mticker
import numpy as np
from scipy.interpolate import make_interp_spline
from .format_date import format_date, get_date_by_code

# COLOR
bg_color_matlab_style = "#1a191c"
font_color_matlab_style = '#7B7980'
green_matlab_style = '#a0c99c'

load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class WeatherDataList:
    timestamp: datetime
    main: str
    description: str
    temperature: float
    # icon: str
    pop: int

@dataclass
class ForecastWeatherData:
    date: str
    weekday: str
    max_temperature: int
    min_temperature: int
    pop: int
    
@dataclass
class CurrentWeatherData:
    city: str
    date: str
    weekday: str
    main: str
    description: str
    temperature: int
    max_temperature: int
    min_temperature: int
    icon: str
    
@dataclass
class ForecastDateKeyPoint:
    city: str
    temp: int
    icon: str
    date: str
    weekday: str
    

CITY = "台北市"
DATE = date.today() + timedelta(days=1)

def get_city_coordinates(city_name):
    city_coordinates_url = "http://api.opencube.tw/twzipcode"
    response = requests.get(city_coordinates_url).json()
    
    for data in response.get("data", []):
        if data.get("city") == city_name:
            return data.get("lat"), data.get("lng")
    
    return None


def get_lat_lon_current_weather(lat, lon, API_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric&appid={API_key}&lang=zh_TW"
    response = requests.get(url).json()
    
    original_description = response.get('weather', [{}])[0].get('description', '')
    modified_description = original_description.replace("，", ", ")
    
    formatted_date, weekday = format_date(date.today())
    
    current_weather = CurrentWeatherData(
        city="現在位置",
        date=formatted_date,
        weekday=weekday,
        main=response.get('weather', [{}])[0].get('main', ''),
        description=modified_description,
        max_temperature=round(response.get('main', {}).get('temp_max', '')),
        min_temperature=round(response.get('main', {}).get('temp_min', '')),
        temperature=round(response.get('main', {}).get('temp', '')),
        icon=response.get('weather', [{}])[0].get('icon', ''),
    )
    
    return current_weather


def get_city_current_weather(city, API_key):
    lat, lon = get_city_coordinates(city)
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric&appid={API_key}&lang=zh_TW"
    response = requests.get(url).json()
    
    original_description = response.get('weather', [{}])[0].get('description', '')
    modified_description = original_description.replace("，", ", ")
    
    formatted_date, weekday = format_date(date.today())
    
    current_weather = CurrentWeatherData(
        city=city,
        date=formatted_date,
        weekday=weekday,
        main=response.get('weather', [{}])[0].get('main', ''),
        description=modified_description,
        max_temperature=round(response.get('main', {}).get('temp_max', '')),
        min_temperature=round(response.get('main', {}).get('temp_min', '')),
        temperature=round(response.get('main', {}).get('temp', '')),
        icon=response.get('weather', [{}])[0].get('icon', ''),
    )
    
    return current_weather



def get_lat_lon_current_forecast_weather(lat, lon, API_key):
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric&appid={API_key}"
    response = requests.get(forecast_url).json()
    # print(response)
    
    count = 0
    # current_forecast_data_list = []
    timestamp_list= []
    temp_list= []
    resp_forecast_list = response.get('list', [])
    
    for forecast in resp_forecast_list:
        dt_txt_str = forecast.get("dt_txt", "")
        dt_obj = datetime.strptime(dt_txt_str, "%Y-%m-%d %H:%M:%S")
        date_part = dt_obj.date()
        time_part = dt_obj.strftime("%H:%M")
        
        #比較日期
        # if date_part == date.today() : # or (date_part == DATE + timedelta(days=1) and time_part == "00:00")
        if count < 8:
            timestamp = dt_obj.strftime("%H:%M")
            main_data = forecast.get('main', {})
            temperature = main_data.get('temp')
            
            timestamp_list.append(timestamp)
            temp_list.append(temperature)            

            # timestamp_weather_data = WeatherDataList(
            #     timestamp=timestamp,
            #     main=None,
            #     description=None,
            #     temperature=temperature,
            #     # icon=None,
            #     pop=None
            # )

            # current_forecast_data_list.append(timestamp_weather_data)
            count+=1
        else:
            break
            
    # print(forecast_url)
    return timestamp_list, temp_list
          

def get_city_current_forecast_weather(city, API_key):
    lat, lon = get_city_coordinates(city)
    timestamp_labels, temp_value = get_lat_lon_current_forecast_weather(lat, lon, API_key)
    
    return timestamp_labels, temp_value


# FORECAST

def get_lat_lon_forecast_weather(lat, lon, API_key, date_code):
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric&appid={API_key}"
    response = requests.get(forecast_url).json()
    # print(response)
    
    decoded_date = get_date_by_code(date_code)
    formatted_date, weekday = format_date(decoded_date)
    # forecast_data_graph_list = []
    timestamp_list= []
    temp_list= []
    average_temp_list = []
    max_temp_list = []
    min_temp_list = []
    pop_list = []
    resp_forecast_list = response.get('list', [])
    
    for forecast in resp_forecast_list:
        dt_txt_str = forecast.get("dt_txt", "")
        dt_obj = datetime.strptime(dt_txt_str, "%Y-%m-%d %H:%M:%S")
        date_part = dt_obj.date()
        time_part = dt_obj.strftime("%H:%M")
        
        # 比較日期
        if date_part == decoded_date : # or (date_part == DATE + timedelta(days=1) and time_part == "00:00")
            timestamp = dt_obj.strftime("%H:%M")
            main_data = forecast.get('main', {})
            temperature = main_data.get('temp')
            weather_main = forecast.get('weather', [{}])[0].get('main')
            description = forecast.get('weather', [{}])[0].get('description')
            # icon = forecast.get('weather', [{}])[0].get('icon')
            pop = int(forecast.get('pop', '') * 100)
            
            average_temp_list.append(temperature)
            pop_list.append(pop)
            max_temp_list.append(main_data.get('temp_max', ''))
            min_temp_list.append(main_data.get('temp_min', ''))
            
            timestamp_list.append(timestamp)
            temp_list.append(temperature) 
            
            
            # timestamp_weather_data = WeatherDataList(
            #     timestamp=timestamp,
            #     main=weather_main,
            #     description=description,
            #     temperature=temperature,
            #     # icon=icon,
            #     pop=pop
            # )

            # forecast_data_graph_list.append(timestamp_weather_data)
        
            
    
    forecast_data = ForecastWeatherData(
        date=formatted_date,
        weekday=weekday,
        max_temperature=round(max(max_temp_list)),
        min_temperature=round(min(min_temp_list)),
        pop=int(max(pop_list))
    )
    
    return forecast_data, timestamp_list, temp_list
    
    # if request.method == "POST":
    #     pass
    # else:
    #     return render()


def get_city_forecast_weather(city, API_key, date_code):
    lat, lon = get_city_coordinates(city)
    city_forecast_data, timestamp_list, temp_list = get_lat_lon_forecast_weather(lat, lon, API_key, date_code)
    
    return city_forecast_data, timestamp_list, temp_list



def get_lat_lon_forecast_keypoint(lat, lon,  API_key):
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric&appid={API_key}"
    response = requests.get(forecast_url).json()
    resp_forecast_list = response.get('list', [])
    
    location_forecast_keypoint_list = []
    count = 0
    
    for forecast in resp_forecast_list:
        dt_txt_str = forecast.get("dt_txt", "")
        dt_obj = datetime.strptime(dt_txt_str, "%Y-%m-%d %H:%M:%S")
        date_part = dt_obj.date()
        
        time_part = dt_obj.strftime("%H:%M")
        if (date_part != date.today()) and (time_part == "09:00") and (count < 4):
            d, weekday = format_date(date_part)
            main_data = forecast.get('main', {})
            temperature = round(main_data.get('temp'))
            icon = forecast.get('weather', [{}])[0].get('icon')
            
            formatted_date, weekday = format_date(date_part)
        
            timestamp_weather_data = ForecastDateKeyPoint(
                city="現在位置",
                temp=temperature,
                icon=icon,
                date=formatted_date,
                weekday=weekday
            )
            location_forecast_keypoint_list.append(timestamp_weather_data) 
            count += 1
    
    return location_forecast_keypoint_list



def get_city_forecast_keypoint(city, API_key):
    lat, lon = get_city_coordinates(city)
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric&appid={API_key}"
    response = requests.get(forecast_url).json()
    resp_forecast_list = response.get('list', [])
    
    city_forecast_keypoint_list = []
    count = 0
    
    for forecast in resp_forecast_list:
        dt_txt_str = forecast.get("dt_txt", "")
        dt_obj = datetime.strptime(dt_txt_str, "%Y-%m-%d %H:%M:%S")
        date_part = dt_obj.date()
        
        time_part = dt_obj.strftime("%H:%M")
        if (date_part != date.today()) and (time_part == "09:00") and (count < 4):
            d, weekday = format_date(date_part)
            main_data = forecast.get('main', {})
            temperature = round(main_data.get('temp'))
            icon = forecast.get('weather', [{}])[0].get('icon')
            
            formatted_date, weekday = format_date(date_part)
        
            timestamp_weather_data = ForecastDateKeyPoint(
                city=city,
                temp=temperature,
                icon=icon,
                date=formatted_date,
                weekday=weekday
            )
            city_forecast_keypoint_list.append(timestamp_weather_data) 
            count += 1
    
    return city_forecast_keypoint_list
            
        
    


def default_get_weather():
    lat, lon = get_city_coordinates(CITY)
    current_weather_data = get_city_current_weather(CITY, api_key)
    # forecast_data_list, forecast_max_temperature, forecast_min_temperature, forecast_average_pop = get_lat_lon_forecast_weather(lat, lon, api_key, DATE)
    return current_weather_data





if __name__ == "__main__":
    lat, lon = get_city_coordinates(CITY)
    current_weather_data = get_city_current_weather(CITY, api_key)
    current_forecast_weather_list = get_lat_lon_current_forecast_weather(lat, lon, api_key)
    forecast_data_list, forecast_max_temperature, forecast_min_temperature, forecast_average_pop = get_lat_lon_forecast_weather(lat, lon, api_key, DATE)    
    
    print("=" * 20)
    print(f"Date: {DATE}")
    print(f"CITY: {CITY}")
    print(f"高/低: {forecast_max_temperature}°/ {forecast_min_temperature}°")
    print(f"降雨機率: {forecast_average_pop}%")
    print("=" * 20)
    
    for forecast_data in forecast_data_list:
        print(f"Timestamp: {forecast_data.timestamp}")
        print(f"Weather Main: {forecast_data.main}")
        print(f"Weather Description: {forecast_data.description}")
        print(f"Temperature: {forecast_data.temperature}°C")
        print(f"POP: {forecast_data.pop}%") 
        # print(f"Icon: {forecast_data.icon}")
        print("-" * 20)
        
    
    # 現在天氣
    print("現在天氣: ")
    print(f"Timestamp: {current_weather_data.date}")
    print(f"Weather Main: {current_weather_data.main}")
    print(f"Weather Description: {current_weather_data.description}")
    print(f"Temperature: {current_weather_data.temperature}°C")
    # print(f"Icon: {current_weather_data.icon}")
    print("-" * 20)
    
    
    
    # for forecast_data in current_forecast_weather_list:
    #     print(f"Timestamp: {forecast_data.timestamp}")
    #     print(f"Temperature: {forecast_data.temperature}°C")
    #     print("-" * 20)
        
    city_forecast_keypoint_list = get_city_forecast_keypoint(CITY, api_key)
    print("-" * 20)
    print("-" * 20)
    print("-" * 20)
    for forecast_data in city_forecast_keypoint_list:
        print(f"T: {forecast_data.temp}°C")
        print(f"icon: {forecast_data.icon}")
        print(f"Date: {forecast_data.date}")
        print("-" * 20)
    
    
    
    
    
    # # 繪圖
    # fig, ax = plt.subplots(facecolor=bg_color_matlab_style)
    # ax.set_facecolor(bg_color_matlab_style)
    # timestamps = np.array([forecast_data.timestamp for forecast_data in forecast_data_list])
    # temperatures = np.array([forecast_data.temperature for forecast_data in forecast_data_list])
    
    # # 樣式
    # plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    
    # # 設置座標軸顏色
    # ax.spines['bottom'].set_color(font_color_matlab_style)
    # ax.spines['top'].set_color(bg_color_matlab_style)
    # ax.spines['right'].set_color(bg_color_matlab_style)
    # ax.spines['left'].set_color(font_color_matlab_style)
    
    # ax.tick_params(axis='x', colors=font_color_matlab_style, labelsize=16)
    # ax.tick_params(axis='y', colors=font_color_matlab_style, labelsize=16)
    
    
    
    # plt.figure(facecolor=bg_color_matlab_style)
    
    # plt.gca().set_facecolor(bg_color_matlab_style)
    # plt.xticks()
    # plt.axes().set_facecolor = 
    
    # matplotlib.rcParams['axes.facecolor'] = bg_color_matlab_style  # 圖表背景色
    # matplotlib.rcParams['figure.facecolor'] = bg_color_matlab_style  # 圖片背景色
    # matplotlib.rcParams['axes.edgecolor'] = font_color_matlab_style  # 邊框顏色
    # matplotlib.rcParams['xtick.color'] = font_color_matlab_style  # x軸刻度顏色
    # matplotlib.rcParams['ytick.color'] = font_color_matlab_style  # y軸刻度顏色
    # matplotlib.rcParams['text.color'] = font_color_matlab_style  # 文本顏色
    # matplotlib.rc('lines', linewidth=4, color='g')
    
    
    
    # 將折線圖換成曲線圖
    # curve_timestamp = np.linspace(1, len(timestamps), len(timestamps))
    # curve_model = make_interp_spline(curve_timestamp, temperatures)
    
    # curve_more_timestamp = np.linspace(1, len(timestamps), 500)
    # curve_temperature = curve_model(curve_more_timestamp)
    
    # matplotlib.rc('font', family='Microsoft JhengHei')
    # plt.plot(curve_more_timestamp, curve_temperature, linestyle='-', linewidth=2.5, color=green_matlab_style)
    
    
    # 這裡
    # ax.plot(timestamps, temperatures, marker = "o", linestyle='-', linewidth=2.5, color=green_matlab_style)
    # plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f°'))
    
    
    
    
    # ax.set_xlabel('', color=font_color_matlab_style)
    # ax.set_ylabel('', color=font_color_matlab_style)
    # # plt.title('Temperature Forecast')
    # plt.xticks(curve_timestamp, timestamps)
    
    # 這裡
    # plt.tight_layout()
    # plt.show()
           
    


# url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY + "&units=metric"

# response = requests.get(url).json()
# # print(response)

# temp_celsius = response['main']['temp']
# temp_max = response['main']['temp_max']
# temp_min = response['main']['temp_min']

# feels_like_celsius = response['main']['feels_like']

# wind_speed = response['wind']['speed']

# humidity = response['main']['humidity']

# description = response['weather'][0]['description']

# sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
# sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

# print(f'Temperature in {CITY}: {temp_min:.2f} ~ {temp_max}°C')
# print(f'Temperature in {CITY}: feels like {feels_like_celsius:.2f}°C')
# print(f'Humidity in {CITY}: {humidity}%')
# print(f'Wind Speed in {CITY}: {wind_speed}m/s')
# print(f'Sin rises in {CITY} at : {sunrise_time}')
# print(f'Sin sets in {CITY} at : {sunset_time}')

# clothes_temp = 26 - temp_celsius
# clothes_temp_max = 26 - temp_max
# clothes_temp_min = 26 - temp_min

# if clothes_temp < 1:
#     print("衣服推薦: 短袖短褲")
# elif 1 <= clothes_temp <= 6:
#     print("衣服推薦: 襯衫 + 長褲")
# elif 5 <= clothes_temp <= 14:
#     print("衣服推薦: 帽T + 長褲 + 外套")
# elif 14 <= clothes_temp <= 21:
#     print("衣服推薦: 厚長袖or厚帽T + 厚外套")
    