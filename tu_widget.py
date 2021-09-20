from PyQt5 import QtCore as Qtc
from PyQt5 import QtGui as Qtg
from PyQt5 import QtWidgets as Qtw
from tu_monitor import TuExpanded
from TUWidget import TuWidget  # This is the widget for the TU when polling realtime
from tu_monitor_data_model import TuMonitorDataModel


class TuConfig(Qtw.QWidget):
    tuwidget_changing = Qtc.pyqtSignal()
    tu_widget_log = Qtc.pyqtSignal(str)

    def __init__(self, parent=None):
        super(TuConfig, self).__init__(parent)

        self.setObjectName("TuWidget")
        font = Qtg.QFont()
        font.setPointSize(10)
        self.setFont(font)

        # create the monitoring data model
        self.monitored_tu = TuMonitorDataModel()

        # create the data model
        self.tu = TuExpanded('tu')

        # Root Layout
        self.layout_root_V = Qtw.QVBoxLayout(self)
        self.layout_root_V.setContentsMargins(5, 5, 5, 5)
        self.layout_root_V.setObjectName("layout_root_V")

        # Welcome Message
        self.txt_welcome_msg = Qtw.QTextBrowser(self)
        self.txt_welcome_msg.setObjectName("txt_welcome_msg")
        self.layout_root_V.addWidget(self.txt_welcome_msg)

        size_policy = Qtw.QSizePolicy(Qtw.QSizePolicy.Fixed, Qtw.QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.txt_welcome_msg.sizePolicy().hasHeightForWidth())
        self.txt_welcome_msg.setSizePolicy(size_policy)
        self.txt_welcome_msg.setMaximumSize(Qtc.QSize(656, 150))
        self.txt_welcome_msg.setSizeAdjustPolicy(Qtw.QAbstractScrollArea.AdjustToContents)
        self.txt_welcome_msg.setObjectName("txt_welcome_msg")
        self.layout_root_V.addWidget(self.txt_welcome_msg)

        # Table widget - expandable
        self.tlb_configurations = Qtw.QToolBox(self)
        self.tlb_configurations.setObjectName("tlb_configurations")
        self.layout_root_V.addWidget(self.tlb_configurations)

        # first button widget
        self.pg_basic_config = Qtw.QWidget()
        self.pg_basic_config.setGeometry(Qtc.QRect(0, 0, 656, 248))
        self.pg_basic_config.setObjectName("pg_basic_config")

        self.layout_grid_basic = Qtw.QGridLayout(self.pg_basic_config)
        self.layout_grid_basic.setSizeConstraint(Qtw.QLayout.SetDefaultConstraint)
        self.layout_grid_basic.setContentsMargins(3, 3, 3, 3)
        self.layout_grid_basic.setObjectName("grid_basic")

        self.txt_unit_name = Qtw.QLineEdit(self)
        self.txt_unit_name.setObjectName("txt_unit_name")
        self.layout_grid_basic.addWidget(self.txt_unit_name, 0, 1, 1, 1)

        self.txt_ssid = Qtw.QLineEdit(self.pg_basic_config)
        self.txt_ssid.setObjectName("txt_ssid")
        self.layout_grid_basic.addWidget(self.txt_ssid, 1, 1, 1, 1)

        self.txt_ssid_password = Qtw.QLineEdit(self)
        self.txt_ssid_password.setObjectName("txt_ssid_password")
        self.layout_grid_basic.addWidget(self.txt_ssid_password, 1, 3, 1, 1)

        self.lbl_ssid_password = Qtw.QLabel(self.pg_basic_config)
        self.lbl_ssid_password.setObjectName("lbl_ssid_password")

        self.lbl_ssid = Qtw.QLabel(self.pg_basic_config)
        self.lbl_ssid.setObjectName("lbl_ssid")
        self.layout_grid_basic.addWidget(self.lbl_ssid, 1, 0, 1, 1)

        self.lbl_unit_name = Qtw.QLabel(self)
        self.lbl_unit_name.setObjectName("lbl_unit_name")
        self.layout_grid_basic.addWidget(self.lbl_unit_name, 0, 0, 1, 1)

        self.lbl_admin_pass = Qtw.QLabel(self)
        self.lbl_admin_pass.setObjectName("lbl_admin_pass")
        self.layout_grid_basic.addWidget(self.lbl_admin_pass, 4, 0, 1, 1)
        ######### Local Network
        self.grp_local = Qtw.QGroupBox(self)
        self.grp_local.setMinimumSize(Qtc.QSize(0, 55))
        self.grp_local.setObjectName("grp_local")

        self.layout_local_v = Qtw.QVBoxLayout(self.grp_local)
        self.layout_local_v.setContentsMargins(0, 0, 0, 0)
        self.layout_local_v.setObjectName("layout_local_v")

        self.layout_local_data_h = Qtw.QHBoxLayout()
        self.layout_local_data_h.setObjectName("layout_local_data_h")

        self.lbl_ip_local = Qtw.QLabel(self.grp_local)
        self.lbl_ip_local.setObjectName("lbl_ip_local")
        self.layout_local_data_h.addWidget(self.lbl_ip_local)

        self.txt_ip_local = Qtw.QLineEdit(self.grp_local)
        self.txt_ip_local.setObjectName("txt_ip_local")
        self.layout_local_data_h.addWidget(self.txt_ip_local)

        self.lbl_prefix_local = Qtw.QLabel(self.grp_local)
        self.lbl_prefix_local.setObjectName("lbl_prefix_local")
        self.layout_local_data_h.addWidget(self.lbl_prefix_local)

        self.txt_prefix_local = Qtw.QLineEdit(self.grp_local)
        self.txt_prefix_local.setObjectName("txt_prefix_local")
        self.layout_local_data_h.addWidget(self.txt_prefix_local)

        self.layout_local_v.addLayout(self.layout_local_data_h)
        self.layout_grid_basic.addWidget(self.grp_local, 2, 0, 1, 4)

        ######## Network Part
        self.grp_network = Qtw.QGroupBox(self)
        self.grp_network.setMinimumSize(Qtc.QSize(0, 55))
        self.grp_network.setObjectName("grp_network")

        self.layout_network_v = Qtw.QVBoxLayout(self.grp_network)
        self.layout_network_v.setContentsMargins(0, 0, 0, 0)
        self.layout_network_v.setObjectName("layout_network_v")

        self.layout_network_h = Qtw.QHBoxLayout()
        self.layout_network_h.setObjectName("layout_network_h")

        self.lbl_ip_network = Qtw.QLabel(self.grp_network)
        self.lbl_ip_network.setObjectName("lbl_ip_network")
        self.layout_network_h.addWidget(self.lbl_ip_network)

        self.txt_ip_network = Qtw.QLineEdit(self.grp_network)
        self.txt_ip_network.setObjectName("txt_ip_network")
        self.layout_network_h.addWidget(self.txt_ip_network)

        self.lbl_prefix_network = Qtw.QLabel(self.grp_network)
        self.lbl_prefix_network.setObjectName("lbl_prefix_network")
        self.layout_network_h.addWidget(self.lbl_prefix_network)

        self.txt_prefix_network = Qtw.QLineEdit(self.grp_network)
        self.txt_prefix_network.setObjectName("txt_prefix_network")
        self.layout_network_h.addWidget(self.txt_prefix_network)

        self.lbl_gateway = Qtw.QLabel(self.grp_network)
        self.lbl_gateway.setObjectName("lbl_gateway")
        self.layout_network_h.addWidget(self.lbl_gateway)

        self.txt_gateway = Qtw.QLineEdit(self.grp_network)
        self.txt_gateway.setObjectName("txt_gateway")
        self.layout_network_h.addWidget(self.txt_gateway)

        self.layout_network_v.addLayout(self.layout_network_h)
        self.layout_grid_basic.addWidget(self.grp_network, 3, 0, 1, 5)
        self.layout_grid_basic.addWidget(self.lbl_ssid_password, 1, 2, 1, 1)

        self.txt_admin_pass = Qtw.QLineEdit(self.pg_basic_config)
        self.txt_admin_pass.setObjectName("txt_admin_pass")
        self.layout_grid_basic.addWidget(self.txt_admin_pass, 4, 1, 1, 1)
        ##### Hidden Menu
        self.grp_hidden = Qtw.QGroupBox(self)
        self.grp_hidden.setObjectName("grp_hidden")

        self.layout_hidden_v = Qtw.QVBoxLayout(self.grp_hidden)
        self.layout_hidden_v.setContentsMargins(0, 0, 0, 0)
        self.layout_hidden_v.setObjectName("layout_hidden_v")

        self.layout_hidden_h = Qtw.QHBoxLayout()
        self.layout_hidden_h.setObjectName("layout_hidden_h")

        self.lbl_ip_hidden = Qtw.QLabel(self.grp_hidden)
        self.lbl_ip_hidden.setObjectName("lbl_ip_hidden")
        self.layout_hidden_h.addWidget(self.lbl_ip_hidden)

        self.txt_ip_hidden = Qtw.QLineEdit(self.grp_hidden)
        self.txt_ip_hidden.setObjectName("txt_ip_hidden")
        self.layout_hidden_h.addWidget(self.txt_ip_hidden)

        self.lbl_user_hidden = Qtw.QLabel(self.grp_hidden)
        self.lbl_user_hidden.setObjectName("lbl_user_hidden")
        self.layout_hidden_h.addWidget(self.lbl_user_hidden)

        self.txt_user_hidden = Qtw.QLineEdit(self.grp_hidden)
        self.txt_user_hidden.setObjectName("txt_user_hidden")
        self.layout_hidden_h.addWidget(self.txt_user_hidden)

        self.lbl_pass_hidden = Qtw.QLabel(self.grp_hidden)
        self.lbl_pass_hidden.setObjectName("lbl_pass_hidden")
        self.layout_hidden_h.addWidget(self.lbl_pass_hidden)

        self.txt_pass_hidden = Qtw.QLineEdit(self.grp_hidden)
        self.txt_pass_hidden.setObjectName("txt_pass_hidden")
        self.layout_hidden_h.addWidget(self.txt_pass_hidden)

        self.layout_hidden_v.addLayout(self.layout_hidden_h)
        self.layout_grid_basic.addWidget(self.grp_hidden, 5, 0, 1, 5)

        self.btn_apply = Qtw.QPushButton(self)
        self.btn_apply.setObjectName("btn_apply")
        self.layout_grid_basic.addWidget(self.btn_apply, 4, 3, 1, 1)

        self.pg_basic_config.setLayout(self.layout_grid_basic)
        self.tlb_configurations.addItem(self.pg_basic_config, "")

        #################################################################################

        ###### Page Advanced configuration
        self.pg_advanced_config = Qtw.QWidget()
        self.pg_advanced_config.setObjectName("pg_advanced_config")
        self.pg_advanced_config.setDisabled(True)

        self.layout_grid_advanced = Qtw.QGridLayout()

        self.cmb_data_line_port = Qtw.QComboBox(self.pg_advanced_config)
        port_list = ['eth1', 'eth2', 'eth3']
        self.cmb_data_line_port.addItems(port_list)
        self.cmb_data_line_port.setObjectName("txt_data_line_port")
        self.layout_grid_advanced.addWidget(self.cmb_data_line_port, 1, 1, 1, 1)

        self.layout_line_port_h = Qtw.QHBoxLayout()
        self.layout_line_port_h.setObjectName("layout_line_port_h")

        self.spn_line_vlan = Qtw.QSpinBox(self.pg_advanced_config)
        self.spn_line_vlan.setMaximum(4094)
        self.spn_line_vlan.setProperty("value", 0)
        self.spn_line_vlan.setObjectName("spn_line_vlan")
        self.layout_line_port_h.addWidget(self.spn_line_vlan)

        spacer_line_vlan = Qtw.QSpacerItem(186, 45, Qtw.QSizePolicy.Expanding, Qtw.QSizePolicy.Minimum)
        self.layout_line_port_h.addItem(spacer_line_vlan)
        self.layout_grid_advanced.addLayout(self.layout_line_port_h, 1, 3, 1, 1)

        self.layout_mngment_vlan_h = Qtw.QHBoxLayout()
        self.layout_mngment_vlan_h.setObjectName("horizontalLayout")

        self.spn_mng_vlan = Qtw.QSpinBox(self.pg_advanced_config)
        self.spn_mng_vlan.setMaximum(4094)
        self.spn_mng_vlan.setProperty("value", 0)
        self.spn_mng_vlan.setObjectName("spn_mng_vlan")
        self.layout_mngment_vlan_h.addWidget(self.spn_mng_vlan)

        space_mng_vlan = Qtw.QSpacerItem(186, 45, Qtw.QSizePolicy.Expanding, Qtw.QSizePolicy.Minimum)
        self.layout_mngment_vlan_h.addItem(space_mng_vlan)

        self.lbl_mng_vlan = Qtw.QLabel(self.pg_advanced_config)
        self.lbl_mng_vlan.setObjectName("lbl_mng_vlan")
        self.layout_grid_advanced.addWidget(self.lbl_mng_vlan, 2, 0, 1, 1)

        self.layout_grid_advanced.addLayout(self.layout_mngment_vlan_h, 2, 1, 1, 1)

        self.btn_apply_advanced = Qtw.QPushButton()
        self.btn_apply_advanced.setObjectName('btn_apply_advanced')
        self.layout_grid_advanced.addWidget(self.btn_apply_advanced, 4, 3, 1, 1)

        self.lbl_data_line_port = Qtw.QLabel(self.pg_advanced_config)
        self.lbl_data_line_port.setObjectName("lbl_data_line_port")
        self.layout_grid_advanced.addWidget(self.lbl_data_line_port, 1, 0, 1, 1)

        self.lbl_line_port_vlan = Qtw.QLabel(self.pg_advanced_config)
        self.lbl_line_port_vlan.setObjectName("lbl_line_port_vlan")
        self.layout_grid_advanced.addWidget(self.lbl_line_port_vlan, 1, 2, 1, 1)

        self.lbl_instructions = Qtw.QLabel(self.pg_advanced_config)
        self.lbl_instructions.setAlignment(Qtc.Qt.AlignCenter)
        self.lbl_instructions.setObjectName("lbl_instructions")
        self.layout_grid_advanced.addWidget(self.lbl_instructions, 0, 0, 1, 4)

        self.pg_advanced_config.setLayout(self.layout_grid_advanced)
        self.tlb_configurations.addItem(self.pg_advanced_config, "")

        ################## Monitor page
        self.pg_monitor = Qtw.QWidget()
        self.pg_monitor.setObjectName("pg_monitor")

        self.layout_monitor_v = Qtw.QVBoxLayout()

        # username password fields
        layout_monitor_logindata_h = Qtw.QHBoxLayout()

        lbl_monitor_username = Qtw.QLabel('User:')
        lbl_monitor_password = Qtw.QLabel('Password:')
        lbl_monitor_ip = Qtw.QLabel('IP:')
        self.txt_monitor_user = Qtw.QLineEdit()
        self.txt_monitor_user.setPlaceholderText('Username')
        self.txt_monitor_password = Qtw.QLineEdit()
        self.txt_monitor_password.setPlaceholderText('Password')
        self.txt_monitor_ip = Qtw.QLineEdit()
        self.txt_monitor_ip.setPlaceholderText('IP address')
        self.btn_monitor_start = Qtw.QPushButton('Connect')

        layout_monitor_logindata_h.addWidget(lbl_monitor_ip)
        layout_monitor_logindata_h.addWidget(self.txt_monitor_ip)
        layout_monitor_logindata_h.addWidget(lbl_monitor_username)
        layout_monitor_logindata_h.addWidget(self.txt_monitor_user)
        layout_monitor_logindata_h.addWidget(lbl_monitor_password)
        layout_monitor_logindata_h.addWidget(self.txt_monitor_password)
        layout_monitor_logindata_h.addWidget(self.btn_monitor_start)

        self.layout_monitor_v.addLayout(layout_monitor_logindata_h)

        self.tu_widget = TuWidget(self.txt_unit_name)
        self.layout_monitor_v.addWidget(self.tu_widget)

        self.pg_monitor.setLayout(self.layout_monitor_v)
        self.tlb_configurations.addItem(self.pg_monitor, "")

        self.retranslate_ui()

        # customizations over generated content
        self.txt_unit_name.setPlaceholderText('Add unit name (Mandatory)')
        self.txt_unit_name.setToolTip('Max 8 characters, possible characters [a-z0-9.-]')
        self.txt_unit_name.setMaxLength(8)

        self.txt_ip_network.setPlaceholderText('IP address')
        self.txt_ip_network.setToolTip('Enter a valid ip address')
        self.txt_ip_network.setMaxLength(16)

        self.txt_prefix_network.setPlaceholderText('Enter prefix')
        prefix_help = """ Set a prefix length. if you are not sure. refere to this table:
             IP     -> Prefix
        255.255.255.255 -> 32
        255.255.255.254 -> 31
        255.255.255.252 -> 30
        255.255.255.248 -> 29
        255.255.255.240 -> 28
        255.255.255.224 -> 27
        255.255.255.192 -> 26
        255.255.255.128 -> 25
        255.255.255.0 -> 24
        255.255.254.0 -> 23
        255.255.252.0 -> 22
        255.255.248.0 -> 21
        255.255.240.0 -> 20
        255.255.224.0 -> 19
        255.255.192.0 -> 18
        255.255.128.0 -> 17
        255.255.0.0 -> 16
        255.254.0.0 -> 15
        255.252.0.0 -> 14
        255.248.0.0 -> 13
        255.240.0.0 -> 12
        255.224.0.0 -> 11
        255.192.0.0 -> 10
        255.128.0.0 -> 9
        255.0.0.0 -> 8
        254.0.0.0 -> 7
        252.0.0.0 -> 6
        248.0.0.0 -> 5
        240.0.0.0 -> 4
        224.0.0.0 -> 3
        192.0.0.0 -> 2
        128.0.0.0 -> 1"""
        self.txt_prefix_network.setToolTip(prefix_help)
        self.txt_prefix_network.setMaxLength(2)

        self.txt_gateway.setPlaceholderText('Gateway ip address')
        self.txt_gateway.setToolTip('Enter a valid IP address')
        self.txt_gateway.setMaxLength(16)

        self.txt_ssid.setPlaceholderText('SSID name (Mandatory)')
        self.txt_ssid.setText('MultiHaul')
        self.txt_ssid.setToolTip('Enter the SSID. Must match remote node SSID')

        self.txt_ssid_password.setPlaceholderText('SSID Password (Mandatory)')
        self.txt_ssid_password.setText('MultiHaul')
        self.txt_ssid_password.setToolTip('Enter SSID password. Must match remote node SSID password')

        self.txt_admin_pass.setPlaceholderText('Admin password (Mandatory)')
        self.txt_admin_pass.setToolTip('Enter password for admin user')
        self.txt_admin_pass.setText('admin')

        self.txt_ip_local.setPlaceholderText('192.168.0.xxx (Mandatory)')
        self.txt_ip_local.setToolTip('Enter valid IP address that will be used for local management. Must be different '
                                     'than the default ip: 192.168.0.1')

        self.txt_prefix_local.setPlaceholderText('Enter Prefix')
        self.txt_prefix_local.setText('24')
        self.txt_prefix_local.setToolTip(prefix_help)
        self.txt_prefix_local.setMaxLength(2)

        self.cmb_data_line_port.setToolTip('Enter the line port that will be used for data services [eth1, eth2, eth3]')

        self.spn_line_vlan.setToolTip('VLAN (Access port to tag all incoming traffic) or 0 to pass all traffic, tagged'
                                      ' or untagged. Note that if entered, you will not be able to manage the radio via'
                                      ' the data line port')

        self.spn_mng_vlan.setToolTip('VLAN or 0(untagged). Note that if entered, you will not be able to manage the '
                                     'radio via the data line port')

        # Hidden menu
        self.grp_hidden.setHidden(True)
        self.txt_ip_hidden.setText('192.168.0.1')
        self.txt_ip_hidden.setDisabled(True)
        self.txt_user_hidden.setText('admin')
        self.txt_user_hidden.setDisabled(True)
        self.txt_pass_hidden.setText('admin')
        self.txt_pass_hidden.setDisabled(True)

        ###### Validators

        # IP
        ip_regex = Qtc.QRegExp(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
        ip_input_validator = Qtg.QRegExpValidator(ip_regex, self)
        self.txt_ip_local.setValidator(ip_input_validator)
        self.txt_ip_network.setValidator(ip_input_validator)
        self.txt_ip_hidden.setValidator(ip_input_validator)
        self.txt_gateway.setValidator(ip_input_validator)
        self.txt_monitor_ip.setValidator(ip_input_validator)

        unit_name_regex = Qtc.QRegExp(r'^[a-z0-9.-]{1,8}$')
        unit_name_validator = Qtg.QRegExpValidator(unit_name_regex, self)
        self.txt_unit_name.setValidator(unit_name_validator)

        prefix_regex = Qtc.QRegExp(r'^([1-9]|[12]\d|3[0-2])$')
        prefix_validator = Qtg.QRegExpValidator(prefix_regex, self)
        self.txt_prefix_network.setValidator(prefix_validator)
        self.txt_prefix_local.setValidator(prefix_validator)

        self.retranslate_ui()

        ########################################
        # our stuff
        ########################################

        self.btn_apply.clicked.connect(self.change)
        self.btn_apply_advanced.clicked.connect(self.change)
        self.btn_monitor_start.clicked.connect(self.monitor)

        # connections

    def change(self):
        print(self.size())
        if self.txt_unit_name.text() != '' and self.txt_ssid.text() != '' and self.txt_ssid_password.text() != '' and self.txt_ip_local.text() != '' and self.txt_admin_pass.text() != '' and self.txt_prefix_local.text() != '':
            if self.txt_ip_local.text() != '192.168.0.1':
                # Take the advanced configuration for the radio
                line_port = self.cmb_data_line_port.currentText()
                vlan_data_port = self.spn_line_vlan.value()
                vlan_mng_port = self.spn_mng_vlan.value()

                self.tuwidget_changing.emit()
                ### """ Do all the changes to the TU"""
                self.tu.name = self.txt_unit_name.text()
                if self.grp_hidden.isHidden() and not self.txt_ip_hidden.isEnabled() and not self.txt_pass_hidden.isEnabled() \
                        and not self.txt_user_hidden.isEnabled():
                    answer = self.tu.connect('192.168.0.1', 'admin', 'admin')  # change to default parameters
                else:
                    answer = self.tu.connect(self.txt_ip_hidden.text(), self.txt_user_hidden.text(),
                                             self.txt_pass_hidden.text())
                #  get the startup-config
                try:
                    if answer:
                        self.tu.get_startup_config()
                    else:
                        self.tu.tu_logs.emit(f'Error - Unable to connect. Make sure the radio is online...')
                        return False
                except AttributeError as e:
                    self.tu.tu_logs.emit(f'Error - Unable to connect. Make sure the radio is online...{e}')
                    return False

                if not self.tu.check_sw_version():
                    return False

                # prepare the new config
                self.tu.prepare_config(self.tu.get_configuration(), self.txt_ssid.text(), self.txt_ssid_password.text(),
                                       self.txt_ip_network.text(), self.txt_prefix_network.text(), self.txt_gateway.text(),
                                       self.txt_admin_pass.text(), self.txt_ip_local.text(), self.txt_prefix_local.text(),
                                       line_port, vlan_data_port, vlan_mng_port)

                if self.tu.send_new_config():
                    if self.tu.connect(self.txt_ip_local.text(), 'admin', self.txt_admin_pass.text()):
                        self.tu.tu_logs.emit('Changes were successfully applied and saved')
                        #############
                        self.tu.save_changes()
                        self.tu.tu_logs.emit('Please Reboot the unit now!')
            else:
                self.tu.tu_logs.emit(f'Local Address needs to be different than: 192.168.0.1')
        else:
            self.tu.tu_logs.emit(f'Some field are blank. Please fill all the information')

    def monitor(self):
        ip_ = self.txt_monitor_ip.text()
        user_ = self.txt_monitor_user.text()
        pass_ = self.txt_monitor_password.text()
        self.monitored_tu.tu_monitor_system_name.connect(self.tu_widget.lbl_name.setText)
        self.monitored_tu.tu_monitor_local_sector.connect(self.tu_widget.lbl_local_sector_counter.setText)
        self.monitored_tu.tu_monitor_remote_sector.connect(self.tu_widget.lbl_remote_sector_counter.setText)
        self.monitored_tu.tu_monitor_remote_mac.connect(self.tu_widget.lbl_remote_mac.setText)
        self.monitored_tu.tu_monitor_local_role.connect(self.tu_widget.lbl_role.setText)
        self.monitored_tu.tu_monitor_rssi.connect(self.tu_widget.lbl_rssi_counter.setText)
        self.monitored_tu.tu_monitor_snr.connect(self.tu_widget.lbl_snr_counter.setText)
        self.monitored_tu.tu_monitor_mcsrx.connect(self.tu_widget.lbl_rxmcs_counter.setText)
        self.monitored_tu.tu_monitor_mcstx.connect(self.tu_widget.lbl_txmcs_counter.setText)
        self.monitored_tu.tu_monitor_perrx.connect(self.tu_widget.lbl_perrx_counter.setText)
        self.monitored_tu.tu_monitor_pertx.connect(self.tu_widget.lbl_pertx_counter.setText)
        #TODO falta Tx Power
        self.monitored_tu.tu_monitor_drrx.connect(self.tu_widget.lbl_rxdr_counter.setText)
        self.monitored_tu.tu_monitor_drtx.connect(self.tu_widget.lbl_txdr_counter.setText)
        self.monitored_tu.tu_monitor_rx_beam.connect(self.tu_widget.lbl_aligment_rx.setText)
        self.monitored_tu.tu_monitor_tx_beam.connect(self.tu_widget.lbl_aligment_tx.setText)
        if self.monitored_tu.connect(ip_, user_, pass_):
            self.monitored_tu.tu_monitor_log.emit('Info - Connected and monitoring')
            self.monitored_tu.setParent(self)
            self.monitored_tu.start()
        else:
            self.tu_widget_log.emit('Error: Unable to connect')

    def closeEvent(self, event):
        self.monitored_tu.connection_state = False

    def retranslate_ui(self):
        _translate = Qtc.QCoreApplication.translate
        self.txt_welcome_msg.setHtml(_translate("Form",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                                "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#00aa00;\">Welcome to Siklu’s MultiHaul TG Terminal Unit configuration wizard</span></p>\n"
                                                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The wizard will allow you to easily configure a fresh Terminal Unit and bring it into service. </p>\n"
                                                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Before we start, make sure your laptop is configured with IP 192.168.0.250 with prefix-length 16 (255.255.0.0) and that you are connected to a fresh Terminal Unit with default settings (<span style=\" color:#00aa00;\">192.168.0.1/24 admin/admin</span>). </p>\n"
                                                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Make sure to be running version: 1.0.2-1817 minimum.</p></body></html>"))
        self.lbl_ssid_password.setText(_translate("Form", "SSID Password:"))
        self.lbl_ssid.setText(_translate("Form", "SSID:"))
        self.lbl_unit_name.setText(_translate("Form", "Unit Name:"))
        self.btn_apply.setText(_translate("Form", "Apply Changes"))
        self.btn_apply_advanced.setText(_translate('Form', 'Apply Changes'))
        self.lbl_admin_pass.setText(_translate("Form", "Admin Password:"))
        self.grp_network.setTitle(_translate("Form", "Network IP settings"))
        self.lbl_ip_network.setText(_translate("Form", "IP Address:"))
        self.lbl_prefix_network.setText(_translate("Form", "Prefix-length:"))
        self.lbl_gateway.setText(_translate("Form", "Gateway:"))
        self.grp_hidden.setTitle(_translate("Form", "Hidden Config Menu - use at your own risk"))
        self.lbl_ip_hidden.setText(_translate("Form", "IP"))
        self.lbl_user_hidden.setText(_translate("Form", "user"))
        self.lbl_pass_hidden.setText(_translate("Form", "pass"))
        self.grp_local.setTitle(_translate("Form", "Local IP settings"))
        self.lbl_ip_local.setText(_translate("Form", "IP Address:"))
        self.lbl_prefix_local.setText(_translate("Form", "Prefix-length:"))
        self.tlb_configurations.setItemText(self.tlb_configurations.indexOf(self.pg_basic_config),
                                            _translate("Form", "Basic Config"))
        self.lbl_mng_vlan.setText(_translate("Form", "Management VLAN:"))
        self.lbl_data_line_port.setText(_translate("Form", "Data Line Port:"))
        self.lbl_line_port_vlan.setText(_translate("Form", "Line Port VLAN:"))
        self.lbl_instructions.setText(_translate("Form", "Use Ctrl + Shift + A to enable/disable\n If enabled all the fields "
                                                         "are mandatory\n VLAN = 0 means Transparent: all traffic, "
                                                         "tagged or untagged"))
        self.tlb_configurations.setItemText(self.tlb_configurations.indexOf(self.pg_advanced_config),
                                            _translate("Form", "Advanced Config"))
        self.tlb_configurations.setItemText(self.tlb_configurations.indexOf(self.pg_monitor),
                                            _translate("Form", "TU Monitor"))
