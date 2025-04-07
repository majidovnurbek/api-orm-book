from tortoise import fields
from tortoise.models import Model

class Book(Model):
    id = fields.IntField(pk=True)
    author = fields.ForeignKeyField('models.User', related_name='books')
    title = fields.CharField(max_length=100)
    description = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
