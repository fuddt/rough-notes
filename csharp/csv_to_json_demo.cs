using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization.Metadata;

namespace CsvToJsonDemo
{
    class Program
    {
        static void Main(string[] args)
        {
            string csvPath = "sample.csv";
            
            // カレントディレクトリに存在しない場合は、ソースファイルと同じ場所を探す
            if (!File.Exists(csvPath))
            {
                csvPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "sample.csv");
            }

            if (!File.Exists(csvPath))
            {
                // さらにワークスペースのパスでフォールバック
                csvPath = Path.Combine(Directory.GetCurrentDirectory(), "sample.csv");
            }

            if (!File.Exists(csvPath))
            {
                Console.WriteLine($"Error: CSV file not found. Please ensure 'sample.csv' is in the same directory.");
                return;
            }

            Console.WriteLine("=== Approach 1: System.Text.Json (Standard) ===");
            try
            {
                string jsonStandard = ConvertWithJsonSerializer(csvPath);
                Console.WriteLine(jsonStandard);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in Approach 1: {ex.Message}");
            }

            Console.WriteLine("\n=== Approach 2: StringBuilder (Manual) ===");
            try
            {
                string jsonManual = ConvertWithStringBuilder(csvPath);
                Console.WriteLine(jsonManual);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in Approach 2: {ex.Message}");
            }
        }

        // Approach 1: System.Text.Json
        static string ConvertWithJsonSerializer(string csvPath)
        {
            var jsonList = new List<Dictionary<string, string>>();

            using (var reader = new StreamReader(csvPath))
            {
                string? headerLine = reader.ReadLine();
                if (headerLine == null) return "[]";
                string[] headers = headerLine.Split(',');

                string? line;
                while ((line = reader.ReadLine()) != null)
                {
                    string[] values = line.Split(',');
                    var row = new Dictionary<string, string>();
                    for (int i = 0; i < headers.Length; i++)
                    {
                        string key = headers[i].Trim();
                        string val = i < values.Length ? values[i].Trim() : "";
                        row[key] = val;
                    }
                    jsonList.Add(row);
                }
            }

            // 単一ファイル実行時のAOT/トリミング制約下でもリフレクションが動くように明示的にResolverを指定
            var options = new JsonSerializerOptions 
            { 
                WriteIndented = true,
                TypeInfoResolver = new DefaultJsonTypeInfoResolver()
            };
            return JsonSerializer.Serialize(jsonList, options);
        }

        // Approach 2: StringBuilder
        static string ConvertWithStringBuilder(string csvPath)
        {
            var sb = new StringBuilder();
            sb.AppendLine("[");

            using (var reader = new StreamReader(csvPath))
            {
                string? headerLine = reader.ReadLine();
                if (headerLine == null) return "[]";
                string[] headers = headerLine.Split(',');

                string? line;
                bool isFirstRow = true;

                while ((line = reader.ReadLine()) != null)
                {
                    if (!isFirstRow)
                    {
                        sb.AppendLine(",");
                    }
                    isFirstRow = false;

                    string[] values = line.Split(',');
                    sb.AppendLine("  {");
                    for (int i = 0; i < headers.Length; i++)
                    {
                        string key = headers[i].Trim();
                        string val = i < values.Length ? values[i].Trim() : "";

                        sb.Append($"    \"{EscapeJsonString(key)}\": \"{EscapeJsonString(val)}\"");
                        if (i < headers.Length - 1)
                        {
                            sb.AppendLine(",");
                        }
                        else
                        {
                            sb.AppendLine();
                        }
                    }
                    sb.Append("  }");
                }
            }

            sb.AppendLine();
            sb.Append("]");
            return sb.ToString();
        }

        static string EscapeJsonString(string value)
        {
            if (string.IsNullOrEmpty(value)) return "";
            return value
                .Replace("\\", "\\\\")
                .Replace("\"", "\\\"")
                .Replace("\n", "\\n")
                .Replace("\r", "\\r")
                .Replace("\t", "\\t");
        }
    }
}
