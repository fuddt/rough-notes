using System;
using System.Drawing;
using System.IO;
using System.IO.Compression;

class Program
{
    static void Main()
    {
        string zipPath = "example.zip"; // ZIPファイルのパス
        string imageFileName = "image.jpg"; // ZIP内の画像ファイル名

        using (FileStream zipFileStream = new FileStream(zipPath, FileMode.Open, FileAccess.Read))
        using (ZipArchive archive = new ZipArchive(zipFileStream, ZipArchiveMode.Read))
        {
            ZipArchiveEntry entry = archive.GetEntry(imageFileName);
            if (entry != null)
            {
                using (Stream imageStream = entry.Open())
                using (Image image = Image.FromStream(imageStream))
                {
                    // 画像の情報を表示
                    Console.WriteLine($"Width: {image.Width}, Height: {image.Height}");
                    
                    // 必要に応じて表示や保存
                    image.Save("output.jpg"); // 一時的に保存する場合
                }
            }
            else
            {
                Console.WriteLine("指定された画像がZIP内に見つかりません。");
            }
        }
    }
}