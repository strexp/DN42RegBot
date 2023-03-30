from utils.registry_reader import process_reg, get_key


def replace_keywords(dat):
    dat = dat.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
    if '\n' in dat:
        dat = '\n' + dat
    return dat


def parse_template(tpl_name, tpl_data, tpl_keys):
    with open(f"templates/{tpl_name}.tpl") as tpl_file:
        tpl = tpl_file.read()
    tpl_info = process_reg(tpl_data)
    return tpl.format([replace_keywords(get_key(tpl_info, k)) for k in tpl_keys])
