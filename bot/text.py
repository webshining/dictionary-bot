from enum import Enum

from django.utils.translation import gettext_lazy as _


class Text(Enum):
    DICTIONARIES_BUTTON = _("🔤 Dictionaries")
    CREATE_DICTIONARY_BUTTON = _("Create dictionary")
    SELECT_DICTIONARY = _("Select dictionary:")
    DICTIONARY_NOT_FOUND = _("Dictionary not found")

    LANGUAGE_BUTTON = _("🌐 Bot language")
    SELECT_LANGUAGE = _("Select language <code>[</code>{}<code>]</code>:")
    LANGUAGE_CHANGED = _("Language changed")

    CARDS_BUTTON = _("🧠 Cards")

    START = _("Hello <b>{}</b>")

    VIEW_BUTTON = _("View")
    SAVE_BUTTON = _("Save")

    def __str__(self):
        return str(self.value)
