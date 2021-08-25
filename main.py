from telegram.ext import Updater, CommandHandler, CallbackContext
from os import listdir
import os
import sys
import time


updater = Updater(token=sys.argv[1], use_context=True)

dispatcher = updater.dispatcher

REGPATH = os.path.expanduser('~') + "/registry/data"

REGPATH_ASN = REGPATH + "/aut-num"

REGPATH_INETNUM = REGPATH + "/inetnum"

REGPATH_INET6NUM = REGPATH + "/inet6num"

CACHEPATH = os.path.expanduser('~') + "/cache_data"

TEMPLATE = "ASN: {0[0]}\nAS Name: {0[1]}\nDescr: {0[2]}\nMNT-by: {0[3]}\nCountry: {0[4]}\nOrg: {0[5]}"


def process_file(dat):
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
            ret = ret + ln
        return ret


def send_new_asn(asn):
    with open(REGPATH_ASN + '/' + asn) as asn_file:
        asn_data = asn_file.read().splitlines()
    asn_info = process_file(asn_data)
    new_arr = [get_key(asn_info, k) for k in ['aut-num',
                                              'as-name', 'descr', 'mnt-by', 'country', 'org']]
    dispatcher.bot.send_message(chat_id=sys.argv[2],
                                text=TEMPLATE.format(new_arr))


def dump_new(resource_name, resource_list):
    if os.path.isfile(CACHEPATH + '/{}.txt'.format(resource_name)):
        with open(CACHEPATH + '/{}.txt'.format(resource_name)) as resource_file:
            resource_file_old_list = resource_file.read().splitlines()
            resource_new = list(
                sorted(set(resource_list) - set(resource_file_old_list)))
    else:
        resource_new = list(
            sorted(set(resource_list))
    with open(CACHEPATH + '/{}.txt'.format(resource_name), 'w') as resource_file:
        resource_file.write('\n'.join(resource_list))
    return resource_new

def main():
    print("Starting new task...")
    asn_list=[f for f in listdir(REGPATH_ASN)]
    inetnum_list=[f for f in listdir(REGPATH_INETNUM)]
    inet6num_list=[f for f in listdir(REGPATH_INET6NUM)]
    asn_new=dump_new('asn', asn_list)
    inetnum_new=dump_new('inetnum', inetnum_list)
    inet6num_new=dump_new('inet6num', inet6num_list)
    for new_asn in asn_new:
        send_new_asn(new_asn)
        time.sleep(3)


if __name__ == '__main__':
    main()
