from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
import json

app = Flask(__name__,static_folder='static')

##################################################################################################################
food_data={
    "appam":{
      "foodName": "Appam",
      "calories": "120 kcal",
      "proteins": "3%",
      "fatContent": "5%",
      "carbohydrates": "18%",      
        "vitamin A": "1%",
        "vitamin C": "0%",
        "calcium": "2%",
        "iron": "1%"
    },
    "bread toast":{
      "foodName": "Bread Toast",
      "calories": "80 kcal",
      "proteins": "2%",
      "fatContent": "1%",
      "carbohydrates": "15%",      
        "vitamin A": "0%",
        "vitamin C": "0%",
        "calcium": "1%",
        "iron": "1%"
    },
    "chapati":{
      "foodName": "Chapati",
      "calories": "100 kcal",
      "proteins": "4%",
      "fatContent": "3%",
      "carbohydrates": "20%",      
        "vitamin A": "0%",
        "vitamin C": "0%",
        "calcium": "2%",
        "iron": "2%"
    },
    "dosa":{
      "foodName": "Dosa",
      "calories": "150 kcal",
      "proteins": "5%",
      "fatContent": "7%",
      "carbohydrates": "22%",      
        "vitamin A": "2%",
        "vitamin C": "0%",
        "calcium": "4%",
        "iron": "2%"
    },
    "fried rice":{
      "foodName": "Fried Rice",
      "calories": "200 kcal",
      "proteins": "6%",
      "fatContent": "10%",
      "carbohydrates": "25%",      
        "vitamin A": "3%",
        "vitamin C": "2%",
        "calcium": "3%",
        "iron": "1%"
    },
    "fruit salad":{
      "foodName": "Fruit Salad",
      "calories": "90 kcal",
      "proteins": "1%",
      "fatContent": "0%",
      "carbohydrates": "22%",      
        "vitamin A": "5%",
        "vitamin C": "10%",
        "calcium": "1%",
        "iron": "1%"
    },
    "idli":{
      "foodName": "Idli",
      "calories": "70 kcal",
      "proteins": "3%",
      "fatContent": "1%",
      "carbohydrates": "15%",      
        "vitamin A": "0%",
        "vitamin C": "0%",
        "calcium": "2%",
        "iron": "1%"
    },
    "kati roll":{
      "foodName": "Kati Roll",
      "calories": "180 kcal",
      "proteins": "8%",
      "fatContent": "6%",
      "carbohydrates": "15%",      
        "vitamin A": "2%",
        "vitamin C": "1%",
        "calcium": "4%",
        "iron": "3%"
    },
    "mysore bajji":{
      "foodName": "Mysore Bajji",
      "calories": "160 kcal",
      "proteins": "4%",
      "fatContent": "8%",
      "carbohydrates": "20%",      
        "vitamin A": "1%",
        "vitamin C": "0%",
        "calcium": "2%",
        "iron": "2%"
    },
    "parotta":{
      "foodName": "Parotta",
      "calories": "220 kcal",
      "proteins": "5%",
      "fatContent": "12%",
      "carbohydrates": "28%",      
        "vitamin A": "3%",
        "vitamin C": "0%",
        "calcium": "5%",
        "iron": "2%"
    },
    "pesarattu":{
      "foodName": "Pesarattu",
      "calories": "120 kcal",
      "proteins": "6%",
      "fatContent": "3%",
      "carbohydrates": "18%",      
        "vitamin A": "1%",
        "vitamin C": "2%",
        "calcium": "4%",
        "iron": "2%"
    },
    "poha":{
      "foodName": "Poha",
      "calories": "100 kcal",
      "proteins": "2%",
      "fatContent": "1%",
      "carbohydrates": "20%",      
        "vitamin A": "0%",
        "vitamin C": "5%",
        "calcium": "2%",
        "iron": "2%"
    },
    "pulihora":{
      "foodName": "Pulihora",
      "calories": "150 kcal",
      "proteins": "3%",
      "fatContent": "5%",
      "carbohydrates": "25%",      
        "vitamin A": "2%",
        "vitamin C": "10%",
        "calcium": "3%",
        "iron": "1%"
    },
    "puri":{
      "foodName": "Puri",
      "calories": "180 kcal",
      "proteins": "4%",
      "fatContent": "8%",
      "carbohydrates": "22%",      
        "vitamin A": "1%",
        "vitamin C": "0%",
        "calcium": "2%",
        "iron": "2%"
    },
    "vada":{
      "foodName": "Vada",
      "calories": "160 kcal",
      "proteins": "5%",
      "fatContent": "10%",
      "carbohydrates": "18%",      
        "vitamin A": "3%",
        "vitamin C": "0%",
        "calcium": "5%",
        "iron": "3%"
    },
        "brinjal curry":{
      "foodName": "Brinjal Curry",
      "calories": "150 kcal",
      "proteins": "5%",
      "fatContent": "8%",
      "carbohydrates": "20%",      
        "vitamin A": "6%",
        "vitamin C": "8%",
        "calcium": "4%",
        "iron": "3%"
    },
    "butter chicken":{
      "foodName": "Butter Chicken",
      "calories": "300 kcal",
      "proteins": "15%",
      "fatContent": "20%",
      "carbohydrates": "10%",      
        "vitamin A": "10%",
        "vitamin C": "6%",
        "calcium": "8%",
        "iron": "5%"
    },
    "chicken biryani":{
      "foodName": "Chicken Biryani",
      "calories": "350 kcal",
      "proteins": "18%",
      "fatContent": "15%",
      "carbohydrates": "30%",      
        "vitamin A": "8%",
        "vitamin C": "4%",
        "calcium": "6%",
        "iron": "10%"
    },
    "chicken curry":{
      "foodName": "Chicken Curry",
      "calories": "250 kcal",
      "proteins": "12%",
      "fatContent": "10%",
      "carbohydrates": "15%",      
        "vitamin A": "6%",
        "vitamin C": "2%",
        "calcium": "4%",
        "iron": "8%"
    },
    "curd rice":{
      "foodName": "Curd Rice",
      "calories": "180 kcal",
      "proteins": "6%",
      "fatContent": "8%",
      "carbohydrates": "25%",      
        "vitamin A": "4%",
        "vitamin C": "2%",
        "calcium": "15%",
        "iron": "2%"
    },
    "dal":{
      "foodName": "Dal",
      "calories": "120 kcal",
      "proteins": "8%",
      "fatContent": "5%",
      "carbohydrates": "18%",      
        "vitamin A": "2%",
        "vitamin C": "1%",
        "calcium": "4%",
        "iron": "6%"
    },
    "fish curry":{
      "foodName": "Fish Curry",
      "calories": "200 kcal",
      "proteins": "20%",
      "fatContent": "12%",
      "carbohydrates": "8%",      
        "vitamin A": "8%",
        "vitamin C": "6%",
        "calcium": "2%",
        "iron": "4%"
    },
    "mutton curry":{
      "foodName": "Mutton Curry",
      "calories": "280 kcal",
      "proteins": "22%",
      "fatContent": "18%",
      "carbohydrates": "12%",      
        "vitamin A": "10%",
        "vitamin C": "4%",
        "calcium": "6%",
        "iron": "15%"
    },
    "palak paneer":{
      "foodName": "Palak Paneer",
      "calories": "220 kcal",
      "proteins": "12%",
      "fatContent": "15%",
      "carbohydrates": "18%",      
        "vitamin A": "15%",
        "vitamin C": "20%",
        "calcium": "25%",
        "iron": "8%"
    },
    "paneer curry":{
      "foodName": "Paneer Curry",
      "calories": "250 kcal",
      "proteins": "15%",
      "fatContent": "12%",
      "carbohydrates": "18%",      
        "vitamin A": "10%",
        "vitamin C": "8%",
        "calcium": "20%",
        "iron": "6%"
    },
    "potato curry":{
      "foodName": "Potato Curry",
      "calories": "180 kcal",
      "proteins": "4%",
      "fatContent": "8%",
      "carbohydrates": "25%",      
        "vitamin A": "2%",
        "vitamin C": "15%",
        "calcium": "4%",
        "iron": "2%"
    },
    "prawn curry":{
      "foodName": "Prawn Curry",
      "calories": "200 kcal",
      "proteins": "20%",
      "fatContent": "10%",
      "carbohydrates": "8%",      
        "vitamin A": "8%",
        "vitamin C": "6%",
        "calcium": "2%",
        "iron": "4%"
    },
    "ragi sangati":{
      "foodName": "Ragi Sangati",
      "calories": "120 kcal",
      "proteins": "5%",
      "fatContent": "2%",
      "carbohydrates": "25%",      
        "vitamin A": "0%",
        "vitamin C": "2%",
        "calcium": "10%",
        "iron": "15%"
    },
    "raita":{
      "foodName": "Raita",
      "calories": "70 kcal",
      "proteins": "3%",
      "fatContent": "1%",
      "carbohydrates": "10%",      
        "vitamin A": "2%",
        "vitamin C": "5%",
        "calcium": "6%",
        "iron": "2%"
    },
    "sambar":{
      "foodName": "Sambar",
      "calories": "150 kcal",
      "proteins": "8%",
      "fatContent": "5%",
      "carbohydrates": "20%",      
        "vitamin A": "15%",
        "vitamin C": "10%",
        "calcium": "8%",
        "iron": "4%"
    },
    "veg biryani":{
      "foodName": "Veg Biryani",
      "calories": "300 kcal",
      "proteins": "10%",
      "fatContent": "15%",
      "carbohydrates": "25%",      
        "vitamin A": "6%",
        "vitamin C": "8%",
        "calcium": "6%",
        "iron": "10%"
    },
    "white rice":{
      "foodName": "White Rice",
      "calories": "200 kcal",
      "proteins": "4%",
      "fatContent": "1%",
      "carbohydrates": "45%",      
        "vitamin A": "0%",
        "vitamin C": "0%",
        "calcium": "2%",
        "iron": "3%"
    },
     "badham milk":{
      "foodName": "Badham Milk",
      "calories": "200 kcal",
      "proteins": "8%",
      "fatContent": "12%",
      "carbohydrates": "15%",
        "vitamin A": "2%",
        "vitamin C": "1%",
        "calcium": "15%",
        "iron": "2%"
    },
    "butter milk":{
      "foodName": "Buttermilk",
      "calories": "50 kcal",
      "proteins": "2%",
      "fatContent": "1%",
      "carbohydrates": "8%",      
        "vitamin A": "1%",
        "vitamin C": "0%",
        "calcium": "2%",
        "iron": "1%"
    },
    "cappucino":{
      "foodName": "Cappucino",
      "calories": "120 kcal",
      "proteins": "3%",
      "fatContent": "8%",
      "carbohydrates": "10%",      
        "vitamin A": "0%",
        "vitamin C": "0%",
        "calcium": "6%",
        "iron": "1%"
    },
    "chai":{
      "foodName": "Chai",
      "calories": "50 kcal",
      "proteins": "1%",
      "fatContent": "2%",
      "carbohydrates": "10%",      
        "vitamin A": "0%",
        "vitamin C": "0%",
        "calcium": "2%",
        "iron": "1%"
    },
    "coffee":{
      "foodName": "Coffee",
      "calories": "5 kcal",
      "proteins": "0%",
      "fatContent": "0%",
      "carbohydrates": "1%",      
        "vitamin A": "0%",
        "vitamin C": "0%",
        "calcium": "0%",
        "iron": "0%"
    },
    "falooda":{
      "foodName": "Falooda",
      "calories": "180 kcal",
      "proteins": "4%",
      "fatContent": "6%",
      "carbohydrates": "25%",      
        "vitamin A": "2%",
        "vitamin C": "5%",
        "calcium": "8%",
        "iron": "3%"
    },
    "green tea":{
      "foodName": "Green Tea",
      "calories": "2 kcal",
      "proteins": "0%",
      "fatContent": "0%",
      "carbohydrates": "0%",      
        "vitamin A": "0%",
        "vitamin C": "2%",
        "calcium": "1%",
        "iron": "0%"
    },
    "lassi":{
      "foodName": "Lassi",
      "calories": "120 kcal",
      "proteins": "5%",
      "fatContent": "8%",
      "carbohydrates": "15%",      
        "vitamin A": "3%",
        "vitamin C": "2%",
        "calcium": "10%",
        "iron": "1%"
    },
    "lemon tea":{
      "foodName": "Lemon Tea",
      "calories": "10 kcal",
      "proteins": "1%",
      "fatContent": "0%",
      "carbohydrates": "3%",      
        "vitamin A": "1%",
        "vitamin C": "15%",
        "calcium": "2%",
        "iron": "1%"
    },
    "milk":{
      "foodName": "Milk",
      "calories": "80 kcal",
      "proteins": "4%",
      "fatContent": "5%",
      "carbohydrates": "10%",      
        "vitamin A": "6%",
        "vitamin C": "0%",
        "calcium": "30%",
        "iron": "1%"
    },
    "apple": {
      "foodName": "Apple",
      "calories": "95 kcal",
      "proteins": "1%",
      "fatContent": "0%",
      "carbohydrates": "25%",
        "vitamin A": "1%",
        "vitamin C": "14%",
        "calcium": "1%",
        "iron": "1%"
    },
    "banana": {
      "foodName": "Banana",
      "calories": "105 kcal",
      "proteins": "1%",
      "fatContent": "0%",
      "carbohydrates": "27%",      
        "vitamin A": "2%",
        "vitamin C": "17%",
        "calcium": "1%",
        "iron": "2%"
    },
    "guava":{
      "foodName": "Guava",
      "calories": "68 kcal",
      "proteins": "2%",
      "fatContent": "1%",
      "carbohydrates": "14%",      
        "vitamin A": "4%",
        "vitamin C": "381%",
        "calcium": "2%",
        "iron": "1%"
    },
    "lemon":{
      "foodName": "Lemon",
      "calories": "17 kcal",
      "proteins": "1%",
      "fatContent": "0%",
      "carbohydrates": "6%",      
        "vitamin A": "0%",
        "vitamin C": "51%",
        "calcium": "1%",
        "iron": "1%"
    },
    "orange":{
      "foodName": "Orange",
      "calories": "62 kcal",
      "proteins": "1%",
      "fatContent": "0%",
      "carbohydrates": "16%",      
        "vitamin A": "5%",
        "vitamin C": "89%",
        "calcium": "4%",
        "iron": "1%"
    },
    "pomegranate":{
      "foodName": "Pomegranate",
      "calories": "83 kcal",
      "proteins": "1%",
      "fatContent": "1%",
      "carbohydrates": "19%",
        "vitamin A": "0%",
        "vitamin C": "17%",
        "calcium": "1%",
        "iron": "2%"
    },
    "ariselu":{
      "foodName": "Ariselu",
      "calories": "180 kcal",
      "proteins": "4%",
      "fatContent": "6%",
      "carbohydrates": "25%",      
        "vitamin A": "2%",
        "vitamin C": "0%",
        "calcium": "6%",
        "iron": "4%"
    },
    "basundhi":{
      "foodName": "Basundi",
      "calories": "220 kcal",
      "proteins": "8%",
      "fatContent": "12%",
      "carbohydrates": "15%",      
        "vitamin A": "4%",
        "vitamin C": "2%",
        "calcium": "20%",
        "iron": "2%"
    },
    "boondi":{
      "foodName": "Boondi",
      "calories": "120 kcal",
      "proteins": "2%",
      "fatContent": "5%",
      "carbohydrates": "18%",      
        "vitamin A": "1%",
        "vitamin C": "0%",
        "calcium": "2%",
        "iron": "1%"
    },
    "chikki":{
      "foodName": "Chikki",
      "calories": "160 kcal",
      "proteins": "6%",
      "fatContent": "8%",
      "carbohydrates": "20%",      
        "vitamin A": "2%",
        "vitamin C": "1%",
        "calcium": "4%",
        "iron": "2%"
    },
    "doodhpak":{
      "foodName": "Doodhpak",
      "calories": "180 kcal",
      "proteins": "7%",
      "fatContent": "10%",
      "carbohydrates": "15%",      
        "vitamin A": "6%",
        "vitamin C": "2%",
        "calcium": "15%",
        "iron": "2%"
    },
    "gavvalu":{
      "foodName": "Gavvalu",
      "calories": "140 kcal",
      "proteins": "3%",
      "fatContent": "5%",
      "carbohydrates": "22%",
        "vitamin A": "1%",
        "vitamin C": "0%",
        "calcium": "2%",
        "iron": "1%"
    },
    "gulab jamun":{
      "foodName": "Gulab Jamun",
      "calories": "200 kcal",
      "proteins": "5%",
      "fatContent": "12%",
      "carbohydrates": "18%",      
        "vitamin A": "2%",
        "vitamin C": "0%",
        "calcium": "4%",
        "iron": "2%"
    },
    "halwa":{
      "foodName": "Halwa",
      "calories": "180 kcal",
      "proteins": "3%",
      "fatContent": "10%",
      "carbohydrates": "22%",      
        "vitamin A": "2%",
        "vitamin C": "1%",
        "calcium": "6%",
        "iron": "2%"     
    },
    "jalebi":{
      "foodName": "Jalebi",
      "calories": "250 kcal",
      "proteins": "4%",
      "fatContent": "15%",
      "carbohydrates": "30%",      
        "vitamin A": "4%",
        "vitamin C": "6%",
        "calcium": "8%",
        "iron": "2%"
    },
    "kajjikaya":{
      "foodName": "Kajjikaya",
      "calories": "160 kcal",
      "proteins": "3%",
      "fatContent": "8%",
      "carbohydrates": "20%",      
        "vitamin A": "2%",
        "vitamin C": "0%",
        "calcium": "4%",
        "iron": "2%"
    },
    "kakinada khaja":{
      "foodName": "Kakinada Khaja",
      "calories": "200 kcal",
      "proteins": "5%",
      "fatContent": "10%",
      "carbohydrates": "18%",      
        "vitamin A": "2%",
        "vitamin C": "2%",
        "calcium": "6%",
        "iron": "3%"
    },
    "kalakand":{
      "foodName": "Kalakand",
      "calories": "180 kcal",
      "proteins": "8%",
      "fatContent": "6%",
      "carbohydrates": "15%",      
        "vitamin A": "4%",
        "vitamin C": "0%",
        "calcium": "15%",
        "iron": "2%"
    },
    "laddu":{
      "foodName": "Laddu",
      "calories": "160 kcal",
      "proteins": "4%",
      "fatContent": "8%",
      "carbohydrates": "18%",      
        "vitamin A": "2%",
        "vitamin C": "1%",
        "calcium": "4%",
        "iron": "2%"
    },
    "mysore pak":{
      "foodName": "Mysore Pak",
      "calories": "220 kcal",
      "proteins": "6%",
      "fatContent": "12%",
      "carbohydrates": "20%",      
        "vitamin A": "6%",
        "vitamin C": "2%",
        "calcium": "10%",
        "iron": "4%"
    },
    "poornalu":{
      "foodName": "Poornalu",
      "calories": "200 kcal",
      "proteins": "5%",
      "fatContent": "10%",
      "carbohydrates": "18%",      
        "vitamin A": "4%",
        "vitamin C": "0%",
        "calcium": "6%",
        "iron": "3%"
    },
    "pootharekulu":{
      "foodName": "Pootharekulu",
      "calories": "250 kcal",
      "proteins": "6%",
      "fatContent": "12%",
      "carbohydrates": "25%",      
        "vitamin A": "8%",
        "vitamin C": "2%",
        "calcium": "8%",
        "iron": "4%"
    },
    "ras malai":{
      "foodName": "Ras Malai",
      "calories": "180 kcal",
      "proteins": "4%",
      "fatContent": "10%",
      "carbohydrates": "15%",      
        "vitamin A": "2%",
        "vitamin C": "1%",
        "calcium": "15%",
        "iron": "2%"
    },
    "rasgulla":{
      "foodName": "Rasgulla",
      "calories": "160 kcal",
      "proteins": "3%",
      "fatContent": "8%",
      "carbohydrates": "18%",
        "vitamin A": "2%",
        "vitamin C": "0%",
        "calcium": "10%",
        "iron": "2%"
    },
    "sheer":{
      "foodName": "Sheer",
      "calories": "200 kcal",
      "proteins": "5%",
      "fatContent": "10%",
      "carbohydrates": "22%",
      "vitamin A": "4%",
      "vitamin C": "2%",
      "calcium": "6%",
      "iron": "3%"
    },
    "soan papdi":{
      "foodName": "Soan Papdi",
      "calories": "180 kcal",
      "proteins": "3%",
      "fatContent": "8%",
      "carbohydrates": "20%",      
      "vitamin A": "2%",
      "vitamin C": "1%",
      "calcium": "4%",
      "iron": "2%"
      },
      "burger":{
      "foodName": "Burger",
      "calories": "250 kcal",
      "proteins": "12%",
      "fatContent": "15%",
      "carbohydrates": "20%",      
        "vitamin A": "8%",
        "vitamin C": "2%",
        "calcium": "10%",
        "iron": "6%"
    },
    "cake":{
      "foodName": "Cake",
      "calories": "300 kcal",
      "proteins": "5%",
      "fatContent": "20%",
      "carbohydrates": "30%",      
        "vitamin A": "10%",
        "vitamin C": "4%",
        "calcium": "8%",
        "iron": "4%"
    },
    "chana masala":{
      "foodName": "Chana Masala",
      "calories": "220 kcal",
      "proteins": "10%",
      "fatContent": "8%",
      "carbohydrates": "18%",      
        "vitamin A": "6%",
        "vitamin C": "15%",
        "calcium": "6%",
        "iron": "10%"
    },
    "crispy chicken":{
      "foodName": "Crispy Chicken",
      "calories": "280 kcal",
      "proteins": "20%",
      "fatContent": "18%",
      "carbohydrates": "12%",      
        "vitamin A": "15%",
        "vitamin C": "6%",
        "calcium": "4%",
        "iron": "8%"
    },
    "fries":{
      "foodName": "Fries",
      "calories": "220 kcal",
      "proteins": "3%",
      "fatContent": "15%",
      "carbohydrates": "25%",      
        "vitamin A": "2%",
        "vitamin C": "8%",
        "calcium": "2%",
        "iron": "4%"
    },
    "ice cream":{
      "foodName": "Ice Cream",
      "calories": "150 kcal",
      "proteins": "2%",
      "fatContent": "8%",
      "carbohydrates": "20%",      
        "vitamin A": "6%",
        "vitamin C": "2%",
        "calcium": "10%",
        "iron": "4%"
    },
    "kulfi":{
      "foodName": "Kulfi",
      "calories": "120 kcal",
      "proteins": "5%",
      "fatContent": "6%",
      "carbohydrates": "15%",      
        "vitamin A": "4%",
        "vitamin C": "0%",
        "calcium": "8%",
        "iron": "2%"
    },
    "manchuria":{
      "foodName": "Manchuria",
      "calories": "200 kcal",
      "proteins": "8%",
      "fatContent": "10%",
      "carbohydrates": "18%",      
        "vitamin A": "2%",
        "vitamin C": "6%",
        "calcium": "4%",
        "iron": "3%"
    },
    "momos":{
      "foodName": "Momos",
      "calories": "150 kcal",
      "proteins": "6%",
      "fatContent": "5%",
      "carbohydrates": "20%",      
        "vitamin A": "3%",
        "vitamin C": "8%",
        "calcium": "6%",
        "iron": "2%"
    },
    "noodles":{
      "foodName": "Noodles",
      "calories": "180 kcal",
      "proteins": "7%",
      "fatContent": "8%",
      "carbohydrates": "22%",      
        "vitamin A": "2%",
        "vitamin C": "0%",
        "calcium": "4%",
        "iron": "2%"
    },
    "omelette":{
      "foodName": "Omelette",
      "calories": "220 kcal",
      "proteins": "14%",
      "fatContent": "18%",
      "carbohydrates": "5%",      
        "vitamin A": "10%",
        "vitamin C": "2%",
        "calcium": "8%",
        "iron": "6%"
    },
    "paani puri":{
      "foodName": "Paani Puri",
      "calories": "50 kcal",
      "proteins": "1%",
      "fatContent": "0%",
      "carbohydrates": "10%",      
        "vitamin A": "0%",
        "vitamin C": "5%",
        "calcium": "2%",
        "iron": "1%"
    },
    "pakode":{
      "foodName": "Pakode",
      "calories": "150 kcal",
      "proteins": "5%",
      "fatContent": "10%",
      "carbohydrates": "15%",      
        "vitamin A": "2%",
        "vitamin C": "4%",
        "calcium": "2%",
        "iron": "3%"
    },
    "pav bhaji":{
      "foodName": "Pav Bhaji",
      "calories": "300 kcal",
      "proteins": "8%",
      "fatContent": "15%",
      "carbohydrates": "40%",      
        "vitamin A": "10%",
        "vitamin C": "15%",
        "calcium": "8%",
        "iron": "4%"
    },
    "pizza":{
      "foodName": "Pizza",
      "calories": "350 kcal",
      "proteins": "12%",
      "fatContent": "20%",
      "carbohydrates": "30%",      
        "vitamin A": "15%",
        "vitamin C": "10%",
        "calcium": "25%",
        "iron": "6%"
    },
    "samosa":{
      "foodName": "Samosa",
      "calories": "200 kcal",
      "proteins": "6%",
      "fatContent": "12%",
      "carbohydrates": "18%",      
        "vitamin A": "8%",
        "vitamin C": "6%",
        "calcium": "4%",
        "iron": "8%"
    },
    "sandwich":{
      "foodName": "Sandwich",
      "calories": "250 kcal",
      "proteins": "10%",
      "fatContent": "8%",
      "carbohydrates": "30%",      
        "vitamin A": "6%",
        "vitamin C": "8%",
        "calcium": "15%",
        "iron": "2%"
    }
}
################################################################################################################
@app.route('/')
def home():
    return render_template('index.html')
    
