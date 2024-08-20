from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
import re
import json
import asyncio
import time
from playwright.async_api import async_playwright


def find_data_value(data):
    text = re.findall(r'<img alt="[\S]{1,10}"',data)
    data = [re.findall(r'["][\S]{1,15}"',x) for x in text]
    value = [i[0] for i in data]
    if len(value) > 0:
        return ",".join(value),len(value)
    return "No colours","No colours"

class Spider_simple_functions():
    def __init__(self):
        pass

    # def html_to_txt(self,url,adress,headers = None,cookies = None,proxys=None,params = None):
        
    #     """

    #     This function help us to save the request in a .txt file to save the number of request
    #     we do in order to not being blocked.
        
    #     """
    #     self.url = url
    #     self.headers = headers
    #     self.cookies = cookies
    #     self.proxys = proxys
    #     self.params = params
    #     self.adress = adress
        
    #     session = HTMLSession()
    
    #     request = session.get(self.url)
    #     with open(adress,"w",encoding="UTF-8") as f:
    #         data = f.write(request.text)
    #         f.close()
            
    #     print(f"HTML succesfully saved in {self.adress}")
    #     return request.text
        
    # def html_to_json(self,url,adress,headers = None,cookies = None,proxys=None,params = None):
    #     """
    #     This function help us to save the request in a .json file to save the number of request
    #     we do in order to not being blocked. Usually this kind of requests are done to an API.
        
        
    #     """
    #     self.url = url
    #     self.headers = headers
    #     self.cookies = cookies
    #     self.proxys = proxys
    #     self.params = params
    #     self.adress = adress
        
    #     session = HTMLSession()
    
    #     request = session.get(self.url)
    #     data = request.json()
        
    #     with open(self.adress,"w") as j:
    #         json.dump(data,j)
            
    #     print(f"JSON file succefully saved in {self.adress}")
            
    #     return request.json()

    def extract_single_page(self,url = None,headers = None,cookies = None,proxys=None,params = None,use_txt=None,adress_txt=None):
        #Extracting compiled urls-----------------------------------------------------
        
        """
        We can extract the data whether from the outcome of the html_to_txt() function using the
        parameters use_txt == True, adress_txt and url == None or straightly do the http request
        to the web page
        """
        if use_txt == True and adress_txt and url == None:
            print("Let's use txt!")
            with open(adress_txt,"r",encoding="UTF-8") as f:
                request = f.read()
                f.close()
            bs = BeautifulSoup(request,"lxml")
            
        else:
            
            self.url = url
            self.headers = headers
            self.cookies = cookies
            self.proxys = proxys
            self.params = params
            session = HTMLSession()

            request = session.get(self.url)
            bs = BeautifulSoup(request.text,"lxml")

        
        self.bs = bs
#         Change class and label-------------------------------------------------------------
        soup = bs.find_all("div",class_="pdp-product--name-container")

#         Defining variables to create the dictionary and afterwards the dataframe-----------
#         print(request.text)  
        title_value = []
        price_value = []
        number_colours_value = []
        colours = []
        link_value = []
        
        # stock_value = []
        # rating_value = []
        
        for text in soup:
#           Fetch the values----------------------------------
            try:

                title = text.find("h3",class_="pdp-product-name")
                link = f'https://www.parfois.com{title.a.attrs["href"]}'
                price = float(text.find("span",class_="value").text.strip().replace("€",""))
                # color = text.find("div",class_="swatches").button.attrs
            except:
                price = "No price"
            
            try:
                # color = text.find("div",class_="swatches").button.attrs
                # color = len(text.find("div",class_="swatches"))
                color,number_colours = find_data_value(str(text.find("div",class_="swatches")))
                # print(color,number_colours)
            except:
                color,number_colours = "No colours","No colours"
                # color,number_colours = find_data_value(str(text.find("div",class_="swatches")))
            
            # stock = text.find("p",class_="instock availability").text.strip()
            # rating = text.p["class"][1]
            
#           Append values to the variables--------------------

            title_value.append(title.text)
            link_value.append(link)
            price_value.append(price)
            colours.append(color)
            number_colours_value.append(number_colours)


            # stock_value.append(stock)
            # rating_value.append(rating)

            
        data_json = {
            "Title" : title_value,
            "Price" : price_value,
            "Number of values" : number_colours_value,
            "Colours" : colours,
            "Link" : link_value
            
            # "Stock" : stock_value,
            # "Rating" : rating_value    
            }
        
        df = pd.DataFrame(data_json)
        
        return df

    

