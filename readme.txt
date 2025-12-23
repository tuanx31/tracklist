========================================
  TRACKLIST GENERATOR - HƯỚNG DẪN
========================================

📦 CÀI ĐẶT DEPENDENCIES:
------------------------
pip install mutagen
pip install opencv-python
pip install pyinstaller

🔧 ĐÓNG GÓI ỨNG DỤNG:
---------------------
WINDOWS:
  Sử dụng file spec có sẵn:
    python -m PyInstaller main.spec
  
  Hoặc đóng gói trực tiếp:
    python -m PyInstaller --name=tracklist --windowed --onefile main.py

MACOS:
  Cần chạy trên máy Mac:
    python -m PyInstaller main_mac.spec
  
  Hoặc đóng gói trực tiếp:
    python -m PyInstaller --name=tracklist --windowed --onefile main.py

📁 KẾT QUẢ:
-----------
WINDOWS:
- File exe: dist/main.exe
- Thư mục build/ (có thể xóa sau khi đóng gói)

MACOS:
- File app: dist/main (hoặc dist/main.app)
- Thư mục build/ (có thể xóa sau khi đóng gói)

⚠️ LƯU Ý:
---------
- File Windows chỉ chạy trên Windows
- File Mac chỉ chạy trên macOS (cần build trên Mac)
- Kích thước file có thể lớn (50-200MB)
- Antivirus có thể cảnh báo (false positive)
- Mac: Có thể cần codesign và entitlements để chạy trên macOS mới

✨ CHẠY ỨNG DỤNG:
-----------------
- Chạy file Python: python main.py
- Hoặc chạy file exe: dist/main.exe
