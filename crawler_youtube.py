import requests as rq #library to make requests to a website
from bs4 import BeautifulSoup as bs

page = rq.get('https://www.youtube.com/') #request to detik.com page
#print(page.status_code) #Check the request status, if it is "200" then it was successfully entered.

soup = bs(page.content, 'html.parser') #get html structure from kompas.com page
i = 0
for news in soup.findAll("div", {"class": "style-scope ytd-rich-item-renderer"}):
  if(i>4): break
  else:
    link =  news.find("a",{"class": "yt-simple-endpoint style-scope ytd-playlist-thumbnail"}).get('href')

    page_inside = rq.get(link)
    soup_inside = bs(page_inside.content, 'html.parser')

    desc = soup_inside.find("span",{"class": "yt-core-attributed-string--link-inherit-color"})
    if desc: desc = desc.text
    else: desc = "No Description or Caption"
    comm = soup_inside.find("span",{"class": "yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap"})
    if desc: desc = desc.text
    else: desc = "No Comment"

    print("<tr>")

    print("<td>",desc,"</td>")
    print("<td><a href='",link,"'></a></td>")
    print("<td>",comm,"</td>")
    print("</tr>")
  i+=1