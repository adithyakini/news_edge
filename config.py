import streamlit as st

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

SEARCH_QUERIES = {

    "NSE": [
        "NSE market moving news Reuters",
        "India stock market macro news",
        "RBI market impact",
        "FII DII market activity"
    ],

    "GOLD": [
        "India gold import duty Reuters",
        "Gold market moving news",
        "Fed gold impact",
        "Central bank gold buying"
    ],

    "SILVER": [
        "Silver market impact news",
        "Industrial silver demand"
    ],

    "CRUDE": [
        "OPEC oil production Reuters",
        "Crude oil inventory Reuters",
        "Oil geopolitical risk"
    ],

    "NATGAS": [
        "Natural gas inventory report",
        "LNG disruption news"
    ],

    "USDINR": [
        "USDINR RBI intervention",
        "Dollar index India impact"
    ],

    "GBPINR": [
        "Pound sterling India impact",
        "GBP macro news"
    ]
}
