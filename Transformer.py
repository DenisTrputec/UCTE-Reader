class Transformer:
    def __init__(self, transformer_line):
        """
        :param transformer_line: line of uct file contaning line
        """
        self.line = transformer_line
        self.node1 = self.line[0:8]
        self.node2 = self.line[9:17]
        self.order_code = self.line[18]
        self.status = self.__get_status()
        self.rated_voltage1 = self.__get_rated_voltage(1)
        self.rated_voltage2 = self.__get_rated_voltage(2)
        self.nominal_power = self.__get_nominal_power()
        self.resistance_r = self.__get_resistance_r()
        self.resistance_x = self.__get_resistance_x()
        self.suscepatance = self.__get_susceptance()
        self.conductance = self.__get_conductance()
        self.current_limit = self.__get_current_limit()
        self.element_name = self.__get_element_name()

    def __get_status(self):
        """
        0: real element IN operation        (R, X only positive values permitted)
        8: real element OUT of operation    (R, X only positive values permitted)
        1: equivalent element IN operation
        9: equivalent element OUT of operation
        :return: integer
        """
        try:
            return int(self.line[20])
        except ValueError:
            return None

    def __get_rated_voltage(self, index):
        """
        Rated voltage 1: non-regulated winding (kV)
        Rated voltage 2: regulated winding (kV)
        :return: float
        """
        try:
            return float(self.line[16 + index * 6: 21 + index * 6])
        except ValueError:
            return None

    def __get_nominal_power(self):
        """
        (MVA)
        :return: float
        """
        try:
            return float(self.line[34:39])
        except ValueError:
            return None

    def __get_resistance_r(self):
        """
        R (Ω) - Pertaining to the rated voltage of the non-regultated winding 1 of the transformer
        :return: float
        """
        try:
            return float(self.line[40:46])
        except ValueError:
            return None

    def __get_resistance_x(self):
        """
        X (Ω)
        the absolute value of the reactance for lines has to be greater than or equal to 0.050 Ω
        (to avoid division by values near zero in load flow calculation)
        :return: float
        """
        try:
            return float(self.line[47:53])
        except ValueError:
            return None

    def __get_susceptance(self):
        """
        B (µS)
        :return: float
        """
        try:
            return float(self.line[54:62])
        except ValueError:
            return None

    def __get_conductance(self):
        """
        G (µS)
        :return: float
        """
        try:
            return float(self.line[63:69])
        except ValueError:
            return None

    def __get_current_limit(self):
        """
        I (A)
        :return: integer
        """
        try:
            return int(self.line[70:76])
        except ValueError:
            return None

    def __get_element_name(self):
        """
        :return: string
        """
        try:
            return self.line[77:89]
        except ValueError:
            return None


if __name__ == "__main__":
    line1 = "HKONJS2  HKONJS1  1 0 231.0 400.0 400.0  0.194   15.6    -8.66    2.4   1000 "
    line2 = "HBILIC5  HBILIC2  1 0 115.0 220.0 150.0  0.252    9.0   -11.94    3.6    753 "
    line3 = "LBERIC1  LBERIC2  1 0 400.0 231.0   400  0.250  15.75  -37.057  5.622   1000 BER400 TR422"
    line4 = "LDIVAC11 LDIVAC21 1 1 400.0 220.0   300  3.579 141.29    0.000  0.000    433 DIV 42 TR EQ"
    lines = [line1, line2, line3, line4]

    for line in lines:
        obj = Transformer(line)
        print(obj.node1, obj.node2, obj.conductance)
