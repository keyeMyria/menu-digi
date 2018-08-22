from datetime import datetime
def site_url(request):
    return {'site':'http://127.0.0.1:8000'}

def today(request):
    return {'today':datetime.now()}

def default_avatars(request):
    return {"human_avatar":"https://res.cloudinary.com/dyuhcszpn/image/upload/v1534950838/chef_hat-512.png",
            "food_avatar":"https://res.cloudinary.com/dyuhcszpn/image/upload/v1534950839/restaurant-200-633659.png",
            "customer_avatar":"https://res.cloudinary.com/dyuhcszpn/image/upload/v1534950837/3bd1c6b19aa1e32ce65b73406651f339.png",
            "food_category_avatar":"https://res.cloudinary.com/dyuhcszpn/image/upload/v1534950838/food-512.png",
            "table_avatar":"https://res.cloudinary.com/dyuhcszpn/image/upload/v1534950837/65388-200.png",
            "restaurant_logo":"https://res.cloudinary.com/dyuhcszpn/image/upload/v1534955607/log2.png",
            "customer_logo":"https://res.cloudinary.com/dyuhcszpn/image/upload/v1534957230/m.png"}