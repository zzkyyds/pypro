with open("pyProject/tmp.txt", "r",encoding='utf-8') as f:
    lines = f.readlines()

with open("pyProject/tmp.txt", "w",encoding='utf-8') as f:
    for i, line in enumerate(lines, start=1):
        f.write(f"[{i}] {line}")
