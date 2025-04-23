# -*- coding: utf-8 -*-
"""Custom wrapper for collective.jsonify."""

from collective.jsonify.methods import _clean_dict
from collective.jsonify.methods import get_catalog_results  # noqa: F401
from collective.jsonify.methods import get_children  # noqa: F401
from collective.jsonify.wrapper import Wrapper
from plone.mls.core.interfaces import ILocalMLSSettings
from plone.mls.listing.browser.listing_collection import IListingCollection
from plone.mls.listing.browser.listing_search import IListingSearch
from plone.mls.listing.browser.localconfig import ILocalAgencyInfo
from plone.mls.listing.browser.recent_listings import IRecentListings
from ps.plone.mls import config
from ps.plone.mls.browser.listings.featured import IFeaturedListings
from ps.plone.mls.interfaces import IDevelopmentCollection
from ps.plone.mls.interfaces import IListingSearchBanner
from zope.annotation.interfaces import IAnnotations

import pprint
import sys
import traceback


try:
    import simplejson as json
except ImportError:
    import json

MLS_IFACE_MAPPING = {
    IDevelopmentCollection: config.SETTINGS_DEVELOPMENT_COLLECTION,
    IListingCollection: config.SETTINGS_LISTING_COLLECTION,
    IFeaturedListings: config.SETTINGS_LISTING_FEATURED,
    IRecentListings: config.SETTINGS_LISTING_RECENT,
    IListingSearch: config.SETTINGS_LISTING_SEARCH,
    IListingSearchBanner: config.SETTINGS_LISTING_SEARCH_BANNER,
    ILocalAgencyInfo: config.SETTINGS_LOCAL_AGENCY,
    ILocalMLSSettings: config.SETTINGS_LOCAL_MLS,
}


def get_item(self):
    """Get information about an item."""

    try:
        context_dict = MLSWrapper(self)
    except Exception, e:
        etype = sys.exc_info()[0]
        tb = pprint.pformat(traceback.format_tb(sys.exc_info()[2]))
        return 'ERROR: exception wrapping object: {0}: {1}\n{2}'.format(
            etype, str(e), tb,
        )

    passed = False
    while not passed:
        try:
            JSON = json.dumps(context_dict)
            passed = True
        except Exception, error:
            if 'serializable' in str(error):
                key, context_dict = _clean_dict(context_dict, error)
                pprint.pprint(
                    'Not serializable member {0} of {1} ignored'.format(
                        key, repr(self),
                    ),
                )
                passed = False
            else:
                return ('ERROR: Unknown error serializing object: {0}'.format(
                    error,
                ))
    self.REQUEST.response.setHeader('Content-type', 'application/json')
    return JSON


class MLSWrapper(Wrapper):
    """Wrapper for MLS embedding objects."""

    def __init__(self, context):
        super(MLSWrapper, self).__init__(context)
        self.get_mls_configuration()

    def get_mls_configuration(self):
        try:
            annotations = IAnnotations(self.context)
        except Exception:
            return

        self['_mls_config'] = {}

        config_items = MLS_IFACE_MAPPING.values()
        for item in config_items:
            settings = annotations.get(item, {})
            if settings:
                self['_mls_config'][item] = settings

        # get active viewlets/integrations
        active = []
        for (iface, config_key) in MLS_IFACE_MAPPING.items():
            if iface.providedBy(self.context):
                active.append(config_key)

        self['_mls_activated'] = active
