# -*- coding: utf-8 -*-
import jwt
import copy
import random
import uuid
from os import environ
from json import JSONEncoder
import curlify
import datetime, time
import requests
import bcrypt
import logging
# import flask_login
import googlemaps
import pytz
from functools import wraps
from bson import ObjectId
from flask import url_for, redirect, g
from itsdangerous import URLSafeTimedSerializer, BadData
from dateutil import parser as datetime_parser
# from app import SLUGS
# from app.constants import BD_PROMOCODE, PEIPL_PROMOCODE, ADMIN_ROLE, EVERYONE, FINANCE_ROLE, DISPATCH_ROLE, TRACKING_ROLE, CALL_CENTRE_ROLE, OFFLINE_TRANSPORTERS_LIST, DEFAULT_TIMEZONE, VENDOR_NAMES
from app.constants import VENDOR_NAMES
from app.mongo import Conn
# from app.consolidation.dhl.utils import check_dhl_ras
# from app.lib.vendors.ecomexpress import _SLUG as ecom_express
# from app.lib.vendors.easypost import EasyPostConfig
# from app.lib.vendors.rivigo import RIVIGO
# from app.lib.vendors.dotzot import DOTZOT
from functools import lru_cache
# from app.lib.freshsales.freshsales import FreshSalesLogiqLabsSDK
from pytz import common_timezones

LOG = logging.getLogger(__name__)

# login_manager = flask_login.LoginManager()
# login_manager.session_protection = 'strong'
prod = ".eshipz.com"
SLEEK_TOKEN = '1715484468d4689b9395bde428bd1a403a68098db'

TRCKING_HOST = environ.get('TRCKING_HOST', 'https://track.eshipz.com')
OFFLINE_TRANSPORTERS_LIST = []
EVERYONE = 'all'
ADMIN_ROLE = 'admin'
FINANCE_ROLE = 'finance'
DISPATCH_ROLE = 'dispatch'
TRACKING_ROLE = 'tracking'
CALL_CENTRE_ROLE = 'call_centre'

# TODO: Make it DB Driven
ACTIVATED_VENDOR_LIST = [
    'fedex_india', 'fedex', 'peipl', 'aramex', 'bluedart',
    'dhl_india', 'delhivery', 'xpressbees', 'delhivery_surface', 'ecom_express', 'dtdc', 'spoton', 'proconnect', 'rivigo',
    'vittal_logistics', 'india_post', 'dtdc_offline', 'gati_kwe', 'ryblue', 'dotzot', 'gms_india', 'unique5pl',
    'growever', 'sme_express', 'transeazy', 'safexpress_offline', 'maruti_couriers', 'tciexpress_offline', 'franchexpress',
    'tpc', 'vrl_logistics', 'vrl_couriers', 'om_logistics_offline', 'vexpress', 'st_courier', 'worldfirst', 'shiprocket', 'shadowfax',
    'cinco_xpreslogistix', 'xpeed_logistics', 'tac_logistics', 'dnxlogistics', 'rblogistics', 'trustus_logistics',
    'wh_now', 'safexpress', 'criticalog', 'delhivery_b2b', 'dunzo', 'smartr_logistics', 'sahara_express', 'shipyaari',
    'anjanadri_logistics', 'newindiacarriers', 'self_delivery', 'dtdc_ltl_offline', 'trackon', 'intercity_express_logistics',
    'calogistics', 'xpressbees_new', 'metroswift', 'kerry_indev', 're_logistics', 'xpressbees_cargo', 'acpl_cargo',
    'orange_cargo', 'moveon_logistics', 'blowhorn', 'ponpurelogistics', 'lakshmicargo', 'bvc_logistics',
    'bansalcargo', 'pavitra_logistics', 'atc_logistics', 'logixfox', 'tciexpress', 'ekart', 'mexpress_cargo','fast_track_cargo','dtdc_ltl',
    'safexpress_propel', 'expeditors', 'jiffy_express', 'govel_logistics', 'spllogistics', 'smartr_logistics_kargo',
    'logicarts', 'mehta_logistics', 'penta_landmarks_xpress', 'scorpion_express', 'essential_logistics', 'stellarvaluechain',
    'smt_transport', 'slr_transport', 'sri_manjunatha_transporter', 'worldex', 'shipdelight', 'relay_express', 'dp_world_india',
    'vxpress', 'om_logistics', 'hackle', 'movin', 'baral_logistics', 'shadowfax_flash', 'naqel_express', 'paapos', 'ekart_b2b',
    'professional_couriers', 'max_pacific', 'sparsh_cargo', 'amazon_transport', 'offline'
] + OFFLINE_TRANSPORTERS_LIST

def get_ttl_hash(seconds=86400):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)


def now():
    """

    :return:
    """
    return datetime.datetime.utcnow()


class User():
    """"
    """

    @property
    def is_authenticated(self):
        return True
@lru_cache()
def create_sleek_token(user_email,user_name):


    user_data = {
        'mail': user_email,
        'name': user_name,
    }

    print("user-mail"+user_name)
    # return JSON Web Token
    return jwt.encode(user_data, SLEEK_TOKEN, algorithm='HS256')


# @login_manager.user_loader
def user_loader(email):
    """

    :param email:
    :return:
    """
    # print('user_loader' + email)
    # reg_email = Conn().customer_infofind_one({"username" : email})
    reg_email = Conn().customer_info.find_one({"email_id": email.lower().strip(), "is_active": True})
    if reg_email is not None:
        user = User()
        user.email_id = email.lower().strip()
        user.id = email.lower().strip()
        user.user_id = str(reg_email.get('_id'))
        user.user_timezone = str(reg_email.get('other_details', {}).get('default_timezone', DEFAULT_TIMEZONE)) or DEFAULT_TIMEZONE
        user.roles = reg_email.get('roles')
        user.username = str(reg_email.get('username', ''))
        user.is_embedded_view = reg_email.get('embed_code') and reg_email.get('enable_embedded_view')
        user.embed_code = reg_email.get('embed_code')
        user.brand_details = reg_email.get('brand_details') or {}
        user.other_details = reg_email.get('other_details') or {}
        user.roles = reg_email.get('roles') or [ADMIN_ROLE]
        user.tenant_details = g.tenant_details
        user.enable_advance_dashboard = asbool(reg_email.get('enable_advance_dashboard', True)) and not asbool(g.tenant_details.get('disable_ecommerce'))
        user.disable_tracking = asbool(reg_email.get('disable_tracking'))
        user.sleek_token = create_sleek_token(email.lower().strip(), str(reg_email.get('username', '')))
        # flask_login.login_user(user, remember=False, force=True)
    else:
        return
    return user


