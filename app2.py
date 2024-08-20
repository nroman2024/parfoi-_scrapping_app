import streamlit as st
from spider_simple_functions import *
from downloader import FileDownloader
import streamlit.components as select_slider
import pandas
import base64
import time
from io import BytesIO
from st_on_hover_tabs import on_hover_tabs
from PIL import Image

timestr = time.strftime("%Y%m%d-%H%M%S")

def scrapping_data(urls=None):
    spider = Spider_simple_functions()
    df_list = []
    counter = 40
    while 1:
        try:

            
            df_value = spider.extract_single_page(url=fr"https://www.parfois.com/on/demandware.store/Sites-PAR_ES-Site/es_ES/Search-UpdateGrid?cgid=2&pmin=0%2c01&prefn1=onlineForCountries&prefv1=ALL%7cES&start={counter}&sz=40&selectedUrl=https%3A%2F%2Fwww.parfois.com%2Fon%2Fdemandware.store%2FSites-PAR_ES-Site%2Fes_ES%2FSearch-UpdateGrid%3Fcgid%3D2%26pmin%3D0%252c01%26prefn1%3DonlineForCountries%26prefv1%3DALL%257cES%26start%3D{counter}%26sz%3D40")
            if len(df_value["Title"].values) > 0:

                df_list.append(df_value)
                counter = counter + 40
                print(counter)
            
            else:
                break
        
        except:
            break

    df_value = pd.concat(df_list,ignore_index=True)
   
    return df_value

def open_image(image):
    return Image.open(image)


st.set_page_config(layout="wide")
def main():
    # values = ["Scrapping","About"]
    # st.sidebar.selectbox("Valores",values)
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Scrapping',"About"],
                            iconName=['dashboard', 'search'], default_choice=0,
                            styles = {'navtab': {'background-color':'#111',
                                                  'color': '#818181',
                                                  'font-size': '18px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'uppercase'},
                                       'tabStyle': {':hover :hover': {'color': 'red',
                                                                      'cursor': 'pointer'}},
                                       'tabStyle' : {'list-style-type': 'none',
                                                     'margin-bottom': '30px',
                                                     'padding-left': '30px'},
                                       'iconStyle':{'position':'fixed',
                                                    'left':'7.5px',
                                                    'text-align': 'left'},
                                       },
                             key="1")

    if tabs == "Scrapping":

    
        st.title("Web scrapping Parfoiç online marketplace")
        with st.form(key="scrapping"):
            st.markdown("**Click the button to scrape :)**")
        
            value = st.form_submit_button("Submit request")
        if value:
            
            df = scrapping_data()
            st.success("Successfully scrapped!")
            st.dataframe(df)
            tab1,tab2,tab3 = st.tabs(["CSV","Excel","JSON"])

            with tab1:
                download = FileDownloader(df.to_csv(), file_ext=".csv").download()

            with tab2:
                towrite = BytesIO()
                df.to_excel(towrite, index=False, engine='openpyxl')
                towrite.seek(0)
                download = FileDownloader(towrite.read(), file_ext="xlsx").download_xlsx()

            with tab3:
                json_data = df.to_json(orient='records')
                download = FileDownloader(json_data, file_ext="json").download_json()

    else:
        st.title("About this web app")
        st.markdown("#### In this web application we web scrappe the Parfoiç marketplace. A purse & clothing store")
        st.image(open_image(r"parfoiç_image.png"))
        st.markdown("*We will have the option to download the file in three diferrent file types of format:  excel, csv or json*")

        




    
    
                



if __name__=="__main__":
    main()
