from __future__ import annotations

import time
import json
from typing import Any, cast
from flask import Blueprint, Response
from flask.views import MethodView

from ckan import types
import ckan.model as model
import ckan.plugins.toolkit as tk
from ckan.lib.redis import connect_to_redis, Redis
from ckanext.selfinfo.utils import get_redis_key, retrieve_additionals_redis_keys_info
import ckanext.selfinfo.config as self_config

selfinfo = Blueprint("selfinfo", __name__)


class SelfinfoView(MethodView):
    def get(self):
        try:
            context: types.Context = cast(
                types.Context,
                {
                    "model": model,
                    "user": tk.current_user.name,
                    "auth_user_obj": tk.current_user,
                },
            )

            tk.check_access("sysadmin", context)
        except tk.NotAuthorized:
            tk.abort(404)

        args = tk.request.args

        if args.get("drop_errors") and tk.asbool(args["drop_errors"]):
            redis: Redis = connect_to_redis()
            key = get_redis_key("errors")
            redis.set(key, json.dumps([]))

            return tk.redirect_to("selfinfo.index")

        data: dict[str, Any] = tk.get_action(
            self_config.selfinfo_get_main_action_name()
        )({}, {})

        profiles = {"default": data}
        additional_keys = self_config.selfinfo_get_additional_redis_keys()

        if additional_keys:
            for key in additional_keys:
                profiles[key] = retrieve_additionals_redis_keys_info(key)

        return tk.render(
            "selfinfo/index.html",
            {
                "profiles": profiles,
            },
        )


@selfinfo.route("/selfinfo/get-ram")
def selfinfo_get_ram():
    try:
        context: types.Context = cast(
            types.Context,
            {
                "model": model,
                "user": tk.current_user.name,
                "auth_user_obj": tk.current_user,
            },
        )

        tk.check_access("sysadmin", context)
    except tk.NotAuthorized:
        tk.abort(404)

    ram = tk.get_action("selfinfo_get_ram")(context, {})

    html = "<tr>"
    html += "<td>" + str(ram["precent_usage"]) + "%</td>"
    html += "<td>" + str(ram["used_ram"]) + "</td>"
    html += "<td>" + str(ram["total_ram"]) + "</td>"
    html += "<td><div class=row>"
    html += "<div class='col-lg-6'><ol start=1>"
    for process in ram["processes"][:5]:
        html += "<li>"
        html += "<span title='memory'>" + process[2] + "</span>, "
        html += "<span title='name'>" + process[1] + "</span>, "
        html += "<span title='PID'>" + str(process[0]) + "</span>"
        html += "</li>"
    html += "</div></ol>"
    html += "<div class='col-lg-6'><ol start=6>"
    for process in ram["processes"][5:]:
        html += "<li>"
        html += "<span title='memory'>" + process[2] + "</span>, "
        html += "<span title='name'>" + process[1] + "</span>, "
        html += "<span title='PID'>" + str(process[0]) + "</span>"
        html += "</li>"
    html += "</div></ol>"
    html += "</div></td>"
    html += "</tr>"
    return html


selfinfo.add_url_rule(
    self_config.selfinfo_get_path(),
    view_func=SelfinfoView.as_view("index"),
)
