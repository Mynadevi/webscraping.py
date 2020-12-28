import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import connect

parser=argparse.ArgumentParser()
parser.add_argument("--page_num",help="Enter the number of pages to parse",type=int)
parser.add_argument("--dbname",help="Enter the dbname",type=int)
args=parser.parse_args()

oyo_url="https://www.oyorooms.com/hotels-in-bangalore/pages="
page_num_MAX=args.page_num_max
scraped_info_lists=[]
connect.connect(args.dbname)

for page_num in range(1,page_num_MAX):
    req=requests.get(oyo_url+str(page_num))
    content=req.content

    soup=BeautifulSoup(content,"html.parser")

    all_hotels=soup.find_all("div",{"class":"hotelCardListing"})

    for hotel in all_hotels:
        hotel_dict={}
        hotel_dict["name"]=hotel.find("h3",{"class":"ListingHotelDescription_hotelName"}).text
        hotel_dict["adress"]=hotel.find("span",{"itemprop":"streetAddress"}).text
        hotel_dict["price"]=hotel.find("span",{"class":"ListingPrice_finalPrice"}).text
        try:
            hotel_dict["rating"]=hotel.find("span",{"class":"hotelRating_ratingSummary"}).text
        except AttributeError:
            hotel_dict["rating"]=None
        parent_amenities_element=hotel.find("div",{"class":"amenityWrapper"})

        amenities_List=[]
        for amenity in parent_amenities_element.find_all("div",{"class":"amenityWrapper_amenity"}):
            amenities_List.append(amenity.find("span",{"class":"d-body-sm"}).text.strip())
        hotel_dict["amenities"]=' ,'.join(amenities_List[:-1])

        scraped_info_List.append(hotel_dict)
        connect.insert_into_table(args.dbname,tuple(hotel_dict.values()))

dataFrame=pandas.DataFrame(scraped_info_List)
dataFrame.to_csv("oyo.csv")
connect.get_hotel_info(args.dbame)
        
            
