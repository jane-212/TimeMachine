import time
import os
import requests
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

def fetch_ten_api(today, name):
    md = os.path.join(today, f"{name}.md")
    if not os.path.exists(md):
        append_to_root_md(name)
        append_to_today_md(today, name)
        
    url = f"https://tenapi.cn/v2/{name}"
    data = requests.get(url).json()["data"]
    
    items = []
    for item in data:
        title = item["name"]
        url = item["url"]
        news_time = time.localtime()
        news_time = time.strftime("%Y-%m-%d %H:%M:%S", news_time)
        
        news = ""
        news += line(f"## [{title}]({url})")
        news += line()
        news += line(f"{news_time}")
        news += line()
        news += line("---")
        
        items.append(news)
        
    with open(md, "w") as f:
        for news in items:
            f.write(news)

def fetch_news(today: str):
    tens = [
        "baiduhot",
        "douyinhot",
        "weibohot",
        "zhihuhot",
        "bilihot",
        "toutiaohot",
    ]
    
    for ten in tens:
        print(f"fetch {ten}")
        fetch_ten_api(today, ten)
        time.sleep(3)

fetch_news(os.path.join(src_dir, str(YEAR), str(MONTH), str(DAY_OF_MONTH)))
