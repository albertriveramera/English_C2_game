# scripts/verify_syntax.ps1
$jsFiles = Get-ChildItem -Path . -Recurse -Filter "*.js"

foreach ($file in $jsFiles) {
    $text = Get-Content $file.FullName -Raw
    $openBraces = ($text.ToCharArray() | Where-Object { $_ -eq '{' }).Count
    $closeBraces = ($text.ToCharArray() | Where-Object { $_ -eq '}' }).Count
    $openParens = ($text.ToCharArray() | Where-Object { $_ -eq '(' }).Count
    $closeParens = ($text.ToCharArray() | Where-Object { $_ -eq ')' }).Count
    $openBrackets = ($text.ToCharArray() | Where-Object { $_ -eq '[' }).Count
    $closeBrackets = ($text.ToCharArray() | Where-Object { $_ -eq ']' }).Count

    Write-Host ("Checking " + $file.Name + ": Braces: " + $openBraces + "/" + $closeBraces + ", Parens: " + $openParens + "/" + $closeParens + ", Brackets: " + $openBrackets + "/" + $closeBrackets)
    if ($openBraces -ne $closeBraces) {
        Write-Warning ("Mismatched braces in " + $file.Name)
    }
    if ($openParens -ne $closeParens) {
        Write-Warning ("Mismatched parens in " + $file.Name)
    }
    if ($openBrackets -ne $closeBrackets) {
        Write-Warning ("Mismatched brackets in " + $file.Name)
    }
}
Write-Host "File structural check complete."
