import re
from .formatting import format_cpf_to_raw

def is_cpf_format(cpf_string: str) -> bool:
        """
        Checks if a string is in the format XXX.XXX.XXX-XX,
        where each X is a digit from 0 to 9.

        Args:
            cpf_string (str): The string to check.

        Returns:
            bool: True if the string matches the format, False otherwise.
        """
        pattern = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
        return bool(re.match(pattern, cpf_string))

def validate_cpf(cpf: str) -> bool:
    """
    Validates a Brazilian CPF number, formatted or not.

    Args:
        cpf (str): The CPF number to be validated.

    Returns:
        bool: True if the CPF is valid, False otherwise.
    """

    if is_cpf_format(cpf):
        # Removes '.' and '-' characters, if necessary
        cpf = format_cpf_to_raw(cpf)
    
    if not cpf.isdigit() or len(cpf) != 11:
        return False

    # Avoid a CPF where all digits are the same
    if all(cpf[i] == cpf[0] for i in range(11)):
        return False

    # Validates the first verification digit
    final_sum = 0
    for i in range(9):
        final_sum += int(cpf[i]) * (10 - i)
    remainder = 11 - (final_sum % 11)
    digit1 = 0 if remainder > 9 else remainder
    if int(cpf[9]) != digit1:
        return False

    # Validates the second verification digit
    final_sum = 0
    for i in range(10):
        final_sum += int(cpf[i]) * (11 - i)
    remainder = 11 - (final_sum % 11)
    digit2 = 0 if remainder > 9 else remainder
    if int(cpf[10]) != digit2:
        return False

    return True