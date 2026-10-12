[Windows.Media.Ocr.OcrEngine, Windows.Foundation.Diagnostics, ContentType = WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime] | Out-Null

$imagePath = (Resolve-Path "gen_insp_orig_p1.png").Path

# Run async in powershell
$fileTask = [Windows.Storage.StorageFile]::GetFileFromPathAsync($imagePath)
$file = $fileTask.GetAwaiter().GetResult()

$streamTask = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read)
$stream = $streamTask.GetAwaiter().GetResult()

$decoderTask = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
$decoder = $decoderTask.GetAwaiter().GetResult()

$bitmapTask = $decoder.GetSoftwareBitmapAsync()
$bitmap = $bitmapTask.GetAwaiter().GetResult()

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($null -eq $engine) {
    Write-Output "Engine null, trying available languages"
    $langs = [Windows.Media.Ocr.OcrEngine]::AvailableRecognizerLanguages
    foreach ($l in $langs) {
        Write-Output "Lang: $($l.LanguageTag)"
    }
} else {
    $ocrResultTask = $engine.RecognizeAsync($bitmap)
    $result = $ocrResultTask.GetAwaiter().GetResult()
    Write-Output "Recognized Text:"
    Write-Output $result.Text
}
