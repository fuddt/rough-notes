using System;
using Microsoft.Office.Interop.PowerPoint;
using Microsoft.Office.Core;

namespace PowerPointWatcher
{
    class Program
    {
        private static Application _powerPointApp;

        static void Main(string[] args)
        {
            // PowerPointアプリケーションを開始
            _powerPointApp = new Application();
            _powerPointApp.Visible = MsoTriState.msoTrue;

            // PowerPointの終了イベントをサブスクライブ
            _powerPointApp.PresentationBeforeClose += new EApplication_PresentationBeforeCloseEventHandler(OnPresentationBeforeClose);

            // PowerPointアプリケーションを開く
            _powerPointApp.Presentations.Open(@"C:\path\to\your\presentation.pptx");

            // メインスレッドを終了させないように待機
            Console.WriteLine("PowerPointを閉じてください...");
            Console.ReadLine();
        }

        // プレゼンテーションが閉じられる前のイベントハンドラ
        private static void OnPresentationBeforeClose(Presentation pres, ref bool Cancel)
        {
            Console.WriteLine("PowerPointが閉じられようとしています。スライドを画像として保存します...");
            SaveSlidesAsImages(pres, @"C:\path\to\save\images");
        }

        // スライドを画像として保存する関数
        private static void SaveSlidesAsImages(Presentation presentation, string savePath)
        {
            int slideIndex = 1;
            foreach (Slide slide in presentation.Slides)
            {
                string slidePath = System.IO.Path.Combine(savePath, $"Slide_{slideIndex}.jpg");
                slide.Export(slidePath, "jpg");
                Console.WriteLine($"スライド {slideIndex} が {slidePath} に保存されました。");
                slideIndex++;
            }
        }
    }
}
