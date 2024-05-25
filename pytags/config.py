import os

home_config = '~/.pytags.cfg.py'
dir_config = 'pytags.cfg.py'
# imp.load_source('pytags.config', dir_config)
overridefiles = os.path.expanduser(home_config)
if os.path.isfile(overridefiles):
    pass
    # imp.load_source('pytags.config', overridefiles)


def show():
    print('reading config from', dir_config, ',', home_config)
    d = locals()
    for ns_name in d:
        if ns_name.startswith('ns_'):
            print(ns_name)
            ns = d.__dict__[ns_name]
            for p in ns.__dict__:
                if p.startswith('p_'):
                    print('\t', p, ns.__dict__[p])


# I added those to quiet warnings down...
ns_product = {
    "product": "",
    "p_description": "",
}
ns_db = {
    "p_host": None,
    "p_user": None,
    "p_password": None,
    "p_db": None,
}
ns_op = {
    "force": True,
    "debug": True,
    "p_sql_debug": True,
}
ns_mgr = {
    "p_suppress_warnings": False,
    "p_dir": None,
}
