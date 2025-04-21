import datetime

from app.mongo import Conn
from itertools import zip_longest
from functools import lru_cache


def upload_serviceable_pincodes(data, user_id, vendor_id, slug):
    # filter the pincodes
    # print(data)
    # print([i for i in data if i.isdigit()])
    # print(data)
    _COD_PINCODES = []
    _PREPAID_PINCODES = []
    _REVERSE_PINCODES = []
    _OPA_PINCODES = []
    _ODA_PINCODES = []
    next(data)
    for pincodes in data:
        cod = pincodes[0] if pincodes[0] and bool(pincodes[0]) else None
        cod_code = pincodes[1] if pincodes[1] and bool(pincodes[1]) else None

        prepaid = pincodes[2] if pincodes[2] and bool(pincodes[2]) else None
        prepaid_code = pincodes[3] if pincodes[3] and bool(pincodes[3]) else None

        reverse = pincodes[4] if pincodes[4] and bool(pincodes[4]) else None
        reverse_code = pincodes[5] if pincodes[5] and bool(pincodes[5]) else None

        opa = pincodes[6] if pincodes[6] and bool(pincodes[6]) else None
        opa_code = pincodes[7] if pincodes[7] and bool(pincodes[7]) else None

        oda = pincodes[8] if pincodes[8] and bool(pincodes[8]) else None
        oda_code = pincodes[9] if pincodes[9] and bool(pincodes[9]) else None

        if cod and not cod.isspace():
            _COD_PINCODES.append({
                cod: cod_code
            })
        if prepaid and not prepaid.isspace():
            _PREPAID_PINCODES.append({
                prepaid: prepaid_code
            })
        if reverse and not reverse.isspace():
            _REVERSE_PINCODES.append({
                reverse: reverse_code
            })
        if opa and not opa.isspace():
            _OPA_PINCODES.append({
                opa: opa_code
            })
        if oda and not oda.isspace():
            _ODA_PINCODES.append({
                oda: oda_code
            })

    # print(_COD_PINCODES)
    # print(_PREPAID_PINCODES)
    # print(_REVERSE_PINCODES)

    d = Conn().pincode_settings.update({
        "user_id": user_id
    }, {
        "$set": {
            vendor_id: {
                "cod_pincode": _COD_PINCODES,
                "prepaid_pincode": _PREPAID_PINCODES,
                "reverse_pincode": _REVERSE_PINCODES,
                "opa_pincode": _OPA_PINCODES,
                "oda_pincode": _ODA_PINCODES
            }
        }
    }, True, True)  # print(d)  # print(cod)  # print(cod_code)


# @lru_cache(10000)
def fetch_pincodes(user_id, vendor_id, pincode, method):
    """

    :param user_id:
    :param vendor_id:
    :param pincode:
    :param method:
    :return:
    """
    pincode_data = None
    if pincode is not None:
        # {"user_id":"5cdead7fb144f819544cf607", "7809783104.cod_pincode":{"$elemMatch":{"12139":{"$exists":True}}}},{"7809783104.cod_pincode.$":1}
        sub_query = "{}.{}".format(vendor_id, method)
        sub_query1 = "{}.{}.$".format(vendor_id, method)
        print("fetch_pincodes--args:", sub_query, user_id, pincode, method)
        cus_query = list(Conn().customer_pin_zone.find({
            "user_id": user_id,
            "vendor_id": vendor_id,
            "isdeleted": False
        }))
        final_keys = ['cod_pincode', 'prepaid_pincode', 'reverse_pincode', 'oda_pincode', 'opa_pincode']
        sample_dict = {
            vendor_id: {}
        }
        if not cus_query:
            # {'_id': ObjectId('662a2124db0b3109fe280fe8'), '3120111629': {'prepaid_pincode': [{'110001': 'BOM'}]}}
            pincode_data = Conn().pincode_settings.find_one({
                "user_id": user_id,
                sub_query: {
                    "$elemMatch": {
                        pincode: {
                            "$exists": True
                        }
                    }
                }
            }, {
                sub_query1: 1
            })
        else:
            acode = None
            val = []
            for data in cus_query:
                # print(data)
                org_pincode = data.get("pincodes", {}).get(pincode)
                if org_pincode:
                    for k, v in org_pincode.items():
                        if v and k not in ['zone', 'validTill', 'validFrom']:
                            key = k.split('_')[1]
                            val = [pin for pin in final_keys if key in pin]
                            if k in 'area_codes':
                                acode = v
                            else:
                                if val[0] == method:
                                    sample_dict[vendor_id].update({
                                        val[0]: [{
                                                     pincode: acode
                                                 }]
                                    })

            if any(len(lst) > 0 for lst in sample_dict[vendor_id].values()):
                pincode_data = sample_dict
            else:
                pincode_data = None

    return pincode_data


