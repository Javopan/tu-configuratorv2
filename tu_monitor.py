from PyQt5 import QtCore as Qtc
from tu_data_model import TuDataModel
from Netconf_Driver import SikluNetconf
from ncclient import NCClientError
from ncclient.xml_ import to_ele
import xml
from lxml import etree


class TuExpanded(TuDataModel, Qtc.QObject):
    # We inherit from the data model for the tu to have al the info available
    # we injerit from Qtc.Object to be able to use signals and slots
    tu_errors = Qtc.pyqtSignal(str)  # send errors
    tu_logs = Qtc.pyqtSignal(str)  # send logs

    def __init__(self, name):
        super().__init__(name)
        super(Qtc.QObject, self).__init__()
        # will hold the configuration
        self.configuration = None
        # Holds the instance of the connection
        self.connection = None
        # Holds the number of ports the unit has
        self.ports_number = 1  # minimum number of ports

    def get_ports_number(self):
        return self.ports_number

    def set_ports_number(self, ports):
        self.ports_number = ports

    def get_name(self):
        return self.name

    def set_configuration(self, config):
        self.configuration = config

    def get_configuration(self):
        return self.configuration

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
        if self.connection.connect():  # try to establish the connection
            self.connection.set_channel_timeout(1)
            self.connection_state = True
            return True
        return False

    def get_startup_config(self):
        """
        This fuction will get the startup configuration of the radio via NetCONF.
        :return: lxml, config tree
        """
        try:
            # calls the ncclient to get the startup config
            startup_config = self.connection.channel.get_config('startup')
            self.tu_logs.emit(f'Got startup config from {self.connection.ip}')
            self.set_configuration(startup_config.data)
        except NCClientError as e:
            self.tu_errors.emit(f'{e}')

    def prepare_config(self, config, new_ssid, new_ssid_pass, new_ip, new_prefix, new_gateway, admin_pass,
                       new_ip_local, new_prefix_local, line_port, line_port_vlan, management_vlan):
        """
        Fuction that will modify the configuration to be accepted by the unit to send
        :param new_prefix_local: str, new local prefix
        :param new_ip_local: str, new local ip
        :param admin_pass: str, new admin pass
        :param new_gateway: str, ip address for the gateway
        :param new_prefix: str, prefix length for the network mask
        :param new_ip: str, ip to assign to the unit
        :param new_ssid_pass: str, password for the ssid
        :param new_ssid: str, new ssid
        :param config: lxml, a configuration just downloaded by the driver. No alterations
        :return: bool, if adapting the configuration was successful
        """

        # Split the tree into it's children to be able to manipulate them easily
        if len(config) == 8:
            database_, interfaces_, ip_, radio_common_, radio_dn_, system_, user_bridge_, user_management_ = \
                config.getchildren()
            ################################################
            #     Remove the radio-dn part of the tree     #
            ################################################
            config.remove(radio_dn_)
            ################################################
            #     change tag from data to config           #
            ################################################
            # this makes the configuration valid
            config.tag = 'config'

            ####### Basic Configuration
            # gets the number of ports
            self.get_ports(interfaces_)

            # changes the configuration name
            self.change_name(system_)

            # change ssid and password
            self.change_radio_common(radio_common_, new_ssid, new_ssid_pass)

            # change the ip part of the radio
            self.change_ip(ip_, new_ip, new_prefix, new_gateway, new_ip_local, new_prefix_local)

            # # change the password
            self.change_user_management(user_management_, admin_pass)

            ######## Advanced Config
            if line_port_vlan > 0 and management_vlan > 0:
                self.user_bridge_manag_vlan_data_vlan(user_bridge_, line_port, line_port_vlan, management_vlan)
            elif line_port_vlan > 0 and management_vlan == 0:
                self.user_bridge_vlan_no_manag_vlan(user_bridge_, line_port, line_port_vlan)
            elif line_port_vlan == 0 and management_vlan > 0:
                self.user_bridge_manag_vlan(user_bridge_, line_port, management_vlan)
            elif line_port_vlan == 0 and management_vlan == 0:
                self.user_bridge_basic(user_bridge_)

    def change_user_management(self, user_management_, new_admin_pass):
        """
        Changes the password of the main user
        :param user_management_: lxml, tree with the user_management of the config
        :param new_admin_pass: str, new password
        :return:
        """
        namespace_ = {'user-management': 'http://siklu.com/yang/tg/user-management'}
        xpath_ = 'user-management:user'

        # get the IP section of the tree
        users = user_management_.xpath(xpath_, namespaces=namespace_)

        # delete all the user
        for user in users:
            user_management_.remove(user)

        # hash new admin pass
        crypt_pass_str = to_ele(f'<crypt-password xmlns="http://siklu.com/yang/tg/user-management">'
                                f'<password>{new_admin_pass}</password></crypt-password>')
        new_pass = self.connection.channel.dispatch(crypt_pass_str)
        if new_pass.ok:
            hash_password = new_pass._root.xpath('user-management:hash/text()', namespaces=namespace_)[0]

            # we create the new user section
            user_node = etree.Element('user')
            username_node = etree.Element('username')
            username_node.text = 'admin'
            password_node = etree.Element('password')
            password_node.text = hash_password

            user_node.insert(0, username_node)
            user_node.insert(1, password_node)

            user_management_.insert(0, user_node)
        else:
            self.tu_errors.emit(f'Unable to get new password hash. PLease contact support')

    def change_ip(self, ip_, new_ip_network_, new_prefix_network_, new_gateway_, new_ip_local, new_prefix_local_):
        """
        Changes everything realted to the ip addres.
        :param ip_: lxml, tree to change
        :param new_ip: str, new ip
        :param new_prefix_: str, new mask prefix
        :param new_gateway_: str, new gateway ip
        :return: None
        """

        namespace_ = {'ip': 'http://siklu.com/yang/tg/ip'}
        xpath_ = 'ip:ipv4'

        # get the IP section of the tree
        ip_params = ip_.xpath(xpath_, namespaces=namespace_)

        # remove the section
        for ip_element in ip_params:
            ip_.remove(ip_element)

        ipv4_node = etree.Element('ipv4')
        # create the new ip address network:
        if new_ip_network_ != '':
            address_node_network = etree.Element('address')
            ip_node_network = etree.Element('ip')
            ip_node_network.text = new_ip_network_
            prefix_node_network = etree.Element('prefix-length')
            prefix_node_network.text = new_prefix_network_
        if new_gateway_ != '':
            gateway_node = etree.Element('default-gateway')
            gateway_node.text = new_gateway_

        # create the new ip local network
        address_node_local = etree.Element('address')
        ip_node_local = etree.Element('ip')
        ip_node_local.text = new_ip_local
        prefix_node_local = etree.Element('prefix-length')
        prefix_node_local.text = new_prefix_local_

        # assemble the node
        if new_ip_network_ != '':
            address_node_network.insert(0, ip_node_network)
            address_node_network.insert(1, prefix_node_network)

        address_node_local.insert(0, ip_node_local)
        address_node_local.insert(1, prefix_node_local)

        ipv4_node.insert(0, address_node_local)
        if new_ip_network_ != '':
            ipv4_node.insert(1, address_node_network)
        if new_gateway_ != '':
            ipv4_node.insert(2, gateway_node)

        ip_.insert(0, ipv4_node)

    def change_radio_common(self, radio_common_, ssid_, ssid_pass_):
        """
        Make changes in the radio common part of the TU. In this case change SSID and SSID_password
        :param ssid_pass_: str, password ofr the ssid
        :param ssid_: str, name for the wireless network
        :param radio_common_: lxml, etree with the condif
        :return: None
        """
        namespace_ = {'radio': 'http://siklu.com/yang/tg/radio'}
        xpath_ = 'radio:node-config/radio:default-ssid-profile'

        # gets the children of default-ssid-profile
        ssid_params = radio_common_.xpath(xpath_, namespaces=namespace_)[0].getchildren()

        if len(ssid_params) == 2:  # we make sure we are changing the correct parameters
            # value 0 is ssid
            if 'ssid' in ssid_params[0].tag:
                ssid_params[0].text = ssid_
            # value 1 is password
            if 'password' in ssid_params[1].tag:
                ssid_params[1].text = ssid_pass_

    def get_ports(self, interfaces_):
        """
        Set's the number of ports on the unit
        :param interfaces_: lxlm, tree with the ports
        :return: None
        """
        self.set_ports_number(len(interfaces_))

    def user_bridge_basic(self, user_bridge_):
        """
        Creates the new user birdge with all the ports and a new rf port in order
        :param user_bridge_:
        :return:
        """

        namespace_ = {'user-bridge': 'http://siklu.com/yang/tg/user-bridge'}
        xpath_ = 'user-bridge:bridge'

        bridges_port_interface = user_bridge_.xpath(xpath_, namespaces=namespace_)

        # Remove all ports from bridge
        user_bridge_.remove(bridges_port_interface[0])

        # create the ports to add to the bridge
        port_list = ['host', 'eth1', 'eth2', 'eth3', 'rf'] if self.ports_number == 3 else ['host', 'eth1', 'rf']
        ports = []
        for index, port in enumerate(port_list):
            ports.append(self.create_bridge_port(f'{index + 1}', f'{port}', 'transparent'))

        # create the new bridge
        bridge_new = self.create_bridge(f'{1}', ports)
        # add new bridge to the user_bridges
        user_bridge_.insert(0, bridge_new)

    ##### Better do the advanced config
    def user_bridge_vlan_no_manag_vlan(self, user_bridge_, data_line_port_, line_port_vlan=None):
        """
        Changes the line data port for advanced fetures
        :param line_port_vlan: vlan to add
        :param data_line_port_: port to remove from bridge and add to new bridge
        :param user_bridge_: tree element with all the user-bridge data
        :return: None
        """
        namespace_ = {'user-bridge': 'http://siklu.com/yang/tg/user-bridge'}
        xpath_ = 'user-bridge:bridge/user-bridge:bridge-port/user-bridge:interface'

        bridges_port_interface = user_bridge_.xpath(xpath_, namespaces=namespace_)

        # Remove selected port from Bridge 1
        for bridge in bridges_port_interface:  # Selects the element of the tree with the selected port
            if bridge.text == data_line_port_:
                bridge_port = bridge.getparent()
                bridges = bridge_port.getparent()
                break

        bridges.remove(bridge_port)  # deletes the eth port from default bridge

        # create a new bridge with id 2 to add RF port + data vlan
        new_data_port_management = self.create_bridge_port(f'{1}', data_line_port_, 'transparent')
        new_data_port_data = self.create_bridge_port(f'{2}', f'rf', 'c-vlan',  f'{line_port_vlan}')
        port_list = [new_data_port_management, new_data_port_data]

        # create the new bridge
        bridge_new = self.create_bridge(f'{2}', port_list)
        # add new bridge to the user_bridges
        user_bridge_.insert(1, bridge_new)

    def user_bridge_manag_vlan(self, user_bridge_, data_line_port_, mng_vlan=None):
        """
                Changes the line data port for advanced fetures
                :param line_port_vlan: vlan to add
                :param new_rf_name_: name of the rf- bridge
                :param data_line_port_: port to remove from bridge and add to new bridge
                :param user_bridge_: tree element with all the user-bridge data
                :return: None
                """
        namespace_ = {'user-bridge': 'http://siklu.com/yang/tg/user-bridge'}
        xpath_ = 'user-bridge:bridge/user-bridge:bridge-port/user-bridge:interface'

        bridges_port_interface = user_bridge_.xpath(xpath_, namespaces=namespace_)

        # Remove selected port from Bridge 1
        for bridge in bridges_port_interface:  # Selects the element of the tree with the selected port
            if bridge.text == data_line_port_:
                bridge_port = bridge.getparent()
                bridges = bridge_port.getparent()
                break
        bridges.remove(bridge_port)  # deletes the eth port from default bridge

        for bridge in bridges_port_interface:  # deletes the RF port
            if bridge.text == 'rf':
                rf_port = bridge.getparent()
                bridges = rf_port.getparent()
                break
        bridges.remove(rf_port)  # deletes the rf port from default bridge

        # create new port to add to user-port bridge id 1 (we add teh rf-name with cvlan tag)
        new_data_port_data = self.create_bridge_port(f'{5}', f'rf', 'c-vlan', f'{mng_vlan}')
        # we add this new port to the bridges (parent or bridge of the removed elements)
        bridges.insert(1, new_data_port_data)

        # create a new bridge with id 2 to add RF port + data vlan
        new_bg_2_port_1 = self.create_bridge_port(f'{2}', f'rf', 'transparent')
        new_bg_2_port_2 = self.create_bridge_port(f'{1}', f'{data_line_port_}', 'transparent')
        port_list = [new_bg_2_port_2, new_bg_2_port_1]

        # create the new bridge
        bridge_new = self.create_bridge(f'{2}', port_list)
        # add new bridge to the user_bridges
        user_bridge_.insert(1, bridge_new)

    def user_bridge_manag_vlan_data_vlan(self, user_bridge_, data_line_port_, line_port_vlan=None,
                                         mng_vlan=None):
        """
                Changes the line data port for advanced fetures
                :param mng_vlan: management vlan to add to the port
                :param line_port_vlan: vlan to add
                :param new_rf_name_: name of the rf- bridge
                :param data_line_port_: port to remove from bridge and add to new bridge
                :param user_bridge_: tree element with all the user-bridge data
                :return: None
                """
        namespace_ = {'user-bridge': 'http://siklu.com/yang/tg/user-bridge'}
        xpath_ = 'user-bridge:bridge/user-bridge:bridge-port/user-bridge:interface'

        bridges_port_interface = user_bridge_.xpath(xpath_, namespaces=namespace_)

        # Remove selected port from Bridge 1
        for bridge in bridges_port_interface:  # Selects the element of the tree with the selected port
            if bridge.text == data_line_port_:
                bridge_port = bridge.getparent()
                bridges = bridge_port.getparent()
                break
        bridges.remove(bridge_port)  # deletes the eth port from default bridge

        for bridge in bridges_port_interface:  # deletes the RF port
            if bridge.text == 'rf':
                rf_port = bridge.getparent()
                bridges = rf_port.getparent()
                break
        bridges.remove(rf_port)  # deletes the rf port from default bridge

        # create new port to add to user-port bridge id 1 (we add teh rf-name with cvlan tag)
        new_data_port_data = self.create_bridge_port(f'{5}', f'rf', 'c-vlan', f'{mng_vlan}')
        # we add this new port to the bridges (parent or bridge of the removed elements)
        bridges.insert(1, new_data_port_data)

        # create a new bridge with id 2 to add RF port + data vlan
        new_bg_2_port_1 = self.create_bridge_port(f'{1}', f'{data_line_port_}', 'transparent')
        new_bg_2_port_2 = self.create_bridge_port(f'{2}', f'rf', 'c-vlan', f'{line_port_vlan}')
        port_list = [new_bg_2_port_1, new_bg_2_port_2]

        # create the new bridge
        bridge_new = self.create_bridge(f'{2}', port_list)
        # add new bridge to the user_bridges
        user_bridge_.insert(1, bridge_new)

    def check_sw_version(self):
        """
        Gets the software version of both banks
        Returns true if active >= 1.0.2
        :return: Bool
        """
        namespace_ = {'sw': 'http://siklu.com/yang/tg/system'}
        xpath_ = 'sw:state/sw:banks-info/sw:banks/sw:software-version/text()'

        software_info = self.connection.get_command('<filter xmlns:tu="http://siklu.com/yang/tg/system" '
                                                    'select="/tu:system/tu:state/tu:banks-info/tu:banks" '
                                                    'type="xpath"/>')
        software_versions = software_info.data_ele.getchildren()[0]

        versions = software_versions.xpath(xpath_, namespaces=namespace_)

        xpath_running = 'sw:state/sw:banks-info/sw:banks/sw:status/text()'
        running = software_versions.xpath(xpath_running, namespaces=namespace_)

        running_software = zip(versions, running)

        for version, running_ in running_software:
            version = version.replace('"', '')
            if version > '1.0.1-1699-0240b7b6' and running_ == 'active':
                return True
            elif version > '1.0.1-1699-0240b7b6':
                self.tu_logs.emit('Version 1.0.2 detected but not active. Please activate in cli using:\n'
                                  'software activate scheduling immediate')
                return False
            else:
                self.tu_logs.emit('Please upgrade to at least version 1.0.2')
        return False

    @staticmethod
    def create_bridge(id_, list_ports):
        """
        creates a bridge with bridge_id id_ and adds a port per port in the list_ports
        :param id_:
        :param list_ports:
        :return:
        """
        bridge_ = etree.Element('bridge')
        bridge_id = etree.Element('bridge-id')
        bridge_id.text = id_
        bridge_.insert(0, bridge_id)
        for index, port_ in enumerate(list_ports):
            bridge_.insert(index + 1, port_)

        return bridge_

    @staticmethod
    def create_bridge_port(id_, interface_name_, bridge_port_type_, vlan=None):
        """
        Create a bridge port xml tree like the following:

        # <bridge-port>
		#	<bridge-port-id>4</bridge-port-id>
		#	<interface>eth3</interface>
		#	<bridge-port-type>transparent</bridge-port-type>
		# </bridge-port>

        :param id_:
        :param interface_name_:
        :param bridge_port_type_:
        :param vlan:
        :return:
        """
        bridge_port_ = etree.Element('bridge-port')
        bridge_id_ = etree.Element('bridge-port-id')
        bridge_id_.text = id_
        bridge_interface_ = etree.Element('interface')
        bridge_interface_.text = interface_name_
        bridge_port_type = etree.Element('bridge-port-type')
        bridge_port_type.text = bridge_port_type_
        if vlan:
            bridge_port_vlan_ = etree.Element(bridge_port_type_)
            bridge_port_vlan_.text = vlan

        # create bridge_port
        bridge_port_.insert(0, bridge_id_)
        bridge_port_.insert(1, bridge_interface_)
        bridge_port_.insert(2, bridge_port_type)
        if vlan:
            bridge_port_.insert(3, bridge_port_vlan_)

        return bridge_port_

    def change_name(self, system_):
        namespace_ = {'system': 'http://siklu.com/yang/tg/system'}
        xpath_ = 'system:name'
        # the element will be returned in a list. So we take the first element
        name_ = system_.xpath(xpath_, namespaces=namespace_)
        name_[0].text = self.get_name()

    def send_new_config(self):
        """
        Sends and validates teh configuration and aplies it
        :return: bool, True if the config was correctly applied, False otherwise
        """
        if self.connection_state:
            if self.connection.channel:
                try:
                    # send configuration
                    answer_edit_config = self.connection.channel.edit_config(self.get_configuration(),
                                                                             target='candidate',
                                                                             default_operation='replace')
                    try:
                        if answer_edit_config.ok:
                            answer_validate_config = self.connection.channel.validate()
                            self.tu_logs.emit(f'Info - New configuration sent...')
                            try:
                                if answer_validate_config.ok:
                                    try:
                                        self.connection.channel.commit()
                                        self.tu_logs.emit(f'Info - New configuration committed')
                                        return True
                                    except NCClientError as e:
                                        self.tu_logs.emit(f'Info - If you set an advanced config and lost connection\n'
                                                          f'- it might be because of the vlan tagging.\n'
                                                          f'- Please connect to another port and save config.')
                                        return True
                                else:
                                    self.tu_errors.emit(f'Error - validation was not successful...removing changes')
                                    self.connection.channel.discard_changes()
                                    return False
                            except NCClientError as e:
                                self.connection_state = False
                                self.tu_errors.emit(f'Error Commit - new configuration: {e}')
                    except NCClientError as e:
                        self.connection_state = False
                        self.tu_errors.emit(f'Error Answer validate - new configuration: {e}')
                        return False

                except NCClientError as e:
                    self.connection_state = False
                    self.tu_errors.emit(f'Error Answer new config - sending new configuration: {e}')
                    return False

    def save_changes(self):
        self.connection.set_channel_timeout(5)
        if self.connection_state:
            if self.connection.channel:
                try:
                    # we save the configuration
                    answer_copy = self.connection.channel.copy_config(source='candidate', target='startup')
                    if answer_copy.ok:
                        return True
                    else:
                        self.tu_errors.emit(f"Error - We couldn't save the file. please try again")
                        return False
                except NCClientError as e:
                    self.tu_errors.emit(f"We couldn't save the file. Please try again\n{e}")
                    return False

    def send_logs(self, message):
        self.tu_logs.emit(message)

    def send_errors(self, message):
        self.tu_errors.emit(message)


if __name__ == '__main__':
    print('Test script')
    print('1-Creating object')
    tu = TuExpanded('uri1')
    print('Done')
    print('2-Creating a conection')
    tu.connect('31.168.34.108', 'admin', 'TGadmin1')
    print('Done')
    print('3-Retriving the configuration')
    tu.get_startup_config()
    print('Done')
    print('4-modifying the configuration')
    tu.prepare_config(tu.get_configuration(), 'javihaul', 'MariachI', '192.168.0.1', '24', '10.10.10.254', 'MariachI')
    print('Done')
    print('5-sending new configuration')
    if tu.send_new_config():
        if tu.connect('192.168.0.1', 'admin', 'MariachI'):
            print('Changes were made sucessfully')
    print('Done')