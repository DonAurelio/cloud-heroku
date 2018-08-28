import requests

def request_videos_for_processing():
    port = 8000
    tenants_domain_url = []
    pending_videos_urls = []
    response = requests.get(r'http://localhost:8000/client/list/json')

    if response.status_code == 200:
        tenants_domain_url = response.json()
        
        for domain_url in tenants_domain_url:
            response = requests.get(f'http://{domain_url}:{port}/client/list/json')
            pending_videos_urls.append(response.json())

    return pending_videos_urls

print('Pending videos urls...')
print(pending_videos_urls)
