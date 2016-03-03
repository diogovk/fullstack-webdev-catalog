from hashlib import md5
from app import app
import os


def get_image_extension(filename):
    """
    Returns the file extension if the extension is allowed, otherwise None
    """
    if '.' in filename:
        extension = filename.rsplit('.', 1)[1]
        if extension:
            return extension
    return None


def save_image(file):
    """
    Saves the image in the image directoryusing its hash as filename

    Returns:
        the path there the image was saved, or None in case of failure
    """
    extension = get_image_extension(file.filename)
    if extension:
        # Use hash as filename, so two uploads with the same filename don't
        # clash with each other
        md5_hash = md5(file.read()).hexdigest()
        filename = md5_hash + '.' + extension
        savepath = os.path.join(app.config['IMAGE_FOLDER'], filename)
        file.seek(0)
        file.save(savepath)
        return savepath
    return None
