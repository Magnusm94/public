# Makes a list that counts up from 1 to len of sublist in a list
def count_each_sublist(lst):
    sublists = []
    for index in lst:
        counter = 1
        for i in index:
            sublists.append(counter)
        counter += 1