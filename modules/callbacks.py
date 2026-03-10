from PySide6.QtWidgets import QColorDialog
from PySide6.QtCore import QObject
from PySide6.QtGui import QColor, QKeyEvent
from modules.ui import Ui_MainWindow
from modules.sticker import Sticker_Data
from functools import partial
import colorsys


class MainWindowCallbacks(QObject):
    def __init__(self, ui: Ui_MainWindow, stickerClass: Sticker_Data):
        super().__init__()
        # Purely here for syntax purposes.
        self.ui: Ui_MainWindow = ui
        self.stickerClass = stickerClass
        self.execute()
        # print('Callbacks initialized')

    # This is pretty aids, I know.
    def execute(self):
        self.ui.pushButton_red.clicked.connect(self.on_red_button_clicked)
        self.ui.pushButton_green.clicked.connect(self.on_green_button_clicked)
        self.ui.pushButton_blue.clicked.connect(self.on_blue_button_clicked)
        self.ui.pushButton_coordType_cartesian_red.pressed.connect(self.get_coordtype)
        self.ui.pushButton_coordType_cartesian_green.pressed.connect(self.get_coordtype)
        self.ui.pushButton_coordType_cartesian_blue.pressed.connect(self.get_coordtype)
        self.ui.pushButton_coordType_polar_red.pressed.connect(self.get_coordtype)
        self.ui.pushButton_coordType_polar_green.pressed.connect(self.get_coordtype)
        self.ui.pushButton_coordType_polar_blue.pressed.connect(self.get_coordtype)
        self.ui.horizontalSlider_tiling_red_x.valueChanged.connect(partial(self.get_tiling, 'red'))
        self.ui.horizontalSlider_tiling_red_y.valueChanged.connect(partial(self.get_tiling, 'red'))
        self.ui.horizontalSlider_tiling_green_x.valueChanged.connect(partial(self.get_tiling, 'green'))
        self.ui.horizontalSlider_tiling_green_y.valueChanged.connect(partial(self.get_tiling, 'green'))
        self.ui.horizontalSlider_tiling_blue_x.valueChanged.connect(partial(self.get_tiling, 'blue'))
        self.ui.horizontalSlider_tiling_blue_y.valueChanged.connect(partial(self.get_tiling, 'blue'))
        self.ui.horizontalSlider_scrollvelocity_red_x.valueChanged.connect(partial(self.get_scrollVelocity, 'red'))
        self.ui.horizontalSlider_scrollvelocity_red_y.valueChanged.connect(partial(self.get_scrollVelocity, 'red'))
        self.ui.horizontalSlider_scrollvelocity_green_x.valueChanged.connect(partial(self.get_scrollVelocity, 'green'))
        self.ui.horizontalSlider_scrollvelocity_green_y.valueChanged.connect(partial(self.get_scrollVelocity, 'green'))
        self.ui.horizontalSlider_scrollvelocity_blue_x.valueChanged.connect(partial(self.get_scrollVelocity, 'blue'))
        self.ui.horizontalSlider_scrollvelocity_blue_y.valueChanged.connect(partial(self.get_scrollVelocity, 'blue'))
        self.ui.horizontalSlider_rotatevelocity_red.valueChanged.connect(partial(self.get_rotateVelocity, 'red'))
        self.ui.horizontalSlider_rotatevelocity_green.valueChanged.connect(partial(self.get_rotateVelocity, 'green'))
        self.ui.horizontalSlider_rotatevelocity_blue.valueChanged.connect(partial(self.get_rotateVelocity, 'blue'))
        self.ui.horizontalSlider_intensity_red.valueChanged.connect(partial(self.get_intensity, 'red'))
        self.ui.horizontalSlider_intensity_green.valueChanged.connect(partial(self.get_intensity, 'green'))
        self.ui.horizontalSlider_intensity_blue.valueChanged.connect(partial(self.get_intensity, 'blue'))
        self.ui.horizontalSlider_rotatecenter_red_x.valueChanged.connect(partial(self.get_rotateCenter, 'red'))
        self.ui.horizontalSlider_rotatecenter_red_y.valueChanged.connect(partial(self.get_rotateCenter, 'red'))
        self.ui.horizontalSlider_rotatecenter_green_x.valueChanged.connect(partial(self.get_rotateCenter, 'green'))
        self.ui.horizontalSlider_rotatecenter_green_y.valueChanged.connect(partial(self.get_rotateCenter, 'green'))
        self.ui.horizontalSlider_rotatecenter_blue_x.valueChanged.connect(partial(self.get_rotateCenter, 'blue'))
        self.ui.horizontalSlider_rotatecenter_blue_y.valueChanged.connect(partial(self.get_rotateCenter, 'blue'))
        self.ui.pushButton_blendType_addition_red.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_subtraction_red.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_multiplication_red.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_replace_red.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_distortion_red.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_addition_green.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_subtraction_green.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_multiplication_green.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_replace_green.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_distortion_green.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_addition_blue.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_subtraction_blue.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_multiplication_blue.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_replace_blue.pressed.connect(self.get_blendtype)
        self.ui.pushButton_blendType_distortion_blue.pressed.connect(self.get_blendtype)
        self.ui.pushButton_color_red.pressed.connect(partial(self.open_color_picker, 'red'))
        self.ui.pushButton_color_green.pressed.connect(partial(self.open_color_picker, 'green'))
        self.ui.pushButton_color_blue.pressed.connect(partial(self.open_color_picker, 'blue'))
        self.ui.pushButton_coord_red.pressed.connect(partial(self.coord_mode))
        self.ui.pushButton_coord_green.pressed.connect(partial(self.coord_mode))
        self.ui.pushButton_coord_blue.pressed.connect(partial(self.coord_mode))


    # Mouse click the OpenGl widget to move the effect on screen
    def handle_click(self, x, y):
        # print(f"Handled click at: {x:.3f}, {y:.3f}")
        xx = x * 2
        offset_x = x - xx
        offset_y = y - 1
        color = self.stickerClass.active_color

        if self.stickerClass.coordinate_mode[color]:
            self.stickerClass.offset[self.stickerClass.active_color] = [offset_x, offset_y]
            # print(f"Probable Offset: {offset_x:.3f}, {offset_y:.3f}")

    # Read keyboard inputs for shortcuts
    def keyboard_handler(self, event: QKeyEvent):
        # print(event.key())
        key = event.key()
        if key == event.Key_Left:
            pass
            # print('omg')
        pass

    def get_color(self, color, value):
        vec3 = self.hue_to_rgb(getattr(self.ui, f'horizontalSlider_color_{color}').value())
        self.stickerClass.color[color] = vec3
        self.ui.statusbar.showMessage(str(self.stickerClass.color[color]), 3000)

    def hue_to_rgb(self, hue):
        """Convert a single hue [0, 360] back to an RGB vec3 [0, 1]."""
        h = hue / 360.0  # Normalize hue
        r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)  # Assume full saturation and brightness
        return (r, g, b) 
    
    def open_color_picker(self, color):
        self.color_picker = QColorDialog()

        existing_color = [1.0, 1.0, 1.0]  # Default to white
        preset_color = QColor.fromRgbF(*existing_color)
        self.color_picker.setCurrentColor(preset_color)

        self.color_picker.setOption(QColorDialog.ShowAlphaChannel, False)

        # Real-time update while dragging
        self.color_picker.currentColorChanged.connect(lambda col: self.update_color(col, color))

        # Finalize color on OK
        self.color_picker.colorSelected.connect(lambda col: self.update_color(col, color))

        self.color_picker.exec()

    def update_color(self, color_obj, color):
        r, g, b = color_obj.redF(), color_obj.greenF(), color_obj.blueF()
        self.stickerClass.color[color] = [r, g, b]
        # print(f"Updated color for {color}: {self.stickerClass.color[color]}")
    
    # Sliders are getting divided to simulate float values, as sliders are only integer values.
    def get_coordinates(self, color, value):
        x_slider = getattr(self.ui, f'horizontalSlider_{color}_x')
        y_slider = getattr(self.ui, f'horizontalSlider_{color}_y')

        x = x_slider.value() / 100
        y = y_slider.value() / 100

        self.stickerClass.offset[color] = [x, y]
        self.ui.statusbar.showMessage(f'Effect Coordinates ({x}, {y})', 3000)

    def get_tiling(self, color, value):
        x_slider = getattr(self.ui, f'horizontalSlider_tiling_{color}_x')
        y_slider = getattr(self.ui, f'horizontalSlider_tiling_{color}_y')

        x = x_slider.value() / 4
        y = y_slider.value() / 4

        self.stickerClass.tiling[color] = [x, y]
        self.ui.statusbar.showMessage(f'Tiling Values ({x}, {y})', 3000)

    def get_scrollVelocity(self, color, value):
        x_slider = getattr(self.ui, f'horizontalSlider_scrollvelocity_{color}_x')
        y_slider = getattr(self.ui, f'horizontalSlider_scrollvelocity_{color}_y')

        x = x_slider.value() / 4
        y = y_slider.value() / 4

        self.stickerClass.scrollvelocity[color] = [x, y]
        self.ui.statusbar.showMessage(f'Scroll Velocity Values ({x}, {y})', 3000)

    def get_rotateCenter(self, color, value):
        x_slider = getattr(self.ui, f'horizontalSlider_rotatecenter_{color}_x')
        y_slider = getattr(self.ui, f'horizontalSlider_rotatecenter_{color}_y')

        x = x_slider.value() / 4
        y = y_slider.value() / 4

        self.stickerClass.rotatecenter[color] = [x, y]
        self.ui.statusbar.showMessage(f'Rotate Center Values ({x}, {y})', 3000)

    def get_rotateVelocity(self, color, value):
        rotateVelocity = getattr(self.ui, f'horizontalSlider_rotatevelocity_{color}').value() / 1000
        self.stickerClass.rotatevelocity[color] = rotateVelocity
        self.ui.statusbar.showMessage(f'Rotate Velocity Value ({rotateVelocity})', 3000)

    def get_intensity(self, color, value):
        intensity = getattr(self.ui, f'horizontalSlider_intensity_{color}').value() / 100
        self.stickerClass.intensity[color] = intensity
        self.ui.statusbar.showMessage(f'Intensity Value ({intensity})', 3000)

    def get_blendtype(self):
        button = self.sender().objectName()
        self.activate_button(button)

        if 'addition' in button:
            blendtype = 0

        elif  'subtraction' in button:
            blendtype = 1

        elif 'multiplication' in button:
            blendtype = 2

        elif 'replace' in button:
            blendtype = 3

        elif 'distortion' in button:
            blendtype = 4

        self.stickerClass.blendtype[self.stickerClass.active_color] = blendtype
        self.ui.statusbar.showMessage(f'Blend Type: {blendtype}', 3000)
    
    def get_coordtype(self):
        button = self.sender().objectName()
        self.activate_button(button)

        if 'cartesian' in button:
            coordtype = 0

        elif 'polar' in button:
            coordtype = 1

        self.stickerClass.coordtype[self.stickerClass.active_color] = coordtype
        self.ui.statusbar.showMessage(f'Coord Type: {coordtype}', 3000)

    def coord_mode(self):
        color = self.stickerClass.active_color
        if self.stickerClass.coordinate_mode[color] is False:

            self.stickerClass.coordinate_mode[color] = True
            getattr(self.ui, f'pushButton_coord_{color}').setStyleSheet('''background-image: url(:/Images/modified_images/com_btn_radio_on.png);''')
        else:
            self.stickerClass.coordinate_mode[color] = False
            getattr(self.ui, f'pushButton_coord_{color}').setStyleSheet('''background-image: url(:/Images/modified_images/com_btn_radio_off.png);''')

    # Turn off coord mode when switch color widgets to prevent unintentionally movement of effect coords.
    def turn_off_coord_mode(self):
        for color in ['red', 'green', 'blue']:
            getattr(self.ui, f'pushButton_coord_{color}').setStyleSheet('''background-image: url(:/Images/modified_images/com_btn_radio_off.png);''')
            self.stickerClass.coordinate_mode[color] = False

    def effect_color_button_on(self, color):
        colors = ['red', 'green', 'blue']
        colors.remove(color)
        for c in colors:
            getattr(self.ui, f'pushButton_{c}').setStyleSheet(f'''background-image: url('resources/modified_images/{c}_effect_off.png');
                                                                    background-color: transparent;
                                                                    color: rgba(255, 255, 255, 150);
                                                                    padding: 5px;
                                                                    text-align: left;
                                                                    border-top-left-radius: 17px;
                                                                    border-bottom-left-radius: 17px;
                                                                    text-align: center;''')

        getattr(self.ui, f'pushButton_{color}').setStyleSheet(f'''background-image: url('resources/modified_images/{color}_effect_on.png');
                                                                    background-color: transparent;
                                                                    color: white;
                                                                    padding: 5px;
                                                                    text-align: left;
                                                                    border-top-left-radius: 17px;
                                                                    border-bottom-left-radius: 17px;
                                                                    text-align: center;''')


    def on_red_button_clicked(self):
        self.ui.stackedWidget_controls.setCurrentIndex(0)

        self.stickerClass.active_color = 'red'
        self.effect_color_button_on('red')
        self.turn_off_coord_mode()

    def on_green_button_clicked(self):
        self.ui.stackedWidget_controls.setCurrentIndex(1)

        self.stickerClass.active_color = 'green'
        self.effect_color_button_on('green')
        self.turn_off_coord_mode()

    def on_blue_button_clicked(self):
        self.ui.stackedWidget_controls.setCurrentIndex(2)

        self.stickerClass.active_color = 'blue'
        self.effect_color_button_on('blue')
        self.turn_off_coord_mode()

    # Maybe combine the callback instead of having to separate ones, use a flag or something.
    def activate_button(self, button):
        color = self.stickerClass.active_color
        button_off = 'QPushButton{' + 'background-image: url(:/Images/modified_images/com_btn_radio_off.png);' + '}'
        button_on = 'QPushButton{' + 'background-image: url(:/Images/modified_images/com_btn_radio_on.png);' + '}'

        buttons_blendType = [f'pushButton_blendType_addition_{color}', f'pushButton_blendType_subtraction_{color}', f'pushButton_blendType_multiplication_{color}',
                   f'pushButton_blendType_replace_{color}', f'pushButton_blendType_distortion_{color}']
        buttons_coordType = [f'pushButton_coordType_polar_{color}', f'pushButton_coordType_cartesian_{color}']
        
        if 'coordType' in button:
            getattr(self.ui, button).setStyleSheet(button_on)
            buttons_coordType.remove(button)
            getattr(self.ui, buttons_coordType[0]).setStyleSheet(button_off)

        elif 'blendType' in button:
            getattr(self.ui, button).setStyleSheet(button_on)
            buttons_blendType.remove(button)
            for button_name in buttons_blendType:
                getattr(self.ui, button_name).setStyleSheet(button_off)

    def activate_button_file_dialog(self, button, color):
        button_off = 'QPushButton{' + 'background-image: url(:/Images/modified_images/com_btn_radio_off.png);' + '}'
        button_on = 'QPushButton{' + 'background-image: url(:/Images/modified_images/com_btn_radio_on.png);' + '}'

        buttons_blendType = [f'pushButton_blendType_addition_{color}', f'pushButton_blendType_subtraction_{color}', f'pushButton_blendType_multiplication_{color}',
                   f'pushButton_blendType_replace_{color}', f'pushButton_blendType_distortion_{color}']
        buttons_coordType = [f'pushButton_coordType_polar_{color}', f'pushButton_coordType_cartesian_{color}']
        
        if 'coordType' in button:
            getattr(self.ui, button).setStyleSheet(button_on)
            buttons_coordType.remove(button)
            getattr(self.ui, buttons_coordType[0]).setStyleSheet(button_off)

        elif 'blendType' in button:
            getattr(self.ui, button).setStyleSheet(button_on)
            buttons_blendType.remove(button)
            for button_name in buttons_blendType:
                getattr(self.ui, button_name).setStyleSheet(button_off)

