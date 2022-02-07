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

CACHEPATH = "cache"


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
    with open("templates/asn.tpl") as tpl_file:
        tpl = tpl_file.read()
    with open(REGPATH_ASN + '/' + asn) as asn_file:
        asn_data = asn_file.read().splitlines()
    asn_info = process_file(asn_data)
    new_arr = [get_key(asn_info, k).replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`") for k in ['aut-num',
                                                                                                                              'as-name', 'descr', 'mnt-by', 'country', 'org']]
    dispatcher.bot.send_message(chat_id=sys.argv[2],
                                text=tpl.format(new_arr), parse_mode='Markdown')


def send_new_inetnum(inetnum):
    with open("templates/inetnum.tpl") as tpl_file:
        tpl = tpl_file.read()
    with open(REGPATH_INETNUM + '/' + inetnum) as inetnum_file:
        inetnum_data = inetnum_file.read().splitlines()
    inetnum_info = process_file(inetnum_data)
    new_arr = [get_key(inetnum_info, k).replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`") for k in ['cidr',
                                                                                                                                  'netname', 'descr', 'mnt-by', 'country', 'org']]
    dispatcher.bot.send_message(chat_id=sys.argv[2],
                                text=tpl.format(new_arr), parse_mode='Markdown')


def send_new_inet6num(inet6num):
    with open("templates/inet6num.tpl") as tpl_file:
        tpl = tpl_file.read()
    with open(REGPATH_INET6NUM + '/' + inet6num) as inetnum_file:
        inetnum_data = inetnum_file.read().splitlines()
    inetnum_info = process_file(inetnum_data)
    new_arr = [get_key(inetnum_info, k).replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`") for k in ['cidr',
                                                                                                                                  'netname', 'descr', 'mnt-by', 'country', 'org']]
    dispatcher.bot.send_message(chat_id=sys.argv[2],
                                text=tpl.format(new_arr), parse_mode='Markdown')


def dump_new(resource_name, resource_list):
    if os.path.isfile(CACHEPATH + '/{}.txt'.format(resource_name)):
        with open(CACHEPATH + '/{}.txt'.format(resource_name)) as resource_file:
            resource_file_old_list = resource_file.read().splitlines()
            resource_new = list(
                sorted(set(resource_list) - set(resource_file_old_list)))
        if len(resource_new) != 0:
            with open(CACHEPATH + '/{}.txt'.format(resource_name), 'w') as resource_file:
                resource_file.write('\n'.join(sorted(resource_list)))
        return resource_new
    else:
        resource_new = list(
            sorted(set(resource_list)))
        with open(CACHEPATH + '/{}.txt'.format(resource_name), 'w') as resource_file:
            resource_file.write('\n'.join(sorted(resource_list)))
        return resource_new[1:5]


def main():
    print("Starting new task...")
    asn_list = [f for f in listdir(REGPATH_ASN)]
    inetnum_list = [f for f in listdir(REGPATH_INETNUM)]
    inet6num_list = [f for f in listdir(REGPATH_INET6NUM)]
    asn_new = dump_new('asn', asn_list)
    inetnum_new = dump_new('inetnum', inetnum_list)
    inet6num_new = dump_new('inet6num', inet6num_list)
    print("New ASN: {}".format(len(asn_list)))
    print("New inetnum: {}".format(len(inetnum_list)))
    print("New inet6num: {}".format(len(inet6num_list)))
    if len(asn_list) < 20:
        for new_asn in asn_new:
            try:
                send_new_asn(new_asn)
            except:
                print("Error in processing new_asn")
            time.sleep(5)
    if len(inetnum_list) < 20:
        for new_inetnum in inetnum_new:
            try:
                send_new_inetnum(new_inetnum)
            except:
                print("Error in processing new_inetnum")
            time.sleep(5)
    if len(inet6num_list) < 20:
        for new_inet6num in inet6num_new:
            try:
                send_new_inet6num(new_inet6num)
            except:
                print("Error in processing new_inet6num")
            time.sleep(5)


if __name__ == '__main__':
    main()
