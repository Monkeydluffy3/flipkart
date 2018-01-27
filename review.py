import bs4 as bs
import urllib.request as req
import archana as vikas

sou = req.urlopen("https://www.flipkart.com/ajc-solid-men-s-grey-track-pants/p/itme494xk9nhywsh?pid=TKPE494XQQEMYZEY&srno=b_1_2&otracker=nmenu_sub_Men_0_Track%20pants&lid=LSTTKPE494XQQEMYZEY7YTVMP&fm=organic&iid=02b4f7cc-73b5-4d55-b83e-e62775655ac9.TKPE494XQQEMYZEY.SEARCH&ppt=Store%20Browse&ppn=Search%20Page&ssid=j85d1fh10x6t40e81513557346759").read()

soup = bs.BeautifulSoup(sou,'lxml')
hello_as = soup.find('div',{'class' : 'col _39LH-M'})
main_link = ''
review_list = []

for xyz in soup.find_all('div' ,{'class' : 'qwjRop'}):
    review_list.append(xyz.text)

    
for i in range (0,len(review_list)):
    review_list[i] = review_list[i].replace('READ MORE','')     


for review in review_list:
   print(review,vikas.sentiment(review.lower()))
