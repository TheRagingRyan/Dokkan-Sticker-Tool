from modules.ui import Ui_MainWindow  # Generated UI class from Designer
import os
from modules.sticker import Sticker_Data
from PySide6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFileDialog
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtCore import QUrl
from OpenGL.GL import *
from modules.renderer import MyOpenGLHandler
from modules.callbacks import MainWindowCallbacks
import json
import numpy as np
from PIL import Image
import re

# Technically just the entire top menu bar
class FileDialog(QFileDialog):
    def __init__(self, stickerClass: Sticker_Data, ui: Ui_MainWindow, callbacks: MainWindowCallbacks):
        super().__init__()
        self.setWindowTitle('Select Files')
        self.setGeometry(0, 0, 600, 400)
        self.stickerClass = stickerClass
        self.ui = ui
        self.callbacks = callbacks


    def open_file_dialog(self):
        """Callback for menu item."""
        self.file_paths, _ = self.getOpenFileNames(self, "Open File", "../character/card", "Json Files & PNG Files(*.json *.png);;All Files (*)")
        
        if not self.file_paths:
            return
            # self.ui.statusbar.showMessage('Files selected should consist of 4 pngs, and 1 json file', 0)

        png_count = len([f for f in self.file_paths if f.endswith(".png")])
        self.png_files = [f for f in self.file_paths if f.endswith(".png")]
        json_count = len([f for f in self.file_paths if f.endswith(".json")])
        self.json_file = [f for f in self.file_paths if f.endswith(".json")]

        # Originally meant to force a user to select X amount of files, however not doing this allows for more customizable displays.
        # Such as displaying only the mask effects by only including the mask image, or a full color like red; to show the red effect isolated.
        # if len(file_paths) != 5 or png_count != 4 or json_count != 1:
            # QMessageBox.warning(None, "Invalid Selection",
                                # "You must select exactly 4 PNG files and 1 JSON file.")
        # else:
            # print("Valid selection:", file_paths)
        
        if self.png_files:
            self.combined_texture = self.stickerClass.load_images_and_combine(self.png_files)
            self.stickerClass.request_combined_texture_update(self.combined_texture, self.stickerClass.combined_texture)
            self.stickerClass.request_combined_texture_update(self.stickerClass.mask_texture_data, self.stickerClass.mask_texture)
            self.stickerClass.mask_image = self.find_mask(self.png_files)
            print(self.find_mask(self.png_files))

        if self.json_file:
            self.set_sticker_data()

    def find_mask(self, png_files: list[str]) -> str | None:
        for file in png_files:
            filename = os.path.basename(file)
            if 'mask' in filename:
                return filename

    def save_file_dialog(self):
        pattern = r"card_(\d+)_decoration_"
        file_path, _ = self.getSaveFileName(self, 'Save File', 'character/card/card_XXXXXXX_decoration_XXXXXXX.json', 'Json Files(*.json);;All Files (*)')
        match = re.search(pattern, file_path)

        if match:
            self.stickerClass.card_id = match.group(1)
            self.ui.statusbar.setStyleSheet("color: green; font-weight: bold;")
            self.ui.statusbar.showMessage('File Saved to (' + file_path + ')', 0)
        else:
            self.ui.statusbar.setStyleSheet("color: red; font-weight: bold;")
            self.ui.statusbar.messageChanged('Card ID not found in file name. Modify the Card ID in the decoration.json or resave with the appropriate name.', 0)

        self.stickerClass.export_data(file_path)

    def github_dialog(self):
        QDesktopServices.openUrl(QUrl("https://github.com/TheRagingRyan/Dokkan-Sticker-Tool"))

    def set_sticker_data(self):
        with open(self.json_file[0], 'r') as file:
            self.stickerClass.sticker_data = json.load(file)
            del self.stickerClass.sticker_data['parameters'][0]

        color = ''
        for param in self.stickerClass.sticker_data['parameters']:
            if param['name'] == 'u_maskTexture':
                pass

            if 'red' in param['name']:
                color = 'red'
            elif 'green' in param['name']:
                color = 'green'
            elif 'blue' in param['name']:
                color = 'blue'

            if param['type'] == 'sampler2D':
                self.stickerClass.sticker_effect[color] = param['value']
                # print(param['value'])

            # The getattr functions aren't setting the correct value yet, so it has to be set before the stickerClass so the callbacks get overwritten, for now.
            elif param['name'] == f'u_{color}_tiling':
                getattr(self.ui, f'horizontalSlider_tiling_{color}_x').setValue(param['value'][0])
                getattr(self.ui, f'horizontalSlider_tiling_{color}_y').setValue(param['value'][1])
                self.stickerClass.tiling[color] = param['value']

            elif param['name'] == f'u_{color}_offset':
                # getattr(self.ui, f'horizontalSlider_{color}_x').setValue(param['value'][0])
                # getattr(self.ui, f'horizontalSlider_{color}_y').setValue(param['value'][1])
                self.stickerClass.offset[color] = param['value']

            elif param['name'] == f'u_{color}_blendType':
                blendtype = 'addition'
                
                if param['value'] == 0:
                    blendtype = 'addition'
                elif param['value'] == 1:
                    blendtype = 'subtraction'
                elif param['value'] == 2:
                    blendtype = 'multiplication'
                elif param['value'] == 3:
                    blendtype = 'replace'
                elif param['value'] == 4:
                    blendtype = 'distortion'

                self.callbacks.activate_button_file_dialog(f'pushButton_blendType_{blendtype}_{color}', color)
                self.stickerClass.blendtype[color] = param['value']

            elif param['name'] == f'u_{color}_color':
                # getattr(self.ui, f'pushButton_color_{color}').setValue(param['value'])
                self.stickerClass.color[color] = param['value']

            elif param['name'] == f'u_{color}_intensity':
                getattr(self.ui, f'horizontalSlider_intensity_{color}').setValue(param['value'] * 100)
                self.stickerClass.intensity[color] = param['value']

            elif param['name'] == f'u_{color}_coordinateType':
                blendtype = 'addition'
                
                if param['value'] == 0:
                    coordtype = 'cartesian'
                elif param['value'] == 1:
                    coordtype = 'polar'

                self.callbacks.activate_button_file_dialog(f'pushButton_coordType_{coordtype}_{color}', color)
                self.stickerClass.coordtype[color] = param['value']


            elif param['name'] == f'u_{color}_scrollVelocity':
                getattr(self.ui, f'horizontalSlider_scrollvelocity_{color}_x').setValue(param['value'][0])
                getattr(self.ui, f'horizontalSlider_scrollvelocity_{color}_y').setValue(param['value'][1])
                self.stickerClass.scrollvelocity[color] = param['value']

            elif param['name'] == f'u_{color}_rotateCenter':
                getattr(self.ui, f'horizontalSlider_rotatecenter_{color}_x').setValue(param['value'][0])
                getattr(self.ui, f'horizontalSlider_rotatecenter_{color}_y').setValue(param['value'][1])
                self.stickerClass.rotatecenter[color] = param['value']

            elif param['name'] == f'u_{color}_rotateVelocity':
                getattr(self.ui, f'horizontalSlider_rotatevelocity_{color}').setValue(param['value'])
                self.stickerClass.rotatevelocity[color] = param['value']

        for color, file_path in self.stickerClass.sticker_effect.items():
            pixmap = QPixmap(file_path)
            getattr(self.ui, f'label_textureimage_{color}').setPixmap(pixmap.scaled(200, 200))
            self.stickerClass.request_combined_texture_update(Image.open(file_path).convert("RGBA"), getattr(self.stickerClass, f'{color}_blendTexture'))
            


