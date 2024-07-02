from django.db import models


class NumberChoicesType(models.IntegerChoices):
    one = 1, 'Исходящий'
    two = 2, 'Входящий'
    three = 3, 'Входящий с перенаправлением'
    four = 4, 'Обратный'


class NumberChoicesAddToChat(models.IntegerChoices):
    zero = 0, 'Не уведомлять'
    one = 1, 'Уведомлять'


class NumberChoicesShow(models.IntegerChoices):
    zero = 0, 'Не показывать карточку звонка'
    one = 1, 'Показывать карточку звонка'


class NumberChoicesCreateCRM(models.IntegerChoices):
    zero = 0, 'Не создавать CRM сущность, связанную со звонком'
    one = 1, 'Создать CRM сущность, связанную со звонком'
