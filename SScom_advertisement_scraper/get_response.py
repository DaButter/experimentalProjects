import requests


def get_ss_resp(payload, request_url, fname_old, fname_new):
    # Debug
    print("New file name: " + fname_old)
    print("Old file name: " + fname_new)
    print("Request URL: " + request_url)

    # Get the value of the PHPSESSID cookie from the response headers
    response = requests.get('https://www.ss.com')
    phpsessid = response.cookies.get('PHPSESSID')
    print("New PHP sessionID: " + phpsessid)

    # Should get new sid?
    # sid_data = response.cookies.get
    # print(sid_data)

    headers_post = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,lv;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f'LG=lv; sid_c=1; sid=afde21d4090be532ac719cf86f3d4c670e351cd88a4f6c40be2d85dea40263c7f61fbd77aa4f585487d92d18d7c39876; PHPSESSID={phpsessid}',
        'origin': 'https://www.ss.com',
        'referer': 'https://www.ss.com/lv/real-estate/flats/riga/centre/sell/filter/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
    }
    requests.post(request_url, data=payload, headers=headers_post)

    # use the same sessionID to use GET ws
    headers_get = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,lv;q=0.8',
        'Cache-Control': 'max-age=0',
        'Cookie': f'LG=lv; sid_c=1; sid=afde21d4090be532ac719cf86f3d4c670e351cd88a4f6c40be2d85dea40263c7f61fbd77aa4f585487d92d18d7c39876; PHPSESSID={phpsessid}',
        'DNT': '1',
        'Referer': 'https://www.ss.com/lv/real-estate/flats/riga/centre/sell/filter/',
        'Sec-Ch-Ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
    }
    response_get = requests.get(request_url, headers=headers_get)
    with open(fname_new, 'w', encoding='utf-8') as f:
        f.write(response_get.text)
    f.close()