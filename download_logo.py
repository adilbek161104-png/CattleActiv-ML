import requests
url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Emblem_of_Karakalpakstan.svg/500px-Emblem_of_Karakalpakstan.svg.png'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, headers=headers)
with open(r'd:\Diplom1\logo.png', 'wb') as f:
    f.write(r.content)
print("Downloaded logo.png")
