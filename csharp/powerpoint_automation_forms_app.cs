using System;
using System.Drawing;
using System.IO;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using Microsoft.Office.Core;
using Microsoft.Office.Interop.PowerPoint;
using Application = Microsoft.Office.Interop.PowerPoint.Application;

namespace PowerPointAutomate
{
    public partial class Form1 : Form
    {
        private Application pptApp;
        private Presentation targetPresentation;
        private string targetPresentationGuid;

        public Form1()
        {
            InitializeComponent();
            Button pptOutputButton = new Button();
            pptOutputButton.Text = "PPT OUTPUT";
            pptOutputButton.Location = new System.Drawing.Point(10, 10);
            pptOutputButton.Click += new EventHandler(PptOutputButton_Click);
            Controls.Add(pptOutputButton);
        }

        private void PptOutputButton_Click(object sender, EventArgs e)
        {
            pptApp = new Application();
            pptApp.PresentationSave += new EApplication_PresentationSaveEventHandler(PptApp_PresentationSave);
            pptApp.PresentationCloseFinal += new EApplication_PresentationCloseFinalEventHandler(PptApp_PresentationCloseFinal);

            // 新しいプレゼンテーションを作成
            targetPresentation = pptApp.Presentations.Add(MsoTriState.msoTrue);
            targetPresentationGuid = Guid.NewGuid().ToString();
            targetPresentation.Tags.Add("TargetGuid", targetPresentationGuid);

            // PowerPointアプリケーションを表示
            pptApp.Visible = MsoTriState.msoTrue;
        }

        private void PptApp_PresentationSave(Presentation Pres)
        {
            if (Pres.Tags["TargetGuid"] == targetPresentationGuid)
            {
                OnTargetPresentationSaved();
            }
        }

        private void PptApp_PresentationCloseFinal(Presentation Pres)
        {
            if (Pres.Tags["TargetGuid"] == targetPresentationGuid)
            {
                OnTargetPresentationClosed(Pres);
            }
        }

        private void OnTargetPresentationSaved()
        {
            Console.WriteLine("Target presentation saved.");
            // ここに追加の処理を記述
        }

        private void OnTargetPresentationClosed(Presentation pres)
        {
            Console.WriteLine("Target presentation closed.");
            SaveSlidesAsImages(pres);
            targetPresentationGuid = null;
            ReleaseComObject(pres);
            ReleaseComObject(pptApp);
        }

        private void SaveSlidesAsImages(Presentation presentation)
        {
            string outputDir = @"C:\path\to\output\directory";
            if (!Directory.Exists(outputDir))
            {
                Directory.CreateDirectory(outputDir);
            }

            for (int i = 1; i <= presentation.Slides.Count; i++)
            {
                Slide slide = presentation.Slides[i];
                string outputPath = Path.Combine(outputDir, $"Slide_{i}.png");
                slide.Export(outputPath, "PNG");
                Console.WriteLine($"Slide {i} saved as {outputPath}");
            }
        }

        private void ReleaseComObject(object obj)
        {
            try
            {
                if (obj != null && Marshal.IsComObject(obj))
                {
                    Marshal.ReleaseComObject(obj);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Exception releasing COM object: {ex}");
            }
            finally
            {
                obj = null;
            }
        }
    }
}
