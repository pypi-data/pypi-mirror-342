from .validation import is_cpf_format

def format_cpf_from_raw(cpf: str) -> str:
    """Adds '.' and '-' to a raw Brazilian CPF number

    Args:
        cpf (str): A raw Brazilian CPF number with no '.' and '-' characters

    Returns:
        str: A formated Brazilian CPF number with '.' and '-' characters
    """

    if cpf.isdigit() and len(cpf) == 11:
        return f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
    
    else:
        raise Exception("Non valid CPF input. It must have 11 digit characters")
    
def format_cpf_to_raw(cpf: str) -> str:
    """Removes '.' and '-' from a Brazilian CPF number

    Args:
        cpf (str): A formated Brazilian CPF number with '.' and '-' characters

    Returns:
        str: A raw Brazilian CPF number with no '.' and '-' characters
    """

    if is_cpf_format(cpf):
        return cpf.translate(str.maketrans('', '', '.-'))
    else:
        raise Exception("Non-valid CPF input. It must be in XXX.XXX.XXX-XX format")
