import time
import requests
import re
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
response = requests.get('https://www.vmgirls.com/sitemap.shtml', headers=headers)
html = response.text
urls = re.findall('<a href="(.*?)" title="(.*?)" target="_blank">', html)
print(urls)
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False
root_dir = 'vmgirls'
if not os.path.exists(root_dir):
    os.mkdir(root_dir)
os.chdir(root_dir)
for url in urls:
    try:
        time.sleep(0.5)
        dir_name = url[1]
        print(dir_name)
        vmgirls = requests.get(url[0], headers=headers)
        vmgirl_urls = re.findall('<a href="(.*?)" alt=".*?" title=".*?">', vmgirls.text)
        print(vmgirl_urls)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        os.chdir(dir_name)
        for vmgirl_url in vmgirl_urls:
            file_name = vmgirl_url.split('/')[-1]
            if not os.path.exists(file_name):
                response = requests.get(vmgirl_url, headers=headers)
                with open(file_name, 'wb') as f:
                    f.write(response.content)
            else:
                print(dir_name + '已存在')
        os.chdir('../')
    except:
        print('[Let me sleep for 5 seconds]')
        time.sleep(5)
        os.chdir('../')
        continue
