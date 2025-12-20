using System;
using System.Drawing;
using System.Windows.Forms;

public class MainForm : Form
{
    private Button showFormButton;

    public MainForm()
    {
        showFormButton = new Button();
        showFormButton.Text = "Show Form";
        showFormButton.Click += ShowFormButton_Click;
        this.Controls.Add(showFormButton);
    }

    private void ShowFormButton_Click(object sender, EventArgs e)
    {
        // ユーザーに入力してもらうフォームのインスタンスを作成
        Form userForm = new Form();
        userForm.Text = "User Input Form";

        // フォームのサイズが変わるたびに中央に位置を調整
        userForm.SizeChanged += (s, args) =>
        {
            // モニターの中央を計算
            Rectangle screen = Screen.PrimaryScreen.WorkingArea;
            userForm.StartPosition = FormStartPosition.Manual; // 手動で位置を設定するモードに変更
            userForm.Location = new Point(
                screen.Left + (screen.Width - userForm.Width) / 2,
                screen.Top + (screen.Height - userForm.Height) / 2
            );
        };

        // フォームを表示
        userForm.ShowDialog();
    }

    [STAThread]
    static void Main()
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        Application.Run(new MainForm());
    }
}