import json
import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.templatetags.static import static


_manifest_contents = None


class NoManifestFileException(FileNotFoundError):
    pass


class NoManifestSetting(KeyError):
    pass


def get_static_url(resource_path, extension=None):
    """Gets static url to resource file.
    Returns:
        Static url to filename or None when filename was'nt in manifest file.
    """
    data = _read_manifest_file()

    if extension:
        filename = data.get(
            '{}.{}'.format(resource_path, extension), None)
    else:
        filename = data.get(resource_path, None)

    if not filename:
        return None
    else:
        return static(filename)


def _read_manifest_file():
    """Reads manifest file.
    Returns:
        If no exception returns json data with filenames and their static paths.
    Raises:
        NoManifestFileException: When no manifest file at path in WEBPACK_MANIFEST_FILE setting.
        ValueError: When file does not contain valid json data.
        IOError: When error while reading file.
    """
    global _manifest_contents

    if not settings.DEBUG and _manifest_contents:
        return _manifest_contents

    if settings.WEBPACK_MANIFEST_FILE:
        path = os.path.normpath(settings.WEBPACK_MANIFEST_FILE)
    else:
        error_string = """
            You have to specify manifest file generated by
            webpack-assets-manifest plugin in your settings like this:
            WEBPACK_MANIFEST_FILE = os.path.join(BASE_DIR, 'example.json')
        """
        raise NoManifestSetting(error_string)

    try:
        with open(path) as file:
            _manifest_contents = json.loads(file.read())
            return _manifest_contents
    except FileNotFoundError as e:
        raise NoManifestFileException(
            'No manifest file at this path ' + path + ' check WEBPACK_MANIFEST_FILE setting.'
        ) from e
    except json.JSONDecodeError as e:
        raise ValueError('Manifest file do not contains valid json data.') from e
    except IOError as e:
        raise IOError('Error while reading manifest file.') from e


def compose_email(
    receivers,
    subject_tpl,
    msg_tpl,
    subject_ctx=None,
    msg_ctx=None,
    reply_to=None,
    attachments=[]):
    sender = settings.DEFAULT_FROM_EMAIL
    subject = loader.render_to_string(subject_tpl, subject_ctx)
    message = loader.render_to_string(msg_tpl, msg_ctx)

    email = EmailMultiAlternatives(
        subject,
        message,
        sender,
        receivers,
        reply_to=[reply_to],
    )
    email.attach_alternative(message, 'text/html')

    for attachment in attachments:
        email.attach(*attachment)

    email.send()