################################################################################################################

@app.route('/breakfast')
def breakfast():
    return render_template('breakfast.html')

model_breakfast = load_model(r'C:\Major Project\RISHIKA PROJECT\New H5 models\breakfast.h5')

def get_info_breakfast(food):
    return food_data.get(food, {})
    
def predict_breakfast(uploaded_image):
    if uploaded_image:
        # Process the image with your model
        img = Image.open(uploaded_image)
        img = img.resize((224, 224))  # Adjust to match the model's input size

        # Convert the image to a numpy array
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize pixel values

        # Make predictions using the model
        predictions = model_breakfast.predict(img_array)

        # Get the predicted class index
        predicted_class_index = np.argmax(predictions)
        
        # Define your class labels
        class_labels = ['appam', 'bread toast','chapati', 'dosa', 'fried rice', 'fruit salad', 'idli',
                        'kati roll','mysore bajji','parotta','pesarattu','poha','pulihora','puri','vada']

        # Get the predicted food class
        predicted_food = class_labels[predicted_class_index]

        return predicted_food
    return "No image Uploaded"

@app.route('/submit1', methods=['GET','POST'])
def get_breakfast():
    if(request.method=='POST'):
        img = request.files['my_image']
        img_path = "static/" + img.filename
        img.save(img_path)
        p = predict_breakfast(img)
        food_info = get_info_breakfast(p)
        return render_template("breakfast.html", prediction=p, img_path=img_path,food_info=food_info)
       
