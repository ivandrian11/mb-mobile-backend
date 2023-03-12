import calendar
import time
import midtransclient


def generate_order_id():
    # Current GMT time in a tuple format
    current_GMT = time.gmtime()
    ts = calendar.timegm(current_GMT)

    # order
    return "ORDER-" + str(ts)


def create_transaction(user, course, total):
    order_id = generate_order_id()

    item_details = []
    # detail data course
    item_details.append({
        'price': total,
        'quantity': 1,
        'name': course.name
    })

    # detail data customer
    customer_details = {
        'first_name': user.name,
        'email': user.email
    }

    # Membuat instance Snap API
    snap = midtransclient.Snap(
        is_production=False,
        server_key='SB-Mid-server-eFH-eBgk0_KQUwygu9d_cxi5',
        client_key='SB-Mid-client-b6qZcZgvB8Hcazsr'
    )
    # Menyiapkan API parameter
    param = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": total,
        },
        "item_details": item_details,
        "customer_details": customer_details
    }
    # Memanggil API midtrans untuk membuat transaksi
    transaction = snap.create_transaction(param)

    data = {}
    data["id"] = order_id
    data["url"] = transaction['redirect_url']

    return data