# @login_manager.request_loader
def request_loader(request):
    """

    :param request:
    :return:
    """
    user = None
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        action = request.form.get('action')
        reg_email = Conn().customer_info.find_one({"email_id": email})
        if not email:
            return
        if action == 'login' and reg_email != None:
            decrypt_pwd = reg_email.get('password')
            reg_pass = pass_encryp(pwd, passkey=decrypt_pwd, encrypt=False)
            if decrypt_pwd == reg_pass:
                user = User()
                user.id = email
                user.email_id = email.lower().strip()
                user.user_id = str(reg_email.get('_id'))
                user.username = str(reg_email.get('username', ''))
                decrypt_pwd = reg_email.get('password') if reg_email else None
                user.is_authenticated = request.form['password'] == decrypt_pwd
                user.roles = reg_email.get('roles') or [EVERYONE]
                user.tenant_details = g.tenant_details
                user.brand_details = reg_email.get('brand_details') or {}
                user.other_details = reg_email.get('other_details') or {}
                user.enable_advance_dashboard = asbool(reg_email.get('enable_advance_dashboard', True)) and not asbool(g.tenant_details.get('disable_ecommerce'))
                user.disable_tracking = asbool(reg_email.get('disable_tracking'))
                # user.is_authenticated = reg_pass == decrypt_pwd
                # flask_login.login_user(user, remember=False, force=True)
        elif action == 'register':
            return
        else:
            if reg_email:
                user = User()
                user.id = email
                user.email_id = email.lower().strip()
                user.user_id = str(reg_email.get('_id'))
                user.username = str(reg_email.get('username', ''))
                user.is_embedded_view = reg_email.get('embed_code') and reg_email.get('enable_embedded_view')
                user.embed_code = reg_email.get('embed_code')
                user.roles = reg_email.get('roles') or [EVERYONE]
                user.tenant_details = g.tenant_details
                user.brand_details = reg_email.get('brand_details') or {}
                user.other_details = reg_email.get('other_details') or {}
                user.enable_advance_dashboard = asbool(reg_email.get('enable_advance_dashboard', True)) and not asbool(g.tenant_details.get('disable_ecommerce'))
                user.disable_tracking = asbool(reg_email.get('disable_tracking'))
                # if user.is_embedded_view:
                    # flask_login.login_user(user, remember=False, force=True)
                    # from app.views import app
                    # app.config.update(
                    #     SESSION_COOKIE_SECURE=True,
                    #     SESSION_COOKIE_HTTPONLY=True,
                    #     SESSION_COOKIE_SAMESITE='None'
                    # )

    is_embedded_view = False
    embed_code = None
    # print(request.form)
    if 'embed_code' in request.args and request.args.get('embed_code'):
        embed_code = request.args.get('embed_code')
        if embed_code:
            user_info = Conn().customer_info.find_one({"embed_code": embed_code, "is_active": True})
            if user_info:
                user_id = str(user_info.get('_id'))
                is_embedded_view = True
                user = User()
                user.email_id = user_info.get('email_id').lower().strip()
                user.user_id = str(user_info.get('_id'))
                user.username = str(user_info.get('username', ''))
                user.id = user_info.get('email_id')
                # user.is_authenticated = True
                user.is_embedded_view = True
                user.embed_code = embed_code
                user.user_timezone = str(user_info.get('other_details', {}).get('default_timezone', DEFAULT_TIMEZONE)) or DEFAULT_TIMEZONE
                user.enable_advance_dashboard = asbool(user_info.get('enable_advance_dashboard', True)) and not asbool(g.tenant_details.get('disable_ecommerce'))
                user.disable_tracking = asbool(user_info.get('disable_tracking'))
                user.brand_details = user_info.get('brand_details') or {}
                user.other_details = user_info.get('other_details') or {}
                # flask_login.login_user(user, remember=False, force=True)
                # from app.views import app
                # app.config.update(
                #     SESSION_COOKIE_SECURE=True,
                #     SESSION_COOKIE_HTTPONLY=True,
                #     SESSION_COOKIE_SAMESITE='None',
                # )

    return user


# @login_manager.unauthorized_handler
def unauthorized_handler():
    """

    :return:
    """
    return redirect(url_for('login'))

USER_ROLES = [EVERYONE, ADMIN_ROLE, FINANCE_ROLE, DISPATCH_ROLE, TRACKING_ROLE, CALL_CENTRE_ROLE]


def get_current_user_role(user):
    return EVERYONE


def error_401_response():
    pass


def user_timezone_convert(date_obj, timezone):
    """
    Utility to convert date into a local timezone
    :param date_obj:
    :param timezone:
    :return:
    """
    if date_obj:
        return date_obj.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
    return date_obj


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                return error_401_response()
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def pass_encryp(form_pass, passkey=None, encrypt=True):
    """

    :param form_pass:
    :param passkey:
    :param encrypt:
    :return:
    """
    hashpass = None
    if form_pass is not None:
        if encrypt:
            hashpass = bcrypt.hashpw(form_pass.encode(
                'utf-8'), bcrypt.gensalt())  # form
        else:
            # hashpass = bcrypt.hashpw(form_pass.encode('utf-8'), passkey.encode('utf-8'))  # db
            hashpass = bcrypt.hashpw(form_pass.encode('utf-8'), passkey)  # db

    return hashpass

@lru_cache()
def timezone_list():
    """

    :return:
    """
    return common_timezones


class IST(datetime.tzinfo):
    """

    """

    def utcoffset(self, *dt):
        return datetime.timedelta(hours=5, minutes=30)

    def tzname(self, dt):
        return DEFAULT_TIMEZONE

    def dst(self, dt):
        pass


def get_ist_datetime(dt_obj, format='%Y-%m-%d %H:%M:%S', to_ist=True, is_day_first=False):
    """

    :param dt_obj:
    :return:
    """
    if isinstance(dt_obj, str):
        try:
            if not format:
                format = '%Y-%m-%d %H:%M:%S'
            dt_obj = datetime_parser.parse(dt_obj, dayfirst=is_day_first)
            # print(dt_obj)
            # dt_obj = datetime.datetime.strptime(dt_obj, format)
            if type(dt_obj) == tuple and len(dt_obj) > 0:
                dt_obj = dt_obj[0]
        except Exception as e:
            LOG.error(str(e))
            # print(dt_obj)
            print(str(e))
            pass
    if to_ist is True and isinstance(dt_obj, datetime.datetime):
        # date = dt_obj + datetime.timedelta(hours=5, minutes=30)
        ist = IST()
        tzoffset = ist.utcoffset()
        date = dt_obj + tzoffset
        return date

    return dt_obj


def get_time_milliseconds(dt_obj):
    milliseconds = int(dt_obj.timestamp() * 1000)
    return milliseconds

