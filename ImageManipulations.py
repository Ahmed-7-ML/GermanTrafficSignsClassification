from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt
import cv2


class ImageManipulations:
    def __init__(self, image_input):
        if isinstance(image_input, Image.Image):
            self.image = image_input
        else:
            self.image = Image.open(image_input)
        self.manipulated = self.image.copy()

    def negative(self):
        self.manipulated = ImageOps.invert(self.image.convert('RGB'))

    def add_tint(self, color=(255, 0, 0), intensity=0.5):
        if not (0.0 <= intensity <= 1.0):
            raise ValueError("Intensity must be between 0.0 and 1.0")
        overlay = Image.new(self.image.mode, self.image.size, color)
        self.manipulated = Image.blend(self.image, overlay, intensity)

    def crop(self, crop_box):
        self.manipulated = self.image.crop(crop_box)

    def adjust_brightness(self, factor=1.5):
        enhancer = ImageEnhance.Brightness(self.image)
        self.manipulated = enhancer.enhance(factor)

    def adjust_contrast(self, factor=1.5):
        enhancer = ImageEnhance.Contrast(self.image)
        self.manipulated = enhancer.enhance(factor)

    def to_grayscale(self):
        self.manipulated = self.image.convert('L')

    def add_shape(self, shape='circle', position=(100, 100), size=50, color=(255, 0, 0)):
        draw = ImageDraw.Draw(self.manipulated)
        if shape == 'circle':
            draw.ellipse((position[0] - size, position[1] - size, position[0] + size, position[1] + size), fill=color)
        elif shape == 'rectangle':
            draw.rectangle([position, (position[0] + size, position[1] + size)], fill=color)

    def add_text(self, text, position=(10, 10), font=None, color=(255, 255, 255)):
        draw = ImageDraw.Draw(self.manipulated)
        if font is None:
            font = ImageFont.load_default()
        draw.text(position, text, fill=color, font=font)

    def histogram_equalization(self):
        image_array = np.array(self.image.convert('L'))
        image_eq = Image.fromarray(cv2.equalizeHist(image_array))
        self.manipulated = image_eq

    def scale(self, width=None, height=None):
        if width is None or height is None:
            raise ValueError("Both width and height must be specified for scaling.")
        self.manipulated = self.image.resize((width, height))

    def translate(self, x, y):
        self.manipulated = self.image.transform(
            self.image.size, Image.AFFINE, (1, 0, x, 0, 1, y))

    def rotate(self, angle):
        self.manipulated = self.image.rotate(angle)

    def blur(self):
        self.manipulated = self.image.filter(ImageFilter.BLUR)

    def sharpen(self):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.manipulated = enhancer.enhance(2.0)

    def edge_detection(self):
        self.manipulated = self.image.filter(ImageFilter.FIND_EDGES)

    def show_manipulated(self):
        plt.imshow(self.manipulated)
        plt.axis('off')
        plt.show()

    def show_source(self):
        plt.imshow(self.image)
        plt.axis('off')
        plt.show()

    def save(self, output_path):
        self.manipulated.save(output_path)
