# Sorts lists in string time format: ['min:secs'] from lowest to highest
def sort_list(lst):
    new = []
    for i in lst:
        temp = str(i).split(':')
        if len(temp) > 1:
            new.append(int(temp[0]) * 60 + int(temp[1]))
        else:
            new.append(int(temp[0]))
    new.sort()
    final = []
    for i in new:
        if i > 59:
            minutes = i / 60
            seconds = i % 60
            final.append('%s:%s' % (int(minutes), int(seconds)))
        else:
            final.append(str(i))
    return final