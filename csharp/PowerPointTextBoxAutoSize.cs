using System;
using Microsoft.Office.Interop.PowerPoint;
using Microsoft.Office.Core;

class Program
{
    static void Main()
    {
        Application pptApp = new Application();
        Presentation presentation = pptApp.Presentations.Add();
        Slide slide = presentation.Slides.Add(1, PpSlideLayout.ppLayoutText);

        // テキストボックスをスライドに追加
        Shape textBox = slide.Shapes.AddTextbox(MsoTextOrientation.msoTextOrientationHorizontal, 100, 100, 300, 100);
        textBox.TextFrame.TextRange.Text = "このテキストがテキストボックス内に収まるように自動でフォントサイズを調整します。";

        // テキストボックスのAutoSizeプロパティを設定
        textBox.TextFrame.AutoSize = PpAutoSize.ppAutoSizeShapeToFitText;

        // プレゼンテーションを保存して終了
        presentation.SaveAs(@"C:\path\to\your\presentation.pptx");
        presentation.Close();
        pptApp.Quit();
    }
}