def create_table(connection):
    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS car (
                        id SERIAL PRIMARY KEY,
                        url TEXT UNIQUE,
                        title TEXT,
                        price_usd INTEGER,
                        odometer INTEGER,
                        username TEXT,
                        phone_number BIGINT,
                        image_url TEXT,
                        images_count INTEGER,
                        car_number TEXT,
                        car_vin TEXT,
                        datetime_found TIMESTAMP DEFAULT NOW()
                        );""")
        connection.commit()
    
def save_cars(cars: list[dict], connection):
    with connection.cursor() as cursor:
        cursor.executemany("""INSERT INTO car
                           (url, title, price_usd, odometer, username, phone_number, 
                           image_url, images_count, car_number, car_vin)
                           VALUES (%(url)s, %(title)s, %(price_usd)s, %(odometer)s, %(username)s, %(phone_number)s, 
                           %(image_url)s, %(images_count)s, %(car_number)s, %(car_vin)s)
                           ON CONFLICT (url) DO NOTHING;""", 
                           cars)
    connection.commit()
        

