import gettext
import os

def setup_translation(locale_code: str, domain: str):
    """
    Sets up the translation for the given locale and domain.
    Args:
        locale_code (str): The locale code (e.g., 'en', 'ar').
        domain (str): The translation domain (e.g., 'helwan_insight').
    Returns:
        function: The _ (gettext) function for translation.
    """
    localedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'locales')
    
    try:
        lang = gettext.translation(domain, localedir=localedir, languages=[locale_code, 'en'], fallback=True)
        lang.install()
        return lang.gettext
    except Exception as e:
        return lambda text: text
