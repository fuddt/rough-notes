var list = new List<string> { "apple", "banana", "cherry", "date" };

var indexes = list
    .Select((value, index) => new { value, index })
    .Where(x => x.value.Contains("a"))
    .Select(x => x.index)
    .ToList();