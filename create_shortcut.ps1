# PowerShell script to create a Desktop shortcut for the Hospital Safety Checker
$WshShell = New-Object -ComObject WScript.Shell
$ShortcutPath = "$([Environment]::GetFolderPath('Desktop'))\Hospital Safety Checker.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Point to the start script in the current directory
$Shortcut.TargetPath = "$PSScriptRoot\start.bat"
$Shortcut.WorkingDirectory = "$PSScriptRoot"
$Shortcut.IconLocation = "$PSScriptRoot\app_icon.ico,0"
$Shortcut.Description = "Launch Hospital Safety Checker"
$Shortcut.Save()

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Desktop Shortcut Created Successfully!" -ForegroundColor Green
Write-Host "Location: $ShortcutPath" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
