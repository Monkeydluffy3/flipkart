import bs4 as bs
import urllib.request as req

sou = req.urlopen("https://www.flipkart.com/mens-clothing/sports-wear/track-pants/pr?count=40&otracker=nmenu_sub_Men_0_Track+pants&p%5B%5D=sort%3Dprice_asc&sid=2oq%2Fs9b%2F6gr%2Frfn").read()

soup = bs.BeautifulSoup(sou,'lxml')
list_av = [[]]   #link,ratting,price
list_final = [[]] #ratting,price,link
w = 0


z = 0
for item_as in soup.find_all('div' ,{'class' : 'col MP_3W3 _31eJXZ'}):
      try:
        list_final[z].append((item_as.find('div',{'class' : 'hGSR34 _2beYZw'})).text)
      except:
        list_final[z].append('Null')
      try:
        list_final[z].append((item_as.find('div',{'class' : '_1vC4OE'})).text)
      except:
        list_final[z].append('Null')  
      list_final[z].append((item_as.find('a',{'class' : '_2cLu-l'})).get('href'))  
      z=z+1
      list_final.append([])
      
for i in range(0,len(list_final)-1):
     list_av[w].append(str(list_final[i][2]))
     list_av[w].append(str(list_final[i][0][0]))
     if(ord(list_final[i][0][1]) != 32) :
       list_av[w][1]=list_av[w][1] + (str(list_final[i][0][1]))
     if(ord(list_final[i][0][2]) <= 100) :  
       list_av[w][1]=list_av[w][1] + (str(list_final[i][0][2]))
     list_av[w].append('')
     for j in range(1,len(list_final[i][1])):
        list_av[w][2] = list_av[w][2] + list_final[i][1][j]
     w=w+1
     list_av.append([]) 
     
      
for i in list_av:
   print(i)
   print("\n\n\n")    
      
         

