import os
import zipfile

def create_zip_with_subdirectories(zip_name, directories):
    """
    指定されたディレクトリを `data/` 配下に格納したZIPファイルを作成。

    Parameters:
        zip_name (str): 作成するZIPファイル名
        directories (list): 圧縮対象のディレクトリリスト
    """
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for directory in directories:
            if os.path.isdir(directory):
                for root, dirs, files in os.walk(directory):
                    # ZIP内のパスを作成 (data/ 以下に配置)
                    relative_path = os.path.relpath(root, os.path.dirname(directory))
                    zip_path = os.path.join("data", relative_path)
                    # ファイルを圧縮
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.join(zip_path, file)
                        zipf.write(file_path, arcname)
            else:
                print(f"Warning: '{directory}' はディレクトリではありません。スキップします。")

# 使用例
directories_to_zip = ['A', 'B']  # 圧縮したいディレクトリ
zip_file_name = 'data.zip'      # 作成するZIPファイル名

create_zip_with_subdirectories(zip_file_name, directories_to_zip)

print(f"{zip_file_name} が作成されました！")

import os
import zipfile
import pandas as pd
import io

def process_csv_and_create_zip(zip_name, directories, modify_function):
    """
    CSVファイルを処理し、変更したデータをZIPに格納する。
    元ファイルは変更せず、変更後のデータはメモリ上で管理。

    Parameters:
        zip_name (str): 作成するZIPファイル名
        directories (list): 圧縮対象のディレクトリリスト
        modify_function (function): CSVを処理する関数。pandasのDataFrameを引数に取り、処理後のDataFrameを返す。
    """
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for directory in directories:
            if os.path.isdir(directory):
                for root, dirs, files in os.walk(directory):
                    relative_path = os.path.relpath(root, os.path.dirname(directory))
                    zip_path = os.path.join("data", relative_path)

                    for file in files:
                        if file.endswith(".csv"):  # CSVファイルのみ対象
                            file_path = os.path.join(root, file)

                            # CSVファイルを読み込み、処理
                            df = pd.read_csv(file_path)
                            modified_df = modify_function(df)

                            # DataFrameをメモリ上に書き込み
                            csv_buffer = io.StringIO()
                            modified_df.to_csv(csv_buffer, index=False)
                            csv_buffer.seek(0)

                            # ZIPにメモリ上のデータを追加
                            arcname = os.path.join(zip_path, file)
                            zipf.writestr(arcname, csv_buffer.getvalue())
                        else:
                            # CSV以外のファイルはそのままZIPに追加
                            file_path = os.path.join(root, file)
                            arcname = os.path.join(zip_path, file)
                            zipf.write(file_path, arcname)

# CSVを処理するサンプル関数（例: 全ての値を大文字に変換）
def modify_csv(df):
    return df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# 使用例
directories_to_zip = ['A', 'B']  # 圧縮対象のディレクトリ
zip_file_name = 'data.zip'      # 作成するZIPファイル名

process_csv_and_create_zip(zip_file_name, directories_to_zip, modify_csv)

print(f"{zip_file_name} が作成されました！")


import os
import zipfile
import pandas as pd
import io

def create_zip_with_cp932(zip_name, directories, modify_function):
    """
    CP932エンコーディングで保存し、日本語の文字化けを防いだZIPファイルを作成。

    Parameters:
        zip_name (str): 出力するZIPファイル名
        directories (list): 圧縮対象のディレクトリリスト
        modify_function (function): CSVファイルを処理する関数
    """
    with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for directory in directories:
            if os.path.isdir(directory):
                for root, dirs, files in os.walk(directory):
                    relative_path = os.path.relpath(root, os.path.dirname(directory))
                    zip_path = os.path.join("data", relative_path)

                    for file in files:
                        if file.endswith(".csv"):  # CSVファイルのみ処理
                            file_path = os.path.join(root, file)
                            df = pd.read_csv(file_path, encoding='cp932')  # 元CSVをcp932で読み込む
                            modified_df = modify_function(df)

                            # メモリ上にCSVをcp932で保存
                            csv_buffer = io.BytesIO()
                            modified_df.to_csv(csv_buffer, index=False, encoding='cp932')
                            csv_buffer.seek(0)

                            # バイナリデータをZIPファイルに保存
                            arcname = os.path.join(zip_path, file)
                            zipf.writestr(arcname, csv_buffer.read())
                        else:
                            # CSV以外のファイルをそのまま追加
                            file_path = os.path.join(root, file)
                            arcname = os.path.join(zip_path, file)
                            zipf.write(file_path, arcname)

# サンプル関数：CSVを加工する（例: 文字列を大文字に変換）
def modify_csv(df):
    return df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# 使用例
directories_to_zip = ['A', 'B']  # 圧縮対象ディレクトリ
zip_file_name = 'data_cp932.zip'

create_zip_with_cp932(zip_file_name, directories_to_zip, modify_csv)

print(f"{zip_file_name} が作成されました！")
