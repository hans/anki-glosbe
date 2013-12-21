import itertools
import json
import urllib

GLOSBE_TRANSLATE_URL = ("http://glosbe.com/gapi_v0_1/translate?format=json&"
                        "from={from_lang}&dest={dest_lang}&phrase={phrase}")

def get_translations(phrase, from_lang, dest_lang):
    """Translate the phrase `phrase` from language `from_lang` to
    language `dest_lang` using the Glosbe API.

    `from_lang` and `dest_lang` must be valid ISO 639-3 language codes.
    `phrase` should be a Unicode string.

    Returns a tuple of the form `(phrases, meanings)`, where `phrases`
    is a list of possible equivalent phrases in the `dest_lang` language
    and `meanings` is a list of meanings for `phrase` (explained in the
    `dest_lang` language). Invalid phrases will yield a result of `([],
    [])`.

    Returns `None` on API error.
    """

    url = GLOSBE_TRANSLATE_URL.format(phrase=phrase, from_lang=from_lang,
                                      dest_lang=dest_lang)
    handle = urllib.urlopen(url)
    data = json.loads(handle.read())
    handle.close()

    if data['result'] != 'ok':
        return None

    phrases = [entry['phrase']['text'] for entry in data['tuc']
               if 'phrase' in entry and entry['phrase']['language'] == dest_lang]

    meanings_nested = [[meaning['text'] for meaning in entry['meanings']
                        if meaning['language'] == dest_lang]
                       for entry in data['tuc'] if 'meanings' in entry]
    meanings = list(itertools.chain.from_iterable(meanings_nested))

    return phrases, meanings
