// 1. 元のサイズで描画するキャンバスを作成
Bitmap originalCanvas = new Bitmap(300, 300);

using (Graphics g = Graphics.FromImage(originalCanvas))
{
    // 風景を描く
    DrawLandscape(g);

    // 点を描く
    DrawPoints(g);
}

// 2. 縮尺をかけたBitmapを作成（例：2倍）
float scale = 2.0f;
int newWidth = (int)(originalCanvas.Width * scale);
int newHeight = (int)(originalCanvas.Height * scale);
Bitmap scaledCanvas = new Bitmap(newWidth, newHeight);

// 3. 元の画像を拡大コピー
using (Graphics g = Graphics.FromImage(scaledCanvas))
{
    // 高品質な拡大をしたいときのオプション
    g.InterpolationMode = System.Drawing.Drawing2D.InterpolationMode.HighQualityBicubic;

    g.DrawImage(originalCanvas, 0, 0, newWidth, newHeight);
}

// 4. 最後にPictureBoxに表示
pictureBox.Image = scaledCanvas;