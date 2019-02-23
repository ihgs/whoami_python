import responder
from whoami.neo4j.client import UserHandler, SystemHandler, Neo4jClient
from whoami.exception import NotLogined
from whoami.identify.user import UserDao
from whoami.session import Session
from pathlib import Path
import os


api = responder.API()
api.add_route(static=True)


def _load_static(type, file):
    staticfile = (Path(os.path.abspath("static")) / type / file).resolve()
    if os.path.exists(staticfile):
        with open(staticfile, "r") as f:
            content = f.read()
    return content


# TODO
@api.route("/js/{file}")
def js(req, resp, file):
    resp.content = None
    resp.text = _load_static("js", file)


@api.route("/css/{file}")
def css(req, resp, file):
    resp.content = None
    resp.text = _load_static("css", file)


def logined_user(req):
    try:
        print(req.cookies)
        key = req.cookies['token']
        value = Session().get(key)
        print(value)
        # TODO
        # return resp.session['username']
        return value
    except KeyError:
        raise NotLogined


@api.route("/api/v1/auth/login")
async def login(req, resp):
    data = await req.media()
    userid = data['userid']
    password = data['password']
    result = UserDao.identify(userid, password)
    key = Session().new(result)
    resp.cookies['token'] = key
    resp.cookies['Path'] = '/'
    resp.media = {'userid': userid}


@api.route("/api/v1/systems")
async def systems(req, resp):
    client = Neo4jClient()
    current_user = logined_user(req)
    sh = SystemHandler(client)
    if req.method == 'get':
        uh = UserHandler(client)
        user = uh.find(current_user["userid"])
        usersystems = uh.systems(user)
        resp.media = []
        for system in sh.list():
            id = system.identity
            system['id'] = id
            for us in usersystems:
                if id == us.end_node.identity:
                    system['use'] = True
                    break
            resp.media.append(system)
    elif req.method == 'post':
        data = await req.media()
        sh.create(data['name'])
        resp.media = ''
        resp.status_code = 202


@api.route("/api/v1/userinfo")
def userinfo(req, resp):
    try:
        current_user = logined_user(req)
        client = Neo4jClient()
        uh = UserHandler(client)
        user = uh.find(current_user["userid"])
        systems = uh.systems(user)
        systemsList = []
        for system in systems:
            end_node = system.end_node
            systemsList.append({
                "id": end_node.identity,
                "name": end_node['name'],
                "loginid": system['loginid']
            })
        userinfo = {
            "userinfo": {
                "id": user.identity,
                "userid": user['userid'],
                "systems": systemsList
            }
        }
        resp.media = userinfo
    except NotLogined:  # TODO errohandling ができるようになったら修正する　https://github.com/kennethreitz/responder/issues/258
        resp.status_code = 403
        resp.text = ''


@api.route("/api/v1/user/system/{system_id}")
async def use_system(req, resp, *, system_id):
    try:
        current_user = logined_user(req)
        client = Neo4jClient()
        if req.method == 'post':
            data = await req.media()
            loginid = data['loginid']
            sh = SystemHandler(client)
            system = sh.get(int(system_id))
            uh = UserHandler(client)
            user = uh.find(current_user["userid"])
            uh.use_system(user, system, loginid, 'memo')  # TODO
        elif req.method == 'delete':
            uh = UserHandler(client)
            user = uh.find(current_user["userid"])
            systems = uh.systems(user)
            for system in systems:
                if system.end_node.identity == int(system_id):
                    uh.disuse_system(system)
    except NotLogined:  # TODO errohandling ができるようになったら修正する　https://github.com/kennethreitz/responder/issues/258
            resp.status_code = 403
            resp.text = ''

if __name__ == '__main__':
    api.run()
