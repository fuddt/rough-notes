import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QTableView, QListWidget,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import QStringListModel, Qt


SAVE_FILE = "folder_paths.txt"  # フォルダパス保存用ファイル


class FolderViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("フォルダプレビュー")
        self.resize(800, 600)

        # --- メインレイアウト（横並び） ---
        main_layout = QHBoxLayout(self)

        # --- 左側：フォルダパス一覧 ---
        self.folder_model = QStringListModel()
        self.folder_table = QTableView()
        self.folder_table.setModel(self.folder_model)
        self.folder_table.setEditTriggers(QTableView.NoEditTriggers)
        self.folder_table.clicked.connect(self.on_folder_selected)

        # --- 右側：ファイル一覧 ---
        self.file_list = QListWidget()

        # --- 下部：フォルダ追加用ボタン ---
        self.add_button = QPushButton("フォルダを追加")
        self.add_button.clicked.connect(self.select_folder_dialog)

        # --- 左側まとめレイアウト ---
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.folder_table)
        left_layout.addWidget(self.add_button)

        # --- メインレイアウトに追加 ---
        main_layout.addLayout(left_layout, 2)
        main_layout.addWidget(self.file_list, 3)

        # 起動時にファイルから復元
        self.load_paths_from_file()

    def select_folder_dialog(self):
        # フォルダ選択ダイアログを表示
        folder = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        if folder:
            self.add_folder_path(folder)

    def add_folder_path(self, path):
        path = path.strip()
        if not os.path.isdir(path):
            QMessageBox.warning(self, "エラー", "存在しないフォルダパスです")
            return

        current = self.folder_model.stringList()
        if path not in current:
            current.append(path)
            self.folder_model.setStringList(current)
            self.save_paths_to_file(current)

    def on_folder_selected(self, index):
        path = self.folder_model.stringList()[index.row()]
        self.show_files_in_folder(path)

    def show_files_in_folder(self, folder_path):
        self.file_list.clear()
        try:
            for name in os.listdir(folder_path):
                full_path = os.path.join(folder_path, name)
                if os.path.isfile(full_path):
                    self.file_list.addItem(name)
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"フォルダの読み込み中にエラーが発生しました:\n{e}")

    def save_paths_to_file(self, paths):
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                for p in paths:
                    f.write(p + "\n")
        except Exception as e:
            QMessageBox.warning(self, "保存エラー", f"ファイル保存に失敗しました：\n{e}")

    def load_paths_from_file(self):
        if not os.path.exists(SAVE_FILE):
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                paths = [line.strip() for line in f if line.strip()]
                self.folder_model.setStringList(paths)
        except Exception as e:
            QMessageBox.warning(self, "読み込みエラー", f"ファイル読み込みに失敗しました：\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = FolderViewer()
    viewer.show()
    sys.exit(app.exec_())