class Node:
    def __init__(self, node_line):
        """
        :param node_line: line of uct file contaning node
        """
        self.line = node_line
        self.code = self.line[0:8]
        self.geographical_name = self.line[9:21]
        self.status = self.__get_status()
        self.type_code = self.__get_type_code()
        self.voltage = self.__get_voltage()
        self.active_load = self.__get_active_load()
        self.reactive_load = self.__get_reactive_load()
        self.active_power_generation = self.__get_active_power_generation()
        self.reactive_power_generation = self.__get_reactive_power_generation()
        self.minimum_permissible_generation_mw = self.__get_minimum_permissible_generation_mw()
        self.maximum_permissible_generation_mw = self.__get_maximum_permissible_generation_mw()
        self.minimum_permissible_generation_mvar = self.__get_minimum_permissible_generation_mvar()
        self.maximum_permissible_generation_mvar = self.__get_maximum_permissible_generation_mvar()
        self.static_of_primary_control = self.__get_static_of_primary_control()
        self.nominal_power_of_primary_control = self.__get_nominal_power_for_primary_control()
        self.three_phase_short_circuit_power = self.__get_three_phase_short_circuit_power()
        self.x_div_r_ratio = self.__get_three_phase_short_circuit_power()
        self.power_plant_type = self.__get_power_plant_type()

    def __get_status(self):
        """
        0 = real
        1 = equivalent
        :return: integer
        """
        try:
            return int(self.line[22])
        except ValueError:
            return None

    def __get_type_code(self):
        """
        0 = P and Q constant (PQ node)
        1 = Q and θ constant
        2 = P and U constant (PU node)
        3 = U and θ constant (global slack node, only one in the whole network)
        :return: integer
        """
        try:
            return int(self.line[24])
        except ValueError:
            return None

    def __get_voltage(self):
        """
        reference value, 0 not allowed
        (kV)
        :return: float
        """
        try:
            return float(self.line[26:32])
        except ValueError:
            return None

    def __get_active_load(self):
        """
        (MW)
        :return: float
        """
        try:
            return float(self.line[33:40])
        except ValueError:
            return None

    def __get_reactive_load(self):
        """
        (MVar)
        :return: float
        """
        try:
            return float(self.line[41:48])
        except ValueError:
            return None

    def __get_active_power_generation(self):
        """
        (MW)
        :return: float
        """
        try:
            return float(self.line[49:56])
        except ValueError:
            return None

    def __get_reactive_power_generation(self):
        """
        (MVar)
        :return: float
        """
        try:
            return float(self.line[57:64])
        except ValueError:
            return None

    def __get_minimum_permissible_generation_mw(self):
        """
        (MW)
        :return: float
        """
        try:
            return float(self.line[65:72])
        except ValueError:
            return None

    def __get_maximum_permissible_generation_mw(self):
        """
        (MW)
        :return: float
        """
        try:
            return float(self.line[73:80])
        except ValueError:
            return None

    def __get_minimum_permissible_generation_mvar(self):
        """
        (MVar)
        :return: float
        """
        try:
            return float(self.line[81:88])
        except ValueError:
            return None

    def __get_maximum_permissible_generation_mvar(self):
        """
        (MVar)
        :return: float
        """
        try:
            return float(self.line[89:96])
        except ValueError:
            return None

    def __get_static_of_primary_control(self):
        """
        (%)
        :return: float
        """
        try:
            return float(self.line[97:102])
        except ValueError:
            return None

    def __get_nominal_power_for_primary_control(self):
        """
        (MW)
        :return: float
        """
        try:
            return float(self.line[103:110])
        except ValueError:
            return None

    def __get_three_phase_short_circuit_power(self):
        """
        (MVA)
        :return: float
        """
        try:
            return float(self.line[111:118])
        except ValueError:
            return None

    def __get_x_div_r_ratio(self):
        """
        ()
        :return: float
        """
        try:
            return float(self.line[119:126])
        except ValueError:
            return None

    def __get_power_plant_type(self):
        """
        H: hydro
        N: nuclear
        L: lignite
        C: hard coal
        G: gas
        O: oil
        W: wind
        F: further
        :return: string
        """
        try:
            return self.line[127]
        except IndexError:
            return None


if __name__ == "__main__":
    line1 = "HDJALE5  HE Dale      0 2  116.5     0.0     0.0   -10.0     7.0    -6.0   -20.4     7.0   -12.0   0.0 "
    line2 = "HDONJM5  Donji Miholj   9  117.0     1.5    -0.4     0.0     0.0 "
    line3 = "HSENJ 2  HE Senj      0 2  246.7     0.0     0.0     0.0     0.0   -35.0   -72.0    31.0   -35.0 "
    line4 = "LDIVAC11 LDIVAC11     A            155.7    28.0     0.0     0.0     0.0     0.0   100.0  -100.0   0.0     0.0     0.0     0.0  "
    line5 = "LSOSTA16 LSOSTA16     0 2  400.8     0.0     0.0  -382.0   -29.8     0.0  -553.0   400.0  -300.0   0.0     0.0     0.0     0.0 L"
    lines = [line1, line2, line3, line4, line5]

    for line in lines:
        obj = Node(line)
        print(obj.code, str(obj.power_plant_type))
