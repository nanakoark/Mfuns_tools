import requests
url2 = 'https://pan.nyaku.moe/f/kx1HZ/%E5%8B%95%E3%81%84%E3%81%A6%E3%81%AA%E3%81%84%E3%81%AE%E3%81%AB%E6%9A%91%E3%81%84%E3%82%88%20%28quilt%20heron%20remix%29%20_%20%EC%B0%8C%EA%B7%B8%EB%9F%AC%EC%A7%84%20%EC%88%98%EC%8B%9C%EB%85%B8%20%EB%A6%AC%EB%AF%B9%EC%8A%A4.mp4'
url3 = 'http://39.103.142.157:22333/f/kdyiZ/HELLO%20WORLD.mp4'
url4 = 'https://pan.nyaku.moe/f/x6l9ug/60E86068-8CFE-4968-BB7A-1E5091277027.jpeg'
header = {
'mftools':'letmepass!'
}

r = requests.get(url2, allow_redirects=True, headers=header,stream=True)
print(r.headers)
print(r.status_code)
filesize = r.headers['content-length']
num = 0
with open(r"C:\Users\31087\Downloads\test.mp4", "wb") as f:
    for chunk in r.iter_content(1024*1024):
        if chunk:
            f.write(chunk)
            num += 1
            print(num)