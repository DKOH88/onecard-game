"""
카드 선택 도구 - Flood Fill 경계 감지 방식
클릭한 위치의 색상을 기준으로 비슷한 색상 영역의 경계를 자동 감지
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from collections import deque
import os

class CardExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("카드 추출기 - Flood Fill 경계 감지")
        self.root.geometry("1200x900")
        
        self.image = None
        self.photo = None
        self.img_array = None
        self.scale = 1.0
        
        # Selection
        self.rect_id = None
        self.selection = None
        
        self.setup_ui()
        
        # Default load
        default_path = r'c:\gemini\원카드\하트.png'
        if os.path.exists(default_path):
            self.load_image(default_path)
    
    def setup_ui(self):
        # Controls
        control_frame = ttk.Frame(self.root, padding="5")
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="이미지 열기", command=self.open_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="선택 저장", command=self.save_selection).pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Label(control_frame, text="색상 허용치:").pack(side=tk.LEFT, padx=5)
        self.tolerance_var = tk.IntVar(value=50)
        tolerance_scale = ttk.Scale(control_frame, from_=10, to=150, variable=self.tolerance_var, 
                                    orient=tk.HORIZONTAL, length=150)
        tolerance_scale.pack(side=tk.LEFT, padx=5)
        self.tolerance_label = ttk.Label(control_frame, text="50")
        self.tolerance_label.pack(side=tk.LEFT)
        tolerance_scale.configure(command=lambda v: self.tolerance_label.configure(text=str(int(float(v)))))
        
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        self.coord_label = ttk.Label(control_frame, text="좌표: -")
        self.coord_label.pack(side=tk.LEFT, padx=5)
        
        self.color_label = ttk.Label(control_frame, text="색상: -")
        self.color_label.pack(side=tk.LEFT, padx=10)
        
        self.selection_label = ttk.Label(control_frame, text="선택: 없음")
        self.selection_label.pack(side=tk.LEFT, padx=10)
        
        # Help text
        help_frame = ttk.Frame(self.root, padding="5")
        help_frame.pack(fill=tk.X)
        ttk.Label(help_frame, text="💡 사용법: 카드 내부 아무 곳이나 클릭하면 해당 색상과 다른 색상의 경계를 자동 감지합니다.", 
                 foreground='blue').pack(side=tk.LEFT)
        
        # Canvas
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg='gray', cursor='crosshair')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_scroll = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scroll.pack(fill=tk.X)
        
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        # Events
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Motion>', self.on_mouse_move)
        
        # Status
        self.status_var = tk.StringVar(value="카드 내부를 클릭하여 경계를 자동 감지하세요")
        ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN).pack(fill=tk.X, side=tk.BOTTOM)
    
    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.load_image(path)
    
    def load_image(self, path):
        try:
            self.image = Image.open(path).convert('RGBA')
            self.img_array = np.array(self.image)
            
            w, h = self.image.size
            max_size = 900
            if w > max_size or h > max_size:
                self.scale = min(max_size / w, max_size / h)
                new_size = (int(w * self.scale), int(h * self.scale))
                display_img = self.image.resize(new_size, Image.Resampling.LANCZOS)
            else:
                self.scale = 1.0
                display_img = self.image
            
            self.photo = ImageTk.PhotoImage(display_img)
            self.canvas.delete('all')
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo, tags='image')
            self.canvas.configure(scrollregion=(0, 0, display_img.width, display_img.height))
            
            self.selection = None
            self.status_var.set(f"이미지 로드됨: {w}x{h} - 카드 내부를 클릭하세요")
        except Exception as e:
            messagebox.showerror("오류", f"이미지 로드 실패: {e}")
    
    def on_mouse_move(self, event):
        if self.img_array is None:
            return
        
        x = int(self.canvas.canvasx(event.x) / self.scale)
        y = int(self.canvas.canvasy(event.y) / self.scale)
        
        h, w = self.img_array.shape[:2]
        if 0 <= x < w and 0 <= y < h:
            r, g, b = self.img_array[y, x, :3]
            self.coord_label.configure(text=f"좌표: ({x}, {y})")
            self.color_label.configure(text=f"RGB: ({r}, {g}, {b})")
    
    def on_click(self, event):
        if self.img_array is None:
            return
        
        x = int(self.canvas.canvasx(event.x) / self.scale)
        y = int(self.canvas.canvasy(event.y) / self.scale)
        
        h, w = self.img_array.shape[:2]
        if not (0 <= x < w and 0 <= y < h):
            return
        
        self.status_var.set("경계 감지 중...")
        self.root.update()
        
        # Flood fill to find bounds
        bounds = self.flood_fill_bounds(x, y)
        
        if bounds:
            x1, y1, x2, y2 = bounds
            self.selection = bounds
            
            if self.rect_id:
                self.canvas.delete(self.rect_id)
            
            self.rect_id = self.canvas.create_rectangle(
                x1 * self.scale, y1 * self.scale,
                x2 * self.scale, y2 * self.scale,
                outline='lime', width=3
            )
            
            self.selection_label.configure(text=f"선택: {x2-x1}x{y2-y1}")
            self.status_var.set(f"경계 감지 완료! 크기: {x2-x1} x {y2-y1}")
            
            # 자동으로 저장 다이얼로그 열기
            self.save_selection()
        else:
            self.status_var.set("경계 감지 실패 - 색상 허용치를 조정해보세요")
    
    def flood_fill_bounds(self, start_x, start_y):
        """Flood fill 방식으로 같은 색상 영역의 경계 찾기"""
        h, w = self.img_array.shape[:2]
        tolerance = self.tolerance_var.get()
        
        # 시작점 색상
        start_color = self.img_array[start_y, start_x, :3].astype(np.int32)
        
        # 방문 체크
        visited = np.zeros((h, w), dtype=bool)
        
        # 경계값
        min_x, max_x = start_x, start_x
        min_y, max_y = start_y, start_y
        
        # BFS
        queue = deque([(start_x, start_y)])
        visited[start_y, start_x] = True
        
        # 성능을 위해 샘플링 스텝 사용
        step = max(1, min(w, h) // 500)
        
        while queue:
            x, y = queue.popleft()
            
            # 경계 업데이트
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            
            # 4방향 탐색
            for dx, dy in [(step, 0), (-step, 0), (0, step), (0, -step)]:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
                    pixel_color = self.img_array[ny, nx, :3].astype(np.int32)
                    color_diff = np.sqrt(np.sum((pixel_color - start_color) ** 2))
                    
                    if color_diff <= tolerance:
                        visited[ny, nx] = True
                        queue.append((nx, ny))
        
        # 최소 크기 체크
        if max_x - min_x < 20 or max_y - min_y < 20:
            return None
        
        # 약간의 마진 추가
        margin = 2
        min_x = max(0, min_x - margin)
        min_y = max(0, min_y - margin)
        max_x = min(w, max_x + margin)
        max_y = min(h, max_y + margin)
        
        return (min_x, min_y, max_x, max_y)
    
    def save_selection(self):
        if not self.selection or not self.image:
            messagebox.showwarning("경고", "먼저 영역을 선택하세요!")
            return
        
        x1, y1, x2, y2 = self.selection
        cropped = self.image.crop((x1, y1, x2, y2))
        
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
        )
        
        if path:
            cropped.save(path)
            self.status_var.set(f"저장 완료: {path}")

def main():
    root = tk.Tk()
    app = CardExtractor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
