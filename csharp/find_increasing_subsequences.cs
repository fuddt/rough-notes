using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        // 入力配列
        int[] array = {1, 5, 8, 2, 3, 4};

        // 一時的に増加列を格納するリスト
        List<int> currentSequence = new List<int>();

        // 増加列の集合を格納する
        List<List<int>> result = new List<List<int>>();

        // 配列を順番に処理する
        for (int i = 0; i < array.Length; i++)
        {
            // 最初の要素、または直前の要素より大きい場合は追加
            if (currentSequence.Count == 0 || array[i] > currentSequence[currentSequence.Count - 1])
            {
                currentSequence.Add(array[i]);
            }
            else
            {
                // 増加が止まったら今までの列を結果に追加（2つ以上のときのみ）
                if (currentSequence.Count > 1)
                {
                    result.Add(new List<int>(currentSequence));
                }

                // 新しいシーケンスを開始
                currentSequence.Clear();
                currentSequence.Add(array[i]);
            }
        }

        // 最後のシーケンスを追加（終端処理）
        if (currentSequence.Count > 1)
        {
            result.Add(currentSequence);
        }

        // 結果の表示
        foreach (var seq in result)
        {
            Console.WriteLine(string.Join(",", seq));
        }
    }
}