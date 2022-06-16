from sqlalchemy import Column, Numeric, String

from scenario.modules.sql import BASE, SESSION


class fforceSubscribe(BASE):
    __tablename__ = "fforceSubscribe"
    chat_id = Column(Numeric, primary_key=True)
    channel = Column(String)

    def __init__(self, chat_id, channel):
        self.chat_id = chat_id
        self.channel = channel


fforceSubscribe.__table__.create(checkfirst=True)


def fs_settings(chat_id):
    try:
        return (
            SESSION.query(fforceSubscribe)
            .filter(fforceSubscribe.chat_id == chat_id)
            .one()
        )
    except:
        return None
    finally:
        SESSION.close()


def add_channel(chat_id, channel):
    adder = SESSION.query(fforceSubscribe).get(chat_id)
    if adder:
        adder.channel = channel
    else:
        adder = fforceSubscribe(chat_id, channel)
    SESSION.add(adder)
    SESSION.commit()


def disapprove(chat_id):
    rem = SESSION.query(fforceSubscribe).get(chat_id)
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
