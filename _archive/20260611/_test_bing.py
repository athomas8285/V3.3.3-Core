import urllib.request
url = 'https://ts3.tc.mm.bing.net/th?id=OSB.%7ch1pa8vGs9kIEqxF2je4Zw--.png'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read()
print('URL:', url)
print('Status:', resp.status)
print('Content-Type:', resp.headers.get('Content-Type'))
print('Content-Length:', len(data))
print('Redirected to:', resp.url)
print('First 16 bytes:', data[:16].hex())
