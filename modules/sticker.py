import json
from PySide6.QtCore import QObject, Signal
from PIL import Image

class Sticker_Data(QObject):
    combined_texture_update_requested = Signal(Image.Image, int)

    def __init__(self):
        super().__init__()
        # Yes, I could do a list comprehension for the floats, but it would make it more aids to read depending on who is reading this.
        self.card_id = 0
        self.coordinate_mode = {'red' : False, 'green' : False, 'blue' : False}
        self.default_texture = None
        self.combined_texture = None
        self.mask_texture = None
        self.red_blendTexture = None
        self.green_blendTexture = None
        self.blue_blendTexture = None
        self.sticker_data = {}
        self.active_color = 'red'
        self.colors = ['red', 'green', 'blue']
        self.sticker_effect = {'red' : 'outgame/special_sticker/general_texture/ef_seamless_smoke.png', 'green' : 'outgame/special_sticker/general_texture/ef_seamless_smoke.png', 'blue' : 'outgame/special_sticker/general_texture/ef_seamless_smoke.png'}
        self.mask_image = ''
        self.tiling = {'red' : [1, -1], 'green' : [1, -1], 'blue' : [1, -1]}
        self.offset = {'red' : [-0.25, -0.25], 'green' : [-0.75, -0.25], 'blue' : [-0.5, -0.75]}
        self.blendtype = {'red' : 0, 'green' : 0, 'blue' : 0}
        self.color = {'red' : [1.0, 1.0, 1.0], 'green' : [1.0, 1.0, 1.0], 'blue' : [1.0, 1.0, 1.0]}
        self.intensity = {'red' : 1.0, 'green' : 1.0, 'blue' : 1.0}
        self.coordtype = {'red' : 1, 'green' : 1, 'blue' : 1}
        self.scrollvelocity = {'red' : [1, 0], 'green' : [1, 0], 'blue' : [1, 0]}
        self.rotatecenter = {'red' : [0, 0], 'green' : [0, 0], 'blue' : [0, 0]}
        self.rotatevelocity = {'red' : 0, 'green' : 0, 'blue' : 0}
        self.common_parameters = [
            ('sampler2D', 'blendTexture', self.sticker_effect),
            ("vec2", "tiling", self.tiling),
            ("vec2", "offset", self.offset),
            ("int", "blendType", self.blendtype),
            ("vec3", "color", self.color),
            ("float", "intensity", self.intensity),
            ("int", "coordinateType", self.coordtype),
            ("vec2", "scrollVelocity", self.scrollvelocity),
            ("vec2", "rotateCenter", self.rotatecenter),
            ("float", "rotateVelocity", self.rotatevelocity)
        ]

    def request_combined_texture_update(self, image_data, replacement_texture):
        self.combined_texture_update_requested.emit(image_data, replacement_texture)
    
    def load_images_and_combine(self, image_path):
        # Load the individual images using PIL
        black_card_only = Image.open('outgame/special_sticker/general_texture/card_black_only.png').convert("RGBA")
        bg_image = black_card_only
        character_image = black_card_only
        effect_image = black_card_only

        # Track which images were replaced
        found_images = {"bg": False, "character": False, "effect": False}

        for file_path in image_path:
            if '_bg' in file_path:
                # print(f"Background image found: {file_path}")
                bg_image = Image.open(file_path).convert("RGBA")
                found_images["bg"] = True
            elif '_character' in file_path:
                # print(f"Character image found: {file_path}")
                character_image = Image.open(file_path).convert("RGBA")
                found_images["character"] = True
            elif '_effect' in file_path:
                # print(f"Effect image found: {file_path}")
                effect_image = Image.open(file_path).convert("RGBA")
                found_images["effect"] = True
            elif '_mask' in file_path:
                # print(f"Mask image found: {file_path}")
                self.mask_texture_data = Image.open(file_path).convert("RGBA")


        # Handle missing images by confirming defaults
        # if not found_images["bg"]:
            # print("No background image found. Using black card.")
        # if not found_images["character"]:
            # print("No character image found. Using black card.")
        # if not found_images["effect"]:
            # print("No effect image found. Using black card.")

        # Ensure all images are the same size, or resize them to match
        bg_image = bg_image.resize((426, 568))
        character_image = character_image.resize((426, 568))
        effect_image = effect_image.resize((426, 568))

        # Combine the images: the background first, then the character, then the effect
        combined_image = Image.alpha_composite(bg_image, character_image)
        combined_image = Image.alpha_composite(combined_image, effect_image)

        # Purely for debugging
        # combined_image.save('./combined_image.png', format="PNG")

        # Flip the image vertically
        # combined_image = combined_image.transpose(Image.FLIP_TOP_BOTTOM)

        return combined_image

    def export_data(self, file_path):
        self.data = {
            "card_id": self.card_id,
            "shader_file": "shader/specialsticker/RGBMaskAnimation",
            "parameters": [
                {
                    "type": "sampler2D",
                    "name": "u_maskTexture",
                    "value": f"character/card/{self.card_id}/{self.mask_image}"
                }
            ]
        }

        for i, color in enumerate(self.color):
            for param_type, param_name, value in self.common_parameters:
                self.data['parameters'].append({
                    'type' : param_type,
                    'name' : f'u_{color}_{param_name}',
                    'value' : value[color]
                })

        with open(file_path, 'w') as file:
            json.dump(self.data, file, indent=4)
            