#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################

class ImageSelectionView(QGraphicsView):
    def __init__(self, stickerClass: Sticker_Data, ui: Ui_MainWindow, parent=None, label=None):
        super().__init__(parent)
        self.texture_label = label
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.stickerClass = stickerClass
        self.ui = ui

        # Sample image paths 
        # print(os.getcwd())
        images = os.listdir("outgame/special_sticker/general_texture/")
        self.image_paths = [f"outgame/special_sticker/general_texture/{image}" for image in images if image not in ["card_blue_only.png", "card_green_only.png", "card_red_only.png", "general_texture_dummy.png"]]
        self.image_size = 200
        self.images_per_row = 3
        self.image_spacing = 4

        self.init_scene()

    def init_scene(self):
        """Load and display the images in the scene."""
        for i, img_path in enumerate(self.image_paths):
            pixmap = QPixmap(img_path).scaled(self.image_size, self.image_size)
            item = QGraphicsPixmapItem(pixmap)

            row = i // self.images_per_row
            col = i % self.images_per_row

            x = col * (self.image_size + self.image_spacing)
            y = row * (self.image_size + self.image_spacing)

            item.setPos(x, y)  # Horizontally position items
            self.scene.addItem(item)

            # Handle image click events
            item.mousePressEvent = lambda event, path=img_path: self.select_image(path)

    def load_image(self, file_path):
        return np.array(Image.open(file_path).convert("RGBA"))


    def select_image(self, path):
        # print(f"Selected image: {path}")
        pixmap = QPixmap(path)

        if self.stickerClass.active_color == 'red':
            self.stickerClass.request_combined_texture_update(Image.open(path).convert("RGBA"), self.stickerClass.red_blendTexture)
            self.ui.label_textureimage_red.setPixmap(pixmap.scaled(200, 200))
            self.ui.statusbar.showMessage(f'Selected Effect: {path}', 2000)
        if self.stickerClass.active_color == 'green':
            self.stickerClass.request_combined_texture_update(Image.open(path).convert("RGBA"), self.stickerClass.green_blendTexture)
            self.ui.label_textureimage_green.setPixmap(pixmap.scaled(200, 200))
            self.ui.statusbar.showMessage(f'Selected Effect: {path}', 2000)
        if self.stickerClass.active_color == 'blue':
            self.stickerClass.request_combined_texture_update(Image.open(path).convert("RGBA"), self.stickerClass.blue_blendTexture)
            self.ui.label_textureimage_blue.setPixmap(pixmap.scaled(200, 200))
            self.ui.statusbar.showMessage(f'Selected Effect: {path}', 2000)

        # self.texture_label.setPixmap(pixmap.scaled(200, 200))
        self.hide()

