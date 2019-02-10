from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import os

class UserHandler:
    _NODE_NAME = 'User'

    def __init__(self, cli):
        self.cli = cli

    def create(self, userid):
        with self.cli.transaction() as tx:
            node = Node(self._NODE_NAME, userid=userid)
            tx.create(node)
            return node

    def find(self, userid):
        matcher = NodeMatcher(self.cli.graph)
        return matcher.match(self._NODE_NAME, userid=userid).first()

    def systems(self, node, limit=100):
        return self.cli.graph.match([node], "USE", limit)

    def use_system(self, node, system, loginid,  memo):
        prop = {
            "loginid": loginid,
            "memo": memo
            }
        with self.cli.transaction() as tx:
            rel = Relationship(node, "USE", system, **prop)
            tx.create(rel)

    def disuse_system(self, system_relation):
        with self.cli.transaction() as tx:
            tx.separate(system_relation)


class SystemHandler:
    _NODE_NAME = 'System'

    def __init__(self, cli):
        self.cli = cli

    def create(self, systemname):
        with self.cli.transaction() as tx:
            node = Node(self._NODE_NAME, name=systemname)
            tx.create(node)
            return node

    def list(self):
        matcher = NodeMatcher(self.cli.graph)
        return matcher.match(self._NODE_NAME)

    def get(self, id):
        matcher = NodeMatcher(self.cli.graph)
        return matcher.get(id)


class Neo4jClient:

    def __init__(self):
        # pylint: disable=unused-variable
        neo4j_host = os.getenv("NEO4J_HOST", "localhost")
        neo4j_port = os.getenv("NEO4J_PORT", "7687")
        self.graph = Graph(f"bolt://{neo4j_host}:{neo4j_port}")

    def transaction(self):
        return self

    def __enter__(self):
        self.tx = self.graph.begin()
        return self.tx

    def __exit__(self, excepiton_type, exception_value, traceback):
        self.tx.commit()


if __name__ == "__main__":
    client = Neo4jClient()
    uh = UserHandler(client)
    sh = SystemHandler(client)

    def seed(uh, sh):
        u = uh.create('testaa')
        s = sh.create('pqml')
        sh.create('ssp')
        uh.use_system(u, s, "pqmlid", "memo")

    # seed(uh, sh)

    # print(list(sh.list()))
    u = uh.find("testaa")
    ss = list(uh.systems(u))
    print(ss)
    print(ss[0].end_node)
    # user.disuse_system(ss[0])


