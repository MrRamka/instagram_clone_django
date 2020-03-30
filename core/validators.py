from django.core import validators


class HashTagValidator(validators.RegexValidator):
    regex = '\w+'
    message = (
        'Enter a valid hashtag. This value may contain only English letters'
    )
    flags = 0

