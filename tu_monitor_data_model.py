import time
from PyQt5 import QtCore as Qtc
from tu_data_model import TuDataModel
from Netconf_Driver import SikluNetconf
from SSH_Driver import SikluSsh, Answer


class TuMonitorDataModel(Qtc.QThread):
    tu_monitor_log = Qtc.pyqtSignal(str)
    tu_monitor_error = Qtc.pyqtSignal(str)
    tu_monitor_system_name = Qtc.pyqtSignal(str)
    tu_monitor_remote_sector = Qtc.pyqtSignal(str)
    tu_monitor_local_sector = Qtc.pyqtSignal(str)
    tu_monitor_remote_mac = Qtc.pyqtSignal(str)
    tu_monitor_local_role = Qtc.pyqtSignal(str)
    tu_monitor_rssi = Qtc.pyqtSignal(str)
    tu_monitor_snr = Qtc.pyqtSignal(str)
    tu_monitor_mcsrx = Qtc.pyqtSignal(str)
    tu_monitor_mcstx = Qtc.pyqtSignal(str)
    tu_monitor_perrx = Qtc.pyqtSignal(str)
    tu_monitor_pertx = Qtc.pyqtSignal(str)
    tu_monitor_txpower = Qtc.pyqtSignal(str)
    tu_monitor_drrx = Qtc.pyqtSignal(str)
    tu_monitor_drtx = Qtc.pyqtSignal(str)
    tu_monitor_rx_beam = Qtc.pyqtSignal(str)
    tu_monitor_tx_beam = Qtc.pyqtSignal(str)

    def __init__(self):
        super(TuMonitorDataModel, self).__init__()
        self.tu = TuDataModel('Monitored-Tu')
        self.connection = None
        self.connection_ssh = None
        self.connection_state = False

    def connect(self, ip_, username_, password_):
        """
        Establishes the connection to the TU
        :param ip_: str, ip no validation will be made
        :param username_: str, username to connect
        :param password_: str, password to connect
        :return: bool, true is connection was made, false otherwise
        """
        self.connection = SikluNetconf(ip_, username_, password_)  # create the connection to the desired IP
        self.connection.siklunetconf_logs.connect(self.send_logs)  # send logs to the print function
        self.connection.siklunetconf_error.connect(self.send_errors)  # send errors to the print function
        self.connection_ssh = SikluSsh(ip_, username_, password_)
        if self.connection.connect() and self.connection_ssh.connect():  # try to establish the connection
            self.connection.set_channel_timeout(1)
            self.connection_state = True
            return True
        return False

    def send_logs(self, message):
        self.tu_monitor_log.emit(message)

    def send_errors(self, message):
        self.tu_monitor_error.emit(message)

    def run(self):
        while self.connection_state:
            self.check_bu_netconf()
            self.check_bu_ssh()
            time.sleep(0.5)

    def check_bu_ssh(self):
        # SSH call for antena aligment info
        command = 'debug radio stats'
        try:
            ssh_answer = self.connection_ssh.send_command(command)
        except:
            self.tu_monitor_log.emit('Error - SSH conection lost')
            ssh_answer = None

        if ssh_answer:
            ssh_text = ssh_answer.decode()
            ssh_list = ssh_text.split('\r\n')
        else:
            ssh_list = []
            self.connection_ssh.connect()
        rx_beam = self.beam(ssh_list, 'rxBeamIdx')
        tx_beam = self.beam(ssh_list, 'txBeamIdx')
        self.tu_monitor_rx_beam.emit(rx_beam)
        self.tu_monitor_tx_beam.emit(tx_beam)

    def check_bu_netconf(self):
        activity_message = '<filter xmlns:rb-tg-radio="http://siklu.com/yang/tg/" select="/" type="xpath"/>'
        tu_answer = self.connection.get_command(activity_message)
        if tu_answer and len(tu_answer.data) == 9:  # there is an answer
            # the elements are: 0 database-version, 1 interfaces, 2 inventory, 3 ip, 4 radio-common, 5 radio-dn,
            # 6 system, 7 user-bridge, 8 user-management
            _, interfaces, inventory, ip, radio_common, radio_dn, system, user_bridge, user_management = \
                tu_answer.data.getchildren()

            # we get the active links
            self.process_radio_common(radio_common)

    @staticmethod
    def beam(answer_list, beam):
        """
        Looks for the beam text in the list and returns the value
        :param answer_list: list with ssh answer
        :param beam: str it can be rxBeamIdx or txBeamIdx
        :return: beam value
        """
        beam_result = 'NA'

        beams = {
            '0': 'Elev: -20 Az: -40',
            '1': 'Elev: -20 Az: -32',
            '2': 'Elev: -20 Az: -24',
            '3': 'Elev: -20 Az: -16',
            '4': 'Elev: -20 Az: -8',
            '5': 'Elev: -20 Az: 0',
            '6': 'Elev: -20 Az: 8',
            '7': 'Elev: -20 Az: 16',
            '8': 'Elev: -20 Az: 24',
            '9': 'Elev: -20 Az: 32',
            '10': 'Elev: -20 Az: 40',
            '11': 'Elev: -10 Az: 44',
            '12': 'Elev: -10 Az: 36',
            '13': 'Elev: -10 Az: 28',
            '14': 'Elev: -10 Az: 20',
            '15': 'Elev: -10 Az: 12',
            '16': 'Elev: -10 Az: 4',
            '17': 'Elev: -10 Az: 0',
            '18': 'Elev: -10 Az: -4',
            '19': 'Elev: -10 Az: -12',
            '20': 'Elev: -10 Az: -20',
            '21': 'Elev: -10 Az: -28',
            '22': 'Elev: -10 Az: -36',
            '23': 'Elev: -10 Az: -44',
            '24': 'Elev: 0 Az: -40',
            '25': 'Elev: 0 Az: -32',
            '26': 'Elev: 0 Az: -24',
            '27': 'Elev: 0 Az: -16',
            '28': 'Elev: 0 Az: -8',
            '29': 'Elev: 0 Az: -4',
            '30': 'Elev: 0 Az: 0',
            '31': 'Elev: 0 Az: 4',
            '32': 'Elev: 0 Az: 8',
            '33': 'Elev: 0 Az: 16',
            '34': 'Elev: 0 Az: 24',
            '35': 'Elev: 0 Az: 32',
            '36': 'Elev: 0 Az: 40',
            '37': 'Elev: 10 Az: 44',
            '38': 'Elev: 10 Az: 36',
            '39': 'Elev: 10 Az: 28',
            '40': 'Elev: 10 Az: 20',
            '41': 'Elev: 10 Az: 12',
            '42': 'Elev: 10 Az: 4',
            '43': 'Elev: 10 Az: 0',
            '44': 'Elev: 10 Az: -4',
            '45': 'Elev: 10 Az: -12',
            '46': 'Elev: 10 Az: -20',
            '47': 'Elev: 10 Az: -28',
            '48': 'Elev: 10 Az: -36',
            '49': 'Elev: 10 Az: -44',
            '50': 'Elev: 20 Az: -40',
            '51': 'Elev: 20 Az: -32',
            '52': 'Elev: 20 Az: -24',
            '53': 'Elev: 20 Az: -16',
            '54': 'Elev: 20 Az: -8',
            '55': 'Elev: 20 Az: 0',
            '56': 'Elev: 20 Az: 8',
            '57': 'Elev: 20 Az: 16',
            '58': 'Elev: 20 Az: 24',
            '59': 'Elev: 20 Az: 32',
            '60': 'Elev: 20 Az: 40',
        }

        for line in answer_list:
            if beam in line:
                beam_result = line
                break
        if beam_result != 'NA':
            return beams[beam_result.split(', ')[2]]
        else:
            return beam_result

    def process_radio_common(self, netconf_msg_):
        """
        currently it will only process active links
        :param netconf_msg_:  lxml element tree with the answer
        :return:
        """
        namespace = {'n366': 'http://siklu.com/yang/tg/radio'}

        # the link names name
        xpath = 'n366:links/n366:active/n366:remote-assigned-name/text()'
        act_links_names = self.process_netconf_answer(netconf_msg_, xpath, namespace)
        if act_links_names:
            self.tu_monitor_system_name.emit(act_links_names[0])
        else:
            self.tu_monitor_system_name.emit('-')

        xpath = 'n366:links/n366:active/n366:actual-remote-sector-index/text()'
        remote_sector = self.process_netconf_answer(netconf_msg_, xpath, namespace)
        if remote_sector:
            self.tu_monitor_remote_sector.emit(remote_sector[0])
        else:
            self.tu_monitor_remote_sector.emit('-')

        xpath = 'n366:links/n366:active/n366:actual-local-sector-index/text()'
        local_sector = self.process_netconf_answer(netconf_msg_, xpath, namespace)
        if local_sector:
            self.tu_monitor_local_sector.emit(local_sector[0])
        else:
            self.tu_monitor_local_sector.emit('-')

        xpath = 'n366:links/n366:active/n366:remote-mac-addr/text()'
        remote_mac = self.process_netconf_answer(netconf_msg_, xpath, namespace)
        if remote_mac:
            self.tu_monitor_remote_mac.emit(remote_mac[0])
        else:
            self.tu_monitor_remote_mac.emit('-')

        xpath = 'n366:links/n366:active/n366:local-role/text()'
        local_role = self.process_netconf_answer(netconf_msg_, xpath, namespace)
        if local_role:
            self.tu_monitor_local_role.emit(local_role[0])
        else:
            self.tu_monitor_local_role.emit('-')

        xpath = 'n366:links/n366:active/n366:rssi/text()'
        rssi = self.process_netconf_answer(netconf_msg_, xpath, namespace)
        if rssi:
            self.tu_monitor_rssi.emit(rssi[0])
        else:
            self.tu_monitor_rssi.emit('-')

        xpath = 'n366:links/n366:active/n366:snr/text()'
        snr = self.process_netconf_answer(netconf_msg_, xpath, namespace)
        if snr:
            self.tu_monitor_snr.emit(snr[0])
        else:
            self.tu_monitor_snr.emit('-')

        xpath = 'n366:links/n366:active/n366:mcs-rx/text()'
        mcs_rx = self.process_netconf_answer(netconf_msg_, xpath, namespace)
        if mcs_rx:
            self.tu_monitor_mcsrx.emit(mcs_rx[0])
        else:
            mcs_rx = ['0']
            self.tu_monitor_mcsrx.emit('-')

        xpath = 'n366:links/n366:active/n366:mcs-tx/text()'
        mcs_tx = self.process_netconf_answer(netconf_msg_, xpath, namespace)
        if mcs_tx:
            self.tu_monitor_mcstx.emit(mcs_tx[0])
        else:
            mcs_tx = ['0']
            self.tu_monitor_mcstx.emit('-')

        xpath = 'n366:links/n366:active/n366:rx-per/text()'
        perrx = self.process_netconf_answer(netconf_msg_, xpath, namespace)
        if perrx:
            self.tu_monitor_perrx.emit(perrx[0])
        else:
            self.tu_monitor_perrx.emit('-')

        xpath = 'n366:links/n366:active/n366:tx-per/text()'
        pertx = self.process_netconf_answer(netconf_msg_, xpath, namespace)
        if pertx:
            self.tu_monitor_pertx.emit(pertx[0])
        else:
            self.tu_monitor_pertx.emit('-')

        xpath = 'n366:links/n366:active/n366:tx-power-index/text()'
        tx_power = self.process_netconf_answer(netconf_msg_, xpath, namespace)
        if tx_power:
            self.tu_monitor_txpower.emit(tx_power[0])
        else:
            self.tu_monitor_txpower.emit('-')

        dr_rx = self.translate_mcs(mcs_rx[0])
        self.tu_monitor_drrx.emit(dr_rx)

        dr_tx = self.translate_mcs(mcs_tx[0])
        self.tu_monitor_drtx.emit(dr_tx)


    @staticmethod
    def translate_mcs(mcs):
        """
        Translates MCS index to datarrate
        :param mcs: index with the datarrate to translate
        :return:
        """

        datarrate_dic = {
            '0': '-',
            '1': '-',
            '2': '620',
            '3': '780',
            '4': '950',
            '5': '-',
            '6': '1025',
            '7': '1580',
            '8': '1900',
            '9': '2050',
            '10': '2500',
            '11': '3150',
            '12': '3800',
        }

        return datarrate_dic[mcs]

    @staticmethod
    def process_netconf_answer(netconf_msg_, xpath, namespace):
        """
        Processes a netconf message to return the text
        :param netconf_msg_: ncclient answer
        :param xpath: str, xpath address in a tree to get the answe
        :param namespace: dict, dictionary with the xlmns
        :return: list, with answer
        """
        processed_msg = netconf_msg_.xpath(xpath, namespaces=namespace)
        return processed_msg
