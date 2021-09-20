from datetime import datetime, timedelta
import pandas as pd


class TuDataModel:
    """
    Class Terminal Unit, never modify any variable direct. The idea is that all gets managed via functions
    """
    def __init__(self, name):
        """
        Constructor of the Tu as a holder for all the TG Tu Data. we will refer in the function descriptions as Tu
        PLease never change parameters directly and use the functions and setters and getters
        :param name: str, name of the instanced unit
        """
        # name of the widget
        self.name = name
        # beginning of time from 1st connection
        self.first_connection = -1
        # counter for disconnections
        self.disc_counter = 0
        # management of disconnections event
        self.disconnection_start = None  # start of event
        self.disconnection_end = None  # end of event
        self.connection_state = False  # state of the connection
        self.disconnection_last_event_time = timedelta(seconds=0)  # the total time of last disconnection
        # total disconnection time
        self.disconnection_total_time = timedelta(seconds=0)
        # total actual availability
        self.availability = 0.00
        # Variables to capture and show
        self.local_sector = None
        self.rssi = None
        self.snr = None
        self.rx_mcs = None
        self.tx_mcs = None
        self.rx_speed_num = None
        self.tx_speed_num = None
        self.rx_mcs_dr = None
        self.tx_mcs_dr = None
        self.tx_power_index = None
        # disconnections dataframe to have the list
        # we need to append with a pd.Series(data_in_a_dict, name=datetime.now()/or time)
        self.disconnections = pd.DataFrame(columns=['Time End', 'Disconnection #', 'Downtime', 'Availability'])
        self.parameters_df = pd.DataFrame(columns=['Power Index', 'RSSI', 'SNR', 'MCS-RX', 'MCS-TX', 'MCS-DR-RX',
                                                   'MCS-DR-TX', 'Local Sector'])

    # setters and getters for the internal variables
    def get_local_sector(self):
        """
        Returns the local sector antenna index of the connected unit
        :return: int, index of connected unit
        """
        return self.local_sector

    def set_local_sector(self, ls):
        """
        Sets the local sector index
        :param ls: int, local sector index of connected unit
        :return: None
        """
        self.local_sector = ls

    def get_rssi(self):
        """
        Gets the rssi value of the connected unit
        :return: int, rssi value of the connected unit
        """
        return self.rssi

    def set_rssi(self, rssi):
        """
        Sets the rssi
        :param rssi: int, rssi to set to the object
        :return: None
        """
        self.rssi = rssi

    def get_snr(self):
        """
        Gets the CINR of the connected unit
        :return: int, CINR of the connected unit
        """
        return self.snr

    def set_snr(self, snr):
        """
        Sets the CINR value of the connected unit
        :param snr: int, CINR value
        :return: None
        """
        self.snr = snr

    def get_rxmcs(self):
        """
        Gets the Rx Modulation Coding Scheme of the connected Unit
        :return: int, Rx MCS value
        """
        return self.rx_mcs

    def set_rxmcs(self, rxmcs):
        """
        Sets the Rx Modulation Coding Scheme of the connected Unit
        :param rxmcs: int, Rx MCS value
        :return: None
        """
        self.rx_mcs = rxmcs

    def get_txmcs(self):
        """
        Gets the Tx Modulation Coding Scheme of the connected Unit
        :return: int, Tx MCS value
        """
        return self.tx_mcs

    def set_txmcs(self, txmcs):
        """
        Sets the Tx Modulation Coding Scheme of the connected Unit
        :param txmcs: int, Tx MCS value
        :return: None
        """
        self.tx_mcs = txmcs

    def get_rxspeednum(self):
        """
        Gets the Rx capacity currently going in the Tu in Mbps
        :return: float, Rx In capacity in Mbps
        """
        return self.rx_speed_num

    def set_rxspeednum(self, rxspeednum):
        """
        Sets the Rx capacity currently going in the Tu in Mbps
        :param rxspeednum: float, Rx In capacity in Mbps
        :return: None
        """
        self.rx_speed_num = rxspeednum

    def get_txspeednum(self):
        """
        Gets the Tx capacity currently going in the Tu in Mbps
        :return: float, Tx In capacity in Mbps
        """
        return self.tx_speed_num

    def set_txspeednum(self, txspeednum):
        """
        Sets the Tx capacity currently going in the Tu in Mbps
        :param txspeednum: float, Rx In capacity in Mbps
        :return: None
        """
        self.tx_speed_num = txspeednum

    def get_rxmcsdr(self):
        """
        Gets the Rx Over the Air Data Rate
        :return: int, Rx OTA DR
        """
        return self.rx_mcs_dr

    def set_rxmcsdr(self):
        """
        Sets the Rx Over the Air Dara Rate. based on the RX-MCS
        :return: None
        """

        self.rx_mcs_dr = self.translate_value(self.get_rxmcs())

    def get_txmcsdr(self):
        """
        Gets the Tx Over the Air Data Rate
        :return: int, Tx OTA DR
        """
        return self.tx_mcs_dr

    def set_txmcsdr(self):
        """
        Sets the Tx Over the Air Dara Rate. Based on TX-MCS
        :return: None
        """

        self.tx_mcs_dr = self.translate_value(self.get_txmcs())

    def get_power_index(self):
        """
        Gets the Power Index
        :return: int, Power Index
        """
        return self.tx_power_index

    def set_power_index(self, power_index_):
        """
        Sets the Power Index
        :return: int, Power Index
        """
        self.tx_power_index = power_index_

    def get_availability(self):
        """
        Gets the Availability
        :return: float, calculated availability value
        """
        return self.availability

    def set_availability(self, availabiliti_to_set):
        """
        Sets the availability
        :param availabiliti_to_set: float with the availability to set
        :return: None
        """
        self.availability = availabiliti_to_set

    def get_disconnection_end(self):
        """
        Gets the disconnection end time
        :return: datetime, disconnection end
        """
        return self.disconnection_end

    def set_disconnection_end(self, disconection_end):
        """
        Sets the disconnection end
        :param disconection_end: datetime, disconnection end
        :return: None
        """
        self.disconnection_end = disconection_end

    def get_disconnection_start(self):
        return self.disconnection_start

    def set_disconnection_start(self, disconnection_start):
        self.disconnection_start = disconnection_start

    def get_disconnection_counter(self):
        """
        Gets the disconnection counters
        :return: int, disconnection counter
        """
        return self.disc_counter

    def get_disconnection_ldt(self):
        return self.disconnection_last_event_time

    def get_disconnection_lds(self):
        return self.disconnection_start

    def get_disconnection_tdt(self):
        return self.disconnection_total_time

    def get_connection_status(self):
        return self.connection_state

    # translation function
    @staticmethod
    def translate_value(value_to_translate):
        """
        Translates the input value MCS to a MCS Data Rate
        :param value_to_translate: int to translate
        :return: value_translated, value in Mbps OTA
        """
        if value_to_translate == '0':
            value_translated = '0'
        elif value_to_translate == '2':
            value_translated = '620'
        elif value_to_translate == '3':
            value_translated = '780'
        elif value_to_translate == '4':
            value_translated = '950'
        elif value_to_translate == '7':
            value_translated = '1580'
        elif value_to_translate == '8':
            value_translated = '1900'
        elif value_to_translate == '9':
            value_translated = '2050'
        elif value_to_translate == '10':
            value_translated = '2500'
        elif value_to_translate == '11':
            value_translated = '3150'
        elif value_to_translate == '12':
            value_translated = '3800'
        else:
            value_translated = '0'

        return value_translated

    # Automated behaviour of the object for connections and disconnections
    def disconnected(self, time_disc):
        """
        Function that sets the start of a disconnection. It will get a datetime time
        :param time_disc: datetime, will set the time
        :return: None
        """
        if self.connection_state:  # the Tu was connected and we will disconnect it
            self.connection_state = False  # Set the connection flag down
            self.disconnection_start = time_disc  # record the time of the disconnection time
            self.disc_counter = self.increment_disconnections(self.disc_counter)  # increment the counter of disconn.
            # We update parameters to reflect the disconnection:
            self.set_rssi(-100)
            self.set_snr(0)
            self.set_rxmcs(0)
            self.set_txmcs(0)
        else:  # we enter the disconnected state but the unit was already disconnected
            # we calculate the total time of the disconnection in realtime
            self.disconnection_total_time = self.update_total_time(self.disconnection_total_time, time_disc)
            # we calculate the availability up to the time
            disconnected_availability = self.calculate_availability(self.disconnection_total_time,
                                                                    self.first_connection,
                                                                    time_disc)
            self.set_availability(disconnected_availability)  # we update the value

    def connected(self, time_con):
        """
        Will update the connection status. It will differentiate if it is a first connection a connection already
        connected or disconnected unit that got connected.
        In the case of a first connection it will set a few parameters to the starting values
        In the case of a connection already established it will update the availability
        In the case of a disconnected unit being reconnected it will update all the counters
        :param time_con: datetime, time of the connection
        :return: None
        """
        if not self.connection_state and self.first_connection != -1:  # the Tu was disconnected and it got connected
            # first_connection works only if it was disconnected for the very first time

            self.set_disconnection_end(time_con)  # record the time the disconnection time ended

            # calculate the total time of the disconnection
            self.disconnection_last_event_time = self.calculate_disconnection_time(self.get_disconnection_start(),
                                                                                   self.get_disconnection_end())

            # calculate the total time of disconnection. In this new modification because we add the time even when it
            # is disconneted we can add it in real time
            self.disconnection_total_time = self.update_total_time(self.disconnection_total_time, time_con)

            # calculate availability
            connected_availability = self.calculate_availability(self.disconnection_total_time,
                                                                 self.first_connection,
                                                                 time_con)
            self.set_availability(connected_availability)
            # update the disconnections dataframe -------------------------------------------------DF
            # update 1 : update time end
            self.update_record(self.disconnections, self.disconnection_start, 'Time End', time_con)
            # update 2: update duration of the disconnection
            self.update_record(self.disconnections, self.disconnection_start, 'Downtime',
                               f'{self.disconnection_last_event_time}')
            # update 3: update of the availability
            self.update_record(self.disconnections, self.disconnection_start, 'Availability', connected_availability)
            # update 4: update of disconnection#
            self.update_record(self.disconnections, self.disconnection_start, 'Disconnection #',
                               self.get_disconnection_counter())

            self.connection_state = True  # change flag to connected

        elif self.first_connection == -1:  # the Tu was first connected
            self.first_connection = time_con
            self.connection_state = True
            self.set_availability(100.00)

        else:
            # calculate availability
            availability = self.calculate_availability(self.disconnection_total_time, self.first_connection, time_con)
            self.set_availability(availability)

    @staticmethod
    def calculate_availability(time_span, start_t, time_t):
        """
        Calculate availability of time_span from start to time
        :param time_span: datetime, time where we can to calculate availability
        :param start_t: datetime, start time to calculate availability
        :param time_t: datetime, time to calculate availability
        :return:  float, availability
        """
        if start_t == -1:  # the unit was never connected
            return 0
        return (1 - (time_span / (time_t - start_t))) * 100

    @staticmethod
    def update_total_time(total_time_counter, update):
        """
        Updates the total_time_counter by update
        :param total_time_counter: datetime, has the current total time
        :param update: datetime, the value to update the total time
        :return: total_time_counter + update
        """
        delta = update - total_time_counter
        return total_time_counter + delta

    @staticmethod
    def calculate_disconnection_time(start, end):
        """
        Calculates the total time of disconnection end - start
        :param start: datetime, start time of the event
        :param end: datetime, end time of the event
        :return: end - start
        """
        return end - start

    @staticmethod
    def update_record(df, find_variable, field, update_data):
        df.loc[find_variable, field] = update_data

    def create_end(self, end_time):
        end_ = pd.Series(
            {'Time End': end_time, 'Disconnection #': self.disc_counter, 'Downtime': f'{self.disconnection_total_time}',
             'Availability': self.calculate_availability(end_time - self.first_connection,
                                                         self.first_connection,
                                                         end_time)}, name='Total')
        self.disconnections = self.disconnections.append(end_)
        # Change type of columns to print in excel to proper value
        self.disconnections['Disconnection #'] = self.disconnections['Disconnection #'].astype(int)
        self.disconnections['Availability'] = self.disconnections['Availability'].astype(float)

    @staticmethod
    def increment_disconnections(counter):
        """
        Function that will add counter + 1 and return it
        :param counter: int, disconnections counter
        :return: int, counter + 1
        """
        return counter + 1

    def print(self):
        print('*****Tu instance*****')
        print(f'- name: {self.name}')
        print(f'- first connected: {self.first_connection}')
        print(f'-------conection status------------')
        print(f'connection: {self.connection_state}')
        print(f'-------disconnection info----------')
        print(f'- diconnections: {self.disc_counter}')
        print(f'- disconnection event-start: {self.disconnection_start}')
        print(f'- disconnection event-end: {self.disconnection_end}')
        print(f'- disconnection event time: {self.disconnection_last_event_time}')
        print(f'----disconnection total time-------')
        print(f'- total time disconnected: {self.disconnection_total_time}')
        print(f'-----total availability at the time of print----')
        print(f'- availability: {self.calculate_availability(self.disconnection_total_time, self.first_connection, datetime.now())}')
        print(f'--------operation parameters-------')
        print(f'- local sector: {self.local_sector}')
        print(f'- rssi: {self.rssi}')
        print(f'- srn: {self.rssi}')
        print(f'- rx_mcs: {self.rx_mcs}')
        print(f'- tx_mcs: {self.tx_mcs}')
        print(f'- rx_speed_num: {self.rx_speed_num}')
        print(f'- tx_speed_num: {self.tx_speed_num}')
        print(f'- rx_mcs_dr: {self.rx_mcs_dr}')
        print(f'- tx_mcs_dr: {self.tx_mcs_dr}')
        print(f'- power_index: {self.tx_power_index}')
        print(f'------------events dataframe-------------')
        print(f'{self.disconnections}')


if __name__ == '__main__':
    import time

    # options to display the whole dataframe for checks
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    print(f'Creating object: Test Tu No. 1')
    test_tu = TuDataModel('Test Tu No. 1')
    # test_tu.print()
    # Testing connecting for the first time
    print(f'Connection the unit to the network for the first time')
    start_time = datetime.now()
    print(start_time)
    test_tu.connected(start_time)
    # test_tu.print()
    # Have connection 10 seconds
    print(f'emulating time for 10 seconds')
    time.sleep(10)
    # after 10 seconds disconnect
    print('dropping for 5 seconds...')
    test_tu.disconnected(datetime.now())
    # test_tu.print()
    time.sleep(5)
    print('reconnecting')
    test_tu.connected(datetime.now())
    print(f'emulating time for 3 seconds')
    time.sleep(3)
    print('reconnecting after 2 seconds')
    test_tu.disconnected(datetime.now())
    time.sleep(2)
    print('reconnecting emulating time for 120 seconds')
    test_tu.connected(datetime.now())
    time.sleep(120)
    print('printing')
    print(datetime.now())
    test_tu.print()