################################################################################################################
@app.route('/main')
def main():
    return render_template('main.html')

model_main = load_model(r'C:\Major Project\RISHIKA PROJECT\New H5 models\main.h5')

def get_info_main(food):
    return food_data.get(food, {})


def predict_main(uploaded_image):
    if uploaded_image:
        # Process the image with your model
        img = Image.open(uploaded_image)
        img = img.resize((224, 224))  # Adjust to match the model's input size

        # Convert the image to a numpy array
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize pixel values

        # Make predictions using the model
        predictions = model_main.predict(img_array)

        # Get the predicted class index
        predicted_class_index = np.argmax(predictions)
        
        # Define your class labels
        class_labels = ['brinjal curry', 'butter chicken', 'chicken biryani', 'chicken curry', 'curd rice', 'dal',                'fish curry', 'mutton curry', 'palak paneer',  'paneer curry', 'potato curry', 
                        'prawn curry', 'ragi sangati', 'raita', 'sambar', 'veg biryani', 'white rice']

        # Get the predicted food class
        predicted_food = class_labels[predicted_class_index]

        return predicted_food
    return "No image Uploaded"


@app.route("/submit2", methods = ['GET', 'POST'])
def get_main():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "static/"+img.filename
        img.save(img_path)
        p = predict_main(img)
        food_info = get_info_main(p)
    return render_template("main.html", prediction = p,img_path=img_path,food_info=food_info)
    
