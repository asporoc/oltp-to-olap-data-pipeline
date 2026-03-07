import random
class Payment:

    PAYMENT_METHODS = ["credit_card", "paypal", "apple_pay", "bank_transfer"]

    ORDER_PAYMENT_MAP = {
        "pending": "pending",
        "paid": "completed",
        "shipped": "completed",
        "delivered": "completed",
        "returned": "refunded",
        "cancelled": "failed"
    }

    @classmethod
    def generate(cls, order_id, order_status, order_total_amount):

        payment_method = random.choice(cls.PAYMENT_METHODS)
        payment_status = cls.ORDER_PAYMENT_MAP[order_status]

        return {
            "order_id": order_id,
            "payment_method": payment_method,
            "payment_status": payment_status,
            "amount": order_total_amount
        }