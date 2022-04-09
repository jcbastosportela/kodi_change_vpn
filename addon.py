#!/usr/bin/env python
__author__ = "Joao Carlos Bastos Portela"
__copyright__ = "left"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "jcbastosportela@gmail.com"

import enum
import xbmcaddon
import xbmcgui
import xbmc
import os
import glob
from functools import partial


class SettingsIds(enum.Enum):
    FIRST_TIME = enum.auto()
    ROOT_PASS = enum.auto()
    OPENVPN_CONFS_PATH = enum.auto()
    OPENVPN_CONF_PATTERN = enum.auto()
    CHANGE_SCRIPT = enum.auto()


addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')


def _inf(msg):
    xbmc.log(f'{addonname} - {msg}' , level=xbmc.LOGINFO)


def get_configured_locations():
    """Gets a list of configured VPN locations for open VPN.

    NOTE: in my setup the servers that have already configured the autentications follows the pattern 'client.conf.[LOCATION_CODE]' 

    Returns:
        list[str]: List of location codes
    """
    OPENVPN_CONFS_PATH = addon.getSettingString(SettingsIds.OPENVPN_CONFS_PATH.name)
    OPENVPN_CONF_PATTERN = addon.getSettingString(SettingsIds.OPENVPN_CONF_PATTERN.name)
    vpn_locations = glob.glob(f'{OPENVPN_CONFS_PATH}{OPENVPN_CONF_PATTERN}*')
    vpn_locations = [l.replace(f'{OPENVPN_CONFS_PATH}{OPENVPN_CONF_PATTERN}','') for l in vpn_locations]
    return vpn_locations


def main():
    """Main
    """
    # if no valid password is set, open the settings menu
    if addon.getSettingBool(SettingsIds.FIRST_TIME.name):
        _inf('First time launch')
        addon.openSettings()
        addon.setSettingBool(SettingsIds.FIRST_TIME.name, False)

    passwd = addon.getSettingString(SettingsIds.ROOT_PASS.name)
    vpn_opts = get_configured_locations()

    change_script = addon.getSettingString(SettingsIds.CHANGE_SCRIPT.name)

    ret = xbmcgui.Dialog().select('Choose VPN location', vpn_opts)
    if ret < len(vpn_opts) and ret >= 0:
        cmd_txt = f'echo "{passwd}" | sudo -S {change_script} {vpn_opts[ret]}'
        _inf(f'Switching VPN to {vpn_opts[ret]}')
        # execute the command
        os.system(cmd_txt)


if __name__ == '__main__':
    main()