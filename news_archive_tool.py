# 游戏新闻归档小工具 - 练手脚本 #2（升级版）
# 功能：扫描 游戏新闻/ 目录下的每日简报，统计数量、日期范围、各文件大小、每份简报的新闻条数
# 用法：python news_archive_tool.py
# 说明：只用 Python 标准库，无需安装任何第三方包
#
# v1 → v2 变更：
#   - 新增：按日期倒序排列（最新的排最前面）
#   - 新增：统计每份简报中的新闻条数（以 "- " 开头的行）

import os
import glob
from datetime import datetime

# 简报所在目录：本脚本在 claw-practice/ 下，游戏新闻在它的上一级目录
NEWS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "游戏新闻")


def count_news_items(filepath):
    """统计一份 .md 文件中以 '- ' 开头的行数，作为新闻条目数的近似值"""
    count = 0
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("- ") or line.startswith("  - "):
                    count += 1
    except Exception:
        pass
    return count


def main():
    # 1) 找到所有 .md 文件，按文件名**倒序**排列（最新日期排最前）
    files = sorted(glob.glob(os.path.join(NEWS_DIR, "*.md")), reverse=True)

    if not files:
        print("没有找到任何简报文件。")
        return

    print(f"共找到 {len(files)} 份简报（按日期倒序）：\n")

    total_size = 0
    total_news = 0
    dates = []

    # 2) 逐个文件读取信息
    for path in files:
        name = os.path.basename(path)
        size = os.path.getsize(path)
        total_size += size

        news_count = count_news_items(path)
        total_news += news_count

        # 从文件名解析日期，例如 2026-07-24.md
        date_str = name.replace(".md", "")
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d")
            dates.append(d)
            date_display = d.strftime("%Y年%m月%d日")
        except ValueError:
            date_display = "（文件名非日期格式）"

        print(f"  - {name}  |  {size:>7} 字节  |  {date_display}  |  约 {news_count} 条新闻")

    # 3) 输出汇总
    print()
    print(f"简报总数：{len(files)}")
    print(f"占用空间：{total_size} 字节（约 {total_size / 1024:.1f} KB）")
    print(f"新闻总条数（估算）：约 {total_news} 条")

    if dates:
        print(f"日期范围：{min(dates).strftime('%Y-%m-%d')} ~ {max(dates).strftime('%Y-%m-%d')}")


if __name__ == "__main__":
    main()
