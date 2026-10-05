# scripts/verify_data.ps1
$files = Get-ChildItem -Path "data" -Filter "*.js"
$total = 0
$ids = @{}

foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw
    $regex = [regex]'id:\s*"([^"]+)"'
    $matches = $regex.Matches($content)
    Write-Host ("[" + $f.Name + "] Found " + $matches.Count + " questions")
    $total += $matches.Count
    foreach ($m in $matches) {
        $id = $m.Groups[1].Value
        if ($ids.ContainsKey($id)) {
            Write-Error ("Duplicate ID: " + $id)
        } else {
            $ids[$id] = $true
        }
    }
}

Write-Host "============================="
Write-Host ("Total Questions Across All 6 Modes: " + $total)
Write-Host ("Unique Question IDs: " + $ids.Count)
