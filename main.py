from telegram.ext import Updater,CommandHandler,CallbackContext
from os import listdir
import os
import sys
import time


updater = Updater(token=sys.argv[1], use_context=True)

dispatcher = updater.dispatcher

REGPATH = os.path.expanduser('~') + "/registry"

CACHEPATH = os.path.expanduser('~') + "/cache_data"

TEMPLATE = "ASN: {0[0]}\nAS Name: {0[1]}\nDescr: {0[2]}\nMNT-by: {0[3]}\nCountry: {0[4]}\nOrg: {0[5]}"

def process_file(dat):
    ret = {}
    prev_spl = "NULL"
    for line in dat:
        spl = line.split(":", 1)
        if len(spl) == 1:
            if spl != "+":
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
            ret = ret + ln
        return ret

def send_new(asn):
    with open(REGPATH + '/' + asn) as asn_file:
        asn_data = asn_file.read().splitlines()
    asn_info = process_file(asn_data)
    new_arr = [get_key(asn_info, k) for k in ['aut-num','as-name','descr','mnt-by','country','org']]
    dispatcher.bot.send_message(chat_id=sys.argv[2], 
                             text=TEMPLATE.format(new_arr))

def main():
    print("Starting new task...")
    asn_list = [f for f in listdir(REGPATH)]
    asn_new = []
    with open(CACHEPATH + '/asn.txt') as asn_file:
        asn_old_list = asn_file.read().splitlines()
        asn_new = list(sorted(set(asn_list) - set(asn_old_list)))
    with open(CACHEPATH + '/asn.txt', 'w') as asn_file:
        asn_file.write('\n'.join(asn_list))
    for new_asn in asn_new:
        send_new(new_asn)
        time.sleep(3)

if __name__ == '__main__':
    main()
