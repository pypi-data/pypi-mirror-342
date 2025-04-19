# cpf_playground

## Description

The package cpf_playground is used to:
    - Generate CPFs (randomly or from staring first 9 digits)
    - Formatting, adding or removing "-" and "." characters
    - Validates formatted or raw CPF numbers

## installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cpf_playground

```bash
pip install cpf_playground
```

## Usage

### Validating a raw CPF number
```python
    from cpf_playground.validation import validate_cpf

    cpf = "12345678909"
    validate_cpf(cpf) # True or false, according to the number
```

### Validating a formatted CPF number
```python
    from cpf_playground.validation import validate_cpf
    
    cpf = "123.456.789-09"
    validate_cpf(cpf) # True or false, according to the number
```

### Creating a new random and valid CPF number
```python
    from cpf_playground.generation import create_cpf

    cpf = create_cpf() # returns a valid CPF number
```

### Creating a valid CPF number from 9 initial digits
```python
    from cpf_playground.generation import create_from_9_digits

    first_9_digits = "123456789"
    cpf = create_from_9_digits(first_9_digits) # returns a valid CPF number
```

### Formatting a raw CPF number into a string with "-" and "." characters
```python
    from cpf_playground.formatting import fromat_cpf_from_raw

    raw_cpf = "12345678909"
    cpf = fromat_cpf_from_raw(raw_cpf) # Returns a formatted CPF, like 123.456.789-09
```

### Formatting a raw CPF number into a string with "-" and "." characters
```python
    from cpf_playground.formatting import fromat_cpf_to_raw

    cpf = "123.456.789-09"
    raw_cpf = fromat_cpf_to_raw(cpf) # Returns a raw CPF, like 12345678909
```

## Author

bernard_clint