import os
import shutil
from tkinter import Tk, Label, Button
from tkinter import filedialog, Label, Button, messagebox
from PIL import Image, ImageTk

class ImageSorter:
    def __init__(self, folder_path, folder_names):
        self.folder_path = folder_path
        self.zoom_factor = 1.0  # Начальный коэффициент увеличения

        # Создаем папки
        self.folders = []
        for folder_name in folder_names:
            folder_path_full = os.path.join(folder_path, folder_name)
            os.makedirs(folder_path_full, exist_ok=True) #exist - не вызывает ошибку если папка уже существует
            self.folders.append(folder_path_full)

        # Загружаем изображения определенных расщирений
        self.images = [f for f in os.listdir(folder_path) if f.endswith(('jpg', 'jpeg', 'png', 'bmp'))]

        self.index = 0 #Считаем количество изображений
        self.setup_ui()

    # Оболочка
    def setup_ui(self):
        self.root = Tk()
        self.root.configure(background='grey')
        self.root.resizable(False, False)
        self.label = Label(self.root) #Элемент для отображения изображений, который добавляется в окно
        self.label.pack(expand=True)

        # Список, где хранятся расположение кнопок (для четырех)
        user_buttons = ['left', 'right', 'top', 'bottom'] 

        # Стрелочки
        directions = ["←", "→", "↑","↓" ]

        # Создание кнопок
        for i in range(len(folder_names)):
            btn = Button(self.root, text=f"{folder_names[i]} {directions[i]}", command=lambda i=i: self.move_to_folder(self.folders[i])) #Замыкаем лямбдой что сохранить i
            btn.pack(side=user_buttons[i])

        # Кнопка для копирования имени изображения
        copy_button = Button(self.root, text="Копировать имя", command=self.copy_image_name)
        copy_button.pack(side='bottom', padx=5)

        # Связываем кнопки с клавиатурый
        self.load_image()
        self.root.bind("<Left>", lambda event: self.move_to_folder(self.folders[0]))
        self.root.bind("<Right>", lambda event: self.move_to_folder(self.folders[1]))
        self.root.bind("<Up>", lambda event: self.move_to_folder(self.folders[2]))
        self.root.bind("<Down>", lambda event: self.move_to_folder(self.folders[3]))

        # Привязываем колесико мыши для увеличения/уменьшения изображения
        self.label.bind("<MouseWheel>", self.zoom_image)
        self.root.mainloop()

    # Загрузка фото в окно
    def load_image(self):
        if self.index < len(self.images):
            image_path = os.path.join(self.folder_path, self.images[self.index])
            img = Image.open(image_path)
            self.display_image(img)
            self.update_title()
        else:
            self.label.config(text="Все изображения отсортированы!")
            self.label.image = None

    # Отображение изображения с учетом масштаба
    def display_image(self, img):
        # Применение коэффициента увеличения
        img = img.resize((int(img.width * self.zoom_factor), int(img.height * self.zoom_factor)), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.label.config(image=self.photo)
        self.label.image = self.photo

    # Устанавливаем заголовок как имя текущего изображения
    def update_title(self):
        self.root.title(f"{self.images[self.index]} | В папке осталось: {len(self.images) - self.index} изображений")

    # Перемещение фото
    def move_to_folder(self, target_folder):
        if self.index < len(self.images):
            source_image_path = os.path.join(self.folder_path, self.images[self.index])
            shutil.move(source_image_path, target_folder)
            self.index += 1
            self.load_image()


    # Метод для изменения масштаба изображения
    def zoom_image(self, event):
        if event.delta > 0:  # Прокрутка вверх
            self.zoom_factor *= 1.1  # Увеличение на 10%
        else:  # Прокрутка вниз
            self.zoom_factor *= 0.9  # Уменьшение на 10%
        
        # Загружаем текущее изображение с новым масштабом
        if self.index < len(self.images):
            image_path = os.path.join(self.folder_path, self.images[self.index])
            img = Image.open(image_path)
            self.display_image(img)

    def copy_image_name(self):
        if self.index < len(self.images):
            image_name = self.images[self.index]
            self.root.clipboard_clear()  # Очищаем буфер обмена
            self.root.clipboard_append(image_name)  # Добавляем название изображения
            messagebox.showinfo("Успешно!", "Cкопировано в буфер обмена!")

if __name__ == '__main__':
    folder_path = filedialog.askdirectory(title="Выберите папку с изображениями")
    if folder_path:
        num_folders = int(input("Введите количество папок для создания: "))
        folder_names = []
        for i in range(num_folders):
            folder_name = input(f"Введите название для папки {i + 1}: ")
            if folder_name:
                folder_names.append(folder_name)

        if folder_names:
            sorter = ImageSorter(folder_path, folder_names)