def download_uploaded_pinzone(user_id, vendor_id, slug=None):
    """

    :param user_id:
    :param vendor_id:
    :param slug:
    :return:
    """
    # {'3120111629': {'cod_pincode': [{'400004': 'BLR'}, {'400002': 'BLR'}], 'prepaid_pincode': [{'110001': 'BOM'}, {'110002': 'BOM'}], 'reverse_pincode': [{'400004': 'BLY'}, {'400002': 'BLY'}], 'opa_pincode': [], 'oda_pincode': [{'117260': None}, {'117261': None}]}}
    cus_query = list(Conn().customer_pin_zone.find({
        "user_id": user_id,
        "vendor_id": vendor_id,
        "isdeleted": False
    }))
    if cus_query:
        uploaded_pincodes = {
            vendor_id: {
                'cod_pincode': [],
                'prepaid_pincode': [],
                'reverse_pincode': [],
                'opa_pincode': [],
                'oda_pincode': []
            }
        }
        acode = None
        for data in cus_query:
            if 'pincodes' in data:
                pincodes = data['pincodes']
            if pincodes:
                for pincode, pincode_info in pincodes.items():
                    acode = None
                    for k, v in pincode_info.items():
                        if v and k:
                            key_parts = k.split('_')
                            if len(key_parts) > 1:
                                key = key_parts[1]
                            else:
                                key = k
                            final_keys = uploaded_pincodes.get(vendor_id, {}).keys()
                            val = [pin for pin in final_keys if key in pin]
                            if not key in ['zone', 'validTill', 'validFrom']:
                                if k == 'area_codes':
                                    acode = v
                                else:
                                    existing_entry = next((entry for entry in uploaded_pincodes[vendor_id][val[0]] if
                                                           pincode in entry), None)
                                    if existing_entry:
                                        existing_entry[pincode] = acode
                                    else:
                                        uploaded_pincodes[vendor_id][val[0]].append({
                                            pincode: acode
                                        })
                    zone_key = pincode_info.get('zone', None)
                    if zone_key:
                        uploaded_pincodes[vendor_id].setdefault(zone_key, []).append(pincode)
    else:
        query_returns = {
            '_id': 0
        }
        if vendor_id:
            query_returns = {
                vendor_id: 1,
                '_id': 0
            }
        uploaded_pincodes = Conn().pincode_settings.find_one({
            "user_id": user_id
        }, query_returns)

    if uploaded_pincodes and vendor_id:
        csv_data = "cod_pincode,area_codes,prepaid_pincode,area_codes,reverse_pincode,area_codes,opa_pincode,area_codes,oda_pincode,area_codes"
        cod_pincode = uploaded_pincodes.get(vendor_id, {}).get('cod_pincode', [])
        prepaid_pincode = uploaded_pincodes.get(vendor_id, {}).get('prepaid_pincode', [])
        reverse_pincode = uploaded_pincodes.get(vendor_id, {}).get('reverse_pincode', [])
        opa_pincode = uploaded_pincodes.get(vendor_id, {}).get('opa_pincode', [])
        oda_pincode = uploaded_pincodes.get(vendor_id, {}).get('oda_pincode', [])

        zones = {key: uploaded_pincodes.get(vendor_id, {}).get(key, []) for key in uploaded_pincodes.get(vendor_id, {})
                 if key.startswith('zone')}
        zone_keys = sorted(zones.keys())
        zone_lists = [zones[key] for key in zone_keys]
        if not zone_keys:
            zone_keys = [f'zone{i}' for i in range(1, 6)]
        csv_header_static = "cod_pincode,area_codes,prepaid_pincode,area_codes,reverse_pincode,area_codes,opa_pincode,area_codes,oda_pincode,area_codes"
        zone_headers = ",".join(zone_keys)
        csv_data = "{},{}\n".format(csv_header_static, zone_headers)
        data = zip_longest(cod_pincode, prepaid_pincode, reverse_pincode, opa_pincode, oda_pincode, *zone_lists)

        for codes in data:
            data = ""
            cod_pin = codes[0]
            prepaid_pin = codes[1]
            reverse_pin = codes[2]
            opa_pin = codes[3]
            oda_pin = codes[4]
            zone_data = codes[5:]
            if cod_pin:
                for k, v in cod_pin.items():
                    if k:
                        v = v if v else ""
                        data += "{},{}".format(k, v)
                    else:
                        data += "{},{}".format("", "")
            else:
                data += "{},{}".format("", "")

            if prepaid_pin:
                for k, v in prepaid_pin.items():
                    if k:
                        v = v if v else ""
                        data += ",{},{}".format(k, v)
                    else:
                        data += ",{},{}".format("", "")
            else:
                data += ",{},{}".format("", "")

            if reverse_pin:
                for k, v in reverse_pin.items():
                    if k:
                        v = v if v else ""
                        data += ",{},{}".format(k, v)
                    else:
                        data += ",{},{}".format("", "")
            else:
                data += ",{},{}".format("", "")

            if opa_pin:
                for k, v in opa_pin.items():
                    if k:
                        v = v if v else ""
                        data += ",{},{}".format(k, v)
                    else:
                        data += ",{},{}".format("", "")
            else:
                data += ",{},{}".format("", "")

            if oda_pin:
                for k, v in oda_pin.items():
                    if k:
                        v = v if v else ""
                        data += ",{},{}".format(k, v)
                    else:
                        data += ",{},{}".format("", "")
            else:
                data += ",{},{}".format("", "")

            for zone in zone_data:
                if zone:
                    data += ",{}".format(zone.strip() if zone.strip() == "" else zone)
                else:
                    data += ",{}".format("")

            csv_data += data + '\n'

        return csv_data
    else:
        return 'cod_pincode,area_codes,prepaid_pincode,area_codes,reverse_pincode,area_codes,opa_pincode,area_codes,oda_pincode,area_codes,zone1,zone2,zone3,zone4,zone5'


