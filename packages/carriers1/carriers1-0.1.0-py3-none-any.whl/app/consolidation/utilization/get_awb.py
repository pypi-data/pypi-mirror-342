from app.mongo import Conn
import calendar
import time
from threading import RLock, Lock

lock = RLock()

def fetch_next_pre_gen_awb(is_cod_booking, user_id, vendor_id, is_reverse, package_number_fetch=False):
    """
    Incase of Pre-generated AWB series, we load them into the Vendor
    :param vendor_info:
    :return:
    """
    # label_lock.acquire()
    # try:

    awb = None
    # if is_test_booking:
    #     return calendar.timegm(time.gmtime())
    lock.acquire()

    shipment_mode = 'prepaid'
    if is_reverse:
        shipment_mode = 'reverse'
    elif is_cod_booking:
        shipment_mode = 'cod'
    elif package_number_fetch:
        shipment_mode = 'package_numbers'

    labels = []
    try:
        main_filter = {"user_id": user_id, "vendor_id": vendor_id, 'is_active': True}
        sub_query = "pre_awbs.{}".format(shipment_mode)
        # subquery : will help only perticular shipment type aws load in memory
        # THIS WILL SAVE MEMORY USAGE IN EXTEND
        # TODO: XpressBees 100 thousands aws for each shipment so we are loading it memory everytime
        # we generate a awb, need find a logic to reduce the memory usuage.
        # Can we store the Large List of Tracking Numbers on to a diff store(EC ?) and the fetch here on demand ?

        vendor_awb_info = Conn().custom_awb.find_one(main_filter, {sub_query: 1})
        # if is_cod_booking:
        awb = None
        # print(vendor_awb_info)
        if vendor_awb_info and vendor_awb_info.get('pre_awbs', {}).get(shipment_mode):
            pre_awbs = vendor_awb_info.get('pre_awbs')
            # pre_awb = {'cod': ['13138202400000', '13138202400001', '13138202400002', '13138202400003' ..]}
            labels = pre_awbs.get(shipment_mode)

            if labels:
                awb = labels.pop()
                pre_awbs[shipment_mode] = labels

            sub_query_mdb = "pre_awbs.{}".format(shipment_mode)
            if awb:
                sub_query = {"pre_awbs.used": {"$in": [awb]}}
                sub_filter = {}
                sub_filter.update(main_filter)
                sub_filter.update(sub_query)
                counts = Conn().custom_awb.count_documents(sub_filter)
                if counts > 0:
                    Conn().custom_awb.update({"user_id": user_id, "vendor_id": vendor_id, 'is_active': True}, {
                        "$set": {
                            sub_query_mdb: pre_awbs[shipment_mode]
                        }
                    })
                    return fetch_next_pre_gen_awb(is_cod_booking, user_id, vendor_id, is_reverse, package_number_fetch)

            sub_query_mdb_used = "pre_awbs.used"
            Conn().custom_awb.update(
                {"user_id": user_id, "vendor_id": vendor_id, 'is_active': True},
                {"$push": {sub_query_mdb_used: awb}, "$set": {
                    sub_query_mdb: pre_awbs[shipment_mode]
                }}
            )
            return str(awb)

        return None
    finally:
        lock.release()

repool_lock = RLock()


def release_to_awb_pool(is_cod, is_reverse, user_id, vendor_id, awb, package_numbers_list=[]):
    """

    :param is_cod:
    :param is_reverse:
    :param user_id:
    :param vendor_id:
    :param docket_list:
    :return:
    """
    repool_lock.acquire()
    shipment_mode = 'prepaid'
    if is_reverse:
        shipment_mode = 'reverse'
    elif is_cod:
        shipment_mode = 'cod'
    if package_numbers_list and type(package_numbers_list) is list and len(package_numbers_list) > 0:
        shipment_mode = 'package_numbers'

    try:
        main_filter = {"user_id": user_id, "vendor_id": vendor_id}
        sub_query = "pre_awbs.{}".format(shipment_mode)

        # TODO: Push into respective pool & Pull from used pool of awbs

    except Exception as e:
        print(str(e))
        repool_lock.release()



if __name__ == "__main__":
    awb = fetch_next_pre_gen_awb(
        False, "5d7602492279c10009ef1281", "3759067623", True
    )
    print(awb)
