#-*- coding: UTF-8 -*-    

import os
from app import create_app, db   #这里没有指定app.说明是从__init__中导入符号
from app.models import User, Role
from flask_migrate import Migrate
from flask_script import Manager, Server    #pip install flask_script

#https://www.cnblogs.com/weedboy/p/6862158.html  解决.format(feature)抛异常：UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128)
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )   #这里定义后，后面字符串就不需要额外使用unicode(comment,'utf-8')， 否则会报错，提示TypeError: decoding Unicode is not supported


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)                                        #数据库迁移更新使用，有时间再琢磨
manager = Manager(app)
manager.add_command('start', Server(host='0.0.0.0', port=5000))


@app.shell_context_processor
def make_shell_context():   #什么作用：  python manage.py shell 支持shell模式，并自动导入db的符号，不用在shell下from xx import yy
    return dict(db=db, User=User, Role=Role)


@app.cli.command()    #什么作用： 测试
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    
#debug=True 表示调试模式，flask检测到文件内容修改会重新启动服务
#host='0.0.0.0' 表示监听监听所有公网 IP，否则只能本地测试http://127.0.0.1:5000/
if __name__ == '__main__':
    manager.run()          #python manage.py start  bash下执行，不要忘记带参数start
    #app.run(host='0.0.0.0', debug=True)
    #db.create_all()
    #db.session.add(Tupian(name='1.jpg',label='特朗普',text='嘲讽  笨蛋 你狠'))
    #db.session.add_all([Tupian(name='2.jpg',label='特朗普',text='嘲讽  笨蛋 你狠'),Tupian(name='3.jpg',label='特朗普',text='嘲讽  笨蛋 你狠'),Tupian(name='4.jpg',label='特朗普',text='嘲讽  笨蛋 你狠')])
    #db.session.commit()
    #Tupian.query.all()