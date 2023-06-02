import re
def get_time(var):
    regex = re.compile('\D+')
    t=regex.split(var)
    print(t)
    return t