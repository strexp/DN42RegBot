from telegram.ext import ApplicationBuilder
from os import listdir
import os
import sys
import time
import dotenv
import asyncio

from utils.tpl_parser import parse_template

dotenv.load_dotenv()

bot = ApplicationBuilder().token(os.getenv("BOTTOKEN")).build()

REGPATH = os.path.expanduser('~') + "/registry/data"

if os.getenv("REGPATH"):
    REGPATH = os.getenv("REGPATH")

CACHEPATH = "cache"

TARGET_CHAT = os.getenv("TARGET_CHAT")


def send_updates(u):
    asyncio.run(bot.bot.sendMessage(chat_id=TARGET_CHAT,
                                    text=u, parse_mode='Markdown'))


def send_new_asn(asn):
    with open(REGPATH + '/aut-num/' + asn) as asn_file:
        asn_data = asn_file.read().splitlines()
    new_arr = parse_template('asn', asn_data, ['aut-num',
                                               'as-name', 'descr', 'mnt-by', 'country', 'org'])
    send_updates(new_arr)


def send_new_inetnum(inetnum):
    with open(REGPATH + '/inetnum/' + inetnum) as inetnum_file:
        inetnum_data = inetnum_file.read().splitlines()
    new_arr = parse_template('inetnum', inetnum_data, ['cidr',
                                                       'netname', 'descr', 'mnt-by', 'country', 'org'])
    send_updates(new_arr)


def send_new_inet6num(inet6num):
    with open(REGPATH + '/inet6num/' + inet6num) as inetnum_file:
        inet6num_data = inetnum_file.read().splitlines()
    new_arr = parse_template('inet6num', inet6num_data, ['cidr',
                                                         'netname', 'descr', 'mnt-by', 'country', 'org'])
    send_updates(new_arr)


def send_new_dns(dns):
    with open(REGPATH + '/dns/' + dns) as dns_file:
        dns_data = dns_file.read().splitlines()
    new_arr = parse_template('dns', dns_data, ['domain',
                                               'descr', 'mnt-by', 'nserver'])
    send_updates(new_arr)


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

def checksize(d):
    if len(d) > 20:
        print("Too much update, assume error recovering...")
        exit(0)

def main():
    print("Starting new task...")
    asn_list = [f for f in listdir(REGPATH + '/aut-num')]
    inetnum_list = [f for f in listdir(REGPATH + '/inetnum')]
    inet6num_list = [f for f in listdir(REGPATH + '/inet6num')]
    dns_list = [f for f in listdir(REGPATH + '/dns')]
    asn_new = dump_new('asn', asn_list)
    inetnum_new = dump_new('inetnum', inetnum_list)
    inet6num_new = dump_new('inet6num', inet6num_list)
    dns_new = dump_new('dns', dns_list)
    print("New ASN: {}".format(len(asn_new)))
    print("New inetnum: {}".format(len(inetnum_new)))
    print("New inet6num: {}".format(len(inet6num_new)))
    print("New dns: {}".format(len(dns_new)))
    checksize(asn_new)
    checksize(inetnum_new)
    checksize(inet6num_new)
    checksize(dns_new)
    for new_asn in asn_new:
        try:
            send_new_asn(new_asn)
        except Exception as e:
            print(e)
            print("Error in processing new_asn")
        time.sleep(5)
    for new_inetnum in inetnum_new:
        try:
            send_new_inetnum(new_inetnum)
        except Exception as e:
            print(e)
            print("Error in processing new_inetnum")
        time.sleep(5)
    for new_inet6num in inet6num_new:
        try:
            send_new_inet6num(new_inet6num)
        except Exception as e:
            print(e)
            print("Error in processing new_inet6num")
        time.sleep(5)
    for new_dns in dns_new:
        try:
            send_new_dns(new_dns)
        except Exception as e:
            print(e)
            print("Error in processing new_dns")
        time.sleep(5)

if __name__ == '__main__':
    main()
