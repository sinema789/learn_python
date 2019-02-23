#
# Configration model
#
# This model provides set_value() and get_value() to update SUT configuration option and get the configuation option value.
#


import ConfigParser
from ConfigParser import NoOptionError, NoSectionError
import os
from common2.lib.globals import return_code
from common2.lib.private import sparklogger

SUT_CONFIG = os.path.abspath(os.path.join(os.path.dirname(__file__), 'SUT_config.cfg'))
SUT_CONFIG_CLIENTS = r'C:\Clients\configuration\SUT_config.cfg'


class MyConfigParser(ConfigParser.ConfigParser):
    def __init__(self, defaluts=None):
        ConfigParser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


def __get_sutconfig_path():
    return SUT_CONFIG_CLIENTS if os.path.exists(SUT_CONFIG_CLIENTS) else SUT_CONFIG


def set_value(section, option, value):
    '''
    This API is used to set value of a SUT configure option.

    1. Please check the input parameter to see if it is a configure option in SUT_config.cfg file. If not, return RET_INVALID_INPUT.

    2. Write the value to the correct configure option in SUT_config.cfg file.

    3. Read the configure file again to see if the configuration option value has been set correctly. If not correct, return RET_ENV_FAIL.

    :param: section: SUT_config.cfg section

            option: config option in one config section of SUT_config.cfg

            value: config option value

    :return:RET_SUCCESS: successful to set value

            RET_INVALID_INPUT: failed to set value due to invalid input

            RET_ENV_FAIL: failed to set value

    :dependency: None

    :black box equivalent class: section and option are valid --> return value = RET_SUCCESS;

                                 section is invalid --> return value = RET_INVALID_INPUT;

                                 option is invalid --> return value = RET_INVALID_INPUT.

                                 return value  = RET_ENV_FAIL
    '''

    # Reference code
    # conf = ConfigParser.ConfigParser()
    # fp = open('SUT_config.cfg', 'w')
    # conf.write(fp)
    # conf.set(section,option,value)    # May raise exception NoSectionError. Capture it and return RET_INVALID_INPUT.
    # fp.close()
    sut_cfg = __get_sutconfig_path()

    if not section or not option or not value or not sut_cfg:
        sparklogger.error(
            r'input value error,section {0},option {1},value {2},sut_cfg {3}'.format(section, option, value, sut_cfg))
        return return_code.RET_INVALID_INPUT
    # conf = ConfigParser.ConfigParser()
    conf = MyConfigParser()
    try:
        conf.read(sut_cfg)
        if not conf.has_section(section):
            sparklogger.error(r'not have section {0}'.format(section))
            return return_code.RET_INVALID_INPUT
        conf.set(section, option, value)
        with open(sut_cfg, 'w') as f:
            conf.write(f)
        sparklogger.debug(r'set_value success end')
        return return_code.RET_SUCCESS
    except Exception:
        sparklogger.error(r'set_value raise error')
        return return_code.RET_ENV_FAIL


def get_value(section, option):
    '''
    This API is used to get the configuration options value.

    :param: section: SUT_config.cfg section

    :return: The input SUT configuration option value.

    :dependency: None

    :black box equivalent class: section and option are valid;

                                 section is invalid --> return RET_INVALID_INPUT;

                                 option is invalid --> return RET_INVALID_INPUT.
    '''

    # Reference code
    # conf = ConfigParser.ConfigParser()
    # conf.read('SUT_config.cfg')
    # value = conf.get(section,option)  # May raise NoOptionError or NoSectionError exception. Capture them and return RET_INVALID_INPUT.
    # return value
    sut_cfg = __get_sutconfig_path()

    if not section or not option or not sut_cfg:
        sparklogger.error(r'input value error,section {0},option {1},sut_cfg {2}'.format(section, option, sut_cfg))
        return return_code.RET_INVALID_INPUT
    # conf = ConfigParser.ConfigParser()
    conf = MyConfigParser()
    try:
        conf.read(sut_cfg)
        return conf.get(section, option)
    except Exception:
        sparklogger.error(r'get_value raise error')
        return return_code.RET_INVALID_INPUT


def get_platform_item(item_name):
    sparklogger.debug('item_name={0} '.format(item_name))

    platform = os.getenv('SUT.platform') if \
        os.getenv('SUT.platform') else get_value('Platform Info', 'platform')

    sparklogger.debug('platform={0}'.format(platform))
    if not platform or platform == return_code.RET_INVALID_INPUT:
        platform = 'Default'

    default_section_name = 'Platform.Default'
    section_name = 'Platform.%s' % platform

    value = get_value(section_name, item_name)
    sparklogger.debug('value={0}'.format(value))
    if value != return_code.RET_INVALID_INPUT:
        return value

    value = get_value(default_section_name, item_name)
    sparklogger.debug('value={0}'.format(value))
    return value
