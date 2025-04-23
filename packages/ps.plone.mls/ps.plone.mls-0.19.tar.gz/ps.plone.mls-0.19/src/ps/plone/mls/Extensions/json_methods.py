# -*- coding: utf-8 -*-
"""Module with all imports used for the ExternalMethod's.

Then create external methods in ZMI for get_item, get_children,
get_catalog_results and export_content as described in the installation docs.
"""
from collective.jsonify import get_catalog_results  # noqa: F401
from collective.jsonify import get_children  # noqa: F401
from collective.jsonify.export import export_content as export_content_orig
from ps.plone.mls.browser.jsonify import get_item  # noqa: F401
from ps.plone.mls.browser.jsonify import MLSWrapper


def export_content(self):
    return export_content_orig(
        self,
        # absolute path to directory for the JSON export
        basedir='/tmp',
        # optional callback. Returns True to skip an item.
        skip_callback=lambda item: False,
        # optional list of classnames to skip
        extra_skip_classname=[],
        custom_wrapper=MLSWrapper,
        # batch_start=0,
        # batch_size=5000,
        # batch_previous_path='/absolute/path/to/last/exported/item'
    )
