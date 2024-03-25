# Immo Charlie Phase 01: Data Collector
[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## 📖 Description

This Data Collector is designed to collect data on real estate properties for sale across Belgium.
It is phase 1 of a total of 4 phases of a larger project to develop a machine learning model for price prediction. See phase 2 (data analysis) [here](https://github.com/emsuru/charlie-02-data-analysis) and phase 3 (ML model development) [here](https://github.com/emsuru/charlie-03-ML-model-development).

## 🌺 Features

- Scrapes real estate listings from the largest Belgian real estate website
- Builds a dataset with detailed property information
- Saves data in both JSON and CSV formats for further analysis


## 👩‍💻 Usage

1. clone this repo on your local machine, navigate to its directory in your terminal and run requirements.txt to install all dependencies.
2. open `main.py` and in there update the number of immoweb.be SRPs (search result pages) that you want the program to scrape. fyi - the bigger this number, the longer the program takes to run
3. execute `main.py`
4. after `main.py` finishes executing, your scraped property data is saved in a CSV and a JSON file in your project directory


```
pip install -r requirements.txt

python3 main.py
```



## ⏱️ Project background & timeline

This project was done over the course of 3 days in February 2024, during the AI Bootcamp in Ghent, Belgium, 2024. 

Its main goals were to practice:

- building a data set completely from scratch
- scraping data from the web at scale
- practicing threading, multiprocessing
- practicing exception handling, error handling

## ⚠️ Warning

All my code is currently heavily:

- docstringed
- commented
- .. and sometimes typed.

This is to help me learn and to make my sessions with our training coach more efficient.

## 🤗 Thank you for visiting my project page!

Connect with me on [LinkedIn](https://www.linkedin.com/in/mirunasuru/) 🤍
