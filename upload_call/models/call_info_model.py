import os

from django.db import models
from django.conf import settings
from mutagen.mp3 import MP3

from upload_call.models.choices_models import NumberChoicesType, NumberChoicesAddToChat, NumberChoicesCreateCRM, NumberChoicesShow


class CallInfo(models.Model):
    user_phone = models.CharField(max_length=20, null=False, blank=False)
    user_id = models.IntegerField(blank=False, null=False)
    phone_number = models.CharField(max_length=50, blank=False, null=False)
    call_date = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(null=False, blank=False,
                               choices=NumberChoicesType.choices)
    duration = models.IntegerField(null=True, blank=True)
    add_to_chat = models.IntegerField(blank=True, null=True,
                                      choices=NumberChoicesAddToChat.choices)
    call_id = models.CharField(max_length=255, null=True, blank=True)

    show_call = models.IntegerField(null=False, blank=False,
                               choices=NumberChoicesShow.choices)
    create_crm = models.IntegerField(null=False, blank=False,
                               choices=NumberChoicesCreateCRM.choices)

    inner_media_path = "rings/"
    filename = ""
    file = models.FileField(upload_to=inner_media_path, null=True, blank=True)
    # file_path = os.path.join(call.inner_media_path, str(call.id) + '.mp3')

    def telephony_externalcall_register(self, but):
        res = but.call_api_method("telephony.externalcall.register", {
            "USER_PHONE_INNER": self.user_phone,
            "USER_ID": self.user_id,
            "PHONE_NUMBER": self.phone_number,
            "CALL_START_DATE": self.call_date,
            "TYPE": self.type,
            "CRM_CREATE": self.create_crm,  # создание лида
            "SHOW": self.show_call, # показывать карточку звонка
        })

        self.call_id = res['result']['CALL_ID']
        self.duration = int(MP3(self.file).info.length)
        # self.filename = str(self.file)[len(self.inner_media_path):-len(os.path.splitext(str(self.file))[-1])]
        self.filename = str(self.file)[len(self.inner_media_path):]

        self.save()

    def telephony_externalcall_finish(self, but):
        but.call_api_method('telephony.externalcall.finish', {
            "CALL_ID": self.call_id,
            "USER_ID": self.user_id,
            "DURATION": self.duration,
            # "RECORD_URL": f'https://{settings.APP_SETTINGS.app_domain}/media/{self.inner_media_path}{self.filename}.mp3',
            "ADD_TO_CHAT": self.add_to_chat,
        })

    def telephony_externalcall_attach_record(self, but):
        # Метод прикрепляет запись к завершенному звонку
        but.call_api_method('telephony.externalCall.attachRecord', {
            "CALL_ID": self.call_id,
            "FILENAME": self.filename,
            "RECORD_URL": f'https://{settings.APP_SETTINGS.app_domain}/media/{self.inner_media_path}{self.filename}',
        })
