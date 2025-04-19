from pathlib import Path

def write_env(path: Path, values: dict):
    with open(path, 'w') as f:
        for k, v in values.items():
            f.write(f"{k}='{v}'\n")

def print_header(title):
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))