#     def extract_multiple_pages(self,df):
#         """
#         We use this function in combination with the extract_single_data() if we are sure we have more than
#         one page to scrape.
#         It's important to provide a Dataframe as result from extract_single_data() to 
#         append the Dataframe to other Dataframes outcomed from this function
        
#         """
#         #We use the Dataframe provided in the function
#         self.df = df
#         #Using the same html code extracted in function extract_simple_page()
#         bs_page = self.bs
#         #We try to find the link to the next page. If it's not found returns 'None link found' 
#         soup = bs_page.find("li",class_="next")
#         if soup.a.text == "next":
#             url1 = f"https://books.toscrape.com/{soup.a.attrs['href']}"
#         else:
#             return "None link found"
        
#         #If the link is found we execute the function in the second found page

#         session = HTMLSession()
#         request = session.get(url1)
#         bs = BeautifulSoup(request.text,"lxml")
#         soup = bs.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
#         title_value = []
#         price_value = []
#         stars_value = []
#         available_value = []
#         for text in soup:
#             title = text.h3.a.text
#             price = text.find("p",class_="price_color").text.replace("Â£","")
#             stars = text.p["class"][1]
#             available = text.find("p",class_="instock availability").text.strip()
            
#             title_value.append(title)
#             price_value.append(price)
#             stars_value.append(stars)
#             available_value.append(available)
# #         Creating Pandas Dataframe
        
#         data = {
            
#                 "Title" : title_value,
#                 "Price" : price_value,
#                 "Stars" : stars_value,
#                 "Available" : available_value

#                     }

                    
#         #Creating the Dataframe of the second page and concatenating the Dataframe
#         #from the first and second page
#         df1 = pd.DataFrame(data)   
#         dfx1 = pd.concat([self.df,df1])
        
        
            
#         try:
# #             Stableshing the next link value
#             value_link = bs.find("li",class_="next")
#             print(value_link)
#             new_link = f"https://books.toscrape.com/catalogue/{value_link.a.attrs['href']}"
#         except:
#             print("Only two pages were scraped in total")
#             return dfx1

#         title1_value = []
#         price1_value = []
#         stars1_value = []
#         available1_value = []
# #       Loop throught all the webpages            
#         while 1:
#             try:


#                 if value_link.a.text == "next":
#                     url1 = f"https://books.toscrape.com/catalogue/{value_link.a.attrs['href']}"
#                     print(url1)
#                     session = HTMLSession()
#                     request = session.get(url1)
                    
        


#                 bs = BeautifulSoup(request.text,"lxml")
#                 soup = bs.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
#         #         Loop straight to labels(a,h1,h2,div) or go to the class
             
#                 for text in soup:
#                     title = text.h3.a.text
#                     price = text.find("p",class_="price_color").text.replace("Â£","")
#                     stars = text.p["class"][1]
#                     available = text.find("p",class_="instock availability").text.strip()

#                     title1_value.append(title)
#                     price1_value.append(price)
#                     stars1_value.append(stars)
#                     available1_value.append(available)
# #                 Getting the link to the next webpage    
#                 value_link = bs.find("li",class_="next")
# #           Except that is executed when the "next" button is no longer found
#             except:
#                 print(value_link)
#                 if len(title1_value) > 0:
#                     data2 = {

#                         "Title" : title1_value,
#                         "Price" : price1_value,
#                         "Stars" : stars1_value,
#                         "Available" : available1_value

#                             }
#                     df2 = pd.DataFrame(data2)
#                     dfx2 = pd.concat([dfx1,df2])
#                     return dfx2
#                 else:
#                     return dfx1
#                 break
            
#     def from_dataframe_to_data(self,df,extension,adress):
        
#         """
#         This function let us to save the data in the format we see fit.
#         We can save in csv,xlsx,sql,json or parquet
        
#         """
#         self.extension = extension
#         self.df = df
#         self.adress = adress
#         if self.extension == "csv":
#             return self.df.to_csv(self.adress,index = False)
#         elif self.extension == "xlsx":
#             return self.df.to_excel(self.adress,index = False)
#         elif self.extension == "sql":
#             return self.df.to_sql(self.adress,index = False)
#         elif self.extension == "json":
#             return self.df.to_json(self.adress,index = False)
#         elif self.extension == "parquet":
#             return self.df.to_parquet(self.adress,index = False)