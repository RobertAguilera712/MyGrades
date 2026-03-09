from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps
from pathlib import Path
from flask import request, jsonify, Blueprint, flash, redirect, url_for
from flask_uploads import UploadSet, IMAGES
from flask_login import LoginManager, current_user
from PIL import Image
import os, base64
from werkzeug.datastructures import FileStorage
from io import BytesIO
import pytz
from datetime import datetime


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "login.log_in"
login_manager.login_message_category = "info"
login_manager.login_message = "Por favor inicia sesión para acceder a esta página"


def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode("utf-8")


def get_current_time():
    mexico_city_timezone = pytz.timezone("America/Mexico_City")
    mexico_city_time = datetime.now(mexico_city_timezone)

    return mexico_city_time


def localize_datetime(datetime):
    mexico_city_timezone = pytz.timezone("America/Mexico_City")
    return mexico_city_timezone.localize(datetime)


def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            if current_user.role not in allowed_roles:
                flash("No tienes permiso para acceder a esta página", "error")
                return redirect(url_for("login.log_in", next=request.url))

            return fn(*args, **kwargs)

        return wrapper

    return decorator


users_imgs = UploadSet(
    "users",
    IMAGES,
    lambda app: os.path.join(app.root_path, Path("./static/img/users")),
)

schools_imgs = UploadSet(
    "schools",
    IMAGES,
    lambda app: os.path.join(app.root_path, Path("./static/img/schools")),
)


def get_image(base64_image):
    image_bytes = base64.b64decode(base64_image)
    image_file = BytesIO(image_bytes)
    image_file.seek(0)  # Reset file pointer

    image_file = compress_image(image_file)

    # Save image to filesystem
    uploaded_file = FileStorage(image_file, filename="upload.webp")
    return uploaded_file


def compress_image(image_bytes):
    # Open the image
    img = Image.open(image_bytes)

    # Convert to RGB
    img = img.convert("RGB")

    # Check if resizing is necessary based on image width
    max_width = 960  # Maximum width for the image

    if img.width > max_width:
        # Calculate the new height to maintain aspect ratio
        width_percent = max_width / float(img.size[0])
        new_height = int(float(img.size[1]) * float(width_percent))

        # Resize the image while preserving aspect ratio
        img = img.resize((max_width, new_height), Image.LANCZOS)

    # Create a BytesIO object to store the compressed image
    output = BytesIO()

    # Compress the image and save it to the BytesIO object
    img.save(output, format="WEBP", quality=70)  # Adjust quality as needed

    # Rewind the BytesIO object to the beginning
    output.seek(0)

    return output