def piece_count_map(parcels=[]):
    """

    :param parcels:
    :return:
    """
    dims_map = {}
    for box in parcels:
        _dim = box.get('dimension', {})
        # _wt = sum([i.get('weight').get('value') for i in box.get('items')])
        lbh = '%s|%s|%s|%s' % (_dim.get('length'), _dim.get('width'), _dim.get('height'), _dim.get('unit', 'cm'))
        _parcel_count = dims_map.get(lbh) or 0
        dims_map[lbh] = _parcel_count + 1

    return dims_map


def datetimeformat(value, format='%H:%M / %d-%m-%Y', from_format='%Y-%m-%d %H:%M:%S', to_ist=True):
    """

    :param value:
    :param format:
    :return:
    """
    value = get_ist_datetime(value, from_format, to_ist=to_ist)
    return value.strftime(format) if value and type(value) in (datetime.datetime, datetime.date) else value or ''


def format_date(val, fmt='%Y-%m-%d'):
    """

    :param val:
    :param fmt:
    :return:
    """
    new_date = datetime.datetime.strptime(str(val), fmt)
    return new_date


def is_list(value):
    """

    :param value:
    :return:
    """
    return isinstance(value, list)


def vendor_cred_check(slug_data, slug, url, user_id=None, carrier_code=None):
    """ vendor_cred_check

    :param slug_data:
    :param slug:
    :param url:
    :return:
    """
    cred_check = {
        "slug": str(slug),
        "cred": slug_data,
        "carrier_code": carrier_code or slug
    }
    # if '127.0.0.1:5000' not in url:
    #     url = url.replace('http:', 'https:')

    if slug in EasyPostConfig.get_easy_post_active_carrier():
        cred_check.update(
            {
                "user_id": user_id
            }
        )
    if prod in url:
        url = url.replace('http:', 'https:')

    url = str(url + "api/v1/affirm_cred")
    headers = {'content-type': "application/json", 'cache-control': "no-cache"}
    response = requests.post(url, json=cred_check, headers=headers)
    resp = response.json()
    return resp.get('meta', {}).get('code')


GMAPS = 'AIzaSyAucH0gxld0uRYHhAU435W7zUY7e0pAN_A'

@lru_cache(100000)
def geocode_address(address_string):
    """

    :param address_string:
    :return:
    """
    # print(address_string)
    if address_string:
        gmaps = googlemaps.Client(key=GMAPS)
        geocode_results = gmaps.geocode(address_string)
        if geocode_results and len(geocode_results) > 0:
            geocode_result = geocode_results[0]
            if geocode_result:
                geocode_location = geocode_result.get('geometry', {}).get('location', {})
                if geocode_location:
                    # print(geocode_location.get('lat'), geocode_location.get('lng'))
                    return geocode_location.get('lat'), geocode_location.get('lng')
    return None, None

