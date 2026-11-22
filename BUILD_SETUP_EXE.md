# بناء ملف Setup.exe لنظام Windows

تم تجهيز مسار بناء على Windows لأن PyInstaller لا ينشئ ملف Windows EXE من بيئة Linux.

## الطريقة الآلية عبر GitHub Actions
1. أنشئ مستودعاً جديداً على GitHub.
2. ارفع محتويات هذا المجلد إلى المستودع، مع مجلد `.github/workflows`.
3. افتح تبويب Actions في المستودع.
4. اختر "Build Windows Setup" ثم "Run workflow".
5. بعد انتهاء البناء بنجاح، افتح نتيجة التشغيل ونزّل Artifact باسم `AlgeriaPayroll-Setup-Windows-x64`.
6. ستجد داخله `AlgeriaPayroll_Setup.exe`، وهو ملف التثبيت النهائي.

## البناء محلياً على Windows
- ثبّت Python 3.11 x64 و Inno Setup 6.
- شغّل `build_windows.bat`.
- سيظهر التطبيق في `dist` والمثبت في `installer_output`.

ملاحظة: هذا البناء ينتج ملف تثبيت Windows حقيقياً، لكنه لم يُبنَ داخل بيئة Linux الحالية.
