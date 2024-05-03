import time
import os
import requests
from lxml import etree as ET
import json

NOW = time.localtime()
YEAR = NOW.tm_year
MONTH = NOW.tm_mon
DAY_OF_MONTH = NOW.tm_mday
DAY_OF_WEEK = NOW.tm_wday

def map_weekday(day_of_week: int) -> str:
    map = {
        0: "星期一",
        1: "星期二",
        2: "星期三",
        3: "星期四",
        4: "星期五",
        5: "星期六",
        6: "星期日",
    }
    
    return map[day_of_week]

def create_dir_not_exist(dir: str):
    if os.path.exists(dir):
        return False
    
    os.mkdir(dir)
    return True
    
src_dir = "src"
summary_md = "SUMMARY.md"
root_summary_md = os.path.join(src_dir, summary_md)

path = os.path.join(src_dir, str(YEAR))
is_first_year = create_dir_not_exist(path)

path = os.path.join(path, str(MONTH))
is_first_month = create_dir_not_exist(path)

path = os.path.join(path, str(DAY_OF_MONTH))
is_first_day = create_dir_not_exist(path)

def line(msg: str = "") -> str:
    return msg + "\n"

with open(root_summary_md, "a") as f:
    if is_first_year:
        f.write(line(f"- [{YEAR}年]({os.path.join(str(YEAR), summary_md)})"))
        
    if is_first_month:
        f.write(line(f"    - [{MONTH}月]({os.path.join(str(YEAR), str(MONTH), summary_md)})"))
            
    if is_first_day:
        f.write(line(f"        - [{DAY_OF_MONTH}日]({os.path.join(str(YEAR), str(MONTH), str(DAY_OF_MONTH), summary_md)})"))
        
with open(os.path.join(src_dir, str(YEAR), summary_md), "a") as f:
    if is_first_month:
        f.write(line(f"- [{MONTH}月]({os.path.join(str(MONTH), summary_md)})"))
        
with open(os.path.join(src_dir, str(YEAR), str(MONTH), summary_md), "a") as f:
    if is_first_day:
        f.write(line(f"- [{DAY_OF_MONTH}日]({os.path.join(str(DAY_OF_MONTH), summary_md)})"))

with open(os.path.join(src_dir, str(YEAR), str(MONTH), str(DAY_OF_MONTH), summary_md), "a") as f:
    if is_first_day:
        f.write(line(f"#### {YEAR}-{MONTH}-{DAY_OF_MONTH}({map_weekday(DAY_OF_WEEK)})"))
        f.write(line())

# fetch news helper

def append_to_root_md(name: str):
    with open(os.path.join(root_summary_md), "a") as f:
        demo_md = os.path.join(str(YEAR), str(MONTH), str(DAY_OF_MONTH), f"{name}.md")
        f.write(line(f"            - [{name}]({demo_md})"))
        
def append_to_today_md(today: str, name: str):
    with open(os.path.join(today, summary_md), "a") as f:
        f.write(line(f"- [{name}]({name}.md)"))

# start fetch news

def fetch_hot_api(today: str, name: str):
    md = os.path.join(today, f"{name}.md")
    if not os.path.exists(md):
        append_to_root_md(name)
        append_to_today_md(today, name)
        
    url = f"https://api-hot.efefee.cn/{name}?cache=true"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Connection": "keep-alive",
        "Host": "api-hot.efefee.cn",
        "Origin": "https://hot.imsyy.top",
        "Referer": "https://hot.imsyy.top/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    }
    data = requests.get(url, headers=headers).json()["data"]
    
    items = []
    for item in data:
        title = item["title"]
        desc = item.get("desc")
        if desc is None:
            desc = "> no description"
        author = item.get("author")
        if author is None:
            author = "no author"
        url = item["url"]
        lines = desc.splitlines()
        new_lines = []
        for single in lines:
            single = "> " + single
            new_lines.append(single)
        desc = "\n".join(new_lines)
        
        new_item = ""
        new_item += line(f"## [{title}]({url})")
        new_item += line("")
        new_item += line(f"author: {author}")
        new_item += line("")
        new_item += line(f"{desc}" if len(desc) > 0 else "> no description")
        new_item += line("---")
        new_item += line()
        items.append(new_item)
    
    with open(md, "w") as f:
        for item in items:
            f.write(item)

def fetch_news(today: str):
    api_names = [
        "bilibili",
        "weibo",
        "douyin",
        "zhihu",
        "36kr",
        "baidu",
        "sspai",
        "ithome",
        "thepaper",
        "toutiao",
        "tieba",
        "qq-news",
        "netease-news",
    ]
    
    for name in api_names:
        fetch_hot_api(today, name)

fetch_news(os.path.join(src_dir, str(YEAR), str(MONTH), str(DAY_OF_MONTH)))
