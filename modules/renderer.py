from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import QTimer, QElapsedTimer, Signal, QObject, QEvent
from PySide6.QtGui import QMouseEvent
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from PIL import Image
import numpy as np
import json
from pyglm import glm
from modules.sticker import Sticker_Data

class MyOpenGLHandler(QObject):
    clicked = Signal(float, float)
    def __init__(self, opengl_widget: QOpenGLWidget, stickerClass: Sticker_Data):
        super().__init__()
        self.opengl_widget = opengl_widget
        self.stickerClass = stickerClass
        self.stickerClass.combined_texture_update_requested.connect(self.update_texture)
        
        self.current_texture = None

        self.timer = QTimer()  # No need to pass self since MyOpenGLHandler is not a QObject
        self.timer.timeout.connect(self.opengl_widget.update)  # Trigger update for OpenGLWidget
        self.target_fps = 60
        self.timer.start(int(1000 / self.target_fps))  # Set the interval for updates

        # Track time for animation
        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()  # Start the timer


        # Override OpenGL functions
        self.opengl_widget.initializeGL = self.initializeGL
        # self.opengl_widget.resizeGL = self.resizeGL
        self.opengl_widget.paintGL = self.paintGL

        self.opengl_widget.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        if obj == self.opengl_widget and event.type() == QEvent.MouseButtonPress:
            x, y = event.position().x(), event.position().y()

            # Normalize to range 0-1
            normalized_x = x / 426
            normalized_y = 1 - (y / 568)

            print(f"Clicked at: {x}, {y} (Normalized: {normalized_x:.3f}, {normalized_y:.3f})")
            self.clicked.emit(normalized_x, normalized_y)  # Emit normalized coordinates
            return True  
        return super().eventFilter(obj, event)

    def mousePressEvent(self, event: QMouseEvent):
        x, y = event.pos().x(), event.pos().y()
        # print(f"Clicked at: {x}, {y}")
        self.clicked.emit(x, y)  # Emit signal with coordinates

    def update_texture(self, image_data: Image.Image, replacement_texture):
        # Convert the image to a NumPy array
        combined_data = np.array(image_data)

        # Create or bind the texture for update
        if self.current_texture is None:
            self.current_texture = glGenTextures(1)
        
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, replacement_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_data.width, image_data.height, 
                     0, GL_RGBA, GL_UNSIGNED_BYTE, combined_data)

        # Set texture parameters (optional)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        

        # Trigger a redraw for real-time updates
        self.opengl_widget.update()
        # print("Texture updated.")

    def update_mask_texture(self, image_data: Image.Image):
        # Convert the image to a NumPy array
        combined_data = np.array(image_data)

        # Create or bind the texture for update
        if self.current_texture is None:
            self.current_texture = glGenTextures(1)
        
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.stickerClass.mask_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_data.width, image_data.height, 
                     0, GL_RGBA, GL_UNSIGNED_BYTE, combined_data)

        # Set texture parameters (optional)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Trigger a redraw for real-time updates
        self.opengl_widget.update()
        # print("Texture updated.")

    def initializeGL(self):
        # print("OpenGL initialized!")
        self.shader_program = self.compile_shader()
        glUseProgram(self.shader_program)
        glClearColor(0.1, 0.2, 0.3, 1.0)

        # Load default black card texture
        default_texture_path = "outgame/special_sticker/general_texture/card_black_only.png"
        self.stickerClass.combined_texture = self.load_texture(default_texture_path)
        self.stickerClass.mask_texture = self.load_texture(default_texture_path)
        self.stickerClass.red_blendTexture = self.load_texture(self.stickerClass.sticker_effect['red'])
        self.stickerClass.green_blendTexture = self.load_texture(self.stickerClass.sticker_effect['green'])
        self.stickerClass.blue_blendTexture = self.load_texture(self.stickerClass.sticker_effect['blue'])

        # May need to flip the images, most likely
        # Setup textures with default
        glActiveTexture(GL_TEXTURE0)
        # print(self.stickerClass.combined_texture)
        glBindTexture(GL_TEXTURE_2D, self.stickerClass.combined_texture)
        glUniform1i(glGetUniformLocation(self.shader_program, "CC_Texture0"), 0)

        glActiveTexture(GL_TEXTURE1)
        # print(self.stickerClass.mask_texture)
        glBindTexture(GL_TEXTURE_2D, self.stickerClass.mask_texture)
        glUniform1i(glGetUniformLocation(self.shader_program, "u_maskTexture"), 1)

        glActiveTexture(GL_TEXTURE2)
        # print(self.stickerClass.red_blendTexture)
        glBindTexture(GL_TEXTURE_2D, self.stickerClass.red_blendTexture)
        glUniform1i(glGetUniformLocation(self.shader_program, "u_red_blendTexture"), 2)

        glActiveTexture(GL_TEXTURE3)
        # print(self.stickerClass.green_blendTexture)
        glBindTexture(GL_TEXTURE_2D, self.stickerClass.green_blendTexture)
        glUniform1i(glGetUniformLocation(self.shader_program, "u_green_blendTexture"), 3)

        glActiveTexture(GL_TEXTURE4)
        # print(self.stickerClass.blue_blendTexture)
        glBindTexture(GL_TEXTURE_2D, self.stickerClass.blue_blendTexture)
        glUniform1i(glGetUniformLocation(self.shader_program, "u_blue_blendTexture"), 4)

        self.VAO = self.create_quad_with_color()
        self.projection_matrix = glm.mat4(1.0)

        loc = glGetUniformLocation(self.shader_program, "CC_PMatrix")
        if loc != -1:
            glUniformMatrix4fv(loc, 1, GL_FALSE, glm.value_ptr(self.projection_matrix))
        else:
            # print("CC_PMatrix uniform not found in shader!")
            self.json_data = self.load_json('character/card/1006700/card_1006700_decoration_0000017.json')
            self.combined_texture = self.combined_texture()    


    # def resizeGL(self, w, h):
        # glViewport(0, 0, w, h)

    def paintGL(self):
        glUseProgram(self.shader_program)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Calculate elapsed time for the animation
        elapsed_time = self.elapsed_timer.elapsed() / 1000.0  # 60 fps
        # elapsed_time = (self.elapsed_timer.elapsed() / 1000.0) * (144 / 60) # 144 fps
        # elapsed_time = (self.elapsed_timer.elapsed() / 1000.0) * (120 / 60)

        # Pass the time to the shader
        loc = glGetUniformLocation(self.shader_program, "u_animationTime")
        if loc != -1:
            glUniform1f(loc, elapsed_time)


        # Bind the updated texture in texture unit 0
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.stickerClass.combined_texture)  # Make sure you're binding the updated texture
        glUniform1i(glGetUniformLocation(self.shader_program, "CC_Texture0"), 0)  # Set the uniform for texture 0

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.stickerClass.mask_texture)  # Make sure you're binding the updated texture
        glUniform1i(glGetUniformLocation(self.shader_program, "u_maskTexture"), 1)  # Set the uniform for texture 0

        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.stickerClass.red_blendTexture)
        glUniform1i(glGetUniformLocation(self.shader_program, "u_red_blendTexture"), 2)

        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, self.stickerClass.green_blendTexture)
        glUniform1i(glGetUniformLocation(self.shader_program, "u_green_blendTexture"), 3)

        glActiveTexture(GL_TEXTURE4)
        glBindTexture(GL_TEXTURE_2D, self.stickerClass.blue_blendTexture)
        glUniform1i(glGetUniformLocation(self.shader_program, "u_blue_blendTexture"), 4)
        


        for color in self.stickerClass.colors:
            for parameter in self.stickerClass.common_parameters:
                # print(parameter)
                if parameter[0] == 'vec2':
                    loc = glGetUniformLocation(self.shader_program, f'u_{color}_{parameter[1]}')
                    # print(parameter[2][color])
                    glUniform2f(loc, *parameter[2][color])
                elif parameter[0] == 'vec3':
                    loc = glGetUniformLocation(self.shader_program, f'u_{color}_{parameter[1]}')
                    glUniform3f(loc, *parameter[2][color])
                elif parameter[0] == 'float':
                    loc = glGetUniformLocation(self.shader_program, f'u_{color}_{parameter[1]}')
                    glUniform1f(loc, parameter[2][color])
                elif parameter[0] == 'int':
                    loc = glGetUniformLocation(self.shader_program, f'u_{color}_{parameter[1]}')
                    glUniform1i(loc, parameter[2][color])



            
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)



    # For Testing Purposes
    def load_json(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
        
    # Compile Shader
    def compile_shader(self):
        with open('shader/special_sticker/RGBMaskAnimation.vsh', 'r') as f:
            vertex_src = f.read()
        with open('shader/special_sticker/RGBMaskAnimation.fsh', 'r') as f:
            fragment_src = f.read()

        vert = compileShader(vertex_src, GL_VERTEX_SHADER)
        frag = compileShader(fragment_src, GL_FRAGMENT_SHADER)

        # Create program manually so we can bind attribute locations before linking
        program = glCreateProgram()
        glAttachShader(program, vert)
        glAttachShader(program, frag)

        # Explicitly bind attribute locations BEFORE linking
        glBindAttribLocation(program, 0, "a_position")
        glBindAttribLocation(program, 1, "a_texCoord")
        glBindAttribLocation(program, 2, "a_color")

        glLinkProgram(program)

        # Check for link errors
        link_log = glGetProgramInfoLog(program)
        print("=== PROGRAM LINK LOG ===")
        print(link_log if link_log else "No errors")

        return program

    
    def load_texture_flipped(self, file_path):
        image = Image.open(file_path).convert("RGBA")  # Ensure RGBA format
        image = image.transpose(Image.FLIP_TOP_BOTTOM) 

        
        width, height = image.size
        texture_data = image.tobytes()

        # Generate and bind the texture
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Upload the image to the bound texture
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture
    
    # Load Texture
    def load_texture(self, file_path):
        image = Image.open(file_path).convert("RGBA")  # Ensure RGBA format

        width, height = image.size
        texture_data = image.tobytes()

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
        return texture
    
    def create_quad_with_color(self):
        # Define quad vertices with position, texture coordinates, and color
        vertices = np.array([
            # Position      Texture Coords  Color (RGBA)
            -1.0, -1.0,     0.0, 1.0,      1.0, 1.0, 1.0, 1.0,  # Bottom-left
             1.0, -1.0,     1.0, 1.0,      1.0, 1.0, 1.0, 1.0,  # Bottom-right
             1.0,  1.0,     1.0, 0.0,      1.0, 1.0, 1.0, 1.0,  # Top-right
            -1.0,  1.0,     0.0, 0.0,      1.0, 1.0, 1.0, 1.0   # Top-left
        ], dtype=np.float32)

        # Define indices for two triangles
        indices = np.array([
            0, 1, 2,  # First triangle
            2, 3, 0   # Second triangle
        ], dtype=np.uint32)

        # Create a Vertex Array Object (VAO)
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        # Create a Vertex Buffer Object (VBO) and load vertex data into it
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Create an Element Buffer Object (EBO) and load index data into it
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        # Define attribute pointers
        # Position attribute (location = 0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Texture coordinate attribute (location = 1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(2 * vertices.itemsize))
        glEnableVertexAttribArray(1)

        # Color attribute (location = 2)
        glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(4 * vertices.itemsize))
        glEnableVertexAttribArray(2)

        # Unbind the VAO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        return VAO
    
    
    # def mousePressEvent(self, event: QMouseEvent):
    #     # Get the position of the mouse click in widget's coordinates
    #     position = event.pos()
    #     print(f"Mouse clicked at: {position.x()}, {position.y()}")

    #     # If you need to convert this to OpenGL coordinates (if your canvas has transformations)
    #     # you can map the widget coordinates to OpenGL coordinates here if needed.

    #     # Example: setting the position as a coordinate to use in further logic
    #     # (e.g., to update your object or perform some action at this coordinate).
    #     self.set_coordinate(position.x(), position.y())

    # def set_coordinate(self, x, y):
    #     # You can use this method to update any coordinates or internal logic.
    #     print(f"Coordinate set to: ({x}, {y})")