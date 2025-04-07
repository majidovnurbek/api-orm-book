from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=120)
    email = fields.CharField(max_length=120,unique=True)
    username=fields.CharField(max_length=120,unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)

        