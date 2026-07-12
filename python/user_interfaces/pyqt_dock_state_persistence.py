from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QTextEdit
)
from PyQt5.QtCore import QSettings, QTimer, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dock状態の復元テスト")

        # QSettings: OSごとに適切な場所に保存してくれる
        self.settings = QSettings("MyCompany", "MyApp")

        # 中央ウィジェット
        self.setCentralWidget(QTextEdit("中央エリア"))

        # Dockの作成
        self.dock = QDockWidget("ドック", self)
        self.dock.setWidget(QTextEdit("ドック内エディタ"))
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)

    def closeEvent(self, event):
        """
        ウィンドウ終了時にDockの状態を保存
        """
        self.settings.setValue("mainWindow/state", self.saveState())
        super().closeEvent(event)

    def restore_dock_state(self):
        """
        最大化完了後に呼んでDockの状態を復元
        """
        state = self.settings.value("mainWindow/state")
        if state is not None:
            self.restoreState(state)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    # 1. まず最大化
    window.showMaximized()
    # 2. 最大化が確定してからDockの状態を復元
    QTimer.singleShot(0, window.restore_dock_state)

    app.exec_()