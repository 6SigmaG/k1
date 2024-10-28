import pandas as pd
from itertools import product
from datetime import datetime
import os

def read_keywords(file_name):
    df = pd.read_excel(file_name)
    keywords = {}
    for col in df.columns:
        keywords[col] = [str(kw).strip().lower() for kw in df[col].dropna() if str(kw).strip()]
    return {k: v for k, v in keywords.items() if v}  # 移除空列

def generate_combinations(keywords):
    return list(product(*keywords.values()))

def format_combination(combination, keywords):
    unique_kw = {}
    for kw, col in zip(combination, keywords.keys()):
        if kw.strip() and kw not in unique_kw:
            unique_kw[kw] = None
    if len(unique_kw) == len(keywords):
        return ' '.join(f'"{kw}"' for kw in unique_kw.keys())
    return None

def remove_duplicates(combinations):
    seen = set()
    unique = []
    for combo in combinations:
        identifier = tuple(sorted(combo.split()))
        if identifier not in seen:
            seen.add(identifier)
            unique.append(combo)
    return unique

def save_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    print(f"执行完毕，已保存至 {filename}")

def normal_mode(keywords):
    combinations = generate_combinations(keywords)
    formatted = [format_combination(combo, keywords) for combo in combinations]
    formatted = [f for f in formatted if f]  # 移除None值
    unique_combinations = remove_duplicates(formatted)
    filename = f"{datetime.now().strftime('%Y%m%d')}_普通模式.txt"
    save_to_file(filename, unique_combinations)

def site_mode(keywords):
    tlds = []
    while True:
        tld = input("请输入国家顶级域名后缀，如au、br等（停止输入请输入No）: ")
        if tld.lower() == 'no':
            break
        tlds.append(tld.lower())

    combinations = generate_combinations(keywords)
    all_results = []

    for tld in tlds:
        formatted = [f"site:.{tld} {format_combination(combo, keywords)}" for combo in combinations]
        formatted = [f for f in formatted if f and f.count('"') == 2 * len(keywords)]  # 确保每列都有关键词
        unique_combinations = remove_duplicates(formatted)
        filename = f"{datetime.now().strftime('%Y%m%d')}_{tld}_site模式.txt"
        save_to_file(filename, unique_combinations)
        all_results.extend(unique_combinations)

    all_filename = f"{datetime.now().strftime('%Y%m%d')}_all_site模式.txt"
    save_to_file(all_filename, remove_duplicates(all_results))

def inurl_mode(keywords):
    inurls = []
    while True:
        inurl = input("请输入内容，如products/services/Industries/solutions/about等（停止输入请输入No）: ")
        if inurl.lower() == 'no':
            break
        inurls.append(inurl.lower())

    combinations = generate_combinations(keywords)
    all_results = []

    for inurl in inurls:
        formatted = [f"inurl:{inurl} {format_combination(combo, keywords)}" for combo in combinations]
        formatted = [f for f in formatted if f and f.count('"') == 2 * len(keywords)]  # 确保每列都有关键词
        unique_combinations = remove_duplicates(formatted)
        filename = f"{datetime.now().strftime('%Y%m%d')}_{inurl}_inurl模式.txt"
        save_to_file(filename, unique_combinations)
        all_results.extend(unique_combinations)

    all_filename = f"{datetime.now().strftime('%Y%m%d')}_all_inurl模式.txt"
    save_to_file(all_filename, remove_duplicates(all_results))

def site_inurl_mode(keywords):
    tlds = []
    while True:
        tld = input("请输入国家顶级域名后缀，如au、br等（停止输入请输入No）: ")
        if tld.lower() == 'no':
            break
        tlds.append(tld.lower())

    inurls = []
    while True:
        inurl = input("请输入内容，如products/services/Industries/solutions/about等（停止输入请输入No）: ")
        if inurl.lower() == 'no':
            break
        inurls.append(inurl.lower())

    combinations = generate_combinations(keywords)
    all_results = []

    for tld in tlds:
        for inurl in inurls:
            formatted = [f"site:.{tld} inurl:{inurl} {format_combination(combo, keywords)}" for combo in combinations]
            formatted = [f for f in formatted if f and f.count('"') == 2 * len(keywords)]  # 确保每列都有关键词
            all_results.extend(formatted)

    unique_results = remove_duplicates(all_results)
    filename = f"{datetime.now().strftime('%Y%m%d')}_all_site+inurl模式.txt"
    save_to_file(filename, unique_results)

def main():
    if not os.path.exists('keywords.xlsx'):
        print("错误：找不到 'keywords.xlsx' 文件。请确保该文件在当前目录中。")
        return

    keywords = read_keywords('keywords.xlsx')

    if not keywords:
        print("错误：无法从 'keywords.xlsx' 读取有效的关键词。")
        return

    while True:
        print("\n本程序为【严格组合版】请选择一个模式：")
        print("【1】普通模式")
        print("【2】site模式")
        print("【3】inurl模式")
        print("【4】site+inurl模式")
        print("【0】退出程序")

        choice = input("请输入对应数字: ")

        if choice == '1':
            normal_mode(keywords)
        elif choice == '2':
            site_mode(keywords)
        elif choice == '3':
            inurl_mode(keywords)
        elif choice == '4':
            site_inurl_mode(keywords)
        elif choice == '0':
            print("程序已退出。")
            break
        else:
            print("无效的选择，请重新输入。")

if __name__ == "__main__":
    main()