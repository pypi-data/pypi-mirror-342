def convert_binary_to_decimal_and_hex(binary_str: str):
    # Переводим двоичную строку в целое число (десятичная система)
    decimal_value = int(binary_str, 2)
    # Переводим полученное число в шестнадцатеричную систему (без префикса '0x')
    hex_value = format(decimal_value, 'x')
    return decimal_value, hex_value