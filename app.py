import streamlit as st
import pandas as pd
from datetime import datetime

# ===============================
# LOAD DATA
# ===============================
sbi = pd.read_csv("SBI_weekly_clean_data.csv")
hdfc = pd.read_csv("HDFC_weekly_clean_data.csv")

sbi_forecast = pd.read_csv("sbi_forecast.csv")
hdfc_forecast = pd.read_csv("hdfc_forecast.csv")

# ===============================
# SORT DATA (VERY IMPORTANT)
# ===============================
sbi = sbi.sort_values("Week").reset_index(drop=True)
hdfc = hdfc.sort_values("Week").reset_index(drop=True)

# ===============================
# CONSTANTS
# ===============================
start_date = datetime(2001, 1, 1)

# ===============================
# FUNCTION: DATE → WEEK
# ===============================
def get_week(date):
    days = (date - start_date).days
    return (days // 7) + 1

# ===============================
# UI
# ===============================
st.title("📊 Stock Return Calculator (SBI & HDFC)")

# ===============================
# BANK SELECTION
# ===============================
bank = st.selectbox("Select Bank", ["SBI", "HDFC"])

if bank == "SBI":
    data = sbi
    forecast = sbi_forecast
else:
    data = hdfc
    forecast = hdfc_forecast

# ===============================
# DATE OPTIONS
# ===============================
days = list(range(1, 32))

months = {
    "January":1, "February":2, "March":3, "April":4,
    "May":5, "June":6, "July":7, "August":8,
    "September":9, "October":10, "November":11, "December":12
}

years_buy = list(range(2001, 2026))   # up to 2026
years_sell = list(range(2001, 2031))  # up to 2031

# ===============================
# BUY DATE
# ===============================
st.subheader("📅 Date of Buy")

col1, col2, col3 = st.columns(3)

with col1:
    buy_day = st.selectbox("Day (Buy)", days)

with col2:
    buy_month_name = st.selectbox("Month (Buy)", list(months.keys()))

with col3:
    buy_year = st.selectbox("Year (Buy)", years_buy)

buy_month = months[buy_month_name]

# ===============================
# SELL DATE
# ===============================
st.subheader("📅  Date of Sale")

col4, col5, col6 = st.columns(3)

with col4:
    sell_day = st.selectbox("Day (Sale)", days)

with col5:
    sell_month_name = st.selectbox("Month (Sale)", list(months.keys()))

with col6:
    sell_year = st.selectbox("Year (Sale)", years_sell)

sell_month = months[sell_month_name]

# ===============================
# CREATE DATE
# ===============================
try:
    buy_date = datetime(buy_year, buy_month, buy_day)
    sell_date = datetime(sell_year, sell_month, sell_day)
except:
    st.error("❌ Invalid Date")
    st.stop()

# ===============================
# VALIDATION (WEEK-BASED)
# ===============================
buy_week = get_week(buy_date)
sell_week = get_week(sell_date)

total_weeks_actual = len(data)
total_weeks_forecast = len(forecast)
max_total_weeks = total_weeks_actual + total_weeks_forecast

# Buy date validation
if buy_week > total_weeks_actual:
    st.error("❌ Buy date exceeds available weekly data")
    st.stop()

# Sell date validation
if sell_week <= buy_week:
    st.error("❌ Sale date must be after Buy date")
    st.stop()

if sell_week > max_total_weeks:
    st.error("❌ Sale date exceeds 5-year forecast limit")
    st.stop()

# ===============================
# GET BUY PRICE
# ===============================
buy_price = data.iloc[buy_week - 1]["Close.Price"]

# ===============================
# GET SELL PRICE
# ===============================
if sell_week <= total_weeks_actual:
    # ACTUAL DATA
    sell_price = data.iloc[sell_week - 1]["Close.Price"]
else:
    # FORECAST DATA
    forecast_index = sell_week - total_weeks_actual - 1
    sell_price = forecast.iloc[forecast_index]["Forecast"]

# ===============================
# CALCULATE RETURN
# ===============================
if st.button("📈 Calculate Return"):

    ret = ((sell_price - buy_price) / buy_price) * 100

    st.success(f"💰 Expected Return: {ret:.2f}%")

    st.write(f"📌 Buy Price: {buy_price:.2f}")
    st.write(f"📌 Sell Price: {sell_price:.2f}")

# ===============================
# DEBUG (OPTIONAL)
# ===============================
# st.write("Buy Week:", buy_week)
# st.write("Sell Week:", sell_week)
# st.write("Total Weeks:", total_weeks_actual)