import re
from rest_framework.serializers import ValidationError


class YoutubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r'(https?://)?(www\.)?'
                         r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
                         r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        tmp_val = dict(value).get(self.field)
        if not bool(reg.match(tmp_val)):
            raise ValidationError('Ссылка должна вести на youtube.com')
