import os
import curses

def list_files(directory):
    """ 指定したディレクトリのファイル一覧を取得 """
    return os.listdir(directory)

def main(stdscr, directory):
    curses.curs_set(0)  # カーソルを非表示にする
    stdscr.clear()

    # ファイル一覧を取得
    files = list_files(directory)
    if not files:
        stdscr.addstr(0, 0, "フォルダにファイルがありません")
        stdscr.refresh()
        stdscr.getch()
        return

    # 選択中のインデックス
    current_index = 0

    while True:
        stdscr.clear()

        # ファイル一覧を描画
        for idx, file in enumerate(files):
            if idx == current_index:
                # カーソル位置（選択中のファイル）
                stdscr.addstr(idx, 0, f"> {file}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx, 0, f"  {file}")

        stdscr.refresh()

        # キー入力を待つ
        key = stdscr.getch()

        # 矢印キーの処理
        if key == curses.KEY_UP and current_index > 0:
            current_index -= 1
        elif key == curses.KEY_DOWN and current_index < len(files) - 1:
            current_index += 1
        elif key == ord('\n'):
            # Enterキーが押されたら選択を確定
            stdscr.addstr(len(files), 0, f"選択: {files[current_index]}")
            stdscr.refresh()
            stdscr.getch()  # 確認のためにもう一度キー入力を待つ
            break

if __name__ == "__main__":
    # 対象のディレクトリ
    directory = "./"  # ここをリストしたいフォルダに変更する
    curses.wrapper(main, directory)