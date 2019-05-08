from peewee import *


class MySQLConnConfig:
    def __init__(self, db_name, user, password, host, port):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port


def init_database(db_name='nb_spam', user='root', password='root', host='localhost', port=3306,
                  mysql_config: MySQLConnConfig = None):
    if mysql_config is not None:
        return MySQLDatabase(mysql_config.db_name, user=mysql_config.user, password=mysql_config.password,
                             host=mysql_config.host, port=mysql_config.port)
    return MySQLDatabase(db_name, user=user, password=password, host=host, port=port)


def init_model(db):
    class MediumTextField(TextField):
        field_type = 'MEDIUMTEXT'

    class MediumBlobField(BlobField):
        field_type = 'MEDIUMBLOB'

    class BaseModel(Model):
        class Meta:
            database = db

    class Mail(BaseModel):
        path = CharField(unique=True)
        spam = BooleanField()
        content = MediumTextField()
        words_blob = MediumBlobField()
        message_blob = MediumBlobField()

    if db.is_closed():
        db.connect()
    db.create_tables([Mail])

    return Mail
