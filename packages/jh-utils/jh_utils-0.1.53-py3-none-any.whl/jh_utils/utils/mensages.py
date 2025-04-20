def attention(string: str):
    ret = f"""
    #############################
    !!!!!!!
    {string} 
    !!!!!!!    
    #############################
    """
    return ret


def log_getcwd():
    import os
    attention(f'{os.getcwd()}')


hello = """
################################################################################
################################################################################
                # #  ###  #   #   ###    # #  ###  #   #   ###
                ###  ##   #   #   # #    ###  ##   #   #   # #
                # #  ###  ##  ##  ###    # #  ###  ##  ##  ###
################################################################################
################################################################################
"""


def get_line(number_of_dots, replicable_value="-", skip_line_before=False, skip_line_after=False):
    first = '\n' if skip_line_before else None
    last = '\n' if skip_line_after else None
    line = f'{first}{replicable_value*number_of_dots}{last}'
    return line


line = get_line(51)
