import os
import shutil
import re

# 📂 プロジェクトのルートディレクトリ
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 📂 main.py のパス
MAIN_FILE_PATH = os.path.join(PROJECT_ROOT, "installer", "src", "main.py")

# 📂 ソースコードのディレクトリ（スクリプトを探す場所）
SRC_DIR = os.path.join(PROJECT_ROOT, "installer", "src", "method")

# 📂 アーカイブディレクトリ
ARCHIVE_DIR = os.path.join(PROJECT_ROOT, "archive")

# 🔍 import 文の正規表現
IMPORT_PATTERN = re.compile(r"^(?:from|import) ([\w.]+)")

# 🚀 1. `import` されているファイルを **再帰的** に取得
def get_imported_files(file_path, checked_files=None):
    if checked_files is None:
        checked_files = set()

    # すでにチェック済みならスキップ
    if file_path in checked_files:
        return checked_files

    checked_files.add(file_path)

    # ファイル名を取得
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    # ファイルを開いて `import` を解析
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = IMPORT_PATTERN.match(line.strip())
            if match:
                imported_module = match.group(1).split(".")[0]

                # `method/` 内のファイルと一致するものがあるか確認
                for root, _, files in os.walk(SRC_DIR):
                    for file in files:
                        if file.endswith(".py") and os.path.splitext(file)[0] == imported_module:
                            imported_path = os.path.join(root, file)
                            get_imported_files(imported_path, checked_files)

    return checked_files

# 🚀 2. `method/` 内の全 Python ファイルを取得
def get_all_source_files():
    source_files = {}

    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]
                source_files[module_name] = file_path

    return source_files

# 🚀 3. 使われていないファイルを `archive/` に移動
def move_unused_files():
    # `main.py` から **再帰的に import されているファイル**
    imported_files = get_imported_files(MAIN_FILE_PATH)
    source_files = get_all_source_files()

    # アーカイブフォルダを作成（なければ）
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    moved_files = []
    for module, file_path in source_files.items():
        if file_path not in imported_files:
            archive_path = os.path.join(ARCHIVE_DIR, os.path.basename(file_path))
            shutil.move(file_path, archive_path)
            moved_files.append(file_path)

    return moved_files

# 🏃 実行
if __name__ == "__main__":
    unused_files = move_unused_files()
    if unused_files:
        print(f"✅ {len(unused_files)} 個の未使用ファイルを 'archive/' に移動しました。")
    else:
        print("🎉 すべてのファイルが 'main.py' で使用されています。")