def sales_channels_settings_fields():
    """ sales_channels_settings_fields
          This settings translates into the HTML form inputs on channel_settings / _settings_box html
    :return:
    """
    return {
        'woocommerce': [
            {"name": "store_url", "type": "url", "label": "Store URL"},
            {"name": "consumer_key", "type": "text", "label": "Consumer Key"},
            {"name": "consumer_secret", "type": "text", "label": "Consumer Secret"},
            {"name": "version", "type": "select", "label": "Select Woocommerce Version", 'options': [
                ('', 'Select Woocommerce Version'),
                ('wc/v3', 'Wordpress(4.4 or later) Woocommerce(3.5.x or later)'),
                ('wc/v2', 'Wordpress(4.4 or later) Woocommerce(3.0.x or later)'),
                ('wc/v1', 'Wordpress(4.4 or later) Woocommerce(2.6.x or later)'),
                ('legacy_v3', 'Wordpress(4.1 or later) Woocommerce(2.4.x or later)'),
                ('legacy_v2', 'Wordpress(4.1 or later) Woocommerce(2.2.x or later)')
            ]
             },
            {"name": "status_codes", "type": "text", "label": "Status Codes"},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"},
            {"name": "status_mapper", "type": "select", "label": "Consumer Secret","types":['InfoReceived','PickedUp','InTransit','OutForDelivery','Delivered','Returned','Cancelled','Exception']}
        ],
        'magento': [
            {"name": "store_url", "type": "url", "label": "Store URL"},
            {"name": "consumer_key", "type": "text", "label": "Consumer Key"},
            {"name": "consumer_secret", "type": "text", "label": "Consumer Secret"},
            {"name": "access_token", "type": "text", "label": "Access token"},
            {"name": "access_token_secret", "type": "text",
             "label": "Access Token Secret"},
            {"name": "status_codes", "type": "text", "label": "Status Codes"},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"}
        ],
        'magento_1': [
            {"name": "store_url", "type": "url", "label": "Store URL"},
            {"name": "username", "type": "text",
             "label": "User Name (API User)"},
            {"name": "password", "type": "text",
             "label": "Password (API Key)"},
            {"name": "status_codes", "type": "text", "label": "Status Codes"},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"}
        ],
        'prestashop': [
            {"name": "store_url", "type": "url", "label": "Store URL"},
            {"name": "consumer_key", "type": "text", "label": "Consumer Key"},
            {"name": "status_codes", "type": "text", "label": "Status Codes", "info": "**In Prestashop Admin Panel Goto 'Shop Parameters -> Order Settings -> statuses' \
                and add the ID(s) you would like to fetch the orders with comma separated Ex: 1,2,3"},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"}
        ],
        'shopify': [
            {"name": "store_name", "type": "text", "label": "Store Name"},
            {"name": "api_key", "type": "text", "label": "Api Key"},
            {"name": "password", "type": "text", "label": "Password"},
            {"name": "order_id", "type": "select", "label": "Order ID Choice", 'options': [
                ('', 'Order ID Preference'),
                ('name', 'Order Name'),
                ('order_number', 'Order Number'),
            ]},
            {"name": "fulfillment_status", "type": "select", "label": "Fulfillment Status", 'options': [
                ('', 'Fulfillment Status'),
                ('shipped', 'Shipped - Show orders that have been shipped.'),
                ('partial', 'Partial - Show partially shipped orders.'),
                ('unshipped', 'Unshipped - Show orders that have not yet been shipped.'),
                ('any', 'Any - Show orders of any fulfillment status.')
            ]},
            {"name": "status", "type": "select", "label": "Filter By Order Status", 'options': [
                ('', 'Filter By Order Status'),
                ('open', 'Open - Show only open orders.'),
                ('closed', 'Closed - Show only closed orders.'),
                ('cancelled', 'Cancelled - Show only canceled orders.'),
                ('any', 'Any - Show orders of any status.')
            ]},
            {'name': 'tags', "type": "text", "label": "Tags",
             "info": "To Sync Orders of Multiple tags, Use comma separated values"},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"},
            {"name": "status_mapper", "type": "select", "label": "Consumer Secret",
             "types": ['InfoReceived', 'PickedUp', 'InTransit', 'OutForDelivery', 'Delivered', 'Returned', 'Cancelled',
                       'Exception']}
        ],
        'amazon_in': [
            # https://docs.developer.amazonservices.com/en_US/dev_guide/DG_Endpoints.html
            {"name": "seller_id", "type": "text", "label": "Seller ID"},
            {"name": "mws_auth_token", "type": "text", "label": "MWS Auth Token"},
            {"name": "marketplace_region", "type": "select", "label": "Marketplace Region", 'options': [
                ('', 'Select Marketplace'),
                ('IN', 'India'),
            ]},
            {"name": "status_codes", "type": "text", "label": "Order Status Codes",
             "info": "**PendingAvailability, Pending, Unshipped, PartiallyShipped, Shipped, InvoiceUnconfirmed, Canceled, Unfulfillable"},
            {"name": "include_easyship", "type": "checkbox", "label": "Sync Easy Ship Orders"},
            {"name": "override_orders", "type": "checkbox", "label": "Override Existing Orders"},
            {"name": "ignore_shipping_costs", "type": "checkbox", "label": "Ignore Shipping Charges"},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"}
        ],
        'amazon_sp': [
            # {"name": "client_id", "type": "text", "label": "Client ID"},
            # {"name": "client_secret", "type": "text", "label": "Client Secret"},
            # {"name": "access_token", "type": "text", "label": "Access Token"},
            # {"name": "refresh_token", "type": "text", "label": "Refresh Token"},
            # {"name": "amazon_access_key", "type": "text", "label": "Amazon Access Key"},
            # {"name": "amazon_secret_key", "type": "text", "label": "Amazon Secret Key"},
            {"name": "status_codes", "type": "text", "label": "Order Status Codes",
             "info": "**PendingAvailability, Pending, Unshipped, PartiallyShipped, Shipped, InvoiceUnconfirmed, Canceled, Unfulfillable"},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"}
        ],
        'wix': [
            {"name": "store_url", "type": "text", "label": "Store URL"},
            {"name": "app_id", "type": "text", "label": "App ID"},
            {"name": "secret_code", "type": "text", "label": "Secret Code"},
            {"name": "refresh_token", "type": "text", "label": "Refresh Token"},
            # {"name": "status", "type": "text",
            #  "label": "Order Status Codes [NOT_FULFILLED, FULFILLED, CANCELED, PARTIALLY_FULFILLED]"},
            {"name": "payment_status", "type": "select", "label": "Order Payment Status Codes", 'options': [
                ('', 'Select Payment Status'),
                ('UNSPECIFIED_PAYMENT_STATUS', 'UNSPECIFIED_PAYMENT_STATUS'),
                ('NOT_PAID', 'NOT_PAID'),
                ('PAID', 'PAID'),
                ('PARTIALLY_REFUNDED', 'PARTIALLY_REFUNDED'),
                ('FULLY_REFUNDED', 'FULLY_REFUNDED'),
                ('PENDING', 'PENDING'),
            ]},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"}
        ],
        "opencart": [
            {"name": "store_url", "type": "text", "label": "Store URL"},
            {"name": "token", "type": "text", "label": "Opencart API Token"},
            {"name": "status_codes", "type": "text", "label": "Order Status Codes"},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"}
        ],
        "ecwid": [
            {"name": "store_url", "type": "text", "label": "Store URL"},
            {"name": "store_id", "type": "text", "label": "Store ID"},
            # {"name": "client_secret", "type": "text", "label": "Client Secret"},
            # {"name": "client_key", "type": "text", "label": "Client Key"},
            {"name": "token", "type": "hidden", "label": "Token"},
            {"name": "payment_status", "type": "select", "label": "Order Payment Status Codes", 'options': [
                ('', 'Select Payment Status'),
                ('AWAITING_PAYMENT', 'AWAITING_PAYMENT'),
                ('CANCELLED', 'CANCELLED'),
                ('PAID', 'PAID'),
                ('PARTIALLY_REFUNDED', 'PARTIALLY_REFUNDED'),
                ('REFUNDED', 'REFUNDED'),
                ('INCOMPLETE', 'INCOMPLETE'),
            ]},
            {"name": "fulfillment_status", "type": "select", "label": "Order Fulfilment Status Codes", 'options': [
                ('', 'Select Fulfilment Status'),
                ('AWAITING_PROCESSING', 'AWAITING_PROCESSING'),
                ('PROCESSING', 'PROCESSING'),
                ('SHIPPED', 'SHIPPED'),
                ('DELIVERED', 'DELIVERED'),
                ('WILL_NOT_DELIVER', 'WILL_NOT_DELIVER'),
                ('RETURNED', 'RETURNED'),
                ('READY_FOR_PICKUP', 'READY_FOR_PICKUP'),
                ('OUT_FOR_DELIVERY', 'OUT_FOR_DELIVERY'),
            ]},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"}
        ],
        'storehippo': [
            {"name": "store_name", "type": "text", "label": "Store Name"},
            {"name": "token", "type": "text", "label": "Token"},
            {"name": "status", "type": "select", "label": "Filter By Order Status", 'options': [
                ('', 'Filter By Order Status'),
                ('open', 'Open - Show only open orders.'),
                ('closed', 'Closed - Show only closed orders.'),
                ('cancelled', 'Cancelled - Show only canceled orders.'),
                ('all', 'All - Show orders of all status.')
            ]},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"},
        ],
        'zoho_inventory': [
            {"name": "organization_id", "type": "text", "label": "Organization Id"},
            # {"name": "access_token", "type": "text", "label": "Access Token"},
            # {"name": "refresh_token", "type":"text", "label":"Refresh Token"},
            # {"name": "delivery_method", "type": "select", "label": "Delivery Method", 'options': [
            #     ('', 'Delivery Method'),
            #     ('prepaid', 'Prepaid'),
            #     ('cod', 'COD')
            # ]},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"},
        ],
         'salla': [
            {"name": "organization_id", "type": "text", "label": "Organization Id"},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"},
        ],
        'zoho_commerce': [
            {"name": "organization_id", "type": "text", "label": "Organization Id"},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"},
        ],
        'bigcommerce': [
            {"name": "access_token", "type": "text", "label": "Access token"},
            {"name": "api_path", "type": "text", "label": "Api Path"},
            {"name": "client_id", "type": "text", "label": "Client Id"},
            {"name": "client_name", "type": "text", "label": "Client Name"},
            {"name": "client_secret", "type": "text", "label": "Client Secret"},
            {"name": "store_name", "type": "text", "label": "Store Name"},
            {"name": "store_hash", "type": "text", "label": "Store Hash"},
            {"name": "is_active", "type": "checkbox", "label": "Active Channel"},
            {"name": "fulfillment_status", "type": "select", "label": "Order Fulfilment Status Codes", 'options': [
                ('', 'Select Fulfilment Status'),
                ("All","all"),
                ("Pending","Pending"),
                ("Awaiting Payment","Awaiting Payment"),
                ("Awaiting Fulfillment","Awaiting Fulfillment"),
                ("Awaiting Shipment","Awaiting Shipment"),
                ("Awaiting Pickup","Awaiting Pickup"),
                ("Partially Shipped","Partially Shipped"),
                ("Completed","Completed"),
                ("Shipped","Shipped"),
                ("Cancelled","Cancelled"),
                ("Declined","Declined"),
                ("Refunded","Refunded"),
                ("Disputed","Disputed"),
                ("Manual Verification Required","Manual Verification Required"),
                ("Partially Refunded","Partially Refunded")
            ]},
            {"name": "status_mapper", "type": "select", "label": "Consumer Secret",
             "types": ['InfoReceived', 'PickedUp', 'InTransit', 'OutForDelivery', 'Delivered', 'Returned', 'Cancelled',
                       'Exception']}
        ]
    }


