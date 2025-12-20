using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Text.Json;
using System.Windows.Forms;

namespace ScatterWinFormsDemo
{
    public class MainForm : Form
    {
        private readonly List<PointItem> _points = new List<PointItem>();
        private PointItem? _draggingPoint = null;
        private Point _dragOffset;

        public MainForm()
        {
            this.Text = "散布図ドラッグ（固定点あり・JSON入力）";
            this.ClientSize = new Size(600, 400);
            this.DoubleBuffered = true;

            // --- ここで JSON から点情報を読み込む ---
            LoadPointsFromJson("points.json");

            // 描画＆マウス系イベント
            this.Paint += MainForm_Paint;
            this.MouseDown += MainForm_MouseDown;
            this.MouseMove += MainForm_MouseMove;
            this.MouseUp += MainForm_MouseUp;
        }

        /// <summary>
        /// JSON ファイルから点のリストを読み込んで _points を作る
        /// </summary>
        private void LoadPointsFromJson(string path)
        {
            if (!File.Exists(path))
            {
                MessageBox.Show($"JSON ファイルが見つかりません: {path}");
                return;
            }

            // ファイルから JSON 文字列を読み込む
            string json = File.ReadAllText(path);

            // JSON → List<PointDto> にデシリアライズ
            var options = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true // 大文字小文字ゆるくマッチ
            };

            List<PointDto>? dtoList = JsonSerializer.Deserialize<List<PointDto>>(json, options);

            if (dtoList == null)
            {
                MessageBox.Show("JSON のパースに失敗しました。");
                return;
            }

            // DTO → PointItem に変換して _points に格納
            foreach (var dto in dtoList)
            {
                var item = new PointItem(
                    csvRow: dto.Row,
                    x: dto.X,
                    y: dto.Y,
                    isFixed: dto.IsFixed
                );
                _points.Add(item);
            }
        }

        // 描画
        private void MainForm_Paint(object? sender, PaintEventArgs e)
        {
            Graphics g = e.Graphics;

            foreach (var p in _points)
            {
                Brush brush = p.IsFixed ? Brushes.Gray : Brushes.Blue;

                float r = p.Radius;
                float left = p.X - r;
                float top = p.Y - r;
                float diameter = 2 * r;

                g.FillEllipse(brush, left, top, diameter, diameter);
                g.DrawEllipse(Pens.Black, left, top, diameter, diameter);

                // 行番号を横に表示しておくとデバッグしやすい
                g.DrawString($"Row:{p.CsvRow}", this.Font, Brushes.Black, p.X + r + 2, p.Y - r);
            }
        }

        // マウス押下（ドラッグ開始）
        private void MainForm_MouseDown(object? sender, MouseEventArgs e)
        {
            if (e.Button != MouseButtons.Left)
                return;

            for (int i = _points.Count - 1; i >= 0; i--)
            {
                var p = _points[i];

                // 固定点はドラッグ対象外
                if (p.IsFixed)
                    continue;

                if (p.HitTest(e.Location))
                {
                    _draggingPoint = p;
                    _dragOffset = new Point(
                        (int)(e.X - p.X),
                        (int)(e.Y - p.Y)
                    );
                    break;
                }
            }
        }

        // マウス移動（ドラッグ中）
        private void MainForm_MouseMove(object? sender, MouseEventArgs e)
        {
            if (_draggingPoint == null)
                return;

            _draggingPoint.X = e.X - _dragOffset.X;
            _draggingPoint.Y = e.Y - _dragOffset.Y;

            Invalidate();
        }

        // マウスアップ（ドラッグ終了）
        private void MainForm_MouseUp(object? sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                _draggingPoint = null;
            }
        }
    }
}