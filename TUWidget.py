from PyQt5 import QtCore as Qtc
from PyQt5 import QtGui as Qtg
from PyQt5 import QtWidgets as Qtw


class TuWidget(Qtw.QWidget):
    def __init__(self, name, parent=None):
        super(TuWidget, self).__init__(parent)

        self.name = name

        ##### Font
        widget_font = Qtg.QFont()
        widget_font.setPointSize(10)

        self.setFont(widget_font)

        ### Auto generated code
        self.setGeometry(Qtc.QRect(0, 0, 308, 178))
        self.setObjectName(f'{self.name}')

        self.layout_general_v = Qtw.QVBoxLayout(self)
        self.layout_general_v.setContentsMargins(0, 0, 0, 0)
        self.layout_general_v.setObjectName("layout_general_v")

        self.lbl_name = Qtw.QLabel(self)
        self.lbl_name.setObjectName("lbl_name")
        self.layout_general_v.addWidget(self.lbl_name)

        self.lbl_remote_mac = Qtw.QLabel(self)
        self.lbl_remote_mac.setObjectName('lbl_remote_mac')
        self.layout_general_v.addWidget(self.lbl_remote_mac)

        self.lbl_role = Qtw.QLabel(self)
        self.lbl_role.setObjectName('lbl_role')
        self.layout_general_v.addWidget(self.lbl_role)

        self.layout_leftright_h = Qtw.QHBoxLayout()
        self.layout_leftright_h.setObjectName("layout_leftright_h")

        self.layout_right_v = Qtw.QVBoxLayout()
        self.layout_right_v.setObjectName("layout_right_v")

        self.layout_ls_av_h = Qtw.QHBoxLayout()
        self.layout_ls_av_h.setObjectName("layout_ls_av_h")

        self.lbl_local_sector = Qtw.QLabel(self)
        self.lbl_local_sector.setObjectName("lbl_local_sector")
        self.layout_ls_av_h.addWidget(self.lbl_local_sector)

        self.lbl_local_sector_counter = Qtw.QLabel(self)
        self.lbl_local_sector_counter.setObjectName("lbl_local_sector_counter")
        self.layout_ls_av_h.addWidget(self.lbl_local_sector_counter)

        self.lbl_remote_sector = Qtw.QLabel(self)
        self.lbl_remote_sector.setObjectName('lbl_remote_sector')
        self.layout_ls_av_h.addWidget(self.lbl_remote_sector)

        self.lbl_remote_sector_counter = Qtw.QLabel(self)
        self.lbl_remote_sector_counter.setObjectName('lbl_remote_sector_counter')
        self.layout_ls_av_h.addWidget(self.lbl_remote_sector_counter)

        self.layout_right_v.addLayout(self.layout_ls_av_h)

        self.layout_rssi_snr_h = Qtw.QHBoxLayout()
        self.layout_rssi_snr_h.setObjectName("layout_rssi_snr_h")

        self.lbl_rssi = Qtw.QLabel(self)
        self.lbl_rssi.setObjectName("lbl_rssi")
        self.layout_rssi_snr_h.addWidget(self.lbl_rssi)

        self.lbl_rssi_counter = Qtw.QLabel(self)
        self.lbl_rssi_counter.setObjectName("lbl_rssi_counter")
        self.layout_rssi_snr_h.addWidget(self.lbl_rssi_counter)

        self.lbl_snr = Qtw.QLabel(self)
        self.lbl_snr.setObjectName("lbl_snr")
        self.layout_rssi_snr_h.addWidget(self.lbl_snr)

        self.lbl_snr_counter = Qtw.QLabel(self)
        self.lbl_snr_counter.setObjectName("lbl_snr_counter")
        self.layout_rssi_snr_h.addWidget(self.lbl_snr_counter)

        self.layout_right_v.addLayout(self.layout_rssi_snr_h)

        self.layout_mcs_h = Qtw.QHBoxLayout()
        self.layout_mcs_h.setObjectName("layout_mcs_h")

        self.lbl_rxmcs = Qtw.QLabel(self)
        self.lbl_rxmcs.setObjectName("lbl_rxmcs")
        self.layout_mcs_h.addWidget(self.lbl_rxmcs)

        self.lbl_rxmcs_counter = Qtw.QLabel(self)
        self.lbl_rxmcs_counter.setObjectName("lbl_rxmcs_counter")
        self.layout_mcs_h.addWidget(self.lbl_rxmcs_counter)

        self.lbl_txmcs = Qtw.QLabel(self)
        self.lbl_txmcs.setObjectName("lbl_txmcs")
        self.layout_mcs_h.addWidget(self.lbl_txmcs)

        self.lbl_txmcs_counter = Qtw.QLabel(self)
        self.lbl_txmcs_counter.setObjectName("lbl_txmcs_counter")
        self.layout_mcs_h.addWidget(self.lbl_txmcs_counter)

        self.layout_right_v.addLayout(self.layout_mcs_h)

        self.layout_datarate_h = Qtw.QHBoxLayout()
        self.layout_datarate_h.setObjectName("layout_datarate_h")

        self.lbl_rxdr = Qtw.QLabel(self)
        self.lbl_rxdr.setObjectName("lbl_rxdr")
        self.layout_datarate_h.addWidget(self.lbl_rxdr)

        self.lbl_rxdr_counter = Qtw.QLabel(self)
        self.lbl_rxdr_counter.setObjectName("lbl_rxdr_counter")
        self.layout_datarate_h.addWidget(self.lbl_rxdr_counter)

        self.lbl_txdr = Qtw.QLabel(self)
        self.lbl_txdr.setObjectName("lbl_txdr")
        self.layout_datarate_h.addWidget(self.lbl_txdr)

        self.lbl_txdr_counter = Qtw.QLabel(self)
        self.lbl_txdr_counter.setObjectName("lbl_txdr_counter")
        self.layout_datarate_h.addWidget(self.lbl_txdr_counter)

        self.layout_right_v.addLayout(self.layout_datarate_h)

        self.layout_per_h = Qtw.QHBoxLayout()
        self.layout_per_h.setObjectName('layout_per_h')

        self.lbl_perrx = Qtw.QLabel(self)
        self.lbl_perrx.setObjectName('lbl_perrx')
        self.layout_per_h.addWidget(self.lbl_perrx)

        self.lbl_perrx_counter = Qtw.QLabel(self)
        self.lbl_perrx_counter.setObjectName('lbl_perrx_counter')
        self.layout_per_h.addWidget(self.lbl_perrx_counter)

        self.lbl_pertx = Qtw.QLabel(self)
        self.lbl_pertx.setObjectName('lbl_pertx')
        self.layout_per_h.addWidget(self.lbl_pertx)

        self.lbl_pertx_counter = Qtw.QLabel(self)
        self.lbl_pertx_counter.setObjectName('lbl_pertx_counter')
        self.layout_per_h.addWidget(self.lbl_pertx_counter)

        self.layout_right_v.addLayout(self.layout_per_h)

        self.layout_aligment = Qtw.QHBoxLayout()

        self.lbl_aligment_rx = Qtw.QLabel(self)
        self.lbl_aligment_rx.setObjectName('lbl_aligment_rx')
        self.layout_aligment.addWidget(self.lbl_aligment_rx)

        self.lbl_aligment_tx = Qtw.QLabel(self)
        self.lbl_aligment_tx.setObjectName('lbl_aligment_tx')
        self.layout_aligment.addWidget(self.lbl_aligment_tx)

        self.layout_right_v.addLayout(self.layout_aligment)

        self.layout_leftright_h.addLayout(self.layout_right_v)

        self.layout_general_v.addLayout(self.layout_leftright_h)

        self.retranslate_ui()

    def retranslate_ui(self, ):
        _translate = Qtc.QCoreApplication.translate
        self.lbl_name.setText(_translate("TuWidget", "Name"))
        self.lbl_local_sector.setText(_translate("TuWidget", "L.S."))
        self.lbl_local_sector_counter.setText(_translate("TuWidget", "0"))
        self.lbl_rssi.setText(_translate("TuWidget", "RSSI:"))
        self.lbl_rssi_counter.setText(_translate("TuWidget", "-100"))
        self.lbl_snr.setText(_translate("TuWidget", "SNR:"))
        self.lbl_snr_counter.setText(_translate("TuWidget", "-100"))
        self.lbl_rxmcs.setText(_translate("TuWidget", "RxMCS:"))
        self.lbl_rxmcs_counter.setText(_translate("TuWidget", "12"))
        self.lbl_txmcs.setText(_translate("TuWidget", "TxMCS:"))
        self.lbl_txmcs_counter.setText(_translate("TuWidget", "12"))
        self.lbl_rxdr.setText(_translate("TuWidget", "Rx DR:"))
        self.lbl_rxdr_counter.setText(_translate("TuWidget", "7000"))
        self.lbl_txdr.setText(_translate("TuWidget", "Tx DR:"))
        self.lbl_txdr_counter.setText(_translate("TuWidget", "7000"))
        self.lbl_remote_sector.setText(_translate('TuWidget', 'R.S.'))
        self.lbl_remote_sector_counter.setText(_translate('TuWidget', '0'))
        self.lbl_remote_mac.setText(_translate('TuWidget', '00:00:00:00:00:00'))
        self.lbl_role.setText(_translate('TuWidget', 'Role'))
        self.lbl_pertx.setText(_translate('TuWidget', 'PER Tx'))
        self.lbl_pertx_counter.setText(_translate('TuWidget', '0.00'))
        self.lbl_perrx.setText(_translate('TuWidget', 'PER Rx'))
        self.lbl_perrx_counter.setText(_translate('TuWidget', '0.00'))