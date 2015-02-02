if __name__ == "__main__":
    from os import rename
    names = {'valet': 11, 'reine': 12, 'roi': 13, 'as': 1}
    for i in range(2, 11):
        names[str(i)] = i
    colors = {'pique': 0, 'treffle': 1, 'carreau': 2, 'coeur': 3}

    for name, lower in names.iteritems():
        for color, higher in colors.iteritems():
            val = (higher<<4) | lower
            old_name, new_name = "%s_%s.png"%(name, color), "%d.png"%(val)
            rename(old_name, new_name)
            print old_name, "->", new_name
