#!/usr/bin/python3
# coding: utf-8
import requests
import sys
import json

session = requests.Session()


def ig_filter(data):
    urls = []

    if len(data) != 0:
        insta_core = data["graphql"]["shortcode_media"]
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
    url = url.split("?")[0] + "?__a=1"
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
    headers = {
        "user-agent": ua
    }
    res_data = session.get(url, headers=headers)
    return ig_filter(res_data.json())


def main():
    # https://www.instagram.com/p/CNFV0Bsgrew/
    url = sys.argv[1]
    results = ig_download(url)
    print(json.dumps(results))


if __name__ == "__main__":
    main()
