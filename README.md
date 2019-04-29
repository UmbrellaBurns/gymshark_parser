# Gymshark parser

[gymshark](https://uk.gymshark.com) products info 

## Make virtualenv:
#### [python3.6](https://www.python.org/downloads/release/python-368/) required
    
```shell
git clone  https://github.com/UmbrellaBurns/gymshark_parser.git
cd gymshark_parser
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
    
## Usage:
* run crawler
```shell
(venv) username@pc:~/../gymshark_parser$ python gymshark/running.py
```
  
* all assets will be available in __gymshark/assets__ directory

## Assets structure
```
gymshark_parser
└── gymshark
   └── assets
       └── 123123131231312 / for instanse, productId
           ├── info.json
           ├── product1.jpg
            ...
           └── productN.jpg
```

#### info.json example
```json
{
    "id": "1731501391987",
    "url": "https://uk.gymshark.com/collections/all-products/products/gymshark-vital-seamless-leggings-black-marl",
    "name": "Gymshark Vital Seamless Leggings - Black Marl",
    "price": "40.00",
    "category": "Womens Leggings",
    "photos": [
        "https://cdn.shopify.com/s/files/1/0098/8822/files/Mens-Nav_82cbed7d-67b5-4867-80e6-b7f8d9bcbdf6_315x315.jpg?v=1556030050",
    ]
}
```