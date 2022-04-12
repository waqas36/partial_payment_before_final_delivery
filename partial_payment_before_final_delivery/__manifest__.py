{
    # App information
    'name': 'Partial Payment Before First Delivery',
    'category': 'sales',
    'summary': 'Partial Payment Before First Delivery',
    'version': '14.1.1.0.1',
    'depends': [
        'base','sale','delivery','stock'
    ],

    'data': [
        'data/mail_template.xml',
        'views/payment_term_view.xml',
        'views/res_config_settings.xml',
    ],

    'images': [
        'static/description/thumbnail.png',
    ],

    # Author
    'author': 'Index World',
    'website': 'https://indexworld.net/',
    'maintainer': 'Index World',

    # Technical
    'price': 30.00,
    'currency': 'USD',
    'installable': True,
    'auto_install': False,

}
