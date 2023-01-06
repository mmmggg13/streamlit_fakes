import base64
from pathlib import Path
import streamlit as st
import sqlite3
import uuid
import datetime

# con = sqlite3.connect("fakes.db")
# cur = con.cursor()
# print("Successfully Connected to SQLite")

def get_now():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%m')#.isoformat()
    return now

def insert_to_db(id, dt, text, emb, label, proba):
    con = sqlite3.connect("fakes.db")
    cur = con.cursor()
    print("Successfully Connected to SQLite")        
    
    data_tuple = id, dt, text, emb, label, proba
    query= """INSERT INTO data VALUES (?, ?, ?, ?, ?, ?);"""
    try:
        cur.execute(query, data_tuple)
        con.commit()
        print('Sucsesfully added data')
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if con:
            con.close()
            print("The SQLite connection is closed")


@st.cache(suppress_st_warning=True)
def get_fvalue(val):
    feature_dict = {"No":1,"Yes":2}
    for key,value in feature_dict.items():
        if val == key:
            return value

def get_value(val,my_dict):
    for key,value in my_dict.items():
        if val == key:
            return value

app_mode = st.sidebar.selectbox('Меню',['Оберіть дію','Перевірити новину', 'Види фейків', 'Як боротись з фейками?'])
if app_mode=='Перевірити новину':
    from PIL import Image

    image = Image.open('image4.jpg')

    st.image(image, width=700)
    customized_button = st.markdown("""
        <style >
        .stDownloadButton, div.stButton {text-align:center}
        .stDownloadButton button, div.stButton > button:first-child {
            background-color: #ADD8E6;
            color:#000000;
            padding-left: 20px;
            padding-right: 20px;
        }

       
            }
        </style>""", unsafe_allow_html=True)
    text_to_check = st.text_input('Введіть текст новини')
    print(text_to_check)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col3:
        st.button('Check')

    id = str(uuid.uuid4())[:8]
    dt = get_now()
    txt = text_to_check
    emb = '[1 2 3]'
    label = 1
    proba = 0.98

    insert_to_db(id, dt, txt, emb, label, proba)
    if txt:
        st.write('Результат передбачння: ', "СХОЖЕ на ПРАВДУ)))" if label == 1 else "СХОЖЕ на ФЕЙК ((( Варто первірти на різних олайн-ресурсах!" )
        st.write('Ймовірність передбачння: ', proba*100,'%')

if app_mode=='Оберіть дію':
    st.title('Що таке фейки?')
    st.write('Фейкові новини (від англ. «fake» – брехня, фальш) – це неправдива інформація, яка цілеспрямовано розповсюджується зацікавленими особами, що переслідують свої (зазвичай політичні) цілі, або бажають заробити на інтернет-трафіку. Поширюють обман, знищують засади цивілізованості та є небезпекою для демократії ')
    st.image("image1.jpg")
if app_mode=='Види фейків':
    st.title('Види фейків')
    st.write('Класифікувати фейки можливо за різними критеріями: ')
    st.write('– за методом поширення: масово медійні (створюють для поширення в рейтингових ЗМІ) і локальні (поширюються під час розмов, у соціальних спільнотах, блогах тощо);')
    st.write('– за зовнішньою формою поширення: фотофейк, відеофейк, фейковий журналістський матеріал, фейковий допис, чутка;')
    st.write('– за територіальною спрямованістю: внутрішні (спрямовані на громадян конкретної території, держави) та зовнішні (спрямовані на представників міжнародної спільноти); ')
    st.write('– за направленістю (аудиторія): представники певних соціальних верств/певного віку (наприклад, студенти, пенсіонери) та всі громадяни;')
    st.write('–  за метою: сіяння паніки, розпалення міжнаціональної (расової, релігійної тощо) ворожнечі; поширення хибної думки; маніпулювання свідомістю; розважальний характер; звернення уваги на когось/щось; підготовка суспільства до сприйняття якоїсь події, явища, рішення тощо.')
    st.image("image2.jpg")