def download_uploaded_pinzone_rate(user_id, vendor_id, slug=None):
    """

    :param user_id:
    :param vendor_id:
    :param slug:
    :return:
    """
    cus_query = Conn().customer_freight_rates.find_one({
        "user_ids": {
            '$in': [user_id]
        },
        f"rate_mapping.{vendor_id}": {
            '$exists': True
        }
    })

    csv_data = "Fromzone,Tozone,Service Type,Min weight,Base price,Volumetric Threshold,Additional/Incremental weight,Additional/Incremental price,Fuel Charges(in percentage),CAF Charges(in percentage),ODA_flat,ODA_percentage,ODA_perkg,ODA_others,COD_minimal_charges,COD_percentage,COD_Flat,2_pay_charges,Freight,AWB Fees,Freight on Value or Insurance,Peak Season Charge(in percentage)\n"

    if cus_query:
        # for vendor_data in cus_query['rate_mapping']:
        #     vendor_id = next(iter(vendor_data))  
        # for service_type, service_details in vendor_data[vendor_id].items():
        for service_type, service_details in cus_query['rate_mapping'][vendor_id].items():
            zone_keys = [key for key in service_details if 'zone' in key]

            for zone_key in zone_keys:
                zone_data = service_details[zone_key]
                from_zone, to_zone = zone_key.split('-')

                min_weight = service_details.get('minimum_weight')
                base_price = zone_data.get('base_price')
                volumetric_threshold = service_details.get('volumetric_threshold')
                additional_weight = service_details.get('incremental_slab')
                additional_price = zone_data.get('incremental_price')
                fuel_charge = service_details.get('fuel_charge') * 100
                caf_charge = service_details.get('caf_charge') * 100
                oda_flat = service_details.get('oda_charges', {}).get('oda_flat')
                oda_percentage = service_details.get('oda_charges', {}).get('oda_percentage') * 100
                oda_perkg = service_details.get('oda_charges', {}).get('oda_perkg')
                oda_others = service_details.get('oda_charges', {}).get('oda_others')
                cod_minimal_charges = service_details.get('cod_minimal_charges', 0)
                cod_flat = service_details.get('cod_flat', 0)
                cod_percentage = service_details.get('cod_percentage', 0) * 100
                two_pay_charges = service_details.get('2_pay_charges', 0)
                freight = service_details.get('freight', 0)
                awb_fees = service_details.get('awb_fees', 0)
                freight_value_or_insurance = service_details.get('freight_value_or_insurance', 0)
                peakseasoncharge = service_details.get('peakseasoncharge', 0) * 100

                row = f"{from_zone},{to_zone},{service_type},{min_weight},{base_price},{volumetric_threshold}," \
                      f"{additional_weight},{additional_price},{fuel_charge},{caf_charge}," \
                      f"{oda_flat},{oda_percentage},{oda_perkg},{oda_others},{cod_minimal_charges},{cod_percentage},{cod_flat}," \
                      f"{two_pay_charges},{freight},{awb_fees},{freight_value_or_insurance},{peakseasoncharge}\n"

                csv_data += row
        return csv_data

    else:
        return csv_data


