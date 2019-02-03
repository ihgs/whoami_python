import responder
from whoami.neo4j.client import UserHandler, SystemHandler, Neo4jClient
from whoami.exception import NotLogined


api = responder.API()


def logined_user(resp):
    try:
        # TODO
        # return resp.session['username']
        return {
            "userid": "testaa",
            "roles": ["admin", "user"]
        }
    except KeyError:
        raise NotLogined


@api.route("/api/v1/auth/login")
def login(req, resp):
    # TODO
    resp.session['userid'] = "testaa"
    print(req.cookies)
    resp.media = {'userid': resp.session['userid']}


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
