{
    "name": "Custom Purchase Fields ",
    "version": "1.0",
    "category": "Purchase",
    "summary": "Custom fields for Purchase Order and Order Line",
    "depends": ["purchase", "sale", "account"],
    "data": [
        "views/purchase_order_view.xml",
        "data/sequence.xml",
    ],
    "installable": True,
    "application": False,
}