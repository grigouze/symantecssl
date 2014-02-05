from __future__ import print_function
from oslo.config import cfg


default_group = cfg.OptGroup(name='default', title='')

default_opts = [
    cfg.StrOpt('message', default=False, help='')
]

CONF = cfg.CONF
CONF.register_group(default_group)
CONF.register_opts(default_opts, default_group)


def main():
    CONF(default_config_files=['../etc/symantecssl/symantecssl.conf'])
    print(CONF.default.message)
    print(add(5, 2))


def add(x, y):
    return x + y


if __name__ == "__main__":
    main()
