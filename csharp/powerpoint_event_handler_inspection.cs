using System;
using System.Reflection;
using Microsoft.Office.Interop.PowerPoint;
using Office = Microsoft.Office.Core;

class Program
{
    static Application pptApp;
    static Presentation targetPresentation;

    static void Main(string[] args)
    {
        pptApp = new Application();
        pptApp.PresentationSave += new EApplication_PresentationSaveEventHandler(PptApp_PresentationSave);
        pptApp.PresentationSave += new EApplication_PresentationSaveEventHandler(AnotherPptApp_PresentationSave);

        // 指定されたパスのプレゼンテーションを開きます
        string filePath = @"C:\path\to\your\presentation.pptx";
        targetPresentation = pptApp.Presentations.Open(filePath);

        Console.WriteLine("Press any key to display the number of handlers.");
        Console.ReadKey();
        
        int handlerCount = GetEventHandlerCount(pptApp, "PresentationSave");
        Console.WriteLine($"Number of event handlers: {handlerCount}");

        Console.WriteLine("Press any key to quit.");
        Console.ReadKey();
    }

    private static void PptApp_PresentationSave(Presentation Pres)
    {
        // 保存されたプレゼンテーションがターゲットのものか確認
        if (object.ReferenceEquals(Pres, targetPresentation))
        {
            OnTargetPresentationSaved();
        }
    }

    private static void AnotherPptApp_PresentationSave(Presentation Pres)
    {
        Console.WriteLine("Another PresentationSave event handler called.");
    }

    private static void OnTargetPresentationSaved()
    {
        // ターゲットプレゼンテーションが保存されたときに実行する関数
        Console.WriteLine("Target presentation saved.");
        // ここに追加の処理を記述
    }

    private static int GetEventHandlerCount(object target, string eventName)
    {
        int count = 0;
        EventInfo eventInfo = target.GetType().GetEvent(eventName);
        if (eventInfo != null)
        {
            FieldInfo field = target.GetType().GetField(eventInfo.Name, BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.GetField);
            if (field != null)
            {
                MulticastDelegate multicastDelegate = field.GetValue(target) as MulticastDelegate;
                if (multicastDelegate != null)
                {
                    count = multicastDelegate.GetInvocationList().Length;
                }
            }
        }
        return count;
    }
}