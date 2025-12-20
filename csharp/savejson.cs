private void SavePointsToJson(string path)
{
    // PointItem → PointDto に変換してから JSON に書き出す
    var dtoList = _points.ConvertAll(p => new PointDto
    {
        Row = p.CsvRow,
        IsFixed = p.IsFixed,
        X = p.X,
        Y = p.Y
    });

    var options = new JsonSerializerOptions { WriteIndented = true };
    string json = JsonSerializer.Serialize(dtoList, options);
    File.WriteAllText(path, json);
}