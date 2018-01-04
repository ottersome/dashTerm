import urllib.request, urllib.error
import json
url = "https://airbrake.io/blog/http-errors/401-unauthorized-error"
req = urllib.request.Request(url,None,{"Authorization":"earer BQDZMqtecuvKu7j6yirXew43PtuYVv7tjLZcbnmwjt_LhRIqEC33LAcDAI42StR1q0_Nfoc3Gskz8EHFInaS9UQx2ypEwRLdc9zQWKt03y8crJEJ4bD40aYlYr-C5WRyI0-eiFKglVauPvUjZrhPxWl8TY2nTkLfUuQ6geGxPS9h85TOKmgGNBCfi3B4kgjHBLpuDMSWidrkYPzZplUWibVHiMROLGsLLmpXKxlG8D5ubK_CU51pepBMaPz2cf9UgZsW0vIKOA"})
f = urllib.request.urlopen(req).read()
for line in f:
    line = line.decode()
    print(line)
