from tensorflow import keras
import streamlit as st
import numpy as np
import tensorflow as tf
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt

import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events



MAX_LEN = 30
model_path = 'model/best_model_1.h5'
model = keras.models.load_model(model_path)
tokenizer = Tokenizer()
okt = Okt()

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

def sentiment_predict(new_sentence):
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = MAX_LEN) # 패딩
    score = float(model.predict(pad_new)) # 예측
    
    if(score > 0.5):
        return str(score)+"긍정 리뷰입니다.\n".format(score * 100)
    else:
        return str(score)+"부정 리뷰입니다.\n".format((1 - score) * 100)

def getPN(text):
  return model.predict([text])

test_text = st.text_input('긍정/부정 문장 판독', '이거 ')

st.write("hello")


btn_clicked = st.button('결과 보기')
if btn_clicked:
  st.write(sentiment_predict(test_text))
  st.write(test_text)

    
    
    
    
    
    


loc_button = Button(label="Get Location")
loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition(
        (loc) => {
            document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
        }
    )
    """))
result = streamlit_bokeh_events(
    loc_button,
    events="GET_LOCATION",
    key="get_location",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_LOCATION" in result:
        st.write(result.get("GET_LOCATION"))
