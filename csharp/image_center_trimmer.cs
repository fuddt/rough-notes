using System;
using System.Drawing;

class Program
{
    static void Main()
    {
        string inputPath = "input.jpg";  // 元画像のパス
        string outputPath = "output.jpg"; // 出力画像のパス

        // 画像を読み込む
        using (Bitmap original = new Bitmap(inputPath))
        {
            int width = original.Width;
            int height = original.Height;

            // 削除する中央部分の幅（全体の30%とする）
            int centerWidth = (int)(width * 0.3);
            int leftWidth = (width - centerWidth) / 2;
            int rightWidth = leftWidth;

            // 新しい幅（中央部分を削除した幅）
            int newWidth = leftWidth + rightWidth;

            // 新しい画像を作成
            using (Bitmap newImage = new Bitmap(newWidth, height))
            using (Graphics g = Graphics.FromImage(newImage))
            {
                // 左部分をコピー
                Rectangle srcLeft = new Rectangle(0, 0, leftWidth, height);
                Rectangle destLeft = new Rectangle(0, 0, leftWidth, height);
                g.DrawImage(original, destLeft, srcLeft, GraphicsUnit.Pixel);

                // 右部分をコピー（右側の開始位置から取得）
                Rectangle srcRight = new Rectangle(leftWidth + centerWidth, 0, rightWidth, height);
                Rectangle destRight = new Rectangle(leftWidth, 0, rightWidth, height);
                g.DrawImage(original, destRight, srcRight, GraphicsUnit.Pixel);

                // 画像を保存
                newImage.Save(outputPath);
            }
        }

        Console.WriteLine("画像の中央を削除して保存しました。");
    }
}