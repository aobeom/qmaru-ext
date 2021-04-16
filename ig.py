#!/usr/bin/python3
# coding: utf-8
import requests
import sys
import json
import os
import re


work_dir = os.path.dirname((os.path.abspath(__file__)))
cfg_path = os.path.join(work_dir, "config.json")

session = requests.Session()


def get_cfg():
    with open(cfg_path, encoding="utf-8") as f:
        data = json.loads(f.read())
    ig_cfg = data["ig"]
    return ig_cfg["username"], ig_cfg["password"]


def ig_filter(data):
    urls = []

    rule1 = r'window._sharedData = (.*?);'
    rule2 = r'window.__additionalDataLoaded\((.*?)\);'

    raw_data = re.findall(rule1, data)
    if len(raw_data) != 0:
        raw_data = raw_data[0]
        main_json = json.loads(raw_data)
        try:
            entry_data_data = main_json["entry_data"]["PostPage"][0]
        except BaseException:
            return []
        if entry_data_data:
            insta_core = main_json["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
        else:
            raw_data = re.findall(rule2, data)
            raw_data = raw_data[0]
            load_data = raw_data.split(",")
            main_data = ','.join(load_data[1:])
            main_json = json.loads(main_data)
            insta_core = main_json["graphql"]["shortcode_media"]

        if insta_core.get("edge_sidecar_to_children"):
            insta_content = insta_core["edge_sidecar_to_children"]["edges"]
            for ins_c in insta_content:
                insta_node = ins_c["node"]
                if insta_node["__typename"] == "GraphImage":
                    urls.append(insta_node["display_url"])
                elif insta_node["__typename"] == "GraphVideo":
                    urls.append(insta_node["video_url"])
        else:
            insta_type = insta_core["is_video"]
            if insta_type:
                urls.append(insta_core["video_url"])
            else:
                urls.append(insta_core["display_url"])
    return urls


def ig_download(url):
    # Thanks https://github.com/arc298/instagram-scraper
    BASE_URL = 'https://www.instagram.com/'
    LOGIN_URL = BASE_URL + 'accounts/login/ajax/'
    STORIES_UA = 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'
    PC_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"

    username, password = get_cfg()
    # 获取 csrftoken
    session.headers.update({"Referer": BASE_URL, "user-agent": STORIES_UA})
    res_base = session.get(BASE_URL)
    # 更新 csrftoken
    session.headers.update({"X-CSRFToken": res_base.cookies["csrftoken"]})
    # 登录账号 获取认证
    login_data = {"username": username, "password": password}
    res_login = session.post(LOGIN_URL, data=login_data)
    session.headers.update({"X-CSRFToken": res_login.cookies["csrftoken"]})
    login_cookies = res_login.cookies
    # 使用 cookies
    session.headers.update({'user-agent': PC_UA})
    res_data = session.get(url, cookies=login_cookies)
    return ig_filter(res_data.text)


def main():
    # https://www.instagram.com/p/CNFV0Bsgrew/
    # url = sys.argv[1]
    # results = ig_download(url)
    print(json.dumps([]))


if __name__ == "__main__":
    main()
