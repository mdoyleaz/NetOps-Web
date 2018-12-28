import ipaddress


class IpCalcVerFour(object):
    """
    IPv4 Calculator, breaks down subnets handles various ip calculations using
    the 'ipaddress' library
    Requires:
        'address' - 'str' type object representing the subnet
        'prefix'  - 'int' type object representing the subnets prefix
    """

    def __init__(self, address, prefix):
        self.address = address
        self.prefix = prefix

        self.subnet = ipaddress.ip_network(f'{address}/{prefix}', strict=False)

        self.usable = f"{self.subnet[2]} - {self.subnet[-2]}"
        self.netmask = str(self.subnet.netmask)
        self.gateway = str(self.subnet[1])
        self.broadcast = str(self.subnet[-1])
        self.total_int = len(list(self.subnet))

    def __dict__(self):
        subnet_breakdown = {'subnet': str(self.subnet),
                            'usable': self.usable,
                            'gateway': self.gateway,
                            'netmask': self.netmask,
                            'broadcast': self.broadcast,
                            'total_int': self.total_int,
                            'total_usable': self.total_int - 3
                            }

        return subnet_breakdown

    def get_supernet(self, prefix):
        supernet = self.subnet.supernet(new_prefix=prefix)

        return supernet

    def split_subnet(self, prefix):
        """
        Takes a subnet and breaks it down into smaller prefixes.
        Requeires: 'prefix' - Integer; Prefix must be smaller than main block.
        """

        try:
            subnet_list = [IpCalcVerFour(child[0], prefix).__dict__()
                           for child in self.subnet.subnets(new_prefix=prefix)]
        except ValueError as e:
            subnet_list = {'error': [str(e).capitalize()]}

        return subnet_list
