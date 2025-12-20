using System;
using Microsoft.Office.Interop.PowerPoint;
using Microsoft.Office.Core;

class Program
{
    static void Main()
    {
        // PowerPointアプリケーションのインスタンスを作成
        Application pptApplication = new Application();
        
        // PowerPointファイルを開く
        Presentation presentation = pptApplication.Presentations.Open(@"C:\path\to\your\presentation.pptx");

        // 各スライドをループ
        foreach (Slide slide in presentation.Slides)
        {
            // 各スライド内のシェイプをループ
            foreach (Shape shape in slide.Shapes)
            {
                // シェイプがテキストフレームを持っている場合
                if (shape.HasTextFrame == MsoTriState.msoTrue)
                {
                    // テキストフレームからテキストを取得
                    TextFrame textFrame = shape.TextFrame;
                    TextRange textRange = textFrame.TextRange;
                    string fullText = "";

                    // 各段落をループしてテキストを結合
                    for (int i = 1; i <= textRange.Paragraphs().Count; i++)
                    {
                        TextRange paragraph = textRange.Paragraphs(i);
                        fullText += paragraph.Text + "\n"; // 各段落の後に改行を追加
                    }

                    Console.WriteLine(fullText);
                }
            }
        }

        // プレゼンテーションを閉じる
        presentation.Close();

        // PowerPointアプリケーションを終了
        pptApplication.Quit();
    }
}