#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Instantiate the UI class here
        self.ui.setupUi(self)     # Set up the UI
        self.stickerClass = Sticker_Data()

        self.callbacks = MainWindowCallbacks(self.ui, self.stickerClass)

        

        # Image Selection View (hidden by default)
        self.image_selection_view = ImageSelectionView(self.stickerClass, self.ui, self, self.ui.label_textureimage_red)
        self.image_selection_view.setGeometry(0, 0, 625, 600)
        self.image_selection_view.hide()

        # File Dialog
        self.file_dialog = FileDialog(self.stickerClass, self.ui, self.callbacks)
        self.file_dialog.hide()


        pixmap = QPixmap('outgame/special_sticker/general_texture/ef_seamless_smoke.png')
        self.ui.label_textureimage_red.setPixmap(pixmap.scaled(200, 200))
        self.ui.label_textureimage_green.setPixmap(pixmap.scaled(200, 200))
        self.ui.label_textureimage_blue.setPixmap(pixmap.scaled(200, 200))
        self.ui.pushButton_texture_red.clicked.connect(self.texture_clicked)
        self.ui.pushButton_texture_green.clicked.connect(self.texture_clicked)
        self.ui.pushButton_texture_blue.clicked.connect(self.texture_clicked)


        # self.ui.widget_effects.setStyleSheet("background-image: url('resources/images/com_bg.png');")
        # pixmap = QPixmap('resources/images/com_btn_tab_02_big_left_off.png')

        self.ui.actionOpen.triggered.connect(self.file_dialog.open_file_dialog)
        self.ui.actionSave.triggered.connect(self.file_dialog.save_file_dialog)
        self.ui.actionGithub.triggered.connect(self.file_dialog.github_dialog)

        stylesheet = self.load_stylesheet('style/style.qss')
        self.setStyleSheet(stylesheet)




        self.opengl_widget = MyOpenGLHandler(self.ui.openGLWidget, self.stickerClass)
        self.opengl_widget.clicked.connect(self.callbacks.handle_click)
        self.setFocus()

    def load_stylesheet(self, file_path) -> str:
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Stylesheet file {file_path} not found.")
            return ""

    def texture_clicked(self):
        self.image_selection_view.show()

    def keyPressEvent(self, event):
        self.callbacks.keyboard_handler(event)
        super().keyPressEvent(event)
