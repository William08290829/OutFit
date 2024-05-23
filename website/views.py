from flask import Blueprint, render_template, send_from_directory, request, jsonify, abort
from .weather import *
from .ootd import get_ootd
from .format_date import get_date_num_by_code
# from .weather import get_city_coordinates, default_get_weather, get_city_current_weather, get_city_forecast_weather
from dotenv import load_dotenv
import os
from datetime import datetime, date, timedelta
 
views = Blueprint('views', __name__)

load_dotenv()
API_KEY = os.getenv('API_KEY')


outfit_image_url = None

# DEFAULT
@views.route('/')
def home():
    outfit_image_url = None
    default_weather_data = default_get_weather()
    forecast_keypoint_data = get_city_forecast_keypoint("台北市", API_KEY)
    # print(int(default_weather_data.temperature))
    
    timestamp_labels, temp_values = get_city_current_forecast_weather("台北市", API_KEY)
    
    
    # if outfit_image_url != []:
    #     print(outfit_image_url)
    
    return render_template(
        "home.html", 
        default_weather_data=default_weather_data,
        forecast_keypoint_data=forecast_keypoint_data,
        timestamp_labels=timestamp_labels,
        temp_values=temp_values,
        outfit_image_url=outfit_image_url
        )

# asyncio.create_task(load_outfit_image(default_weather_data.temperature))

# async def load_outfit_image(temperature):
#     global outfit_image_url
#     outfit_image_url = get_ootd(temperature)


@views.route('/get_outfit_image_urls_default')  # 這個路由是給前端呼叫的
def get_outfit_image_urls_default():
    default_weather_data = default_get_weather()
    outfit_image_url = get_ootd(default_weather_data.temperature, default_weather_data.max_temperature, default_weather_data.min_temperature)
    return jsonify({'outfit_image_url': outfit_image_url})


# ========================================================================================================


