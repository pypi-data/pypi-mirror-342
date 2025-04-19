
<h1 align="center">
  <img src="https://s6.uupload.ir/files/11zon_cropped_(1)_nev9.png" alt="ParsWeather Logo" width="150">
  <br>ParsWeather – Iran's Ultimate Weather Package 🇮🇷
</h1>

<p align="center">
  <b>📡 Get the most accurate weather information for Iran with a single Python package!</b><br>
  🌦️ Temperature, Air Quality, Radar Images, Sunrise & Sunset Times, and much more! 🌍
</p>

---

## 📥 Quick Installation  

Install **ParsWeather** via **pip** in no time:  

```bash
pip install ParsWeather
```

💡 **Requirements:**  
- **Python 3.7+**  
- **Internet connection** to fetch the latest weather data  

---

## 🚀 How to Use – It's Easy and Fun!  

No need for complex setups – just a few lines of code and you're good to go! Here's an example:  
بله، حالا کد به زبان انگلیسی آماده شده است و شما می‌توانید نام شهرها را به انگلیسی وارد کنید:

### 1. **Current Temperature**
```python
from ParsWeather import WeatherForecast as wf  

city = "Tehran"  # 📍 Replace with the city you want to check (e.g., Tehran)

# Current Temperature
print(f"🌡️ Current Temperature: {wf.get_temperature(city)}°C")
```

### 2. **Real Feel Temperature**
```python
# Real Feel Temperature
print(f"🤔 Real Feel Temperature: {wf.get_realfeel(city)}°C")
```

### 3. **Air Quality**
```python
# Air Quality
print(f"🍃 Air Quality: {wf.get_air_quality(city)}")
```

### 4. **Air Quality Index (AQI)**
```python
# Air Quality Index (AQI)
print(f"📊 Air Quality Index (AQI): {wf.get_air_quality_aqi(city)}")
```

### 5. **Dust & Allergen Levels**
```python
# Dust & Allergen Levels
print(f"🏜️ Dust & Allergen Levels: {wf.get_dust_dander_data(city)}")
```

### 6. **Full Weather Forecast**
```python
# Full Weather Forecast
print(f"🌦️ Full Weather Forecast: {wf.get_weather_forecast(city)}")
```

### 7. **Radar Image Link**
```python
# Radar Image Link
print(f"🛰️ Radar Image Link: {wf.get_radar_image_link(city)}")
```

### 8. **Sunrise & Sunset Times**
```python
# Sunrise & Sunset Times
print(f"🌅 Sunrise & Sunset Times: {wf.get_sun_times(city)}")
```

### 9. **Detailed Weather Forecast**
```python
# Detailed Weather Forecast
print(f"🔎 Detailed Weather Forecast: {wf.get_forecast_details(city)}")
```

### 10. **Combined Weather & AQI**
```python
# Combined Weather & AQI
print(f"🌍 Combined Weather & AQI: {wf.get_weather_forecast_air_aqi(city)}")
```

### 11. **Radar GIF Link**
```python
# Radar GIF Link
print(f"🛰️ Radar GIF Link:{wf.download_specific_image()}")
```

### 12. **Pollutant Data**
```python
# Pollutant Data
pollutant_data = wf.get_pollutant_info(city)
if isinstance(pollutant_data, dict):
    for pollutant, info in pollutant_data.items():
        print(pollutant)
        print(f"{info['concentration']}")
        print(f"{info['statement']}")
        print('-' * 50)
else:
    print(pollutant_data)
```

### 13. **Earth Satellite Image URL**
```python
# Earth Satellite Image URL
image_url = wf.get_earth_satellite_image_url()
print(image_url)
```

### 14. **Daily Weather Forecast**
```python
# Daily Weather Forecast
daily_forecast = wf.get_daily_weather_info(city, "12/25")  # You can replace with any date
print(daily_forecast)
```

---

### **Important Notes**:
1. **City Names**: Replace `city` with the name of the city you want to check in English (e.g., `Tehran` instead of `تهران`).
2. **Dates**: For daily weather forecasts, you can input the date in the format `"MM/DD"`, for example, `"12/25"` for December 25th.

With these changes, the code will work smoothly for any city, and the outputs will be provided in English.
🎯 Just plug in your city name and get precise, real-time weather updates! It's that simple!

---

## 🔥 Why Choose **ParsWeather**?

✅ **Up-to-Date & Reliable Data** – Get the latest weather insights with absolute accuracy.  
✅ **User-Friendly** – Just a few lines of code to pull comprehensive data!  
✅ **Comprehensive** – Covers everything from temperature and air quality to radar images and sun times!  
✅ **Tailored for Iran** – Designed with Iranian cities in mind, it's the only weather tool you'll need for Iran 🇮🇷.

---

## 📍 Key Features:

🌡️ **Current Temperature** – Check the temperature in real-time!  
🤔 **Real Feel Temperature** – How does it *really* feel outside?  
🍃 **Air Quality** – Find out how fresh the air is!  
📊 **Air Quality Index (AQI)** – Know how polluted the air is.  
🏜️ **Dust & Allergen Levels** – Prepare for allergies or dusty days.  
🌦️ **Full Weather Forecast** – Hour-by-hour or daily forecast.  
🛰️ **Radar Images** – See weather systems moving in!  
🌅 **Sunrise & Sunset Times** – Never miss a sunrise or sunset again.  
🔎 **Detailed Forecast** – Get an in-depth look at the upcoming weather.  
📍 **Supported Cities** – Check if your city is covered.  
🌍 **Combined Weather & AQI** – Get the full picture of both weather and air quality.

---

## 💡 Possible Use Cases

🚗 **Travel & Navigation Apps** – Never get caught in a rainstorm again!  
📱 **Smart Assistants and Bots** – Show your users the weather with ease.  
🏫 **School/Office Systems** – Announce closures due to bad air quality or extreme weather.  
🏕️ **Outdoor Adventures** – Check the weather before you hit the trails or mountains.

---

## 🏆 Why is **ParsWeather** the Best Choice?

| Feature | ParsWeather | Other Methods |
|---------|-------------|---------------|
| ⚡ Speed | ✅ Lightning fast | ❌ Slow updates |
| 🎯 Accuracy | ✅ Super precise | ❌ Hit or miss |
| 🌎 Iran Coverage | ✅ Complete list of cities | ❌ Missing major cities |
| 🚀 Easy to Use | ✅ Just a few lines | ❌ Complex API integrations |
| 📡 Satellite & Radar Images | ✅ Yes | ❌ No radar images |

✨ **ParsWeather is the only package specifically built for accurate, up-to-date weather information for Iranian cities!**

---

## 📚 Want More Info?

🔗 **GitHub:** [Check it out on GitHub](https://github.com/MrAAQPy/ParsWeather/)  
🔗 **Website:** [Visit the website](https://mraaqpy.github.io/)

📌 **Start using ParsWeather today and say goodbye to unpredictable weather surprises!** 🌪️🌈

---

✅ **What do you think of this documentation? Any other features or suggestions? Drop your feedback!** 🤔


Here’s a more complete footer for the **ParsWeather** package documentation, including copyright and developer information:

---

## **Developed by** [Ali Ayati Qaffari](https://mraaqpy.github.io/)

© 2025 **ParsWeather** – All rights reserved.  

This project is developed and maintained by **Ali Ayati Qaffari**. Unauthorized use, distribution, or reproduction of any part of this package without explicit permission is prohibited.

