# 📖 Epub / E-reader Batch Image Normalizer Plugin for Calibre

![Banner](https://img.shields.io/badge/Calibre-Plugin-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Version](https://img.shields.io/badge/Version-1.0.3-orange.svg)

Enhance the visual quality of images in your ebooks with the **Ebook Image Normalizer Plugin** for Calibre! This plugin automatically normalizes, despeckles*, and optimizes images in your ebooks, making scanned pages cleaner, text sharper, and file sizes more manageable—all with a single click.

The settings in this tool are primarily for scanned .pdf converted to .epub with Zamzar and fixed layouts. So the entire .epub file is images. To improve readability with E-ink and E-reader devices like the Kindle / Kindle Paperwhite / etc. Processing the .epubs with this plugin dramatically increases readability on these devices.

## ✨ Features

- **Contrast & Brightness Enhancement**: Automatically adjusts contrast and brightness using `ImageOps.autocontrast` and `ImageEnhance` to make text pop and improve readability.
- **Despeckling**: Removes noise and speckles from scanned images using a median filter, ensuring cleaner pages without sacrificing text clarity.
- **Grayscale Conversion**: Converts images to grayscale to reduce file size while maintaining quality, perfect for text-heavy ebook scans.
- **File Size Optimization**: Saves images with a reduced JPEG quality (default: 75) to keep file sizes manageable, typically reducing bloat by up to 50% compared to unoptimized normalization.
- **Batch Processing**: Processes all images in an ebook in one go, saving you time.
- **Error Handling**: Gracefully handles errors by returning the original image if processing fails, ensuring no data loss.

## 🚀 Installation

### Prerequisites
- [Calibre](https://calibre-ebook.com/) (version 5.0 or higher recommended)
- Python 3.x (included with Calibre)
- Pillow (PIL) library (included with Calibre)

### Steps
1. **Download the Plugin**:
   - Download the latest release from the [Releases](https://github.com/groovedexter/calibre-batch-contrast-normalize) page.
   - Alternatively, clone this repository.
     ```bash
     git clone https://github.com/groovedexter/calibre-batch-contrast-normalize.git
     ```


3. **Install the Plugin in Calibre**:
   - Open Calibre.
   - Go to `Preferences` > `Plugins` > `Load plugin from file`.
   - Navigate to the downloaded ZIP file (`EditorNormalizeImages.zip`) and select it.
   - Click `OK` to install the plugin.
   - Restart Calibre to activate the plugin.

4. **Verify Installation**:
   - In Calibre, go to `Preferences` > `Plugins` and search for "Normalize Images".
   - Ensure the plugin is enabled (check the box if needed).

## 🛠️ Usage

1. **Select an Ebook**:
   - In Calibre Editor, select the ebook you want to process (e.g., an EPUB or MOBI file containing images).

2. **Run the Plugin**:
   - Click the "Normalize Images" button in the Calibre toolbar (or access it via the `Preferences` > `Plugins` menu).
   - The plugin will process all images in the ebook, applying normalization, grayscale conversion, and file size optimization.

3. **Check the Results**:
   - After processing, the ebook will be updated with the enhanced images.
   - Open the ebook in Calibre’s viewer to verify the improved image quality.
   - Check the Calibre log for debug information (e.g., image sizes before and after processing).

### Example Output
- **Before**: Scanned page with low contrast, speckles, and large file size (e.g., 140 KB per image).
- **After**: Enhanced contrast, grayscale, and reduced file size (e.g., ~80 KB per image).

## 🔧 Customization

The plugin is highly customizable! You can tweak the settings in `image.py` to suit your needs:

- **Contrast/Brightness**: Adjust the `ImageEnhance` parameters:
  ```python
  normalized_image = ImageEnhance.Brightness(normalized_image).enhance(1.2)  # Change 1.2 to desired value
  normalized_image = ImageEnhance.Contrast(normalized_image).enhance(1.5)    # Change 1.5 to desired value
  ```
- **Despeckling**: *You can add despeckling. In testing I didn't have good results with it, but it may reduce noise for some .epub scans. Drop this line into image.py using Notepad.
  ```python
  normalized_image = normalized_image.filter(ImageFilter.MedianFilter(size=3))  # Change size to 5 for more aggressive despeckling
  ```
- **JPEG Quality**: Adjust the quality setting to balance file size and quality:
  ```python
  normalized_image.save(buf, format='JPEG', quality=75)  # Change 75 to desired value (e.g., 60 for smaller files)
  ```

After making changes, re-zip the plugin folder and reinstall it in Calibre.

## 📜 License

This project is licensed under the MIT License—see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please ensure your code follows the existing style and includes appropriate comments.

## 📬 Contact

Have questions or suggestions? Open an issue on GitHub or reach out to [me on github](https://github.com/groovedexter).

---

⭐ **Star this repository if you find it useful!** ⭐
