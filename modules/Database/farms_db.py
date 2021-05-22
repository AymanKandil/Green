import sqlite3

class Database():
    def __init__(self, db_location):
        self.__DB_LOCATION = db_location
        self.__connection = sqlite3.connect(self.__DB_LOCATION)
        self.cursor = self.__connection.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                product_id INTEGER PRIMARY KEY,
                name VARCHAR(50) UNIQUE,
                description VARCHAT(500)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS farms (
                farm_id INTEGER PRIMARY KEY,
                name VARCHAR(50) UNIQUE,
                description VARCHAR(500)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ProductFarm (
                product_id REFERENCES Products(product_id),
                farm_id REFERENCES Farms(farm_id),
                PRIMARY KEY(product_id, farm_id)
            )
        """)

    def insert_farm(self, name, description):
        sql = """
            INSERT INTO farms (name, description)
            VALUES (?, ?)
        """
        try:
            self.cursor.execute(sql, (name, description))
            self.__connection.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Farm {name} already exists")
        return -1

    def select_farm(self, farm_id):
        sql = """
            SELECT * FROM farms
            WHERE farm_id = ?
        """
        self.cursor.execute(sql, (farm_id, ))
        return self.cursor.fetchone()

    def select_farms(self, limit=10):
        # https://gist.github.com/ssokolow/262503
        # sql = """
        #     SELECT * FROM Farms
        #     WHERE id NOT IN (   SELECT id FROM Farms
        #                         ORDER BY name ASC LIMIT 0 )
        #     ORDER BY name ASC LIMIT 2
        # """
        sql = """
            SELECT * FROM farms
            LIMIT 10
        """
        self.cursor.execute(sql, )
        return self.cursor.fetchall()

    def insert_product(self, name, description):
        sql = """
            INSERT INTO Products (name, description)
            VALUES (?, ?)
        """
        try:
            self.cursor.execute(sql, (name, description))
            self.__connection.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Product {name} already exists")

    def select_product(self, product_id):
        sql = """
            SELECT * FROM Products
            WHERE product_id = ?
        """
        self.cursor.execute(sql, (product_id, ))
        return self.cursor.fetchone()

    def select_products(self, limit=10):
        sql = """
            SELECT * FROM Products
            LIMIT 10
        """
        self.cursor.execute(sql, )
        return self.cursor.fetchall()

    def insert_product_farm(self, product_id, farm_id):
        sql = """
            INSERT INTO ProductFarm(product_id, farm_id)
            VALUES (?, ?)
        """
        try:
            self.cursor.execute(sql, (product_id, farm_id))
            self.__connection.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Farm already has {product_id}")

    def select_product_farm(self, product_id):
        sql = """
            SELECT ProductFarm.product_id, farms.name, farms.farm_id
            FROM ProductFarm
            INNER JOIN Products ON Products.product_id = ProductFarm.product_id
            INNER JOIN farms ON farms.farm_id = ProductFarm.farm_id
            WHERE Products.product_id = ?
        """
        self.cursor.execute(sql, (product_id, ))
        return self.cursor.fetchall()