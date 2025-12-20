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
            _powerPointApp.PresentationCloseFinal += new EApplication_PresentationCloseFinalEventHandler(OnPresentationCloseFinal);

            // PowerPointアプリケーションを開く
            _powerPointApp.Presentations.Open(@"C:\path\to\your\presentation.pptx");

            // メインスレッドを終了させないように待機
            Console.WriteLine("PowerPointを閉じてください...");
            Console.ReadLine();
        }

        // プレゼンテーションが閉じられたときのイベントハンドラ
        private static void OnPresentationCloseFinal(Presentation pres)
        {
            Console.WriteLine("PowerPointが閉じられました。自作の関数を実行します...");
            MyCustomFunction();
        }

        // 自作の関数
        private static void MyCustomFunction()
        {
            Console.WriteLine("自作の関数が実行されました。");
            // ここにあなたのロジックを追加
        }
    }
}
