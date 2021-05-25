import sqlite3


class UserDatabase():
    def __init__(self, db_location):
        self.__DB_LOCATION = db_location
        self.__connection = sqlite3.connect(self.__DB_LOCATION)
        self.cursor = self.__connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username VARCHAR(20) UNIQUE,
                first_name VARCHAR(20),
                last_name VARCHAR(20),
                email VARCHAR(20),
                password TEXT,
                access INTEGER
                
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                role_id INTEGER PRIMARY KEY,
                name VARCHAR(32) UNIQUE,
                description VARCHAR(300),
                colour VARCHAR(6) DEFAULT f0ffff
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS farms (
	            farm_ID	INTEGER,
	            name	VARCHAR(20),
	            description	VARCHAR(500),
	            PRIMARY KEY("farm_ID" AUTOINCREMENT)
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                product_id INTEGER PRIMARY KEY,
                name VARCHAR(50) UNIQUE,
                description VARCHAT(500)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ProductFarm (
                product_id REFERENCES Products(product_id),
                farm_id REFERENCES Farms(farm_id),
                PRIMARY KEY(product_id, farm_id)
            )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS "userfarms" (
	        "UserID"	INTEGER,
	        "FARMID"	INTEGER,
	        PRIMARY KEY("UserID","FARMID")
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS "productPerFarm" (
            "ID"	INTEGER UNIQUE,
            "ProductName"	VARCHAR(500),
            "Boxes"	INTEGER,
            "pricePerBox"	NUMERIC,
            "farmName"	VARCHAR(500),
            "farmID"	INTEGER,
            PRIMARY KEY("ID" AUTOINCREMENT)
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS "farmsSellingProduct" (
            "ProductID"	INTEGER,
            "FarmID"	INTEGER,
            PRIMARY KEY("ProductID","FarmID")
        )
        """)

    

 
        

    def insert_user(self, username, first_name, last_name, email, password):
            sql = """
                INSERT INTO users (username, first_name, last_name, email, password, access)
                VALUES (?, ?, ?, ? , ? , ?)
            """
            self.cursor.execute(sql, (username, first_name, last_name, email, password, 2))
            self.__connection.commit()

    def check_user(self, username):
            sql = """
                SELECT username, password, id, access
                FROM users
                WHERE username = ?
            """
            self.cursor.execute(sql, (username, ))
            return self.cursor.fetchone()

    def get_users(self):
            sql = """
                SELECT * FROM users
            """
            self.cursor.execute(sql, )
            return self.cursor.fetchall()

    

    def remove_user(self, username):
            """ Deletes user and user_role mappings """
            sql = """
                DELETE FROM users
                WHERE username =?
            """
            self.cursor.execute(sql, (username, ))
            self.__connection.commit()
            return

    def insert_role(self, name):
            sql = """
                INSERT INTO roles (name)
                VALUES (?)
            """
            self.cursor.execute(sql, (name, ))
            self.__connection.commit()
            return True

    def check_role(self, name):
            sql = """
                SELECT *
                FROM roles
                WHERE name = ?
            """
            self.cursor.execute(sql, (name, ))
            return self.cursor.fetchone()
    def check_role_id(self, role_id):
            sql = """
                SELECT *
                FROM roles
                WHERE role_id = ?
            """
            self.cursor.execute(sql, (role_id, ))
            selected_role=self.cursor.fetchone()
            if not selected_role:
                selected_role=(0,"no role","", "808080")
            return selected_role
    def update_role_id(self, role_id, user_id):
            sql = """
                UPDATE users
                SET access=?
                WHERE id =? 
            """
            self.cursor.execute(sql, (role_id, user_id ))
            self.__connection.commit()
            return True

    def get_roles(self):
            sql = """
                SELECT *
                FROM roles
            """
            self.cursor.execute(sql, )
            return self.cursor.fetchall()

    def get_logged_farmer(self, loggedusername):
            sql = """
                SELECT username, first_name, last_name, email
                FROM users
                WHERE username = ?
            """
            self.cursor.execute(sql, (loggedusername,))
            loggeduser = self.cursor.fetchall()
            return loggeduser

    def get_userID(self, loggedusername):
            sql = """
                SELECT id
                FROM users
                WHERE username = ?
            """
            self.cursor.execute(sql, (loggedusername,))
            loggeduser = self.cursor.fetchall()
            return loggeduser

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

    def insert_userfarm(self, name, description):
            sql = """
                INSERT INTO farms (name, description)
                VALUES (?, ?)
            """
            self.cursor.execute(sql, (name, description))
            self.__connection.commit()

    def select_product_farm(self, product_id):
        sql = """
            SELECT ProductFarm.product_id, farms.name, farms.farm_id
            FROM ProductFarm
            INNER JOIN Products ON Products.product_id = ProductFarm.product_id
            INNER JOIN Farms ON farms.farm_id = ProductFarm.farm_id
            WHERE Products.product_id = ?
        """
        self.cursor.execute(sql, (product_id, ))
        return self.cursor.fetchall()

    def select_farm_product(self, farm_id):
        sql = """
            SELECT ProductFarm.farm_id, Products.name, Products.product_id
            FROM ProductFarm
            INNER JOIN Products ON Products.product_id = ProductFarm.product_id
            INNER JOIN Farms ON farms.farm_id = ProductFarm.farm_id
            WHERE farms.farm_id = ?
        """
        self.cursor.execute(sql, (farm_id, ))
        return self.cursor.fetchall()

    def select_productsfilter(self, productname, ):
        sql = """
            SELECT * FROM Products
            WHERE name = ?
        """
        self.cursor.execute(sql, (productname, ))
        return self.cursor.fetchall()

    def select_farmidbyproductid(self, pid, ):
        sql = """
            SELECT farm_id FROM ProductFarm
            WHERE product_id = ?
        """
        self.cursor.execute(sql, (pid, ))
        return self.cursor.fetchall()
    
    def get_farmID(self, farmIDint):
        sql = """
                SELECT FARMID
                FROM userfarms
                WHERE userID = ?
            """
        self.cursor.execute(sql, (farmIDint,))
        currentuserfarmID = self.cursor.fetchall()
        return currentuserfarmID
    
    def get_farminfo(self, finalfarmID):
        sql = """
                SELECT farm_id, name, description
                FROM farms
                WHERE farm_ID = ?
            """
        self.cursor.execute(sql, (finalfarmID,))
        farminfo = self.cursor.fetchall()
        return farminfo

    def get_farmname(self, finalfarmID):
        sql = """
                SELECT name
                FROM farms
                WHERE farm_ID = ?
            """
        self.cursor.execute(sql, (finalfarmID,))
        farmnames = self.cursor.fetchall()
        return farmnames
    
 

    def get_farmidbyname(self, farmname):
        sql = """
                SELECT farm_ID
                FROM farms
                WHERE name = ?
            """
        self.cursor.execute(sql, (farmname,))
        addedfarmid = self.cursor.fetchall()
        return addedfarmid

    def get_productname(self):
        sql = """
                SELECT name
                FROM Products
            """
        self.cursor.execute(sql, )
        return self.cursor.fetchall()
        

    
    def get_productidbyfarmid(self, fid):
        sql = """
                SELECT ProductID
                FROM farmsSellingProduct
                WHERE FarmID = ?
            """
        self.cursor.execute(sql, (fid,))
        addedpid = self.cursor.fetchall()
        return addedpid
    
    def get_productinfo(self, pid):
        sql = """
                SELECT ProductName, Boxes, pricePerBox, farmName
                FROM productPerFarm
                WHERE farmID = ?
            """
        self.cursor.execute(sql, (pid,))
        productinfo = self.cursor.fetchall()
        return productinfo

    def get_productidbyname(self, pname):
        sql = """
                SELECT product_id
                FROM Products
                WHERE name = ?
            """
        self.cursor.execute(sql, (pname,))
        productid = self.cursor.fetchall()
        return productid

    

    def insert_userandfarm(self, uid, fid):
            sql = """
                INSERT INTO userfarms (UserID, FARMID)
                VALUES (?, ?)
            """
            self.cursor.execute(sql, (uid, fid))
            self.__connection.commit()
    
    def insert_farmProduct(self, name, boxes, pbb, farmName):
            sql = """
                INSERT INTO productPerFarm (ProductName, Boxes, pricePerBox, farmName)
                VALUES (?, ?, ?, ?)
            """
            self.cursor.execute(sql, (name, boxes, pbb, farmName))
            productID = self.cursor.lastrowid
            self.__connection.commit()
            return productID
        
    def insert_farmandproduct(self, pid, fid):
            sql = """
                INSERT INTO farmsSellingProduct (ProductID, FarmID)
                VALUES (?, ?)
            """
            self.cursor.execute(sql, (pid, fid))
            self.__connection.commit()
    
    def insert_productfarm(self, pid, fid):
            sql = """
                INSERT INTO ProductFarm (product_id, farm_id)
                VALUES (?, ?)
            """
            self.cursor.execute(sql, (pid, fid))
            self.__connection.commit()
    
    def insert_farmProductid(self, fid, pid):
            sql = """
                UPDATE productPerFarm
                SET farmID = ?
                WHERE ID = ?
            """
            self.cursor.execute(sql, (fid, pid ))
            self.__connection.commit()
    
    def delete_farms(self, fid):
            sql = """
                DELETE FROM farms
                WHERE farm_ID = ?

            """
            self.cursor.execute(sql, (fid,))
            self.__connection.commit()
    
    def delete_productfarm(self, fid):
            sql = """
                DELETE FROM ProductFarm
                WHERE farm_id = ?

            """
            self.cursor.execute(sql, (fid,))
            self.__connection.commit()

    def delete_farmsellingProduct(self, fid):
            sql = """
                DELETE FROM farmsSellingProduct
                WHERE FarmID = ?

            """
            self.cursor.execute(sql, (fid,))
            self.__connection.commit()

    def delete_productPerFarm(self, fid):
            sql = """
                DELETE FROM productPerFarm
                WHERE farmID = ?

            """
            self.cursor.execute(sql, (fid,))
            self.__connection.commit()

    def delete_userfarms(self, fid):
            sql = """
                DELETE FROM userfarms
                WHERE FARMID = ?

            """
            self.cursor.execute(sql, (fid,))
            self.__connection.commit()

    def update_farm(self, name, description, fid):
            sql = """
                UPDATE farms
                SET name = ?, description = ?
                WHERE farm_ID =? 
            """
            self.cursor.execute(sql, (name, description, fid ))
            self.__connection.commit()
            
    def update_productperfarm(self, name, fid):
            sql = """
                UPDATE productPerFarm
                SET farmName = ?
                WHERE farmID =? 
            """
            self.cursor.execute(sql, (name, fid ))
            self.__connection.commit()
    

    
    def __del__(self):
            self.__connection.close()