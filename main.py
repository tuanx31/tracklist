import os
import re
from mutagen.mp3 import MP3
from mutagen import File as MutagenFile
import datetime
from tkinter import *
from tkinter import filedialog, scrolledtext
from tkinter import ttk
import cv2


class TracklistApp:
    """Ứng dụng tạo tracklist từ các file MP3/MP4/WAV"""
    
    # Màu sắc cho các nút lặp
    LAP_COLORS = {
        2: '#ff0000',
        3: '#ff9d00',
        4: '#ffff00',
        5: '#00ff1a',
        6: '#00ddff',
        7: '#4B0082',
        8: '#c800ff',
        9: '#c800ff',
        10: '#ff0066'
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Tracklist Generator")
        self.root.geometry("800x700")
        self.root.configure(bg='#2b2b2b')
        
        # Biến trạng thái
        self.duration = 0
        self.lap_count = 1
        self.current_file_path = ""
        self.lap_buttons = {}
        self.remove_number_var = BooleanVar(value=True)  # Mặc định bật xóa số thứ tự
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=10, font=('Segoe UI', 10))
        
        # Frame chính
        main_frame = Frame(self.root, bg='#2b2b2b', padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Tiêu đề
        title_label = Label(
            main_frame,
            text="🎵 Tracklist Generator",
            font=('Segoe UI', 18, 'bold'),
            bg='#2b2b2b',
            fg='#ffffff'
        )
        title_label.pack(pady=(0, 20))
        
        # Frame chọn số lần lặp
        lap_frame = LabelFrame(
            main_frame,
            text="Chọn số lần lặp",
            font=('Segoe UI', 11, 'bold'),
            bg='#3c3c3c',
            fg='#ffffff',
            padx=15,
            pady=15
        )
        lap_frame.pack(fill=X, pady=(0, 15))
        
        lap_inner = Frame(lap_frame, bg='#3c3c3c')
        lap_inner.pack()
        
        # Tạo các nút lặp
        for i in range(2, 11):
            btn = Button(
                lap_inner,
                text=str(i),
                command=lambda n=i: self.set_lap_count(n),
                width=4,
                height=2,
                font=('Segoe UI', 10, 'bold'),
                bg='#4a4a4a',
                fg='#ffffff',
                activebackground=self.LAP_COLORS[i],
                activeforeground='#ffffff',
                relief=RAISED,
                bd=2
            )
            btn.pack(side=LEFT, padx=5)
            self.lap_buttons[i] = btn
        
        # Hiển thị số lần lặp hiện tại
        self.lap_display = Label(
            lap_frame,
            text=f"Lần lặp hiện tại: {self.lap_count}",
            font=('Segoe UI', 10),
            bg='#3c3c3c',
            fg='#00ff88'
        )
        self.lap_display.pack(pady=(10, 0))
        
        # Checkbox xóa số thứ tự
        checkbox_frame = Frame(lap_frame, bg='#3c3c3c')
        checkbox_frame.pack(pady=(10, 0))
        
        self.remove_number_checkbox = Checkbutton(
            checkbox_frame,
            text="Xóa số thứ tự ở đầu tên file",
            variable=self.remove_number_var,
            font=('Segoe UI', 10),
            bg='#3c3c3c',
            fg='#ffffff',
            selectcolor='#2b2b2b',
            activebackground='#3c3c3c',
            activeforeground='#ffffff'
        )
        self.remove_number_checkbox.pack()
        
        # Frame các nút chức năng
        button_frame = Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(fill=X, pady=(0, 15))
        
        # Nút chọn folder
        self.select_folder_btn = Button(
            button_frame,
            text="📁 Chọn Folder Lưu Nhạc",
            command=self.process_tracklist,
            font=('Segoe UI', 11, 'bold'),
            bg='#4CAF50',
            fg='#ffffff',
            activebackground='#45a049',
            activeforeground='#ffffff',
            relief=RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.select_folder_btn.pack(side=LEFT, padx=5, fill=X, expand=True)
        
        # Nút mở file
        self.open_file_btn = Button(
            button_frame,
            text="📄 Mở File TXT",
            command=self.open_txt_file,
            font=('Segoe UI', 11, 'bold'),
            bg='#2196F3',
            fg='#ffffff',
            activebackground='#0b7dda',
            activeforeground='#ffffff',
            relief=RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.open_file_btn.pack(side=LEFT, padx=5, fill=X, expand=True)
        
        # Hiển thị đường dẫn file
        path_frame = Frame(main_frame, bg='#2b2b2b')
        path_frame.pack(fill=X, pady=(0, 10))
        
        path_label_title = Label(
            path_frame,
            text="Đường dẫn file:",
            font=('Segoe UI', 10, 'bold'),
            bg='#2b2b2b',
            fg='#ffffff'
        )
        path_label_title.pack(anchor=W)
        
        self.path_var = StringVar()
        self.path_display = Label(
            path_frame,
            textvariable=self.path_var,
            font=('Segoe UI', 9),
            bg='#3c3c3c',
            fg='#00ff88',
            anchor=W,
            padx=10,
            pady=5,
            relief=SUNKEN,
            bd=1
        )
        self.path_display.pack(fill=X, pady=(5, 0))
        
        # Text box hiển thị nội dung
        text_frame = LabelFrame(
            main_frame,
            text="Nội dung Tracklist",
            font=('Segoe UI', 11, 'bold'),
            bg='#3c3c3c',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        text_frame.pack(fill=BOTH, expand=True)
        
        self.text_box = scrolledtext.ScrolledText(
            text_frame,
            height=20,
            width=70,
            font=('Consolas', 10),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='#ffffff',
            relief=SUNKEN,
            bd=2,
            wrap=WORD
        )
        self.text_box.pack(fill=BOTH, expand=True)
        
    def set_lap_count(self, count):
        """Thiết lập số lần lặp và cập nhật giao diện"""
        self.lap_count = count
        
        # Reset tất cả nút về màu mặc định
        for btn in self.lap_buttons.values():
            btn.configure(bg='#4a4a4a')
        
        # Đánh dấu nút được chọn
        if count in self.lap_buttons:
            self.lap_buttons[count].configure(bg=self.LAP_COLORS[count])
        
        # Cập nhật hiển thị
        self.lap_display.config(text=f"Lần lặp hiện tại: {self.lap_count}")
        
    def format_time(self, seconds):
        """Chuyển đổi giây thành (giờ, phút, giây)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return (hours, minutes, int(secs))
    
    def get_txt_file_path(self, directory):
        """Tạo đường dẫn file txt"""
        file_name = 'AAAAAAA.txt'
        file_path = os.path.join(directory, file_name)
        return file_path
    
    def initialize_tracklist_file(self, file_path):
        """Khởi tạo file tracklist"""
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write("Tracklist:\n")
    
    def write_time_to_file(self, file_path, duration):
        """Ghi thời gian vào file"""
        hours, minutes, seconds = self.format_time(duration)
        delta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        with open(file_path, 'a', encoding="utf-8") as f:
            f.write(str(delta) + " ")
    
    def get_file_duration(self, file_path):
        """Lấy độ dài của file MP3, MP4 hoặc WAV"""
        if file_path.endswith(".mp3"):
            try:
                audio = MP3(file_path)
                return audio.info.length
            except Exception as e:
                print(f"Lỗi đọc file MP3 {file_path}: {e}")
                return 0
        elif file_path.endswith(".mp4"):
            try:
                cap = cv2.VideoCapture(file_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cap.release()
                if fps > 0:
                    return frame_count / fps
                return 0
            except Exception as e:
                print(f"Lỗi đọc file MP4 {file_path}: {e}")
                return 0
        elif file_path.endswith(".wav"):
            try:
                audio = MutagenFile(file_path)
                if audio is not None and hasattr(audio, 'info') and hasattr(audio.info, 'length'):
                    return audio.info.length
                return 0
            except Exception as e:
                print(f"Lỗi đọc file WAV {file_path}: {e}")
                return 0
        return 0
    
    def get_file_name_without_extension(self, file_path):
        """Lấy tên file không có extension và xóa số thứ tự ở đầu nếu checkbox được chọn"""
        name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(name)[0]
        # Xóa số thứ tự ở đầu nếu checkbox được chọn (ví dụ: "01 ", "01. ", "04 ", v.v.)
        if self.remove_number_var.get():
            name_cleaned = re.sub(r'^\d+[.\s]+', '', name_without_ext)
            return name_cleaned
        return name_without_ext
    
    def process_files(self, directory, txt_file_path):
        """Xử lý tất cả các file trong thư mục"""
        for root_dir, dirs, files in os.walk(os.path.abspath(directory)):
            for file in files:
                file_path = os.path.join(root_dir, file)
                
                if file.endswith((".mp3", ".mp4", ".wav")):
                    # Ghi tên file
                    name = self.get_file_name_without_extension(file_path)
                    with open(txt_file_path, 'a', encoding="utf-8") as f:
                        f.write(name + "\n")
                    
                    # Cập nhật duration và ghi thời gian
                    file_duration = self.get_file_duration(file_path)
                    self.duration += file_duration
                    self.write_time_to_file(txt_file_path, self.duration)
    
    def remove_last_chars(self, file_path, num_chars=9):
        """Xóa số ký tự cuối cùng của file"""
        try:
            with open(file_path, "rb+") as f:
                f.seek(-num_chars, os.SEEK_END)
                f.truncate()
        except Exception as e:
            print(f"Lỗi xóa ký tự cuối: {e}")
    
    def process_loop(self, txt_file_path, directory):
        """Xử lý một lần lặp"""
        self.write_time_to_file(txt_file_path, self.duration)
        self.process_files(directory, txt_file_path)
        self.remove_last_chars(txt_file_path)
    
    def process_tracklist(self):
        """Hàm chính xử lý tracklist"""
        directory = filedialog.askdirectory(title="Chọn thư mục chứa nhạc")
        if not directory:
            return
        
        # Reset duration
        self.duration = 0
        
        # Tạo file txt
        txt_file_path = self.get_txt_file_path(directory)
        self.current_file_path = txt_file_path
        self.path_var.set(txt_file_path)
        
        # Khởi tạo file
        self.initialize_tracklist_file(txt_file_path)
        
        # Xử lý các lần lặp
        for _ in range(self.lap_count):
            self.process_loop(txt_file_path, directory)
        
        # Tính tổng thời gian trước khi reset
        hours, minutes, seconds = self.format_time(self.duration)
        total_delta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        
        # Xóa thời gian cuối cùng bị thừa (nếu có)
        # Đọc file và xóa thời gian thừa ở cuối
        try:
            with open(txt_file_path, 'r', encoding="utf-8") as f:
                content = f.read()
            
            # Xóa thời gian thừa đứng ngay sau tên file (không có khoảng trắng)
            # Ví dụ: "...We_ll Get Through0:13:57" -> "...We_ll Get Through"
            # Pattern: tìm thời gian đứng ngay sau ký tự (không phải khoảng trắng, không phải xuống dòng)
            content = re.sub(r'([^\s\n])(\d+:\d{2}:\d{2})$', r'\1', content, flags=re.MULTILINE)
            
            # Xóa dòng chỉ có thời gian ở cuối file
            lines = content.split('\n')
            cleaned_lines = []
            for i, line in enumerate(lines):
                line_stripped = line.strip()
                # Bỏ qua dòng trống
                if not line_stripped:
                    continue
                
                # Nếu dòng chỉ có thời gian và là dòng cuối cùng (sau khi bỏ dòng trống)
                if re.match(r'^\d+:\d{2}:\d{2}$', line_stripped):
                    # Kiểm tra xem có phải là dòng cuối cùng không
                    remaining_lines = [l.strip() for l in lines[i+1:] if l.strip()]
                    if not remaining_lines:
                        # Đây là dòng cuối cùng, bỏ qua
                        continue
                
                cleaned_lines.append(line)
            
            # Ghi lại file
            with open(txt_file_path, 'w', encoding="utf-8") as f:
                result = '\n'.join(cleaned_lines)
                f.write(result)
                if result and not result.endswith('\n'):
                    f.write('\n')
        except Exception as e:
            print(f"Lỗi xử lý file cuối: {e}")
        
        # Reset
        self.duration = 0
        self.lap_count = 1
        self.set_lap_count(1)
        
        # Hiển thị thông báo
        self.text_box.delete("1.0", END)
        self.text_box.insert(END, f"✅ Đã tạo tracklist thành công!\n")
        self.text_box.insert(END, f"📁 File: {txt_file_path}\n")
        self.text_box.insert(END, f"🔄 Số lần lặp: {self.lap_count}\n")
        self.text_box.insert(END, f"⏱️ Tổng thời gian: {total_delta}\n")
        
    def open_txt_file(self):
        """Mở và hiển thị file txt"""
        if self.current_file_path and os.path.exists(self.current_file_path):
            file_path = self.current_file_path
        else:
            file_path = filedialog.askopenfilename(
                title="Chọn file TXT",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    contents = f.read()
                    self.text_box.delete("1.0", END)
                    self.text_box.insert(END, contents)
                    self.path_var.set(file_path)
                    self.current_file_path = file_path
            except Exception as e:
                self.text_box.delete("1.0", END)
                self.text_box.insert(END, f"❌ Lỗi đọc file: {e}")


def main():
    root = Tk()
    app = TracklistApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
