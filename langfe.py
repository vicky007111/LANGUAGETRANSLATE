import streamlit as st
import requests


BACKEND_URL="https://languagetranslate-nf8e.onrender.com/translate"


st.title('LANGUAGE TRANSLATOR')

text_to_translate = st.text_area('Enter the text you want to translate:', '')

languages = {
    'English':'en',
    'Tamil':'ta',
    'Telugu':'te',
    'Hindi':'hi',
    'Malayalam':'ml',
    'Kannada':'kn'
}

target_language = st.selectbox('Select the target language:', list(languages.keys()))


if st.button('Translate'):
    if text_to_translate:
        
        data = {
            'text':text_to_translate,
            'lang':languages[target_language]
        }

        
        try:
            response = requests.post(BACKEND_URL, json=data)
            result = response.json()

            
            if 'translatedText' in result:
                st.subheader('Translated Text:')
                st.success(result['translatedText'])
            else:
                st.error(result['error'])
        except requests.exceptions.RequestException as e:
            st.error("Failed to connect to the backend. Please make sure the backend is running.")
    else:
        st.error("Please enter some text to translate.")
