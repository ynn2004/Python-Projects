from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.metrics import dp
import cv2
import os

from pyimagesearch.git_scanner import main as scan_document  # <-- your scanner function

class ScannerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation='vertical'
        
        
        # Add instructions
        self.instructions = Label(text="Drag and drop a document image here to scan.")
        self.add_widget(self.instructions)
        
        self.img = KivyImage()
        self.add_widget(self.img)

        # Enable file drop
        Window.bind(on_dropfile=self.on_file_drop)
        
        
    def on_file_drop(self, window, file_path):
        # Convert from bytes to string
        file_path = file_path.decode("utf-8")
        print(f"Dropped file: {file_path}")

        if not os.path.isfile(file_path):
            print("Error: Dropped file does not exist.")
            return

        # Check for supported file formats
        if not file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
            print("Error: Unsupported file format.")
            return

        # Define output path
        output_path = os.path.splitext(file_path)[0] + "_scanned.jpg"

        try:
            scan_document(file_path, output_path)
        except Exception as e:
            print(f"Error scanning document: {e}")
            return

        # Load and show scanned result
        scanned = cv2.imread(output_path)
        if scanned is None:
            print("Failed to load scanned image.")
            return

        scanned_gray = cv2.cvtColor(scanned, cv2.COLOR_BGR2GRAY)
        buf = cv2.flip(scanned_gray, 0).tobytes()
        texture = Texture.create(size=(scanned_gray.shape[1], scanned_gray.shape[0]), colorfmt='luminance')
        texture.blit_buffer(buf, colorfmt='luminance', bufferfmt='ubyte')
        self.img.texture = texture


class ScannerApp(App):
    def build(self):
        return ScannerLayout()


if __name__ == '__main__':
    ScannerApp().run()
