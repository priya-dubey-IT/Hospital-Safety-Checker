# PowerShell script to fix/create shortcuts on both Desktop locations
$WshShell = New-Object -ComObject WScript.Shell
$TargetPath = "c:\Users\Rohit\OneDrive\Desktop\New folder\start.bat"
$IconPath = "c:\Users\Rohit\OneDrive\Desktop\New folder\app_icon.ico,0"
$WorkingDir = "c:\Users\Rohit\OneDrive\Desktop\New folder"
$ShortcutName = "Hospital Safety Checker.lnk"

# Potential desktop paths
$Paths = @(
    "$([Environment]::GetFolderPath('Desktop'))",
    "$env:USERPROFILE\Desktop",
    "$env:USERPROFILE\OneDrive\Desktop"
)

foreach ($Path in $Paths) {
    if (Test-Path $Path) {
        $ShortcutPath = Join-Path $Path $ShortcutName
        Write-Host "Creating/Fixing shortcut at: $ShortcutPath" -ForegroundColor Cyan
        $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
        $Shortcut.TargetPath = $TargetPath
        $Shortcut.WorkingDirectory = $WorkingDir
        $Shortcut.IconLocation = $IconPath
        $Shortcut.Description = "Launch Hospital Safety Checker"
        $Shortcut.Save()
        Write-Host "Successfully updated $ShortcutPath" -ForegroundColor Green
    }
}
