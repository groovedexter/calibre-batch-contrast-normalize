#!/usr/bin/env python
# vim:fileencoding=utf-8

__license__ = 'MIT'
__copyright__ = '2025, Austin Krause'

from calibre.gui2 import error_dialog
from calibre.gui2.tweak_book import current_container
from calibre.gui2.tweak_book.plugin import Tool
from calibre.ebooks.oeb.base import JPEG_MIME, PNG_MIME, WEBP_MIME
from qt.core import QAction, QProgressDialog, Qt, QTimer, QMessageBox
from calibre_plugins.EditorNormalizeImages.image import normalize_image

class NormalizeImagesTool(Tool):
    name = 'normalize-images'
    allowed_in_toolbar = True
    allowed_in_menu = True
    default_shortcut = ('Ctrl+Shift+Alt+N',)

    RASTER_IMAGES = {JPEG_MIME, PNG_MIME, WEBP_MIME}

    def __init__(self):
        self.job_data = None
        self.pd_timer = QTimer()

    def create_action(self, for_toolbar=True):
        ac = QAction('Normalize Images', self.gui)
        if not for_toolbar:
            self.register_shortcut(ac, self.name, default_keys=self.default_shortcut)
        ac.triggered.connect(self.normalize_images)
        return ac

    def normalize_images(self):
        if not self.ensure_book(_('You must first open a book in order to normalize images.')):
            return

        self.boss.commit_all_editors_to_container()
        self.boss.add_savepoint('Before: Normalizing images')
        self.process_images()

    def process_images(self):
        container = self.current_container
        images = self.get_images_from_collection(container)

        if len(images) == 0:
            dialog = QMessageBox()
            dialog.setText('No images found!')
            dialog.exec_()
            return

        print(f"Total images to process: {len(images)}")  # Debug log
        progress = self.create_progress_dialog(len(images))
        self.job_data = (images, images.copy(), progress, container)

        self.pd_timer.timeout.connect(self.do_one)
        self.pd_timer.start()

    def get_images_from_collection(self, container):
        images = []
        for name, media_type in container.mime_map.items():
            if media_type in self.RASTER_IMAGES:
                print(f"Found image: {name}, MIME: {media_type}")  # Debug log
                images.append(name)
        return images

    def create_progress_dialog(self, image_count):
        progress = QProgressDialog('Normalizing images...', _('&Stop'), 0, image_count + 1, self.gui)
        progress.setWindowTitle('Normalizing...')
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setValue(0)
        progress.show()
        return progress

    def do_one(self):
        try:
            images, all_images, progress, container = self.job_data
            if len(images) == 0 or progress.wasCanceled():
                self.pd_timer.stop()
                self.do_end()
                return

            name = images.pop()
            print(f"Processing image: {name}")  # Debug log
            img_data = container.raw_data(name, decode=False)
            print(f"Original image data length: {len(img_data)}")  # Debug log
            normalized_data = normalize_image(img_data)
            print(f"Normalized image data length: {len(normalized_data)}")  # Debug log
            container.replace(name, normalized_data)
            container.dirty(name)  # Mark the file as modified
            container.commit_item(name, keep_parsed=True)  # Commit the change
            print(f"Replaced and committed image: {name}")  # Debug log
            index = len(all_images) - len(images)
            progress.setValue(index)
        except Exception:
            import traceback
            error_dialog(self.gui, _('Failed to normalize images'),
                         _('Failed to normalize images, click "Show details" for more info'),
                         det_msg=traceback.format_exc(), show=True)
            self.boss.revert_requested(self.boss.global_undo.previous_container)
            self.pd_timer.stop()

    def do_end(self):
        _, all_images, progress, container = self.job_data

        progress.setValue(len(all_images) + 1)

        self.boss.apply_container_update_to_gui()
        self.boss.commit_all_editors_to_container()
        print("Finished processing images")  # Debug log

    def ensure_book(self, msg=None):
        msg = msg or _('No book is currently open. You must first open a book.')
        if current_container() is None:
            error_dialog(self.gui, _('No book open'), msg, show=True)
            return False
        return True