################################################################################################################
@app.route('/drinks')
def drinks():
    return render_template('drinks.html')

model_drinks = load_model(r'C:\Major Project\RISHIKA PROJECT\New H5 models\drinks.h5')

def get_info_drinks(food):
    return food_data.get(food, {})

def predict_drinks(uploaded_image):
    if uploaded_image:
        # Process the image with your model
        img = Image.open(uploaded_image)
        img = img.resize((224, 224))  # Adjust to match the model's input size

        # Convert the image to a numpy array
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize pixel values

        # Make predictions using the model
        predictions = model_drinks.predict(img_array)

        # Get the predicted class index
        predicted_class_index = np.argmax(predictions)
        
        # Define your class labels
        class_labels = ['badham milk', 'butter milk', 'cappucino', 'chai', 'coffee', 
                        'falooda',  'green tea', 'lassi', 'lemon tea', 'milk']

        # Get the predicted food class
        predicted_food = class_labels[predicted_class_index]

        return predicted_food
    return "No image Uploaded"


@app.route("/submit3", methods = ['GET', 'POST'])
def get_drinks():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "static/"+img.filename
        img.save(img_path)
        p = predict_drinks(img)
        food_info = get_info_drinks(p)
    return render_template("drinks.html", prediction = p,img_path=img_path,food_info=food_info)
 
