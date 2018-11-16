from whichcraft import which


def find_zip():
    # check to see if we can find zip
    zip = which('zip')
    return zip


def find_pyuic5():
    pyuic5 = which('pyuic5')
    return pyuic5


def find_7z():
    # check for 7z
    zip = which('7z')
    return zip


pyuic5_exec = find_pyuic5()
