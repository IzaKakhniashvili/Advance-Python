import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import json


lock = threading.Lock()
posts = []

def get_post(i, ):
        url = f"https://jsonplaceholder.typicode.com/posts/{i + 1}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            with lock:
                posts.append(data)
        else:
            print(f"Error: {response.status_code}")
            
            
strat_time = time.time()           
threads = []

with ThreadPoolExecutor(max_workers = 77) as executor:
    for i in range(77):
        thread = executor.submit(get_post, i)
        threads.append(thread)
        
for thread in threads:
    thread.result()
    
with open('posts.json', 'w') as f:
    json.dump(posts, f, indent=4)
    
print(f"End time: {time.time() - strat_time}")