@views.route('/static/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename, mimetype='application/javascript')


# ========================================================================================================


# CITY
@views.route('/weather')
def weather():
    outfit_image_url = None
    city = request.args.get('city', '')
    selected_date = request.args.get('date', '')
    forecast_keypoint_data = get_city_forecast_keypoint(city, API_KEY)
    
    if city:
        
        current_city_weather_data =  get_city_current_weather(city, API_KEY)
        
        if selected_date == "d0":
            # outfit_image_url = get_ootd(current_city_weather_data.temperature)
            timestamp_labels, temp_values = get_city_current_forecast_weather(city, API_KEY)
            return render_template(
                "city.html",
                current_city_weather_data=current_city_weather_data,
                forecast_keypoint_data=forecast_keypoint_data,
                timestamp_labels=timestamp_labels,
                temp_values=temp_values,
                outfit_image_url=outfit_image_url
            )
            
        elif selected_date == "d1" or selected_date == "d2" or selected_date == "d3" or selected_date == "d4":
            date_num = get_date_num_by_code(selected_date) - 1
            # outfit_image_url = get_ootd(forecast_keypoint_data[date_num].temp)
            
            city_forecast_data, timestamp_labels, temp_values = get_city_forecast_weather(city, API_KEY, selected_date)
            return render_template(
                "city.html",
                current_city_weather_data=current_city_weather_data,
                forecast_keypoint_data=forecast_keypoint_data,
                city_forecast_data=city_forecast_data,
                timestamp_labels=timestamp_labels,
                temp_values=temp_values,
                outfit_image_url=outfit_image_url    
            )
    
    abort(404)
    # print(f"Received input value: {city}") 
    return f"Received input value: {city}"


@views.route('/get_outfit_image_urls_city')
def get_outfit_image_urls_city():
    city = request.args.get('city', '')
    selected_date = request.args.get('date', '')
    forecast_keypoint_data = get_city_forecast_keypoint(city, API_KEY)
    
    if city:
        
        current_city_weather_data =  get_city_current_weather(city, API_KEY)
        
        if selected_date == "d0":
            outfit_image_urls = get_ootd(current_city_weather_data.temperature, current_city_weather_data.max_temperature, current_city_weather_data.min_temperature)
            return jsonify(outfit_image_urls=outfit_image_urls)
            
        elif selected_date == "d1" or selected_date == "d2" or selected_date == "d3" or selected_date == "d4":
            date_num = get_date_num_by_code(selected_date) - 1
            city_forecast_data, timestamp_labels, temp_values = get_city_forecast_weather(city, API_KEY, selected_date)
            outfit_image_urls = get_ootd(forecast_keypoint_data[date_num].temp, city_forecast_data.max_temperature, city_forecast_data.min_temperature)
            return jsonify(outfit_image_urls=outfit_image_urls)
            
    abort(404)    
    # 在此處獲取 outfit_image_url 列表
    print(f"Received input value: {city}")
    return jsonify(outfit_image_urls=outfit_image_urls)


# ========================================================================================================


# LOCATION
@views.route('/location-weather')
def location_weather():
    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')
    selected_date = request.args.get('date', '')
    forecast_keypoint_data = get_lat_lon_forecast_keypoint(lat, lon, API_KEY)
    outfit_image_url = None
    
    if lat and lon:
        
        current_location_weather_data =  get_lat_lon_current_weather(lat, lon, API_KEY)
        
        if selected_date == "d0":
            # outfit_image_url = get_ootd(current_location_weather_data.temperature)
            timestamp_labels, temp_values = get_lat_lon_current_forecast_weather(lat, lon, API_KEY)
            return render_template(
                "location.html",
                location=[lat, lon],
                current_location_weather_data=current_location_weather_data,
                forecast_keypoint_data=forecast_keypoint_data,
                timestamp_labels=timestamp_labels,
                temp_values=temp_values,
                outfit_image_url=outfit_image_url
            )
            
        elif selected_date == "d1" or selected_date == "d2" or selected_date == "d3" or selected_date == "d4":
            date_num = get_date_num_by_code(selected_date) - 1
            # outfit_image_url = get_ootd(forecast_keypoint_data[date_num].temp)
            
            location_forecast_data, timestamp_labels, temp_values = get_lat_lon_forecast_weather(lat, lon, API_KEY, selected_date)
            return render_template(
                "location.html",
                location=[lat, lon],
                current_location_weather_data=current_location_weather_data,
                forecast_keypoint_data=forecast_keypoint_data,
                location_forecast_data=location_forecast_data,
                timestamp_labels=timestamp_labels,
                temp_values=temp_values,
                outfit_image_url=outfit_image_url    
            )
    
    abort(404)


@views.route('/get_outfit_image_urls_location')
def get_outfit_image_urls_location():
    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')
    selected_date = request.args.get('date', '')
    forecast_keypoint_data = get_lat_lon_forecast_keypoint(lat, lon, API_KEY)
    
    if lat and lon:
        
        current_loaction_weather_data =  get_lat_lon_current_weather(lat, lon, API_KEY)
        
        if selected_date == "d0":
            outfit_image_urls = get_ootd(current_loaction_weather_data.temperature, current_loaction_weather_data.max_temperature, current_loaction_weather_data.min_temperature)
            return jsonify(outfit_image_urls=outfit_image_urls)
            
        elif selected_date == "d1" or selected_date == "d2" or selected_date == "d3" or selected_date == "d4":
            date_num = get_date_num_by_code(selected_date) - 1
            location_forecast_data, timestamp_labels, temp_values = get_lat_lon_forecast_weather(lat, lon, API_KEY, selected_date)
            outfit_image_urls = get_ootd(forecast_keypoint_data[date_num].temp, location_forecast_data.max_temperature, location_forecast_data.min_temperature)
            return jsonify(outfit_image_urls=outfit_image_urls)
            
    abort(404)


# ========================================================================================================


# 404 error handler
@views.errorhandler(404)
def invalid_route(e):
    return render_template("404.html"), 404