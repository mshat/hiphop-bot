def format_print(values: list, column_width: list[int], number_symbols_after_comma=5):
    assert column_width
    current_column_width = 0
    for i, value in enumerate(values):
        if len(column_width) - 1 >= i:
            current_column_width = column_width[i]
        if isinstance(value, float):
            value = round(value, number_symbols_after_comma)
        print(str(value).ljust(current_column_width), end=' ')
    print()