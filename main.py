from telegram.ext import Updater,CommandHandler,CallbackContext
from os import listdir
import os
import sys
import time


updater = Updater(token=sys.argv[1], use_context=True)

dispatcher = updater.dispatcher

jobq = updater.job_queue

REGPATH = os.path.expanduser('~') + "/registry"

CACHEPATH = os.path.expanduser('~') + "/cache_data"

TEMPLATE = "ASN: {0[0]}\nAS Name: {0[1]}\nDescr: {0[2]}\nMNT-by: {0[3]}\nCountry: {0[4]}\nOrg: {0[5]}"

def process_file(dat):
    ret = {}
    for line in dat:
        spl = line.split(":", 1)
        if spl[0] in ret:
            ret[spl[0]].append(spl[1].lstrip())
        else:
            ret[spl[0]] = [spl[1].lstrip()]
    return ret

def get_key(dat, key):
    if key not in dat:
        return "None"
    else:
        ret = ""
        for ln in dat[key]:
            ret = ret + ln
        return ret

def send_new(context, asn):
    with open(REGPATH + '/' + asn) as asn_file:
        asn_data = asn_file.read().splitlines()
    asn_info = process_file(asn_data)
    new_arr = [get_key(asn_info, k) for k in ['aut-num','as-name','descr','mnt-by','country','org']]
    context.bot.send_message(chat_id=sys.argv[2], 
                             text=TEMPLATE.format(new_arr))

def main_task(context: CallbackContext):
    print("Starting new task...")
    asn_list = [f for f in listdir(REGPATH)]
    asn_new = []
    with open(CACHEDIR + '/asn.txt') as asn_file:
        asn_old_list = asn_file.read().splitlines()
        asn_new = list(sorted(set(asn_list) - set(asn_old_list)))
    with open(CACHEDIR + '/asn.txt', 'w') as asn_file:
        asn_file.write('\n'.join(asn_list))
    for new_asn in asn_new:
        send_new(context, new_asn)
        time.sleep(3)

def main():
    main_job = jobq.run_repeating(main_task, interval=60, first=0)
    print("Bot started.")

if __name__ == '__main__':
    main()
