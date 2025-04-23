# -*- coding: utf-8 -*-
"""Configuration options for the Propertyshelf MLS Plone Embedding."""

from plone.mls.core.browser import localconfig as localconfig_core
from plone.mls.listing.browser import listing_collection
from plone.mls.listing.browser import listing_search
from plone.mls.listing.browser import localconfig
from plone.mls.listing.browser import recent_listings


PROFILE_ID = u'profile-ps.plone.mls'
INSTALL_PROFILE = '{0}:default'.format(PROFILE_ID)
UNINSTALL_PROFILE = '{0}:uninstall'.format(PROFILE_ID)
PROJECT_NAME = 'ps.plone.mls'

#: Configuration key for development collection settings.
SETTINGS_DEVELOPMENT_COLLECTION = 'ps.plone.mls.developmentcollection'

#: Configuration key for featured listings settings.
SETTINGS_LISTING_FEATURED = 'ps.plone.mls.listing.featuredlistings'

#: Configuration key for listing search banner settings.
SETTINGS_LISTING_SEARCH_BANNER = 'ps.plone.mls.listingsearchbanner'

SETTINGS_LOCAL_AGENCY = localconfig.CONFIGURATION_KEY
SETTINGS_LOCAL_MLS = localconfig_core.CONFIGURATION_KEY
SETTINGS_LISTING_COLLECTION = listing_collection.CONFIGURATION_KEY
SETTINGS_LISTING_RECENT = recent_listings.CONFIGURATION_KEY
SETTINGS_LISTING_SEARCH = listing_search.CONFIGURATION_KEY
