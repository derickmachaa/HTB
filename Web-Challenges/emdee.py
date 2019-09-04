#!/usr/bin/env python3

#required modules
import requests
import hashlib
from bs4 import BeautifulSoup

def connect(url):
    try:
        print("\033[94m[+] Getting String to Hash From\033[0m",url)
        page=requests.get(url,timeout=10)
        return page
    except:
        print("\033[91m[+] Failed \033[0m")
        print("\033[94m[+] Trying Again\033[0m")
        try:
            print("\033[94m[+] Getting String to Hash From\033[0m",url)
            page=requests.get(url,timeout=10)
            return page
        except:
            print("\033[91m[-] Failed ... Check your internet connection or the url\033[0m")

def hashing(page):
    string=BeautifulSoup(page,'html.parser').find('h3').get_text()
    print("\033[92m[+] Gotten String\033[0m")
    print("[+] Encoding string")
    encoded=string.encode()
    print("[+] Encoded")
    print("\033[92m[+] Hashing String\033[0m")
    hashed=hashlib.md5(encoded).hexdigest()
    print("[+] Hashed")
    data={"hash":hashed}
    return data

def posting(url,data,page):
    print("\033[94m[+] Posting the Hash\033[0m")
    posted=requests.post(url,data=data,cookies=page.cookies,timeout=10)
    print("\033[94m[+] Posted\033[0m")
    soup=BeautifulSoup(posted.text,'html.parser')
    response=soup.find('p').get_text()
    return response

def main():
    port=int(input("Enter port >>>"))
    print("\033[92m[+] Port\033[0m",port)
    url="http://docker.hackthebox.eu:"+str(port)+"/"
    print("\033[92m[+] URL \033[0m",url)
    tries=input("[*] Enter number of tries to use::Press Enter for Default::Default is 5>")
    if(tries==""):
        tries=5
    for i in range(int(tries)):
        page=connect(url)
        if not(page):
            pass
        else:
            data=hashing(page.text)
            response=posting(url,data,page)
            if not(response.__contains__("HTB")):
                continue
            else:
                print("[+] Flag Gotten <<<--->>>")
                print("\033[91m[+] %s \033[0m" % response)
                break
    

if __name__ == '__main__':
    main()

