from __future__ import annotations

from typing import Any


from ckan import types
import ckan.plugins.toolkit as tk
import ckan.plugins as p

import ckanext.selfinfo.utils as selfutils
from ckanext.selfinfo.interfaces import ISelfinfo
import ckanext.selfinfo.config as self_config


@tk.side_effect_free
def get_selfinfo(
    context: types.Context,
    data_dict: dict[str, Any],
) -> dict[str, Any]:

    tk.check_access("sysadmin", context, data_dict)

    categories = self_config.selfinfo_get_categories()

    data = {
        "python_modules": selfutils.get_python_modules_info,
        "platform_info": selfutils.get_platform_info,
        "ram_usage": selfutils.get_ram_usage,
        "disk_usage": selfutils.get_disk_usage,
        "git_info": selfutils.gather_git_info,
        "freeze": selfutils.get_freeze,
        "errors": selfutils.retrieve_errors,
        "actions": selfutils.ckan_actions,
        "auth_actions": selfutils.ckan_auth_actions,
        "blueprints": selfutils.ckan_bluprints,
        "helpers": selfutils.ckan_helpers,
        "status_show": selfutils.get_status_show,
    }

    data = {
        key: func() for key, func in data.items() if not categories or key in categories
    }

    # data modification
    for item in p.PluginImplementations(ISelfinfo):
        item.selfinfo_after_prepared(data)

    return data


def selfinfo_get_ram(
    context: types.Context,
    data_dict: dict[str, Any],
) -> dict[str, Any]:

    tk.check_access("sysadmin", context, data_dict)

    return selfutils.get_ram_usage()
