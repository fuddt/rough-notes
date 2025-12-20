using System.Text.Json.Serialization;

namespace ScatterWinFormsDemo
{
    /// <summary>
    /// JSON から読むための生データ用クラス
    /// JSON のキーとプロパティ名を合わせておく
    /// </summary>
    public class PointDto
    {
        [JsonPropertyName("row")]
        public int Row { get; set; }

        [JsonPropertyName("isFixed")]
        public bool IsFixed { get; set; }

        [JsonPropertyName("x")]
        public float X { get; set; }

        [JsonPropertyName("y")]
        public float Y { get; set; }
    }

    /// <summary>
    /// 実際に画面に描画・ドラッグする点
    /// CSV 行番号も持っておく
    /// </summary>
    public class PointItem
    {
        // CSV 上の行番号
        public int CsvRow { get; }

        // 点の中心座標
        public float X { get; set; }
        public float Y { get; set; }

        // 表示半径
        public float Radius { get; set; } = 8f;

        // 固定かどうか
        public bool IsFixed { get; }

        public PointItem(int csvRow, float x, float y, bool isFixed)
        {
            CsvRow = csvRow;
            X = x;
            Y = y;
            IsFixed = isFixed;
        }

        /// <summary>
        /// マウス位置がこの点の中に入っているかどうかを判定
        /// </summary>
        public bool HitTest(Point mousePos)
        {
            float dx = mousePos.X - X;
            float dy = mousePos.Y - Y;
            float distanceSquared = dx * dx + dy * dy;
            return distanceSquared <= Radius * Radius;
        }
    }
}