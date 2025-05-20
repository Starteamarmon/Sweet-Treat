from tortoise import Tortoise, fields, models

class User(models.Model):
    chat_id = fields.IntField(unique=True)
    name = fields.CharField(max_length=100)

    def __str__(self):
        return f"User(id={self.id}, name={self.name})"


class Order(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='orders')
    order = fields.CharField(max_length=255)
    date_creat = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ номер {self.id}\n{self.order}\nДата создания:{self.date_creat})"

