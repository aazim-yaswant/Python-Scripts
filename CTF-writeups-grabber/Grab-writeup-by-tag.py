import requests as re
from bs4 import BeautifulSoup as bs

#url="https://ctftime.org/writeups?page=1&hidden-tags=pwn%2Cpwning%2Cpwnable%2Cangr%2Cbinary%2Cbinaryexploitation%2Cexploitation%2Cexploit%2Cre%2Creverse+engineering%2Cpwntools"

base_url="https://ctftime.org"
ctf_url="https://ctftime.org/writeups?page=1&hidden-tags="
      
def urlincontent(old_soup):
    text=old_soup.select('div').pop(4).select('div').pop(4).select('div').pop(0).text
    lower=text.find('[')+1
    upper=text.find(']')
    final_url=text[lower:upper]
    return final_url

def getReadurl(writeup_url):
    writeup_page=re.get(writeup_url)
    writeup_soup=bs(writeup_page.text,"lxml")
    read_url=writeup_soup.select('div').pop(9).select('a').pop(0).get('href')
    if read_url==None:
        return urlincontent(writeup_soup)
    else:
        return read_url

def printdetails(content):
    while 1:
        event=content.pop(1)
        event_url=event.get('href')
        event_name=event.text

        task=content.pop(1)
        task_url=task.get('href')
        task_name=task.text

        team=content.pop(1)
        team_url=team.get('href')
        team_name=team.text

        writeup=content.pop(1)
        writeup_url=base_url+writeup.get('href')
        writeup_text=writeup.text

        if writeup_text !="Read":
            break

        read_url=getReadurl(writeup_url)
        if "http" not in read_url:
            print "\n\nSorry, Please check this link manually: %s, for the challenge %s, Event: %s\n\n"%(writeup_url,task_name,event_name)
        else:
            print "Event: %s, Challenge: %s, Writeup url: %s, Read: %s"%(event_name,task_name,writeup_url,read_url)

def addTags(ctf_url,tags):
    tagged_url=ctf_url
    for tag in tags:
        tagged_url=tagged_url+tag+"%2C"
    return tagged_url

def getTags():
    tags=[]
    print "Enter the tags and 'enough' for exit:\n"
    while 1:
        tag=str(raw_input())
        if tag=='enough':
            break
        else:
            tags.append(tag)
    return tags
    
def modifyUrl(ctf_url,i):
    modified_url=ctf_url.replace('1',str(int(i)+1))
    return modified_url
        
def main():
    no_of_pages=int(raw_input("Enter the number of pages:\n"))
    tags=getTags()
    for i in range(no_of_pages):
        modified_url=modifyUrl(ctf_url,i)
        url=addTags(modified_url,tags)
        page=re.get(url)
        soup=bs(page.text,"lxml")
        content=soup.select('div').pop(5).select('a')
        printdetails(content)
    
if __name__=="__main__":
    main()
