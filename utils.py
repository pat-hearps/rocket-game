


def scale_variable(variable, inverse_difficulty):
    """applies slightly non-linear increasing scale to speed etc based on difficulty level"""
    return variable * (2 * (1.25 ** -inverse_difficulty))

