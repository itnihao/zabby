from zabby.core.utils import validate_mode
from zabby.hostos import detect_host_os

__all__ = ['incoming', 'outgoing', ]

NET_MODES = ['bytes', 'packets', 'errors', 'dropped', ]


def incoming(interface_name, mode="bytes", host_os=detect_host_os()):
    """
    Returns amount of received bytes or packets, dropped incoming packets or
    receive errors

    :depends on: [host_os.net_interface_names, host_os.net_interface_info]
    :raises: WrongArgument if unsupported mode is supplied
    :raises: WrongArgument if interface is not present on this host
    :type interface_name: str
    """
    validate_mode(mode, NET_MODES)

    interface_names = host_os.net_interface_names()
    validate_mode(interface_name, interface_names)

    info = host_os.net_interface_info(interface_name)

    return info._asdict()[
        "{direction}_{mode}".format(direction='in', mode=mode)
    ]


def outgoing(interface_name, mode="bytes", host_os=detect_host_os()):
    """
    Returns amount of sent bytes or packets, dropped outgoing packets or
    send errors

    :depends on: [host_os.net_interface_names, host_os.net_interface_info]
    :raises: WrongArgument if unsupported mode is supplied
    :raises: WrongArgument if interface is not present on this host
    :type interface_name: str
    """
    validate_mode(mode, NET_MODES)

    interface_names = host_os.net_interface_names()
    validate_mode(interface_name, interface_names)

    info = host_os.net_interface_info(interface_name)

    return info._asdict()[
        "{direction}_{mode}".format(direction='out', mode=mode)
    ]
