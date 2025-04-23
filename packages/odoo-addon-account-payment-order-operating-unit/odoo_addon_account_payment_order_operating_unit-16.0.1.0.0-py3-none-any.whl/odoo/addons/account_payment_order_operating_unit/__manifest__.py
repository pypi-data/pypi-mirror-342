{
    'name': "account_payment_order_operating_unit",

    'summary': """
        Configuration to properly relate payment orders and operating units
    """,

    'author': "Coopdevs Treball SCCL",
    'website': "https://git.coopdevs.org/coopdevs/odoo/odoo-addons/enhancements-operating-unit",

    'category': 'Operating units',
    'version': "16.0.1.0.0",

    'depends': [
        'base',
        'account_payment_order',
        'operating_unit',
        'account_operating_unit',
        'account_banking_sepa_direct_debit'
    ],

    # always loaded
    'data': [
        #         'security/ir.model.access.csv',
        'views/account_payment_line.xml',
    ]
}
