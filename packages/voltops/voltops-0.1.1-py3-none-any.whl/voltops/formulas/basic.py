class BasicFormulas:
    @staticmethod
    def ohms_law(voltage: float = None, current: float = None, resistance: float = None) -> float:
        """
        Calculate the missing parameter in Ohm's Law (V = I * R).
        """
        if voltage is None and current and resistance:
            return current * resistance
        elif current is None and voltage and resistance:
            return voltage / resistance
        elif resistance is None and voltage and current:
            return voltage / current
        else:
            raise ValueError("Provide exactly two parameters: voltage, current, or resistance.")

    @staticmethod
    def power(voltage: float, current: float) -> float:
        """
        Calculate electrical power (P = V * I).
        """
        return voltage * current