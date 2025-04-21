import ipaddress
import logging


class IpNetworks:
    """
    A Class that contains a list of IPvXNetwork objects.

    Credits to https://djangosnippets.org/snippets/1862/
    """

    networks = []

    def __init__(self, addresses):
        """Create a new IpNetwork object for each address provided."""
        for address in addresses:
            self.networks.append(ipaddress.ip_network(address))

    def __contains__(self, address):
        """Check if the given address is contained in any of our Networks."""
        logger = logging.getLogger(__name__)
        logger.debug('Checking address: "%s".', address)
        for network in self.networks:
            if ipaddress.ip_address(address) in network:
                return True
        return False
