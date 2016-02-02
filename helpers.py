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
    Saves the image using it's hash as filename in the image directory

    Returns:
        the path there the image was saved, or None in case of failure
    """
    extension = get_image_extension(file.filename)
    # Save image using it's hash as filename, so two uploads with the
    # same filename don't clash with each other
    if extension:
        md5_hash = md5(file.read()).hexdigest()
        filename = md5_hash + '.' + extension
        savepath = os.path.join(app.config['IMAGE_FOLDER'], filename)
        file.seek(0)
        file.save(savepath)
        return savepath
    return None