truthy = frozenset(('t', 'true', 'y', 'yes', 'on', '1'))


def asbool(s):
    """ Return the boolean value ``True`` if the case-lowered value of string
    input ``s`` is any of ``t``, ``true``, ``y``, ``on``, or ``1``, otherwise
    return the boolean value ``False``.  If ``s`` is the value ``None``,
    return ``False``.  If ``s`` is already one of the boolean values ``True``
    or ``False``, return it."""
    if s is None:
        return False
    if isinstance(s, bool):
        return s
    s = str(s).strip()
    return s.lower() in truthy


class BaseDataTables:
    """

    """

    def __init__(self, request, columns, order_count, collection):

        self.columns = columns

        self.collection = collection

        # values specified by the datatable for filtering, sorting, paging
        self.request_values = request.values

        # results from the db
        self.result_data = None

        # total in the table after filtering
        self.cardinality_filtered = order_count

        # total in the table unfiltered
        self.cardinality = order_count

        self.run_queries()

    def output_result(self):

        output = {}

        # output['sEcho'] = str(int(self.request_values['sEcho']))
        output['iTotalRecords'] = str(self.cardinality)
        output['iTotalDisplayRecords'] = str(self.cardinality_filtered)
        aaData_rows = []

        for row in self.result_data:
            aaData_row = []
            for i in range(len(self.columns)):
                # #print row, self.columns, self.columns[i]
                aaData_row.append(str(row[self.columns[i]]))
            aaData_rows.append(aaData_row)

        output['aaData'] = aaData_rows

        return output

    def run_queries(self):

        self.result_data = self.collection
        # self.cardinality_filtered = self.order_count
        # self.cardinality = len(self.result_data)


def _flatten_address(address):
    """

    :param address:
    :return:
    """
    str_address = ''
    if address:
        str_address = '%s, %s, %s' % (
            address.get('company_name', '') or address.get('contact_name', ''),
            address.get('street1', ''), address.get('street2', '')
        )
        if address.get('street3', ''):
            str_address = '%s, %s' % (str_address, address.get('street3', ''))
        if address.get('city', ''):
            str_address = '%s, %s' % (str_address, address.get('city', ''))
        if address.get('state', ''):
            str_address = '%s, %s' % (str_address, address.get('state', ''))
        if address.get('postal_code', ''):
            str_address = '%s - %s' % (str_address, address.get('postal_code', ''))
        if address.get('country', ''):
            str_address = '%s, %s' % (str_address, address.get('country', ''))

    return str_address


def flatten_address(addr):
    """

    :param addre:
    :return:
    """
    if not addr:
        return ''
    _addr = addr.get('address')
    if not _addr or _addr is None:
        _addr = {}

    first_name = addr.get('first_name') if addr.get('first_name') is not None else addr.get('name') if addr.get('name') is not None else ''
    last_name = addr.get('last_name') if addr.get('last_name') is not None else ''
    '''
    address = ','.join(line for line in _addr if line)
    comma = ',' if address != '' and addr.get('city', '') != '' else ''
    address = '%(name)s <br>%(email)s %(phone)s<br>%(company)s %(address)s %(comma)s %(city)s %(state)s %(country)s %(postcode)s' % \
          {
              'name': '%s %s' % (first_name, last_name),
              'email': addr.get('email', '') if addr.get('email') is not None else '',
              'phone': addr.get('phone', '') if addr.get('phone') is not None else '',
              'company': addr.get('company', '') if addr.get('company') is not None else '' ,
              'address': address,
              'comma':comma,
              'city': addr.get('city', '') if addr.get('city') is not None else '',
              'state': addr.get('state', '') if addr.get('state') is not None else '',
              'country': addr.get('country', '') if addr.get('country') is not None else '',
              'postcode': addr.get('postcode', '') if addr.get('postcode') is not None else ''
          }
    # print(address)
    '''
    return '%s %s' % (first_name, last_name)


def send_password_reset_email(new_pass, receipent, name):
    """
    Method to
    :param new_pass:
    :param receipent:
    :param name:
    :return:
    """
    from app.src.eshipz_mail import MailEshipz

    # from app.views import app
    # mail = Mail(app)
    # msg = Message('Password Reset | eShipz', sender='hello@eshipz.com', reply_to='devops@ecourierz.com',
    #              recipients=[receipent])
    html = """
    <h3>Hi %s,</h3>
    <p style='font-size:14px;padding-left:20px'> We have received a request to reset your password for your eShipz Account</p>
    <p style='font-size:14px'>Your new password is <b> %s </b></p>
    """ % (name, new_pass)
    b = MailEshipz(
        receipent_email=receipent,
        data=html,
        is_html=True,
        sub="Passsword Reset",
        replay_to="support@eshipz.com"
    )
    b.send_mail()


def barcode_formatter(contents, barcode_format):
    if 'code128' == barcode_format:
        return barcode_encode128(contents)
    return barcode_format


def list_join(seq):
    ''' Join a sequence of lists into a single list, much like str.join
        will join a sequence of strings into a single string.
    '''
    return [x for sub in seq for x in sub]


code128B_mapping = dict((chr(c), [98, c + 64] if c < 32 else [c - 32]) for c in range(128))
code128C_mapping = dict([(u'%02d' % i, [i]) for i in range(100)] + [(u'%d' % i, [100, 16 + i]) for i in range(10)])
code128_chars = u''.join(chr(c) for c in [212] + list(range(33, 126 + 1)) + list(range(200, 211 + 1)))


