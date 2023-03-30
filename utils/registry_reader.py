def process_reg(dat):
    ret = {}
    prev_spl = "NULL"
    for line in dat:
        spl = line.split(":", 1)
        if len(spl) == 1:
            if spl != "+":
                if prev_spl in ret:
                    ret[prev_spl].append(spl[0].lstrip())
        else:
            if spl[0] in ret:
                ret[spl[0]].append(spl[1].lstrip())
            else:
                ret[spl[0]] = [spl[1].lstrip()]
            prev_spl = spl[0]
    return ret

def get_key(dat, key):
    if key not in dat:
        return "None"
    else:
        ret = ""
        for ln in dat[key]:
            if ret != "":
                ret = ret + '\n'
            ret = ret + ln
        return ret