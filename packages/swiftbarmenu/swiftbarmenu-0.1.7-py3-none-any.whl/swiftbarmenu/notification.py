from __future__ import annotations

import os
from os.path import basename
import sys
from urllib.parse import urlencode, quote


class Notification:
    def __init__(self, title: str, subtitle=None, body=None, href=None):
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.href = href

    def show(self, silent=False) -> Notification:
        plugin_path = os.getenv("SWIFTBAR_PLUGIN_PATH", sys.argv[0])
        plugin_name = basename(plugin_path)

        payload = {
            "plugin":   plugin_name,     # required
            "title":    self.title,      # required
            "subtitle": self.subtitle,
            "body":     self.body,
            "href":     self.href,
            "silent":   "true" if silent else None
        }

        notification_payload = dict(
            filter(lambda item: item[1] is not None, payload.items())
        )

        # Format parameters for query
        query = urlencode(notification_payload, quote_via=quote)

        # Trigger notification through SwiftBar
        os.system("open -g 'swiftbar://notify?%s'" % query)

        return self

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Notification(title='{self.title}', subtitle='{self.subtitle}', body='{self.body}', href='{self.href}')"
