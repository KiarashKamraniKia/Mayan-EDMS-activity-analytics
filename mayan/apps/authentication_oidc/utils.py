import unicodedata


def generate_username_from_email(email):
    return unicodedata.normalize('NFKC', email)[:150]
