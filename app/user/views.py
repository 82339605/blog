#针对用户业务逻辑处理的视图和路由
from . import user
@user.route('/user')
def userfirst():
    return '这是user首页'