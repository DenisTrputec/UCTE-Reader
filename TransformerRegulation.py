class TransformerRegulation:
    def __init__(self, transformer_line):
        """
        :param transformer_line: line of uct file contaning line
        """
        self.line = transformer_line
        self.node1 = self.line[0:8]
        self.node2 = self.line[9:17]
        self.order_code = self.line[18]
        self.phase_regulation_delta = self.__get_delta(0)
        self.phase_regulation_number_of_taps = self.__get_number_of_taps(0)
        self.phase_regulation_tap_postion = self.__get_tap_position(0)
        self.phase_regulation_voltage = self.__get_tap_changer_voltage()
        self.angle_regulation_delta = self.__get_delta(1)
        self.angle_regulation_number_of_taps = self.__get_number_of_taps(1)
        self.angle_regulation_tap_postion = self.__get_tap_position(1)
        self.angle_regulation_theta = self.__get_theta()
        self.angle_regulation_active_power = self.__get_tap_changer_active_power()
        self.angle_regulation_type = self.__get_type()

    def __get_delta(self, index):
        """
        δu (%)
        :parameter: index = 0 for phase regulation and index = 1 for angle regulation
        :return: float
        """
        try:
            return float(self.line[20 + 19 * index:25 + 19 * index])
        except ValueError:
            return None

    def __get_number_of_taps(self, index):
        """
        n = number of taps, counted the following way: it is the difference between the intermediate position (neutral)
        and the positive or negative ultimate position  (e.g. a transformer with total 27 taps (+13,neutral,-13)
        is given as n = 13 in the UCTE format)
        :parameter: index = 0 for phase regulation and index = 1 for angle regulation
        :return: integer
        """
        try:
            return int(self.line[26 + 25 * index:28 + 25 * index])
        except ValueError:
            return None

    def __get_tap_position(self, index):
        """
        n'
        :parameter: index = 0 for phase regulation and index = 1 for angle regulation
        :return: integer
        """
        try:
            return int(self.line[29 + 25 * index:32 + 25 * index])
        except ValueError:
            return None

    def __get_tap_changer_voltage(self):
        """
        U (kV) (optional): On load tap changer voltage target for node 2 (V2 or UL)
        :return: float
        """
        try:
            return float(self.line[33:38])
        except ValueError:
            return None

    def __get_theta(self):
        """
        Θ (°)
        :return: float
        """
        try:
            return float(self.line[45:50])
        except ValueError:
            return None

    def __get_tap_changer_active_power(self):
        """
        P (MW) (optional): On load tap changer active power flow target.
        :return: float
        """
        try:
            return float(self.line[58:63])
        except ValueError:
            return None

    def __get_type(self):
        """
        Type (ASYM: asymmetrical, SYMM: symmetrical)
        :return: string
        """
        try:
            return self.line[64:68]
        except ValueError:
            return None


if __name__ == "__main__":
    line1 = "LDIVAC11 LDIVAC12 1 0.000  0   0  0.00  2.27    90 32   0   650 SYMM"
    line2 = "HSENJ 5  HSENJ 2  1  0.00  0   0        1.10 60.00 12  10 "
    line3 = "HPLAT 5  HPLAT 2  2  1.25 12   9        0.00  0.00  0   0 "
    line4 = "HZERJA2  HZERJA1  1  0.00  0   0        0.90 60.00 12  -1 "
    lines = [line1, line2, line3, line4]

    for line in lines:
        obj = TransformerRegulation(line)
        print(obj.node1, obj.node2, obj.angle_regulation_type)
