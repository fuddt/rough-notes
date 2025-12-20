using System;
using System.Collections.Generic;
using System.Drawing;
using System.Runtime.InteropServices;
using Excel = Microsoft.Office.Interop.Excel;
using System.Windows.Forms; // クリップボード使用

class ExcelToImage
{
    [STAThread] // Clipboard使用にはSTAスレッドが必須
    static void Main(string[] args)
    {
        if (args.Length != 2)
        {
            Console.WriteLine("Usage: ExcelToImage <input.xlsx> <output.png>");
            return;
        }

        string inputPath = args[0];
        string outputPath = args[1];

        var excelApp = new Excel.Application();
        excelApp.Visible = false;
        excelApp.DisplayAlerts = false;

        try
        {
            var workbook = excelApp.Workbooks.Open(inputPath);
            var worksheet = (Excel.Worksheet)workbook.Sheets[1];
            var usedRange = worksheet.UsedRange;

            // セル範囲を画像としてコピー
            usedRange.CopyPicture(
                Excel.XlPictureAppearance.xlScreen,
                Excel.XlCopyPictureFormat.xlBitmap
            );
            worksheet.Paste();
            var pastedShape = worksheet.Shapes[worksheet.Shapes.Count];

            // 図形を集める
            List<string> shapeNames = new List<string>();
            foreach (Excel.Shape shape in worksheet.Shapes)
            {
                if (IsShapeInUsedRange(shape, usedRange) || shape.Name == pastedShape.Name)
                {
                    shapeNames.Add(shape.Name);
                }
            }

            // グループ化してコピー
            var group = worksheet.Shapes.Range(shapeNames.ToArray()).Group();
            group.Copy();

            // Clipboardから画像を取得
            if (Clipboard.ContainsImage())
            {
                Image img = Clipboard.GetImage();
                img.Save(outputPath, System.Drawing.Imaging.ImageFormat.Png);
                Console.WriteLine("Image saved to: " + outputPath);
            }
            else
            {
                Console.WriteLine("Failed to get image from clipboard.");
            }

            // クリーンアップ
            group.Delete();
            pastedShape.Delete();
            workbook.Close(false);
        }
        catch (Exception ex)
        {
            Console.WriteLine("ERROR: " + ex.Message);
        }
        finally
        {
            excelApp.Quit();
            Marshal.ReleaseComObject(excelApp);
        }
    }

    static bool IsShapeInUsedRange(Excel.Shape shape, Excel.Range usedRange)
    {
        float shapeLeft = shape.Left;
        float shapeTop = shape.Top;
        float shapeRight = shapeLeft + shape.Width;
        float shapeBottom = shapeTop + shape.Height;

        float rangeLeft = (float)usedRange.Left;
        float rangeTop = (float)usedRange.Top;
        float rangeRight = rangeLeft + (float)usedRange.Width;
        float rangeBottom = rangeTop + (float)usedRange.Height;

        return !(shapeRight < rangeLeft || shapeLeft > rangeRight ||
                 shapeBottom < rangeTop || shapeTop > rangeBottom);
    }
}