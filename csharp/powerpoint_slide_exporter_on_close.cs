using System;
using System.Diagnostics;
using System.Threading;
using Microsoft.Office.Interop.PowerPoint;
using Microsoft.Office.Core;

namespace PowerPointWatcher
{
    class Program
    {
        private static Application _powerPointApp;
        private static int _powerPointProcessId;

        static void Main(string[] args)
        {
            // PowerPointアプリケーションを開始
            _powerPointApp = new Application();
            _powerPointApp.Visible = MsoTriState.msoTrue;

            // PowerPointのプロセスIDを取得
            _powerPointProcessId = GetPowerPointProcessId();
            Console.WriteLine($"PowerPointプロセスID: {_powerPointProcessId}");

            // PowerPointの終了イベントをサブスクライブ
            _powerPointApp.PresentationBeforeClose += OnPresentationBeforeClose;

            // PowerPointアプリケーションを開く
            _powerPointApp.Presentations.Open(@"C:\path\to\your\presentation.pptx");

            // メインスレッドを終了させないように待機
            Console.WriteLine("PowerPointを閉じてください...");
            WaitForPresentationsToClose();
        }

        // PowerPointプロセスのIDを取得する関数
        private static int GetPowerPointProcessId()
        {
            var currentProcessList = Process.GetProcessesByName("POWERPNT");
            foreach (var process in currentProcessList)
            {
                // 新しいPowerPointアプリケーションを起動した後の最も最近のプロセスを取得
                if (process.MainWindowTitle != "")
                {
                    return process.Id;
                }
            }
            return -1;
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
                // スライドのリソースを解放
                System.Runtime.InteropServices.Marshal.ReleaseComObject(slide);
            }
            // プレゼンテーションを閉じる
            presentation.Close();
            // プレゼンテーションのリソースを解放
            System.Runtime.InteropServices.Marshal.ReleaseComObject(presentation);
        }

        // すべてのプレゼンテーションが閉じられるのを待機する関数
        private static void WaitForPresentationsToClose()
        {
            while (_powerPointApp.Presentations.Count > 0)
            {
                Thread.Sleep(1000); // 1秒待機
            }

            // すべてのプレゼンテーションが閉じられたので、PowerPointアプリケーションを終了
            ClosePowerPoint();

            // 念のため、プロセスが残っていないことを確認して終了
            EnsureSpecificPowerPointProcessIsTerminated();
        }

        // PowerPointアプリケーションを終了する関数
        private static void ClosePowerPoint()
        {
            if (_powerPointApp != null)
            {
                // PowerPointアプリケーションを終了
                _powerPointApp.Quit();
                System.Runtime.InteropServices.Marshal.ReleaseComObject(_powerPointApp);
                _powerPointApp = null;
                Console.WriteLine("PowerPointアプリケーションが終了されました。");
            }
        }

        // 特定のPowerPointプロセスが終了していることを確認する関数
        private static void EnsureSpecificPowerPointProcessIsTerminated()
        {
            try
            {
                Process process = Process.GetProcessById(_powerPointProcessId);
                if (!process.HasExited)
                {
                    process.Kill();
                    Console.WriteLine("特定のPowerPointプロセスを強制終了しました。");
                }
            }
            catch (ArgumentException)
            {
                Console.WriteLine("特定のPowerPointプロセスは既に終了しています。");
            }
        }
    }
}