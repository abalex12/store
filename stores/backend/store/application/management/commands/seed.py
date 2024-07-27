from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from application.models import Profile, Category, Brand, Product, Purchase, Sale,Brands_list
import random

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        # brands = self.create_categories_and_brands()
        self.create_products()
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))

    # def create_categories_and_brands(self):
    #     # Define categories and their respective brands
    #     categories_brands = {
    #         'Phone': ['Apple', 'Samsung', 'OnePlus', 'Nokia', 'Sony'],
    #         'Laptop': ['Dell', 'HP', 'Apple', 'Lenovo', 'Asus'],
    #         'Headphone': ['Bose', 'Sony', 'Sennheiser', 'JBL', 'Beats'],
    #         'Tablet': ['Apple', 'Samsung', 'Lenovo', 'Microsoft', 'Amazon'],
    #         'Earphone': ['Apple', 'Samsung', 'JBL', 'Sony', 'OnePlus'],
    #         'Smartwatch': ['Apple', 'Samsung', 'Garmin', 'Fitbit', 'Huawei'],
    #         'Camera': ['Canon', 'Nikon', 'Sony', 'Fujifilm', 'Panasonic'],
    #         'Printer': ['HP', 'Canon', 'Epson', 'Brother', 'Samsung'],
    #         'Monitor': ['Dell', 'HP', 'Samsung', 'LG', 'Acer'],
    #         'Smart TV': ['Samsung', 'LG', 'Sony', 'Vizio', 'TCL'],
    #         'Gaming Console': ['Sony', 'Microsoft', 'Nintendo', 'Sega', 'Atari'],
    #         'Router': ['TP-Link', 'Netgear', 'Asus', 'Linksys', 'D-Link'],
    #         'Smart Speaker': ['Amazon', 'Google', 'Apple', 'Sonos', 'Bose'],
    #         'Drone': ['DJI', 'Parrot', 'Yuneec', 'Autel Robotics', 'Skydio'],
    #         'External Hard Drive': ['Seagate', 'Western Digital', 'Toshiba', 'Samsung', 'LaCie'],
    #         'Projector': ['Epson', 'BenQ', 'Optoma', 'ViewSonic', 'Sony'],
    #         'Fitness Tracker': ['Fitbit', 'Garmin', 'Xiaomi', 'Samsung', 'Huawei'],
    #         'VR Headset': ['Oculus', 'HTC', 'Sony', 'Samsung', 'Valve'],
    #         'Home Security Camera': ['Ring', 'Nest', 'Arlo', 'Blink', 'Wyze'],
    #         'Bluetooth Speaker': ['JBL', 'Bose', 'Sony', 'Ultimate Ears', 'Marshall']
    #     }

    #     # Create categories and brands
    #     brands = []
    #     brands_lists = []
    #     for category_name, brand_names in categories_brands.items():
    #         category, created = Category.objects.get_or_create(category_name=category_name)
    #         for brand_name in brand_names:
    #             brands_list, created =Brands_list.objects.get_or_create(brand_name=brand_name)
    #             brands_lists.append(brands_list)
    #             brand, created = Brand.objects.get_or_create(brand_name=brands_list, category=category)
    #             brands.append(brand)
                
    #             self.stdout.write(self.style.SUCCESS(f'In category {category_name},{brand_name} is created .'))

    #     return brands

    def create_products(self):
        # Define specific models for each brand
        products = {
            'Phone': {
                'Apple': ['iPhone 12', 'iPhone 13', 'iPhone SE'],
                'Samsung': ['Galaxy S21', 'Galaxy Note 20', 'Galaxy A52'],
                'OnePlus': ['OnePlus 9', 'OnePlus 8T', 'OnePlus Nord'],
                'Nokia': ['Nokia 8.3', 'Nokia 5.4', 'Nokia 3.4'],
                'Sony': ['Xperia 1', 'Xperia 5', 'Xperia 10']
            },
            'Laptop': {
                'Dell': ['XPS 13', 'Inspiron 15', 'Latitude 14'],
                'HP': ['Spectre x360', 'Pavilion 15', 'Envy 13'],
                'Apple': ['MacBook Air', 'MacBook Pro 13', 'MacBook Pro 16'],
                'Lenovo': ['ThinkPad X1', 'Yoga 7i', 'IdeaPad 3'],
                'Asus': ['ZenBook 14', 'ROG Zephyrus G14', 'VivoBook 15']
            },
            'Headphone': {
                'Bose': ['QuietComfort 35', '700', 'SoundSport'],
                'Sony': ['WH-1000XM4', 'WH-1000XM3', 'WF-1000XM3'],
                'Sennheiser': ['HD 450BT', 'Momentum 3', 'CX 400BT'],
                'JBL': ['Live 650BTNC', 'Tune 750BTNC', 'Quantum 800'],
                'Beats': ['Solo Pro', 'Powerbeats Pro', 'Studio3']
            },
            'Tablet': {
                'Apple': ['iPad Pro', 'iPad Air', 'iPad Mini'],
                'Samsung': ['Galaxy Tab S7', 'Galaxy Tab A7', 'Galaxy Tab S6 Lite'],
                'Lenovo': ['Tab P11', 'Tab M10', 'Yoga Smart Tab'],
                'Microsoft': ['Surface Pro 7', 'Surface Go 2', 'Surface Pro X'],
                'Amazon': ['Fire HD 10', 'Fire HD 8', 'Fire 7']
            },
            'Earphone': {
                'Apple': ['AirPods Pro', 'AirPods', 'BeatsX'],
                'Samsung': ['Galaxy Buds Pro', 'Galaxy Buds Live', 'Galaxy Buds+'],
                'JBL': ['Free X', 'Reflect Flow', 'Endurance Peak'],
                'Sony': ['WF-1000XM3', 'WF-SP800N', 'WF-XB700'],
                'OnePlus': ['Buds Z', 'Buds', 'Buds Pro']
            },
            'Smartwatch': {
                'Apple': ['Apple Watch Series 6', 'Apple Watch SE', 'Apple Watch Series 3'],
                'Samsung': ['Galaxy Watch 3', 'Galaxy Watch Active 2', 'Galaxy Fit2'],
                'Garmin': ['Forerunner 945', 'Fenix 6', 'Venu Sq'],
                'Fitbit': ['Versa 3', 'Charge 4', 'Inspire 2'],
                'Huawei': ['Watch GT 2', 'Watch Fit', 'Band 4 Pro']
            },
            'Camera': {
                'Canon': ['EOS R5', 'EOS 90D', 'PowerShot G7X'],
                'Nikon': ['Z6 II', 'D850', 'Coolpix P1000'],
                'Sony': ['Alpha 7C', 'Alpha 7 III', 'Cyber-shot RX100'],
                'Fujifilm': ['X-T4', 'X-S10', 'X100V'],
                'Panasonic': ['Lumix GH5', 'Lumix G95', 'Lumix S1']
            },
            'Printer': {
                'HP': ['OfficeJet Pro 9015', 'LaserJet Pro M404dw', 'Envy 6055'],
                'Canon': ['PIXMA TR8520', 'imageCLASS MF644Cdw', 'PIXMA G6020'],
                'Epson': ['EcoTank ET-2760', 'WorkForce WF-2830', 'Expression Home XP-4100'],
                'Brother': ['HL-L2350DW', 'MFC-L2750DW', 'DCP-L2550DW'],
                'Samsung': ['Xpress M2020W', 'ProXpress SL-M3320ND', 'Xpress SL-M2070FW']
            },
            'Monitor': {
                'Dell': ['UltraSharp U2720Q', 'P2720D', 'S2721QS'],
                'HP': ['Omen 27i', 'Pavilion 27', 'EliteDisplay E243'],
                'Samsung': ['Odyssey G7', 'UR59C', 'SR650'],
                'LG': ['UltraFine 5K', '27UK850-W', '34WN80C-B'],
                'Acer': ['Predator X34', 'Nitro XV273K', 'R240HY']
            },
            'Smart TV': {
                'Samsung': ['Q80T', 'The Frame', 'TU8000'],
                'LG': ['CX OLED', 'Nano 90', 'UN7300'],
                'Sony': ['X950H', 'A8H OLED', 'X800H'],
                'Vizio': ['P-Series Quantum', 'M-Series Quantum', 'V-Series'],
                'TCL': ['6-Series', '5-Series', '4-Series']
            },
            'Gaming Console': {
                'Sony': ['PlayStation 5', 'PlayStation 4 Pro', 'PlayStation 4 Slim'],
                'Microsoft': ['Xbox Series X', 'Xbox Series S', 'Xbox One X'],
                'Nintendo': ['Switch', 'Switch Lite', '3DS XL'],
                'Sega': ['Genesis Mini', 'Mega Drive Mini', 'Saturn'],
                'Atari': ['Atari VCS', 'Flashback 9', '2600']
            },
            'Router': {
                'TP-Link': ['Archer A7', 'Deco X20', 'Archer AX50'],
                'Netgear': ['Nighthawk AX12', 'Orbi RBK852', 'Nighthawk AC2300'],
                'Asus': ['RT-AX88U', 'ZenWiFi AX', 'RT-AC68U'],
                'Linksys': ['Velop MX10', 'MR9000', 'EA7500'],
                'Western Digital': ['My Passport', 'Elements', 'My Book'],
                'Toshiba': ['Canvio Basics', 'Canvio Advance', 'Canvio Flex'],
                'Samsung': ['T7 Touch', 'T5', 'X5'],
                'LaCie': ['Rugged Mini', 'd2 Professional', 'Porsche Design']
            },
            'Projector': {
                'Epson': ['Home Cinema 5050UB', 'EH-TW7100', 'PowerLite 1781W'],
                'BenQ': ['HT3550', 'TK850', 'GS2'],
                'Optoma': ['HD146X', 'UHD50X', 'GT1080HDR'],
                'ViewSonic': ['PX747-4K', 'M1 Mini Plus', 'X10-4K'],
                'Sony': ['VPL-VW295ES', 'VPL-HW45ES', 'VPL-VW570ES']
            },
            'Fitness Tracker': {
                'Fitbit': ['Charge 5', 'Sense', 'Inspire 2'],
                'Garmin': ['Forerunner 945', 'Venu 2', 'Vivomove HR'],
                'Xiaomi': ['Mi Band 6', 'Mi Band 5', 'Mi Watch'],
                'Samsung': ['Galaxy Fit 2', 'Galaxy Watch Active2', 'Galaxy Watch 4'],
                'Huawei': ['Band 6', 'Watch Fit', 'Watch GT 3']
            },
            'VR Headset': {
                'Oculus': ['Quest 2', 'Rift S', 'Quest'],
                'HTC': ['Vive Pro 2', 'Vive Cosmos', 'Vive Flow'],
                'Sony': ['PlayStation VR', 'PlayStation VR2'],
                'Samsung': ['Odyssey+', 'HMD Odyssey'],
                'Valve': ['Index']
            },
            'Home Security Camera': {
                'Ring': ['Ring Stick Up Cam', 'Ring Spotlight Cam', 'Ring Doorbell Pro'],
                'Nest': ['Nest Cam Indoor', 'Nest Cam Outdoor', 'Nest Hello'],
                'Arlo': ['Ultra 2', 'Pro 4', 'Essential'],
                'Blink': ['Blink Outdoor', 'Blink Mini', 'Blink XT2'],
                'Wyze': ['Wyze Cam v3', 'Wyze Cam Pan', 'Wyze Cam Outdoor']
            },
            'Bluetooth Speaker': {
                'JBL': ['Charge 5', 'Flip 6', 'Xtreme 3'],
                'Bose': ['SoundLink Flex', 'SoundLink Revolve', 'SoundLink Micro'],
                'Sony': ['SRS-XB43', 'SRS-XB33', 'SRS-XB23'],
                'Ultimate Ears': ['Boom 3', 'Megaboom 3', 'Hyperboom'],
                'Marshall': ['Kilburn II', 'Stockwell II', 'Woburn II']
            }
        }

        # Create products for each brand
        for category_name, brand_data in products.items():
            category = Category.objects.get(category_name=category_name)
            for brand_name, product_models in brand_data.items():
               # Fetch or create Brands_list object
                brands_list, created = Brands_list.objects.get_or_create(brand_name=brand_name)
                
                # Fetch or create Brand object
                brand, created = Brand.objects.get_or_create(
                    brand_name=brands_list,
                    category=category
                )
                for model in product_models:
                    Product.objects.create(
                        product_name=model,
                        brand=brand,
                        purchase_price=random.uniform(50.00, 500.00),
                        sale_price=random.uniform(100.00, 1000.00),
                        quantity_in_stock=random.randint(10, 100)
                    )
        self.stdout.write(self.style.SUCCESS('Products have been successfully created.'))

