import face_recognition as fr
import numpy as np
import logging
from profiles.models import Profile

logger = logging.getLogger(__name__)

def is_ajax(request):
    logger.debug("Checking if request is AJAX.")
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def get_encoded_faces():
    """
    Load all user profile images, encode their faces, and return a dict of {email: encoding}.
    """
    logger.debug("Retrieving all Profile objects from the database.")
    qs = Profile.objects.all()

    encoded = {}

    logger.debug(f"Found {len(qs)} profiles.")
    for p in qs:
        try:
            logger.debug(f"Processing profile for user: {p.user.email}")
            # Load the user's profile image
            face = fr.load_image_file(p.photo.path)
            logger.debug(f"Loaded image from {p.photo.path}")

            # Encode the face
            face_encodings = fr.face_encodings(face)
            if len(face_encodings) > 0:
                encoding = face_encodings[0]
                encoded[p.user.email] = encoding
                logger.debug(f"Successfully encoded face for {p.user.email}")
            else:
                logger.warning(f"No face found in image for user: {p.user.email}")

        except Exception as e:
            logger.error(f"Error encoding face for user {p.user.email}: {e}", exc_info=True)

    logger.debug("Completed encoding all faces.")
    return encoded

def classify_face(img):
    """
    Classify the first detected face in the given image.
    Returns the matching user's email or 'Unknown' if no match is found.
    Returns False if no faces are found or an error occurs.
    """
    logger.debug(f"Attempting to classify face in image: {img}")

    # Load known faces
    logger.debug("Loading known faces and their encodings.")
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    logger.debug(f"Number of known faces: {len(known_face_names)}")

    # Attempt to load the input image
    try:
        logger.debug("Loading the input image for classification.")
        test_image = fr.load_image_file(img)
    except Exception as e:
        logger.error(f"Error loading image {img}: {e}", exc_info=True)
        return False

    try:
        logger.debug("Locating faces in the provided image.")
        face_locations = fr.face_locations(test_image)

        if not face_locations:
            logger.warning("No faces found in the provided image.")
            return False

        logger.debug(f"Found {len(face_locations)} face(s) in the image.")
        logger.debug("Encoding faces found in the image.")
        unknown_face_encodings = fr.face_encodings(test_image, face_locations)

        if not unknown_face_encodings:
            logger.warning("No encodings generated for detected face(s).")
            return False

        logger.debug("Comparing detected face encodings to known faces.")
        face_names = []
        for i, face_encoding in enumerate(unknown_face_encodings):
            logger.debug(f"Comparing face {i+1}/{len(unknown_face_encodings)}")

            matches = fr.compare_faces(faces_encoded, face_encoding)
            face_distances = fr.face_distance(faces_encoded, face_encoding)

            best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else None
            if best_match_index is not None and matches[best_match_index]:
                name = known_face_names[best_match_index]
                logger.debug(f"Match found: {name}")
            else:
                name = "Unknown"
                logger.debug("No match found for this face.")

            face_names.append(name)

        if face_names:
            logger.debug(f"Returning the first detected face name: {face_names[0]}")
            return face_names[0]
        else:
            logger.debug("No face names identified.")
            return False

    except Exception as e:
        logger.error(f"Error occurred during face classification: {e}", exc_info=True)
        return False
