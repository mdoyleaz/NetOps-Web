import ipaddress


class IpCalcVerFour(object):
    def __init__(self, address, prefix):
        self.address = address
        self.prefix = prefix

        self.subnet = ipaddress.ip_network(f'{address}/{prefix}')

        self.usable = f"{self.subnet[2]} - {self.subnet[-2]}"
        self.netmask = str(self.subnet.netmask)
        self.gateway = str(self.subnet[1])
        self.total_int = len(list(self.subnet))

    def __dict__(self):
        subnet_breakdown = {'subnet': str(self.subnet),
                            'usable': self.usable,
                            'gateway': self.gateway,
                            'netmask': self.netmask,
                            'total_int': self.total_int,
                            'total_usable': self.total_int - 3}


        return subnet_breakdown

    def get_supernet(self, prefix):
        supernet = self.subnet.supernet(new_prefix=prefix)

        return supernet

    def get_children(self, prefix):
        subnet_list = [str(child) for child in list(
            self.subnet.subnets(new_prefix=prefix))]

        return subnet_list

    def children_as_gateawy(self, prefix):
        pass
