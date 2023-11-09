import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import keyboard
import webbrowser

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("pyPaint")
        self.root.iconbitmap("ico.ico")

        self.current_color = "black"
        self.current_tool = "brush"
        self.brush_size = 5

        self.canvas_width = 800
        self.canvas_height = 400

        self.canvas = tk.Canvas(self.root, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        self.undo_stack = []

        copyright_label = ttk.Label(self.root, text="© 2023 NNsDEW. Все права защищены.", style="TLabel", foreground="gray")
        copyright_label.pack(side="bottom", anchor="e")

        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить (Shift + S)", command=self.save_image)
        file_menu.add_command(label="Импорт изображения", command=self.import_image)

        format_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Формат", menu=format_menu)
        format_menu.add_command(label="Изменить размер холста", command=self.change_canvas_size)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about_dialog)

        button_frame = ttk.Frame(self.root)
        button_frame.pack()

        self.brush_button = ttk.Button(button_frame, text="Кисть", command=self.use_brush)
        self.eraser_button = ttk.Button(button_frame, text="Ластик", command=self.use_eraser)
        self.clear_button = ttk.Button(button_frame, text="Очистить слой", command=self.clear_canvas)
        self.color_button = ttk.Button(button_frame, text="Выбрать цвет", command=self.select_color)
        self.import_button = ttk.Button(button_frame, text="Импорт", command=self.import_image)
        #self.undo_button = ttk.Button(button_frame, text="Отменить", command=self.undo)

        self.brush_button.pack(side="left", fill="both", expand=True)
        self.eraser_button.pack(side="left", fill="both", expand=True)
        self.clear_button.pack(side="left", fill="both", expand=True)
        self.color_button.pack(side="left", fill="both", expand=True)
        self.import_button.pack(side="left", fill="both", expand=True)
        #self.undo_button.pack(side="left", fill="both", expand=True)

        self.brush_size_label = ttk.Label(button_frame, text="Размер кисти:")
        self.brush_size_label.pack(side="left")

        self.brush_size_scale = ttk.Scale(button_frame, from_=1, to=20, orient="horizontal", command=self.change_brush_size)
        self.brush_size_scale.set(self.brush_size)
        self.brush_size_scale.pack(side="left")

        keyboard.add_hotkey("shift+s", self.save_image)
        keyboard.add_hotkey("ctrl+z", self.undo)

    def change_brush_size(self, event):
        self.brush_size = self.brush_size_scale.get()

    def paint(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)

        if self.current_tool == "brush":
            item = self.canvas.create_oval(x1, y1, x2, y2, fill=self.current_color, outline=self.current_color)
            self.undo_stack.append(item)
            self.canvas.update_idletasks()  # Обновление холста
        elif self.current_tool == "eraser":
            item = self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="white")
            self.undo_stack.append(item)
            self.canvas.update_idletasks()  # Обновление холста


    def reset(self, event):
        pass

    def use_brush(self):
        self.current_tool = "brush"

    def use_eraser(self):
        self.current_tool = "eraser"

    def clear_canvas(self):
        self.canvas.delete("all")
        self.undo_stack.clear()

    def select_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_color = color

    def undo(self):
        for _ in range(10):
            if self.undo_stack:
                item = self.undo_stack.pop()
                self.canvas.delete(item)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg"), ("GIF files", "*.gif"), ("All files", "*.*")])
        if file_path:
            image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
            draw = ImageDraw.Draw(image)
            for item in self.canvas.find_all():
                x1, y1, x2, y2 = self.canvas.coords(item)
                fill_color = self.canvas.itemcget(item, "fill")
                draw.ellipse([x1, y1, x2, y2], fill=fill_color)

            if file_path.endswith(".png"):
                image.save(file_path, "PNG")
            elif file_path.endswith(".jpg"):
                image.save(file_path, "JPEG")
            elif file_path.endswith(".gif"):
                image.save(file_path, "GIF")

    def change_canvas_size(self):
        canvas_size_dialog = tk.Toplevel(self.root)
        canvas_size_dialog.title("Изменить размер холста")

        canvas_size_frame = ttk.Frame(canvas_size_dialog)
        canvas_size_frame.pack()

        width_label = ttk.Label(canvas_size_frame, text="Ширина:")
        width_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        height_label = ttk.Label(canvas_size_frame, text="Высота:")
        height_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        width_entry = ttk.Entry(canvas_size_frame)
        width_entry.grid(row=0, column=1, padx=5, pady=5)
        width_entry.insert(0, str(self.canvas_width))

        height_entry = ttk.Entry(canvas_size_frame)
        height_entry.grid(row=1, column=1, padx=5, pady=5)
        height_entry.insert(0, str(self.canvas_height))

        apply_button = ttk.Button(canvas_size_dialog, text="Применить", command=lambda: self.apply_canvas_size_dialog(width_entry, height_entry, canvas_size_dialog))
        apply_button.pack(pady=10)

    def apply_canvas_size_dialog(self, width_entry, height_entry, canvas_size_dialog):
        new_width = int(width_entry.get())
        new_height = int(height_entry.get())
        if new_width > 0 and new_height > 0:
            self.canvas.config(width=new_width, height=new_height)
            self.canvas_width = new_width
            self.canvas_height = new_height
            canvas_size_dialog.destroy()

    def show_about_dialog(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")

        about_window.geometry("400x750")  # Задаем размер окна

        # Запрещаем изменять размер окна
        about_window.resizable(False, False)

        with open("description.txt", "r", encoding="utf-8") as file:
            description_text = file.read()

        text_width = 350
        text_height = len(description_text) // 40

        about_text = tk.Text(about_window, wrap=tk.WORD, width=text_width, height=text_height)
        about_text.insert(tk.END, description_text)
        about_text.pack(padx=20, pady=(10, 0), side="top", fill="both", expand=True)

        button_frame = ttk.Frame(about_window)
        button_frame.pack(pady=(0, 10), side="top", fill="both", expand=True)
        
        close_button = ttk.Button(button_frame, text="Закрыть", command=about_window.destroy)
        close_button.pack(side="right", padx=10)

        github_button = ttk.Button(button_frame, text="GitHub", command=self.open_github_profile)
        github_button.pack(side="right", padx=10)



    def open_github_profile(self):
        webbrowser.open("https://github.com/NNsDEW")

    def import_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.gif;*.bmp;*.tif")])
        if file_path:
            self.imported_image = Image.open(file_path)
            self.imported_image = self.imported_image.resize((self.canvas_width, self.canvas_height), Image.ANTIALIAS)
            self.imported_image = ImageTk.PhotoImage(self.imported_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imported_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()