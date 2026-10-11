$ErrorActionPreference = "Stop"

$LambdaDir = $PSScriptRoot
$PackageDir = Join-Path $LambdaDir "package"

if (Test-Path $PackageDir) {
    Remove-Item $PackageDir -Recurse -Force
}

New-Item -ItemType Directory -Path $PackageDir -Force | Out-Null

py -3.12 -m pip install `
    --disable-pip-version-check `
    --target $PackageDir `
    -r (Join-Path $LambdaDir "requirements.txt")

if ($LASTEXITCODE -ne 0) {
    throw "No se pudieron instalar las dependencias de Lambda."
}

Copy-Item (Join-Path $LambdaDir "handler.py") $PackageDir

Write-Host "Paquete de Lambda preparado en: $PackageDir"
$BuildDir = Join-Path $LambdaDir "build"
$ZipPath = Join-Path $BuildDir "lambda.zip"

New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null

if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

Compress-Archive `
    -Path (Join-Path $PackageDir "*") `
    -DestinationPath $ZipPath `
    -CompressionLevel Fastest

Write-Host "ZIP de Lambda generado en: $ZipPath"