import json
from collections import defaultdict


def find_duplicate_ids(jsonl_file):
    # 用于记录每个 id 出现的行号
    id_to_lines = defaultdict(list)

    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line.strip())
                if "id" in data:
                    id_value = data["id"]
                    id_to_lines[id_value].append(line_num)
            except json.JSONDecodeError:
                print(f"警告：第 {line_num} 行不是有效的 JSON，已跳过。")

    # 筛选出重复的 id
    duplicates = {
        id_val: lines for id_val, lines in id_to_lines.items() if len(lines) > 1
    }

    return duplicates


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description="检查JSONL文件中的重复ID")
    parser.add_argument("jsonl_file", help="要检查的JSONL文件路径")
    return parser.parse_args()


def main():
    args = parse_args()
    duplicates = find_duplicate_ids(args.jsonl_file)

    if duplicates:
        print("发现重复的 id：")
        for id_val, lines in duplicates.items():
            print(f"id '{id_val}' 在以下行重复出现: {lines}")
    else:
        print("未发现重复的 id。")


if __name__ == "__main__":
    main()
