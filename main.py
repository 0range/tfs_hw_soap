import logging
logging.basicConfig(level=logging.DEBUG)

from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode

from spyne import Iterable
from spyne import ComplexModel

from spyne.protocol.soap import Soap11

from spyne.server.wsgi import WsgiApplication

class ResponseUsersListItem(ComplexModel):
    userName = Unicode
    userId = Unicode

class ResponseUserInfo(ComplexModel):
    userId = Unicode
    userHWHard = Unicode
    userHWEasy = Unicode

class HomeWorkSevice(ServiceBase):
    @rpc(Unicode, _returns=Iterable(ResponseUsersListItem))
    def users(ctx, name):
        with open('data.data','r') as inputFile:
            for line in inputFile:
                if name in line.split(',')[0]:
                    retval = ResponseUsersListItem()
                    retval.userName = line.split(',')[0]
                    retval.userId = line.split(',')[1]
                    yield retval

    @rpc(Unicode, _returns=ResponseUserInfo)
    def userInfo(ctx, id):
        with open('data.data','r') as inputFile:
            for line in inputFile:
                if id in line.split(',')[1]:
                    retval = ResponseUserInfo()
                    retval.userId = id
                    retval.userHWEasy = """1. Заведите бота в телеграм с
названием tfs_hw_name_surname_bot
2. Изучите API Telegram, научитесь с помощью Postman читать сообщения, 
которые пишут в бота, и отправлять ботом сообщения
3. Сделайте, чтобы бот в ответ на сообщение отправлял его же 
(здесь можно использовать сервис konnektor.io)"""
                    if len(line.split(',')[0]) % 3 == 0:
                        retval.userHWHard = """Научите своего бота
 переводить полученное сообщение на английский"""
                    elif len(line.split(',')[0]) % 3 == 1:
                        retval.userHWHard = """Научите своего бота
отправлять в ответ на сообщение картинку со схожим смыслом"""
                    else:
                        retval.userHWHard = """Научите своего бота
вести осмысленный диалог"""
                    return retval

application = Application([HomeWorkSevice],
    tns='tfs.homework',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 80, wsgi_app)
    server.serve_forever()
