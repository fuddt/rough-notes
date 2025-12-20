import tempfile
import os
import shutil

# テスト用の関数
def copy_file(source_dir, target_dir, filename):
    source_file = os.path.join(source_dir, filename)
    target_file = os.path.join(target_dir, filename)
    shutil.copy(source_file, target_file)

# テストケース
def test_copy_files_without_with():
    # 一時ディレクトリを手動で作成
    dir_A = tempfile.TemporaryDirectory()
    dir_B = tempfile.TemporaryDirectory()

    try:
        # ディレクトリAにファイルを作成
        filename = "test_file.txt"
        file_path_A = os.path.join(dir_A.name, filename)
        with open(file_path_A, "w") as f:
            f.write("This is a test file.")

        # ファイルが正しく作成されたか確認
        assert os.path.exists(file_path_A), "File should exist in directory A"

        # ファイルをAからBへコピー
        copy_file(dir_A.name, dir_B.name, filename)

        # Bにファイルが正しくコピーされたか確認
        file_path_B = os.path.join(dir_B.name, filename)
        assert os.path.exists(file_path_B), "File should exist in directory B after copy"
        with open(file_path_B, "r") as f:
            content = f.read()
            assert content == "This is a test file.", "Content should be the same after copy"

        print("Test passed!")

    finally:
        # 一時ディレクトリをクリーンアップ（削除）
        dir_A.cleanup()
        dir_B.cleanup()

# テスト実行
test_copy_files_without_with()