def barcode_encode128(s):
    ''' Code 128 conversion for a font as described at
        https://en.wikipedia.org/wiki/Code_128 and downloaded
        from http://www.barcodelink.net/barcode-font.php
        Only encodes ASCII characters, does not take advantage of
        FNC4 for bytes with the upper bit set. Control characters
        are not optimized and expand to 2 characters each.
        Coded for https://stackoverflow.com/q/52710760/5987
    '''
    if s.isdigit() and len(s) >= 2:
        # use Code 128C, pairs of digits
        codes = [105] + list_join(code128C_mapping[s[i:i + 2]] for i in range(0, len(s), 2))
    else:
        # use Code 128B and shift for Code 128A
        codes = [104] + list_join(code128B_mapping[c] for c in s)
    check_digit = (codes[0] + sum(i * x for i, x in enumerate(codes))) % 103
    codes.append(check_digit)
    codes.append(106)  # stop code
    return u''.join(code128_chars[x] for x in codes)


def fetch_default_address_id(user_obj, type_wh=None):
    """ fetch_default_address_id for a user

    :param user_obj:
    :return:
    """
    if not user_obj:
        return None

    warehouse_addresses = []

    if type_wh == "pickup":
        warehouse_addresses = user_obj.get("warehouse_address", {})
    elif type_wh == "rx":
        warehouse_addresses = user_obj.get("receiver_address", {})
    elif type_wh == "rto":
        warehouse_addresses = user_obj.get("rto_address", {})

    # If there is only one Warehouse created, set that as the primary warehouse
    if len(warehouse_addresses) == 1:
        return list(warehouse_addresses.keys())[0]
    # Else, iterate to find the Primary Warehouse
    for wh_id in warehouse_addresses:
        warehouse = warehouse_addresses[wh_id]
        if 'is_primary' in warehouse and warehouse['is_primary']:
            return wh_id

    return None


def generate_activation_code(email, secret_key, salt):
    """

    :param email:
    :param app:
    :return:
    """
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=salt)


