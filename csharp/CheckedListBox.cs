using System;
using System.Windows.Forms;

public class NonActivatedForm : Form
{
    // 子フォームが表示されてもアクティブにならないようにするために
    // CreateParams をオーバーライドして WS_EX_NOACTIVATE を追加する
    protected override CreateParams CreateParams
    {
        get
        {
            // 基本のパラメータを取得
            CreateParams cp = base.CreateParams;
            // WS_EX_NOACTIVATE の値 0x08000000 を ExStyle に追加
            cp.ExStyle |= 0x08000000;
            return cp;
        }
    }

    public NonActivatedForm()
    {
        // 必要に応じた初期化処理
        this.Text = "非アクティブな子フォーム";
        this.StartPosition = FormStartPosition.CenterParent;
        // サイズやその他のプロパティを設定
        this.Size = new System.Drawing.Size(300, 200);
    }
}