################################################################################################################ 
@app.route('/fruit')
def fruit():
    return render_template('fruits.html')

model_fruits = load_model(r'C:\Major Project\RISHIKA PROJECT\New H5 models\fruits.h5')

def get_info_fruits(food):
    return food_data.get(food, {})

def predict_fruits(uploaded_image):
    if uploaded_image:
        # Process the image with your model
        img = Image.open(uploaded_image)
        img = img.resize((224, 224))  # Adjust to match the model's input size

        # Convert the image to a numpy array
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize pixel values

        # Make predictions using the model
        predictions = model_fruits.predict(img_array)

        # Get the predicted class index
        predicted_class_index = np.argmax(predictions)
        
        # Define your class labels
        class_labels = ['apple','banana','guava','lemon','orange','pomegranate']

        # Get the predicted food class
        predicted_food = class_labels[predicted_class_index-1]

        return predicted_food
    return "No image Uploaded"


@app.route("/submit4", methods = ['GET', 'POST'])
def get_fruits():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "static/"+img.filename
        img.save(img_path)
        p = predict_fruits(img)
        food_info = get_info_fruits(p)
    return render_template("fruits.html", prediction = p,img_path=img_path,food_info=food_info)

################################################################################################################
@app.route('/sweets')
def sweets():
    return render_template('sweets.html')

