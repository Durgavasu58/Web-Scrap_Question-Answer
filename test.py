import requests
from bs4 import BeautifulSoup


import sqlite3 as sql
conn =sql.connect('data.db')
cur=conn.cursor()
cur.execute("create table if not exists mydata( s_title text ,s_answer text ,s_pages text)")

print("Table created")







url="https://www.udemy.com/topic/django/"
response=requests.get(url)
soup=BeautifulSoup(response.content,'html.parser')

#================= "" Question "" ===============
tt1=[]
titles=soup.find_all('span',class_='udlite-accordion-panel-title')
for title in titles:
    tt1.append(title.text)


#================= "" Answers "" ===============
ans=[]
answers=soup.find_all('div',class_='udlite-text-sm questions-and-answers--answer--2PMFk')
for answer in answers:
    ans.append(answer.text)

#================= "" Related Page urls "" ===============
rd=[]

for read in soup.find_all('div',{'class':'udlite-heading-md questions-and-answers--link--11XUK'}):
    link = read.find('a',href=True)
    if link is None:
        continue
    rd.append(link['href'])

#print(rd)
for n,p,r in zip(tt1,ans,rd):
    question=n
    answer=p
    pages=r
    
    cur.execute('''insert into mydata values(?,?,?)''', (question,answer,pages))
    #print('complete')

conn.commit()
cur.execute('''select * from mydata''')
results=cur.fetchall()
print(results)
conn.close()








