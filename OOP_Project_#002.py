class Server:
    IP = 0

    def __init__(self):
        self.buffer = []
        self.ip = Server.IP

    def __new__(cls, *args, **kwargs):
        cls.IP += 1
        return object.__new__(cls)

    def send_data(self, data):
        Router.buffer.append(data)

    def get_data(self):
        copy_buffer = self.buffer[:]
        self.buffer = []
        return copy_buffer

    def get_ip(self):
        return self.ip


class Router:
    buffer = []
    link_servers = {}

    def link(self, server):
        if not server.ip in self.link_servers:
            self.link_servers[server.ip] = server

    def unlink(self, server):
        if server.ip in self.link_servers:
            del self.link_servers[server.ip]

    def send_data(self):
        for i in self.buffer:
            if i.ip in self.link_servers:
                self.link_servers[i.ip].buffer.append(i)
            else:
                continue
        self.buffer = []
        self.link_servers = {}


class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip


router = Router()
sv_from = Server()
sv_from2 = Server()
router.link(sv_from)
router.link(sv_from2)
router.link(Server())
router.link(Server())
sv_to = Server()
router.link(sv_to)
sv_from.send_data(Data("Hello", sv_to.get_ip()))
sv_from2.send_data(Data("Hello", sv_to.get_ip()))
sv_to.send_data(Data("Hi", sv_from.get_ip()))
router.send_data()
msg_lst_from = sv_from.get_data()
msg_lst_to = sv_to.get_data()