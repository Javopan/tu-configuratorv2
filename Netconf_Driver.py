from PyQt5 import QtCore as Qtc
from ncclient import manager, transport
from ncclient import NCClientError


class SikluNetconf(Qtc.QObject):
    siklunetconf_error = Qtc.pyqtSignal(str)
    siklunetconf_logs = Qtc.pyqtSignal(str)

    def __init__(self, ip_, user_='admin', password_='admin', port_=22, timeout_=5, device_params_={'name': 'nexus'},
                 hostkey_verify_=False):
        super(SikluNetconf, self).__init__()
        
        self.ip = ip_
        self.username = user_
        self.password = password_
        self.port = port_
        self.timeout = timeout_
        self.device_params = device_params_
        self.host_key = hostkey_verify_
        self.channel = None
        self.log_message = ''

    def set_connection_timeout(self, time_out_):
        self.timeout = time_out_
        self.siklunetconf_logs.emit(f'Changed the connection timeout to {time_out_}')

    def get_connection_timeout(self):
        return self.timeout

    def set_channel_timeout(self, timeout_):
        if self.channel:
            self.channel.timeout = timeout_
            self.siklunetconf_logs.emit(f'Changed the channel timeout to {timeout_}')

    def get_command(self, command_):
        """
                This fuction will send the commands to the radio via NetCONF.
                :param command_:
                Command will be the command to check, working on execution
                :return:
                tree output
                """
        try:
            if self.channel:
                answer = self.channel.get(command_)
                # self.siklunetconf_logs.emit(f'Got answer from {self.ip}')
                return answer
            return None
        except NCClientError as e:
            self.siklunetconf_error.emit(f'{e}')
            return None

    def connect(self):
        """
        Creates a connection with the given parameters via a Netconf Shell.
        By default it will auto add keys
        :return: True if connection successfully connected, False if not
        """
        try:
            self.channel = manager.connect(host=self.ip,
                                           port=self.port,
                                           username=self.username,
                                           password=self.password,
                                           device_params=self.device_params,
                                           hostkey_verify=self.host_key,
                                           timeout=self.timeout)
            self.siklunetconf_logs.emit(f'Connection sucessful to {self.ip}')
            return True
        except transport.SSHError as e:
            # print(f'Could not connect. Please check the device is enabled.\nActual python error: {e}')
            # self.log_message = e
            self.siklunetconf_error.emit(f'{e}')
            return False
        except transport.AuthenticationError as e:
            # print(f'Could not connect. Bad user/pass combination. Please review.\nActual python error: {e}')
            # self.log_message = e
            self.siklunetconf_error.emit(f'{e}')
            return False
        except transport.TransportError as e:
            # print(f'Connection suddenly broke\nActual python error: {e}')
            # self.log_message = e
            self.siklunetconf_error.emit(f'{e}')
            return False
        except NCClientError as e:
            # print(f'Something went wrong...oops\nActual python error: {e}')
            # self.log_message = e
            self.siklunetconf_error.emit(f'{e}')
            return False

    def close(self):
        self.channel.close_session()
        self.siklunetconf_logs.emit(f'Connection to {self.ip} closed')


if __name__ == '__main__':
    ip = '192.168.0.1'
    command = ''

    n366 = SikluNetconf(ip, 'admin', 'admin')
    if n366.connect():
        n366.set_channel_timeout(3)
        n366_active = n366.get_command('<filter xmlns:n366="http://siklu.com/yang/tg/radio" select="/n366:radio-common/n366:links/n366:active/n366:remote-assigned-name" type="xpath"/>')
        print(n366_active)
        print(n366.log_message)
    else:
        print('No me pude conectar')
        print(n366.log_message)
    print('Done')
    # n366_conf = n366.get_command('<filter xmlns:n366="http://siklu.com/yang/tg/radio/dn" select="/n366:radio-dn/n366:links" type="xpath"/>')
    # print(n366_conf)
    #
    # print('The_end')
