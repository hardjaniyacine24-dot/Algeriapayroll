[Setup]
AppId={{A1D31B4E-0F5C-4C88-9C14-7A1E6B5C9D20}
AppName=Algeria Payroll
AppVersion=1.0.1
AppPublisher=Algeria Payroll
DefaultDirName={autopf}\Algeria Payroll
DefaultGroupName=Algeria Payroll
OutputDir=installer_output
OutputBaseFilename=AlgeriaPayroll_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayIcon={app}\AlgeriaPayroll.exe

[Files]
Source: "dist\AlgeriaPayroll.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Algeria Payroll"; Filename: "{app}\AlgeriaPayroll.exe"
Name: "{autodesktop}\Algeria Payroll"; Filename: "{app}\AlgeriaPayroll.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\AlgeriaPayroll.exe"; Description: "Launch Algeria Payroll"; Flags: nowait postinstall skipifsilent
