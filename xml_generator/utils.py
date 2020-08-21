def safe_bool(input_val) -> bool:
    if type(input_val) is str:
        return input_val.lower() in ['1', 't', 'true']
    elif type(input_val) is bool:
        return input_val
    elif type(input_val) is int or type(input_val) is float:
        return input_val == 1
    else:
        exception_msg = f"input value type {type(input_val)} is not supported"
        raise Exception(exception_msg)
