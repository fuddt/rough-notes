<table class="soft-blue-table">
  <thead>
    <tr>
      <th>列A</th>
      <th>列B</th>
      <th>列C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><div class="cell-wrap">短いテキスト</div></td>
      <td><div class="cell-wrap">すごく長いテキストです。すごく長いテキストです。すごく長いテキストです。すごく長いテキストです。すごく長いテキストです。すごく長いテキストです。すごく長いテキストです。すごく長いテキストです。すごく長いテキストです。</div></td>
      <td><div class="cell-wrap">短い</div></td>
    </tr>
    <tr>
      <td><div class="cell-wrap">これも短い</div></td>
      <td><div class="cell-wrap">めちゃめちゃ長い文章がここに入ります。めちゃめちゃ長い文章がここに入ります。めちゃめちゃ長い文章がここに入ります。めちゃめちゃ長い文章がここに入ります。めちゃめちゃ長い文章がここに入ります。</div></td>
      <td><div class="cell-wrap">短文</div></td>
    </tr>
  </tbody>
</table>

<style>
.soft-blue-table {
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
  font-family: "Segoe UI", Arial, sans-serif;
  background: #fafdff;
  border: 2px solid #b9e2fa;
  border-radius: 12px;
  box-shadow: 0 1px 8px rgba(128, 192, 255, 0.10);
  overflow: hidden;
}

.soft-blue-table th, .soft-blue-table td {
  border: 1px solid #d0ebff;
  padding: 0; /* パディングはラッパーdivに移す */
  text-align: left;
  font-size: 15px;
  background: transparent;
  height: 80px;       /* 強制固定。必ず高さ80px */
  max-height: 80px;
  vertical-align: top;
  /* overflow-yは指定しない（div側で指定） */
}

.cell-wrap {
  height: 80px;
  max-height: 80px;
  overflow-y: auto;
  padding: 10px 16px;
  box-sizing: border-box;
  word-break: break-all;
  white-space: pre-wrap; /* 折り返し */
  display: block;
}

.soft-blue-table thead th {
  background: #eaf6ff;
  color: #25609e;
  font-weight: 600;
  font-size: 16px;
  letter-spacing: 0.05em;
  border-bottom: 2px solid #b9e2fa;
  height: 48px;
  max-height: 48px;
}

.soft-blue-table tbody tr {
  background: #fafdff;
  transition: background 0.2s;
}

.soft-blue-table tbody tr:hover {
  background: #eaf6ff;
}

.soft-blue-table {
  margin: 24px 0;
}
</style>