model_sweets = load_model(r'C:\Major Project\RISHIKA PROJECT\New H5 models\sweets.h5')

def get_info_sweets(food):
    return food_data.get(food, {})

def predict_sweets(uploaded_image):
    if uploaded_image:
        # Process the image with your model
        img = Image.open(uploaded_image)
        img = img.resize((224, 224))  # Adjust to match the model's input size

        # Convert the image to a numpy array
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize pixel values

        # Make predictions using the model
        predictions = model_sweets.predict(img_array)

        # Get the predicted class index
        predicted_class_index = np.argmax(predictions)
        
        # Define your class labels
        class_labels = ['ariselu', 'basundi', 'boondi', 'chikki', 'doodhpak', 'gavvalu', 'gulab jamun', 'halwa',                'jalebi', 'kajjikaya', 'kakinada khaja', 'kalakand', 'laddu' , 'mysore pak', 'poornalu',                'pootharekulu', 'ras malai', 'rasgulla', 'sheer', 'soan papdi']

        # Get the predicted food class
        predicted_food = class_labels[predicted_class_index]

        return predicted_food
    return "No image Uploaded"


@app.route("/submit5", methods = ['GET', 'POST'])
def get_sweets():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "static/"+img.filename
        img.save(img_path)
        p = predict_sweets(img)
        food_info = get_info_sweets(p)
    return render_template("sweets.html", prediction = p,img_path=img_path,food_info=food_info)

