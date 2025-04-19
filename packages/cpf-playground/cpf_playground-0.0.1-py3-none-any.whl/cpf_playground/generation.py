from random import randint

def create_cpf() -> str:
    """
    Creates a random Brazilian CPF number.

    Args:
        None

    Returns:
        str: A valid Brazilian CPF number.
    """
    
    first_9_digits = ""
    while True:
        # Generates the next digit
        first_9_digits += str(randint(0,9))
        
        if len(first_9_digits) == 9:
            # Checks if all the 9 digits are not the same
            if not all(first_9_digits[i] == first_9_digits[0] for i in range(9)):
                break
            else:
                # resets the proccess
                first_9_digits = ""

    # Validates the first verification digit
    final_sum = 0
    for i in range(9):
        final_sum += int(first_9_digits[i]) * (10 - i)
    remainder = 11 - (final_sum % 11)
    digit1 = 0 if remainder > 9 else remainder
    
    cpf = first_9_digits + str(digit1)

    # Validates the second verification digit
    final_sum = 0
    for i in range(10):
        final_sum += int(cpf[i]) * (11 - i)
    remainder = 11 - (final_sum % 11)
    digit2 = 0 if remainder > 9 else remainder
    
    return cpf + str(digit2)

def create_from_9_digits(first_9_digits: str) -> str:
    """
    Concatenates the last 2 verification digits to achieve a valid Brazilian CPF number

    Args:
        first_9_digits (str): String with the first 9 digits of a possible Brazilian CPF number

    Returns:
        str: A valida Brazilian CPF number
    """
    if first_9_digits.isdigit() and len(first_9_digits) == 9 and not all(first_9_digits[i] == first_9_digits[0] for i in range(9)):
        
        # Validates the first verification digit
        final_sum = 0
        for i in range(9):
            final_sum += int(first_9_digits[i]) * (10 - i)
        remainder = 11 - (final_sum % 11)
        digit1 = 0 if remainder > 9 else remainder
        
        cpf = first_9_digits + str(digit1)

        # Validates the second verification digit
        final_sum = 0
        for i in range(10):
            final_sum += int(cpf[i]) * (11 - i)
        remainder = 11 - (final_sum % 11)
        digit2 = 0 if remainder > 9 else remainder
        
        return cpf + str(digit2)
    
    else:
        raise Exception("Invalid input.")