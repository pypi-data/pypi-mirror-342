def blitz_payload_mapping(shipment_info):
    

    payload_map = {
        "channelId": 'order_source',
        "returnShipmentFlag": 'is_reverse',
        "code": 'customer_reference',
        "orderCode": 'customer_reference',
        "weight": 'total_weight',  
        "length": 'box_length',  
        "height": 'box_height',   
        "breadth": 'box_width',  
        "items": 'item_details',

        "delivery_name": 'ship_to.contact_name',
        "delivery_phone": 'ship_to.phone',
        "delivery_address1": 'ship_to.street1',
        "delivery_address2": 'ship_to.street2', 
        "delivery_pincode": 'ship_to.postal_code',
        "delivery_city": 'ship_to.city',
        "delivery_state": 'ship_to.state',
        "delivery_country": 'ship_to.country',
        "delivery_lat": 'drop_coordinates.lat',
        "delivery_lng": 'drop_coordinates.lng',

        "pickup_name": 'ship_from.contact_name',
        "pickup_phone": 'ship_from.phone',
        "pickup_address1": 'ship_to.street1',
        "pickup_address2": 'ship_to.street1',
        "pickup_pincode": 'ship_to.postal_code',
        "pickup_city": 'ship_from.city',
        "pickup_state": 'ship_from.state',
        "pickup_country": 'ship_from.country',
        "pickup_lat": 'pickup_coordinates.lat',
        "pickup_lng": 'pickup_coordinates.lat',

        "currencyCode": 'cod_currency',
        "paymentMode": 'is_cod',
        "totalAmount": 'total_inv_val',
        "collectableAmount": 'collect_on_delivery',
    }
    mapped_payload = {}

    for key, value in payload_map.items() :
        mapped_payload[key] = shipment_info.get(value)

    return mapped_payload

def blitz_response_mapping(response) :
    response_map =  {
        'awb' : 'docket_number',
        'label' : 'shipping_label'
    }
    #for ....
    return response_map

    
