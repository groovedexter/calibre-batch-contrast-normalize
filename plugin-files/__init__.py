from calibre.customize import EditBookToolPlugin
from calibre.gui2.tweak_book.plugin import Tool
from PIL import Image, ImageOps
import io
from qt.core import QAction

def normalize_image(img_data):
    try:
        img = Image.open(io.BytesIO(img_data))
        normalized_img = ImageOps.autocontrast(img)
        output = io.BytesIO()
        normalized_img.save(output, format=img.format or 'JPEG', quality=95)
        return output.getvalue()
    except Exception as e:
        print(f"Error normalizing image: {e}")
        return img_data  # Return original if error

class NormalizeImagesTool(Tool):
    name = 'normalize-images'  # Unique name for the tool
    allowed_in_menu = True
    allowed_in_toolbar = True

    def create_action(self, for_widget):
        print("Creating action for Normalize Images tool")  # Debug print
        ac = QAction('Normalize Images', self.gui)
        ac.setStatusTip('Normalize contrast for all images in the book')
        ac.triggered.connect(self.normalize_images)
        return ac

    def normalize_images(self):
        boss = self.current_boss()
        if not boss.currently_editing:
            boss.gui.popup('No book open', 'Please open a book to normalize images.')
            return
        
        container = boss.current_container
        if not container:
            boss.gui.popup('Error', 'Could not access book container.')
            return
        
        log = boss.global_undo_redo.log
        log.clear()
        log('Starting image normalization...')
        
        image_count = 0
        try:
            for name, mime in container.mime_map.items():
                if mime.startswith('image/'):
                    try:
                        img_data = container.raw_data(name, decode=False)
                        normalized_data = normalize_image(img_data)
                        with container.open(name, 'wb') as f:
                            f.write(normalized_data)
                        image_count += 1
                        log(f'Normalized image: {name}')
                    except Exception as e:
                        log(f'Error normalizing {name}: {str(e)}')
            
            container.dirty = True
            log(f'Completed normalization: {image_count} images processed')
            boss.show_status_message(f'Normalized {image_count} images', 5000)
        except Exception as e:
            log(f'Failed to normalize images: {str(e)}')
            boss.gui.popup('Error', f'Normalization failed: {str(e)}')

class NormalizeImagesPlugin(EditBookToolPlugin):
    name = 'Normalize Images'
    description = 'Add a tool to normalize image contrast in the Calibre Editor.'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Austin Krause'
    version = (1, 0, 3)  # Bumped version to 1.0.1
    minimum_calibre_version = (5, 0, 0)
    can_be_disabled = True

    def initialize(self):
        print("Initializing Normalize Images plugin")  # Debug print
        self.tool = NormalizeImagesTool()

    def tweak(self, boss):
        print("Registering Normalize Images tool")  # Debug print
        self.tool.register(boss)