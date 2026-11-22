param([Parameter(Mandatory)] [string] $Path)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.UTF8Encoding]::new()
$source = (Resolve-Path -LiteralPath $Path).Path.Replace('"', '""')
$db = [Data.OleDb.OleDbConnection]::new('Provider=Microsoft.ACE.OLEDB.12.0;Data Source="' + $source + '";Extended Properties="Excel 8.0;HDR=NO;IMEX=1"')
try {
    $db.Open()
    foreach ($sheet in $db.GetSchema('Tables').Rows) {
        $name = $sheet.TABLE_NAME.Trim("'")
        if (!$name.EndsWith('$')) { continue }
        $query = $db.CreateCommand()
        $query.CommandText = 'SELECT * FROM [' + $name.Replace(']', ']]') + ']'
        $reader = $query.ExecuteReader()
        try {
            while ($reader.Read()) {
                $cells = for ($i=0; $i -lt $reader.FieldCount; $i++) { [string]$reader.GetValue($i) }
                ConvertTo-Json -InputObject $cells -Compress
            }
        } finally { $reader.Close() }
    }
} finally { $db.Dispose() }