def confirm_token(token, app, expiration=3600):
    """ confirm_token

    :param token:
    :param app:
    :param expiration:
    :return:
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except BadData as sign_expired:
        LOG.error(str(sign_expired))
        raise sign_expired
    except Exception as e:
        LOG.error(str(e))
        print(str(e))
        return False
    return email


def currency_cargo_mapper():
    resp = {
        'USD': 670,
        'GBP': 480,
        'INR': 49999,
    }
    values = Conn().currency_mapper.find_one({}, {'_id': 0})
    if values:
        return values

    return resp


def fetch_shipment_awb_by_order_id(order_id):
    """

    :param order_id:
    :return:
    """
    if order_id:
        awb_details = Conn().final_orders.find_one({'order_id': order_id}, {'awb': 1})
        if awb_details:
            awb = awb_details.get('awb')
            if awb and list == type(awb):
                return awb[0]
            return awb
    return None


def fetch_default_package_settings(user_id):
    """ fetch_default_package_settings

    :param user_id:
    :return:
    """
    if user_id:
        package_settings = Conn().package_settings.find_one(
            {'user_id': user_id})
        if package_settings:
            existing_packages = package_settings.get("package_settings")

            for key, package in existing_packages.items():
                if package.get('set_default', False):
                    return package
    return {
        "name": "Custom",
        "length": "1",
        "width": "1",
        "height": "1",
        "weight": "0.0",
        "set_default": False
    }


DEFAULT_STORE_LIST = set([
    'woocommerce', 'magento', 'magento_1', 'prestashop', 'shopify', 'amazon', 'amazon_in', 'wix',
    "opencart", "ecwid", 'storehippo','zoho_inventory','bigcommerce','1mg','healthmug','flipkart','amazon_sp',"zoho_commerce"
])


def get_store_defaults(user_id):
    """

    :param user_id:
    :return:
    """
    store_defaults = [
        {
            "sort_id": "1", "user_id": user_id, "store_type": "woocommerce",
            "settings": {
                "store_url": "", "consumer_secret": "", "consumer_key": "", "status_codes": "",
                "is_active": "off", "version": "","status_mapper":{'InfoReceived':"",'PickedUp':"",'InTransit':"",'OutForDelivery':"",'Delivered':"",'Returned':"",'Cancelled':"",'Exception':""}
            }
        },
        {
            "sort_id": "2", "user_id": user_id, "store_type": "magento",
            "settings": {
                "store_url": "", "consumer_secret": "", "consumer_key": "", "access_token": "",
                "access_token_secret": "", "status_codes": "", "is_active": "off"
            }
        },
        {
            "sort_id": "3", "user_id": user_id, "store_type": "magento_1",
            "settings": {
                "store_url": "", "username": "", "password": "", "status_codes": "", "is_active": "off"
            }
        },
        {
            "sort_id": "4", "user_id": user_id, "store_type": "prestashop",
            "settings": {
                "store_url": "", "consumer_key": "", "status_codes": "", "is_active": "off"
            }
        },
        {
            "sort_id": "5", "user_id": user_id, "store_type": "shopify","store_id":str(uuid.uuid4()).replace("-", ""),
            "settings": {
                "store_name": "", "api_key": "", "password": "", "fulfillment_status": "", "status": "", "order_id": "",
                "tags": "", "is_active": "off","status_mapper":{'InfoReceived':"",'PickedUp':"",'InTransit':"",'OutForDelivery':"",'Delivered':"",'Returned':"",'Cancelled':"",'Exception':""}
            }
        },
        {
            "sort_id": "6", "user_id": user_id, "store_type": "amazon",
            "settings": {
                "store_url": "", "consumer_key": "", "status_codes": "", "is_active": "off"
            }
        },
        {
            "sort_id": "7", "user_id": user_id, "store_type": "amazon_in",
            "settings": {
                "seller_id": "", "mws_auth_token": "", "marketplace_region": "", "status_codes": "",
                "include_easyship": "off", "override_orders": "off", "ignore_shipping_costs": "off", "is_active": "off"
            }
        },
        {
            "sort_id": "8", "user_id": user_id, "store_type": "wix",
            "settings": {
                "app_id": "", "secret_code": "",
                "store_url": "","refresh_token": "", "is_active": "off", "payment_status": ""
            }
        },
        {
            "sort_id": "9", "user_id": user_id, "store_type": "ecwid",
            "settings": {
                "store_url": "", "store_id": "",
                # "client_secret": "", "client_key": "",
                "token": "",
                "payment_status": "",
                "is_active": "off", "fulfillment_status": ""
            }
        },
        {
            "sort_id": "10", "user_id": user_id, "store_type": "opencart",
            "settings": {
                "store_url": "", "token": "", "status_codes": "",
                "is_active": "off"
            }
        },
        {
            "sort_id": "11", "user_id": user_id, "store_type": "storehippo","store_id": str(uuid.uuid4()).replace("-", ""),
            "settings": {
                "store_name": "", "token": "",
                "status": "all",
                "is_active": "off"
            }
        },
        {
            "sort_id": "12", "user_id": user_id, "store_type": "zoho_inventory", "store_id": str(uuid.uuid4()).replace("-", ""),
            "settings": {
                "organization_id":"",
                "delivery_method": "", "is_active": "off"
            }
        },
        {
            "sort_id": "13", "user_id": user_id, "store_type": "bigcommerce", "store_id": str(uuid.uuid4()).replace("-", ""),
            "settings": {
                "access_token":"","api_path":"","client_id":"",
                "client_name":"","client_secret":"","store_name":"","store_hash":"","fulfillment_status": "","is_active":"",
                "status_mapper":{'InfoReceived':"",'PickedUp':"",'InTransit':"",'OutForDelivery':"",'Delivered':"",'Returned':"",'Cancelled':"",'Exception':""}
            }
        },
        {
            "sort_id": "14", "user_id": user_id, "store_type": "1mg","store_id": str(uuid.uuid4()).replace("-", ""),
            "settings": {
                "store_url": "", "consumer_key": "", "status_codes": "", "is_active": "off"
            }
        },
        {
            "sort_id": "15", "user_id": user_id, "store_type": "healthmug","store_id": str(uuid.uuid4()).replace("-", ""),
            "settings": {
                "store_url": "", "consumer_key": "", "status_codes": "", "is_active": "off"
            }
        },
        {
            "sort_id": "16", "user_id": user_id, "store_type": "flipkart","store_id": str(uuid.uuid4()).replace("-", ""),
            "settings": {
                "store_url": "", "consumer_key": "", "status_codes": "", "is_active": "off"
            }
        },
        {
            "sort_id": "17", "user_id": user_id, "store_type": "amazon_sp","store_id": str(uuid.uuid4()).replace("-", ""),
            "settings": {
                "status_codes": "", "is_active": "off"
            }
        },
        {
            "sort_id": "17", "user_id": user_id, "store_type": "zoho_commerce",
            "store_id": str(uuid.uuid4()).replace("-", ""),
            "settings": {
                "organization_id":"","is_active": "off"
            }
        }

    ]

    return store_defaults


def fetch_configured_carrier_vendors(user_id):
    """
    Returns only the current / historically configured slug list
    :param user_id:
    :return:
    """
    configured_services = Conn().vendor_info.find_one({'user_id': user_id})
    if configured_services:
        slugs = configured_services.get('accounts', {}).keys()
        if slugs:
            return sorted(list(set(slugs)))
    return []


def fetch_activated_vendors(user_id):
    """ fetch the list of activated vendors' slugs

    :param user_id:
    :return:
    """
    customer_info = Conn().customer_info.find_one({'_id': ObjectId(user_id)})
    activated_vendors = copy.deepcopy(ACTIVATED_VENDOR_LIST)
    activated_vendors.extend(EasyPostConfig.get_easy_post_active_carrier())

    # IF BD Promocode, we enable only BD
    if customer_info.get('subscription', {}).get('plan') and customer_info.get('subscription', {}).get('plan') in BD_PROMOCODE:
        activated_vendors = ['bluedart']
    elif customer_info.get('subscription', {}).get('plan') and PEIPL_PROMOCODE == customer_info.get('subscription', {}).get('plan'):
        activated_vendors = ['peipl']
    # sorted the carries according name
    try:
        from flask import g
        if g.tenant_details and g.tenant_details.get('slugs'):
            activated_vendors = g.tenant_details.get('slugs')
    except Exception as e:
        pass

    return sorted(activated_vendors)


# def check_manifest_draft(user_id):
#     manifest = Conn().manifest_orders.find_one({'user_id': user_id, "draft": True, "manifest_date":{"$exists":False}})
#     if manifest:
#         print("draft manifest id {}".format(manifest.get("_id")))
#         print(manifest.get("order_ids"))
#         return True, manifest.get("_id"), manifest.get("user_manifest_id"), manifest.get("order_ids")
#     else:
#         return False, '', '', []

def is_dhl_service_enable(user_id):
    """

    :param user_id:
    :return:
    """
    q = "accounts.{}".format('dhl_india')
    exist = Conn().vendor_info.find_one({"user_id": user_id, '$or': [
        {q: {'$exists': True}, "accounts.bluedart": {"$exists": True}}]})
    if exist:
        slugs = ['bluedart', 'dhl_india']
        for slug in slugs:
            for vendor in exist.get("accounts").get(slug):
                if exist.get("accounts").get(slug).get(vendor).get('is_enabled'):
                    return True
    return False


def is_ras_shipment(country_code, pincode, user_id, city=None):
    """

    :param country_code:
    :param pincode:
    :param user_id:
    :param city:
    :return:
    """
    if country_code:
        is_international_order = True if country_code.strip().lower() != "IN".lower().strip() else False
        if is_international_order:
            is_dhl_or_bluedart_ser_enable = is_dhl_service_enable(user_id)
            if is_dhl_or_bluedart_ser_enable:
                is_ras = check_dhl_ras(country_code, pincode, city)
                return is_ras
    return False


def update_custome_email_settings(request, user_id, email_id):
    import werkzeug.utils
    from json import dumps
    import base64

    footer_text = request.values.get('text_free')
    d = request.files['png_file']
    # update in eshipz data base
    filename = werkzeug.utils.secure_filename(d.filename)
    image_cont = d.stream.read()

    encoded_img = ''
    try:
        encoded_img = base64.b64encode(image_cont)
    except Exception as e:
        LOG.error(e)
    # print(encoded_img)
    resp = Conn().user_presets.update({'user_id': user_id}, {"$set": {
        "custom_email_logo": encoded_img,
        "custom_email_footer": footer_text
    }}, upsert=True)

    # update in tracking app
    headers = {
        'Content-Type': 'application/json',
        'password': 'password',
        'source': 'eshipz',
        'user': 'devops'}
    data = {
        "email_templ_logo": encoded_img,
        "footer_text": footer_text,
        "user_id": user_id,
        "email_id": email_id
    }
    url = 'http://{}/api/v1.0/userPersist'.format(TRCKING_HOST)
    print("USER PERSIST Eztrack url", url)
    response = requests.put(url, headers=headers, data=dumps(data, default=str))
    print("----------userPersist-------------->", response)
    # except Exception as e:
    #     LOG.error(e)


def validate_api_key(api_key):
    """

    :param api_key:
    :return:
    """
    try:
        if api_key:
            if api_key.strip() == "":
                return False, {"status": 401, "remark": "Authentication Failed"}
            else:
                exist = Conn().customer_info.find_one(
                    {"_id": ObjectId(str(api_key).strip()), "is_active": True})
                if exist:
                    return True, {"status": 200, "remark": "Authentication Success"}
                else:
                    return False, {"status": 401, "remark": "Authentication Failed"}

        return False, {"status": 401, "remark": "Authentication Failed"}
    except Exception as ex:
        return False, {"status": 401, "remark": "Authentication Failed"}


def get_paper_setting(slug, vendor_id, vendor_info):
    """

    :param slug:
    :param vendor_id:
    :param vendor_info:
    :return:
    """
    paper_size = "PAPER_4X6"
    try:
        if slug == 'fedex_india':
            return str(vendor_info.get("accounts", {}).get('fedex_india', {}).get(vendor_id, {}).get("label_setting", "PAPER_4X6")).strip()
        return paper_size
    except Exception as ex:
        print(str(ex))
        LOG.error(str(ex))
        return paper_size


def get_vendor_name_from_slug(slug):
    return VENDOR_NAMES.get(slug)


def _get_error_resp(err_msg):
    fullresp = {
        "meta": {
            "status": "error",
            "code": 400,
            "message": "The request was invalid or cannot be otherwise served.",
            "details": [err_msg]

        },
        "data": {}
    }
    return fullresp


def custom_encoder(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()


def get_state_from_pincode(pincode):
    """

    :param pincode:
    :return:
    """
    data = {
        'Andaman and Nicobar Islands': (744101, 744306),
        'Andhra Pradesh': (500001, 535594),
        'Arunachal Pradesh': (790001, 792131),
        'Assam': (781001, 788931),
        'Bihar': (800001, 855117),
        'Chhattisgarh': (490001, 497778),
        "Chandigarh": (160001, 160102),
        "dadra and nagar haveli": (396193, 396240),
        "daman and diu": (396210, 396235),
        "Delhi": (110001, 110098),
        'Goa': (403001, 403806),
        'Gujarat': (360001, 396590),
        'Haryana': (121001, 136156),
        'Himachal Pradesh': (171001, 177601),
        'Jammu and Kashmir': (180001, 194404),
        'Jharkhand': (800001, 835325),
        'Karnataka': (560001, 591349),
        'Kerala': (680001, 695615),
        'Madhya Pradesh': (450001, 488448),
        'Maharashtra': (400001, 445402),
        'Manipur': (795001, 795159),
        'Meghalaya': (793001, 794115),
        'Mizoram': (796001, 796901),
        'Nagaland': (797001, 798627),
        'Odisha': (751001, 770076),
        'Punjab': (143001, 160104),
        'Rajasthan': (302001, 345034),
        'Tamil Nadu': (600001, 643253),
        'Telangana': (500001, 509411),
        'Tripura': (799001, 799291),
        'Uttar Pradesh': (200001, 285223),
        'Uttarakhand': (248001, 263680),
        'West Bengal': (700001, 743711),
        "Ladakh": (194101, 194109),
        "Lakshadweep": (682551, 682559),
        "Puducherry": (605001, 609609),
        "Sikkim": (737101, 737139)

    }
    for state, (start, end) in data.items():
        if start <= int(pincode) <= end:
            return state.lower()

    return None  # Return None if pincode doe   sn't belong to any state


STATE_DETAILS = {
    "andaman and nicobar islands": {
        "code": "35",
        "statecode": "AN"
    },
    "andhra pradesh": {
        "code": "28",
        "statecode": "AP"
    },
    "arunachal pradesh": {
        "code": "12",
        "statecode": "AR"
    },
    "assam": {
        "code": "18",
        "statecode": "AS"
    },
    "bihar": {
        "code": "10",
        "statecode": "BR"
    },
    "chandigarh": {
        "code": "04",
        "statecode": "CH"
    },
    "chhattisgarh": {
        "code": "22",
        "statecode": "CT"
    },
    "dadra and nagar haveli": {
        "code": "26",
        "statecode": "DH"
    },
    "daman and diu": {
        "code": "26",
        "statecode": "DH"
    },
    "delhi": {
        "code": "07",
        "statecode": "DL"
    },
    "goa": {
        "code": "30",
        "statecode": "GA"
    },
    "gujarat": {
        "code": "24",
        "statecode": "GJ"
    },
    "haryana": {
        "code": "06",
        "statecode": "HR"
    },
    "himachal pradesh": {
        "code": "02",
        "statecode": "HP"
    },
    "jammu and kashmir": {
        "code": "01",
        "statecode": "JK"
    },
    "jharkhand": {
        "code": "20",
        "statecode": "JH"
    },
    "karnataka": {
        "code": "29",
        "statecode": "KA"
    },
    "kerala": {
        "code": "32",
        "statecode": "KL"
    },
    "ladakh": {
        "code": "01",
        "statecode": "LA"
    },
    "lakshadweep": {
        "code": "31",
        "statecode": "LD"
    },
    "madhya pradesh": {
        "code": "23",
        "statecode": "MP"
    },
    "maharashtra": {
        "code": "27",
        "statecode": "MH"
    },
    "manipur": {
        "code": "14",
        "statecode": "MN"
    },
    "meghalaya": {
        "code": "17",
        "statecode": "ML"
    },
    "mizoram": {
        "code": "15",
        "statecode": "MZ"
    },
    "nagaland": {
        "code": "13",
        "statecode": "NL"
    },
    "odisha": {
        "code": "21",
        "statecode": "OD"
    },
    "puducherry": {
        "code": "34",
        "statecode": "PY"
    },
    "punjab": {
        "code": "03",
        "statecode": "PB"
    },
    "rajasthan": {
        "code": "08",
        "statecode": "RJ"
    },
    "sikkim": {
        "code": "11",
        "statecode": "SK"
    },
    "tamil nadu": {
        "code": "33",
        "statecode": "TN"
    },
    "telangana": {
        "code": "36",
        "statecode": "TS"
    },
    "tripura": {
        "code": "16",
        "statecode": "TR"
    },
    "uttarakhand": {
        "code": "05",
        "statecode": "UT"
    },
    "uttar pradesh": {
        "code": "09",
        "statecode": "UP"
    },
    "west bengal": {
        "code": "19",
        "statecode": "WB"
    }
}



def get_ttl_hash(seconds=43200):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)


@lru_cache(500)
def fetch_token_map(api_key, env, ttl_hash=None):
    """
        # Usage: token, message = fetch_token_map(self.api_key, self.__env, ttl_hash=get_ttl_hash())

    :param client_uuid:
    :param client_key:
    :param app_id:
    :param device_id:
    :param env:
    :param ttl_hash:
    :return:
    """
    # url = "https://smartexpress-uat-api-appservice.azurewebsites.net/SKMobilityWS.asmx/GenerateToken"
    # Make API call to the carrirers' auth API and capture the token
    # token = <>
    #
    # return token, "Success"
    pass

    return None, '<error_message>'




if __name__ == "__main__":
    # print(barcode_formatter('3456155661'))
    print(get_ist_datetime('2021-01-03T00:00:00.000', '%Y-%m-%dT%H:%M:%S.%f'))
    # import json
    #
    # print(json.dumps(create_order(
    #     Conn, "5cdcf99c8057401bb5d93662",
    #     "bluedart",
    #     "2719349336", "Ground",
    #     "1234",
    #     "WH-VIS-530001-O17"
    # ), indent=4))