def download_uploaded_pincodes(user_id, vendor_id, slug=None):
    """

    :param user_id:
    :param vendor_id:
    :param slug:
    :return:
    """
    query_returns = {
        '_id': 0
    }
    if vendor_id:
        query_returns = {
            vendor_id: 1,
            '_id': 0
        }
    uploaded_pincodes = Conn().pincode_settings.find_one({
        "user_id": user_id
    }, query_returns)
    if uploaded_pincodes and vendor_id:
        csv_data = "cod_pincode,area_codes,prepaid_pincode,area_codes,reverse_pincode,area_codes,opa_pincode,area_codes,oda_pincode,area_codes\n"
        cod_pincode = uploaded_pincodes.get(vendor_id, {}).get('cod_pincode', [])
        prepaid_pincode = uploaded_pincodes.get(vendor_id, {}).get('prepaid_pincode', [])
        reverse_pincode = uploaded_pincodes.get(vendor_id, {}).get('reverse_pincode', [])
        opa_pincode = uploaded_pincodes.get(vendor_id, {}).get('opa_pincode', [])
        oda_pincode = uploaded_pincodes.get(vendor_id, {}).get('oda_pincode', [])
        data = zip_longest(cod_pincode, prepaid_pincode, reverse_pincode, opa_pincode, oda_pincode)
        for codes in data:
            data = ""
            cod_pin = codes[0]
            prepaid_pin = codes[1]
            reverse_pin = codes[2]
            opa_pin = codes[3]
            oda_pin = codes[4]
            if cod_pin:
                for k, v in cod_pin.items():
                    if k:
                        v = v if v else ""
                        data += "{},{}".format(k, v)
                    else:
                        data += "{},{}".format("", "")
            else:
                data += "{},{}".format("", "")

            if prepaid_pin:
                for k, v in prepaid_pin.items():
                    if k:
                        v = v if v else ""
                        data += ",{},{}".format(k, v)
                    else:
                        data += ",{},{}".format("", "")
            else:
                data += ",{},{}".format("", "")

            if reverse_pin:
                for k, v in reverse_pin.items():
                    if k:
                        v = v if v else ""
                        data += ",{},{}".format(k, v)
                    else:
                        data += ",{},{}".format("", "")
            else:
                data += ",{},{}".format("", "")

            if opa_pin:
                for k, v in opa_pin.items():
                    if k:
                        v = v if v else ""
                        data += ",{},{}".format(k, v)
                    else:
                        data += ",{},{}".format("", "")
            else:
                data += ",{},{}".format("", "")

            if oda_pin:
                for k, v in oda_pin.items():
                    if k:
                        v = v if v else "  "
                        data += ",{},{}".format(k, v)
                    else:
                        data += ",{},{}".format("", "")
            else:
                data += ",{},{}".format("", "")

            csv_data += data + '\n'

        return csv_data
    else:
        print("Not Found any pincode")
        return 'cod_pincode,area_codes,prepaid_pincode,area_codes,reverse_pincode,area_codes,opa_pincode,area_codes,oda_pincode,area_codes'


