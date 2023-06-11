Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c main.py", 0
Set WshShell = Nothing