import time
import os

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

path = os.path.join(src_dir, str(YEAR))
is_first_year = create_dir_not_exist(path)
year_md = os.path.join(path, "SUMMARY.md")
year_rel = os.path.join(str(YEAR), "SUMMARY.md")

path = os.path.join(path, str(MONTH))
is_first_month = create_dir_not_exist(path)
month_md = os.path.join(path, "SUMMARY.md")
month_rel = os.path.join(str(MONTH), "SUMMARY.md")

today_md = os.path.join(path, str(DAY_OF_MONTH) + ".md")
today_exists = os.path.exists(today_md)
summary_md = os.path.join(src_dir, "SUMMARY.md")

def fetch_news() -> str:
    news = ""
    news += f"{map_weekday(DAY_OF_WEEK)}\n"
    news += "## 你好\n"
    
    return news

news = fetch_news()
with open(today_md, "w") as f:
    f.write(news)

relative_path = os.path.join(str(DAY_OF_MONTH) + ".md")
with open(summary_md, "a") as f:
    if is_first_year:
        f.write(f"- [{YEAR}年]({year_rel})\n")
        
    if is_first_month:
        with open(year_md, "a") as yf:
            yf.write(f"- [{MONTH}月]({month_rel})\n")
            
        month_rel = os.path.join(str(YEAR), month_rel)
        f.write(f"    - [{MONTH}月]({month_rel})\n")
        
    if not today_exists:
        with open(month_md, "a") as mf:
            mf.write(f"- [{DAY_OF_MONTH}日]({relative_path})\n")
            
    if not today_exists:
        day_rel = os.path.join(str(YEAR), str(MONTH), relative_path)
        f.write(f"        - [{DAY_OF_MONTH}日]({day_rel})\n")
