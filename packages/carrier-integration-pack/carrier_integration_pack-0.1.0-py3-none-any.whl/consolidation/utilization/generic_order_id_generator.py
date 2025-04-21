import random
from flask import g

import strgen
from app.mongo import Conn

ORDER_INI = "EZ"


def get_order_id():
    """ Order ID

    :return:
    """
    prefix = ORDER_INI
    # Provision to define order prefix for multi-tenancy
    try:
        from flask import g
        if g and g.get('tenant_details', {}) and g.get('tenant_details', {}).get('order_prefix'):
            prefix = g.get('tenant_details', {}).get('order_prefix') or ORDER_INI
    except Exception as e:
        prefix = ORDER_INI

    return generate_order_id(prefix=prefix)
    # order_id = strgen.StringGenerator("[\d]{5}").render()
    # c = Conn().final_orders.find({"order_id": order_id}).count()
    # if c > 0:
    #     order_id = strgen.StringGenerator("[\d]{7}").render()
    # return ORDER_INI + str(order_id)


def random_with_N_digits(n):
    """
    Generates random number with n digits
    """
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    rand_instc = random.Random()
    return rand_instc.randint(range_start, range_end)


def generate_order_id(n=9, prefix=ORDER_INI):
    """
    Generates a 10 digit Random Order Id
    :return:
    """
    order_id = '%s%s' % (prefix, str(random_with_N_digits(n)))
    # A Safe check to ensure we dont generate duplicate OrderIds
    order = Conn().final_orders.find_one({'order_id': order_id})
    if order is not None:
        return generate_order_id(n=n)

    return order_id


if __name__ == '__main__':
    for i in range(1000):
        print(generate_order_id(n=7))
