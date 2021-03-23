#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uncurl

# 将curl命令转换成python代码
cmd = """curl 'https://www.jianshu.com/u/66ffe8731054' \
  -H 'Connection: keep-alive' \
  -H 'Cache-Control: max-age=0' \
  -H 'sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'Sec-Fetch-Site: none' \
  -H 'Sec-Fetch-Mode: navigate' \
  -H 'Sec-Fetch-User: ?1' \
  -H 'Sec-Fetch-Dest: document' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Cookie: read_mode=day; default_font=font2; locale=zh-CN; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1616237295; __yadk_uid=ynf9cBVSMNLLsCZzCeKyg7tsQHodqm8B; web_login_version=MTYxNjIzNzMyOA%3D%3D--d359cc29a88014cd936a9af99bd35db45a669991; _ga=GA1.2.1476924542.1616237344; remember_user_token=W1sxMjI0MTIyNl0sIiQyYSQxMSRZNk1ESFBXbHNqYlhVSjEuTjM2bWcuIiwiMTYxNjQyOTk2MC45NzI0NTgxIl0%3D--f2fad88d4e055ce210350d8082be86b075ddcf75; _m7e_session_core=d100c914638dc090d837d9b63f072033; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221784f3ff75853c-0c274aca237e5-5771031-1327104-1784f3ff7599a3%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221784f3ff75853c-0c274aca237e5-5771031-1327104-1784f3ff7599a3%22%7D; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1616429971' \
  -H 'If-None-Match: W/"f44091782b9faf76ebeaca98cfd8b7b7"' \
  --compressed"""

result = uncurl.parse(cmd)
print(result)
"""
result:
requests.get("https://www.jianshu.com/u/66ffe8731054",
    headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "If-None-Match": "W/\"f44091782b9faf76ebeaca98cfd8b7b7\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0"
    },
    cookies={
        "Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068": "1616429971",
        "Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068": "1616237295",
        "__yadk_uid": "ynf9cBVSMNLLsCZzCeKyg7tsQHodqm8B",
        "_ga": "GA1.2.1476924542.1616237344",
        "_m7e_session_core": "d100c914638dc090d837d9b63f072033",
        "default_font": "font2",
        "locale": "zh-CN",
        "read_mode": "day",
        "remember_user_token": "W1sxMjI0MTIyNl0sIiQyYSQxMSRZNk1ESFBXbHNqYlhVSjEuTjM2bWcuIiwiMTYxNjQyOTk2MC45NzI0NTgxIl0%3D--f2fad88d4e055ce210350d8082be86b075ddcf75",
        "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%221784f3ff75853c-0c274aca237e5-5771031-1327104-1784f3ff7599a3%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221784f3ff75853c-0c274aca237e5-5771031-1327104-1784f3ff7599a3%22%7D",
        "web_login_version": "MTYxNjIzNzMyOA%3D%3D--d359cc29a88014cd936a9af99bd35db45a669991"
    },
)
"""
