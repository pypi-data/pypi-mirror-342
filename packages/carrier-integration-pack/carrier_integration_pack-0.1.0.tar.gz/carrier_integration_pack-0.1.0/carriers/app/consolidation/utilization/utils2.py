def get_total_weight(parcel_info):
    return sum([float(parcel.get("weight", {}).get("value", 0.0) or 0.0) * (int(parcel.get("quantity", 1)) or 1) for parcel in parcel_info])


def get_total_value(parcel_info):
    return sum([float(item.get("price", {}).get("amount", 0.0) or 0.0) * (int(item.get("quantity", 1)) or 1) for parcel in parcel_info for item in parcel.get("items", [])])


def get_order_currency(parcel_info):
    currency = "INR"
    for parcel in parcel_info:
        if parcel.get("items", []):
            currency = parcel.get("items")[0].get("price", {}).get("currency")
            break
    return currency
