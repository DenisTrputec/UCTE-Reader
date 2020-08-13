class Line:
    def __init__(self, line_line):
        """
        :param line_line: line of uct file contaning line
        """
        self.line = line_line
        self.node1 = self.line[0:8]
        self.node2 = self.line[9:17]
        self.order_code = self.line[18]
        self.status = self.__get_status()
        self.resistance_r = self.__get_resistance_r()
        self.resistance_x = self.__get_resistance_x()
        self.susceptance = self.__get_susceptance()
        self.current_limit = self.__get_current_limit()
        self.element_name = self.__get_element_name()

    def __get_status(self):
        """
        0: real element IN operation        (R, X only positive values permitted)
        8: real element OUT of operation    (R, X only positive values permitted)
        1: equivalent element IN operation
        9: equivalent element OUT of operation
        2: busbar coupler IN operation      (definition: R=0, X=0, B=0)
        7: busbar coupler OUT of operation  (definition: R=0, X=0, B=0)
        :return: integer
        """
        try:
            return int(self.line[20])
        except ValueError:
            return None

    def __get_resistance_r(self):
        """
        R (Ω)
        :return: float
        """
        try:
            return float(self.line[22:28])
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
            return float(self.line[29:35])
        except ValueError:
            return None

    def __get_susceptance(self):
        """
        B (µS)
        :return: float
        """
        try:
            return float(self.line[36:44])
        except ValueError:
            return None

    def __get_current_limit(self):
        """
        I (A)
        :return: integer
        """
        try:
            return int(self.line[45:51])
        except ValueError:
            return None

    def __get_element_name(self):
        """
        :return: string
        """
        try:
            return self.line[52:64]
        except ValueError:
            return None


if __name__ == "__main__":
    line1 = "HERNES1  XER_PE11 1 8   1.28  13.47   161.48   2001 "
    line2 = "HBRINJ2  HVEPAD2  1 0  11.59  60.82   392.46    780 "
    line3 = "LBERIC2  LKLECE2  2 1  4.000 53.500  120.000    640 BER-KLE220EQ"
    line4 = "HDOLIN5  HMEDUL5  1 0   0.96   3.31    22.35  "
    line5 = "HDOLIN5  HMEDUL5    0   1      3.31    22.35    470 "
    lines = [line1, line2, line3, line4, line5]

    for line in lines:
        obj = Line(line)
        print(obj.node1, obj.node2, obj.element_name)
