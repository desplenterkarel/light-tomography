class Image:
    def __init__(self, array, mode, extension, color_model):
        self.array = array  # Array representing the image
        self.mode = mode  # Tomo, flat, dark
        self.extension = extension  # Format: .jpg, .png, .tiff, etc...
        self.color_model = color_model  # RGB or Grayscale


    def get_array(self):
        return self.array

    def set_array(self, array):
        self.array = array

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

    def get_extension(self):
        return self.extension

    def set_extension(self, extension):
        self.extension = extension

    def get_color_model(self):
        return self.color_model

    def set_color_model(self, color_model):
        self.color_model = color_model