################################################################################################################
@app.route('/snacks')
def snacks():
    return render_template('snacks.html')

model_snacks = load_model(r'C:\Major Project\RISHIKA PROJECT\New H5 models\sweets.h5')

def get_info_snacks(food):
    return food_data.get(food, {})


def predict_snacks(uploaded_image):
    if uploaded_image:
        # Process the image with your model
        img = Image.open(uploaded_image)
        img = img.resize((224, 224))  # Adjust to match the model's input size

        # Convert the image to a numpy array
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize pixel values

        # Make predictions using the model
        predictions = model_snacks.predict(img_array)

        # Get the predicted class index
        predicted_class_index = np.argmax(predictions)
        
        # Define your class labels
        class_labels = ['burger', 'cake', 'chana masala', 'crispy chicken',
                        'fries', 'ice cream', 'kulfi', 'manchuria', 'momos', 
                        'noodles', 'omelette', 'paani puri', 'pakode', 'pav bhaji',
                        'pizza', 'samosa', 'sandwich']

        # Get the predicted food class
        predicted_food = class_labels[predicted_class_index]

        return predicted_food
    return "No image Uploaded"


@app.route("/submit6", methods = ['GET', 'POST'])
def get_snacks():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "static/"+img.filename
        img.save(img_path)
        p = predict_snacks(img)
        food_info = get_info_snacks(p)
    return render_template("snacks.html", prediction = p,img_path=img_path,food_info=food_info)

#################################################################################################################

if __name__ == '__main__':
    app.run(debug=True)

