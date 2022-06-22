from django.core.validators import RegexValidator


class UsernameValidator(RegexValidator):
    regex = r'^[\w.@+-]+$'
    flags = 0
