$folder = "D:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร"
Get-ChildItem -Path $folder -Filter *.xlsx -File | ForEach-Object {
    $src = $_.FullName
    $dst = Join-Path $folder ($_.BaseName + "_converted.pdf")
    Write-Host "Converting $src -> $dst"
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $workbook = $excel.Workbooks.Open($src)
    # 0 = xlTypePDF
    $workbook.ExportAsFixedFormat(0, $dst)
    $workbook.Close($false)
    $excel.Quit()
}