def awb_stock_notification_download(user_id, vendor_id, action):
    """

    :param user_id:
    :param vendor_id:
    :param action:
    :return:
    """
    awb_stocks = Conn().custom_awb.find_one({
        'user_id': user_id,
        'vendor_id': vendor_id,
        'is_active': True
    }, {
        'pre_awbs': 1
    })

    if 'clear' == action:
        # TODO: We can probably drop an email with this attachment and then delete it from the DB
        Conn().custom_awb.update_one({
            'user_id': user_id,
            'vendor_id': vendor_id,
            'is_active': True
        }, {
            '$set': {
                'is_active': False,
                'deactivated_on': datetime.datetime.utcnow(),
                'deactivated_by': user_id
            }
        })

    return awb_stocks


def upload_awbs(data, user_id, vendor_id, slug):
    """

    :param data:
    :param user_id:
    :param vendor_id:
    :param slug:
    :return:
    """
    print(user_id, vendor_id, slug)
    _COD_AWBS = []
    _PREPAID_AWBS = []
    _REVERSE_AWBS = []
    # Spl case for Gati
    _PACKAGE_NUMBERS = []

    for index, awb in enumerate(data):
        # TODO: Make it smarter
        if index == 0:
            if awb != ['PREPAID', 'COD', 'REVERSE'] and awb != ['PREPAID', 'COD', 'REVERSE', 'PACKAGE_NUMBERS']:
                raise Exception("Not a valid format!")
            continue

        prepaid = awb[0] if len(awb) > 0 and awb[0] and bool(awb[0]) else None
        cod = awb[1] if len(awb) > 1 and awb[1] and bool(awb[1]) else None
        reverse = awb[2] if len(awb) > 2 and awb[2] and bool(awb[2]) else None

        package_numbers = None
        if awb and len(awb) > 3:
            package_numbers = awb[3] if awb[3] and bool(awb[3]) else None

        if cod and not cod.isspace():
            _COD_AWBS.append(cod.strip())
        if prepaid and not prepaid.isspace():
            _PREPAID_AWBS.append(prepaid.strip())
        if reverse and not reverse.isspace():
            _REVERSE_AWBS.append(reverse.strip())
        if package_numbers and not package_numbers.isspace():
            _PACKAGE_NUMBERS.append(package_numbers.strip())

    # print(_COD_AWBS)
    # print(_PREPAID_AWBS)
    # print(_REVERSE_AWBS)

    f = Conn().custom_awb.update({
        "user_id": user_id,
        "vendor_id": vendor_id,
        'is_active': True
    }, {
        "$set": {
            "pre_awbs.cod": _COD_AWBS,
            "pre_awbs.prepaid": _PREPAID_AWBS,
            "pre_awbs.reverse": _REVERSE_AWBS,
            "pre_awbs.package_numbers": _PACKAGE_NUMBERS,
            'updated_on': datetime.datetime.utcnow(),
            'updated_by': user_id
        },
    }, upsert=True)
    print(f)


if __name__ == "__main__":
    user_id = "5d1c32767e233b75d000eae9"
    vendor_id = "4678692087"
    slug = "fedex_india"
    download_uploaded_pincodes(user_id, vendor_id)

#     # d = fetch_pincodes(
#     #     "5cdead7fb144f819544cf607",
#     #     "7809783104",
#     #     "1213",
#     #     "cod_pincode"
#     # )
#     # print(d)
# #     slug = 'fedex_india'
# #     user_id = '5cebc9d47a621400091ab864'
# #     vendor_id = '4173012248'
# #     import csv
# #     with open('/home/mock/COM/pincodes_upload.csv','rt')as f:
# #         data = csv.reader(f)
# #         upload_serviceable_pincodes(data, user_id, vendor_id, slug)
