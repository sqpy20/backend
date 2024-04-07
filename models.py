import sqlite3
import requests

class UserDatabase:
    """_summary_
    This is db object for the user data
    """
    def __init__(self, db_name='userdata.db'):
        self.db_name = db_name
        self.create_table()

    def create_connection(self):
        '''_summary_
        Function to create a connection to SQLite database
        '''
        conn = sqlite3.connect(self.db_name)
        return conn

    def create_table(self):
        """_summary_
        Create table to store user data
        """
        conn = self.create_connection()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT,
                     password TEXT,
                     ip_address TEXT,
                     account_type TEXT,
                     city TEXT,
                     region TEXT,
                     country TEXT,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def get_all_users(self):
        """_summary_
        Function to fetch all users from the database
        Returns:
            _type_: _user from db_
        """
        conn = self.create_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        conn.close()
        return users

    def delete_user(self, user_id: int):
        """_summary_
        Function to delete a user from the database
        Args:
            user_id (int): _id of the user to be deleted_
        """
        conn = self.create_connection()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()

    def fetch_geo_location(self, ip_address):
        '''_summary_
        arg -> ip address
        
        Function to fetch geo-location information from the API
        Returns:
            _type_: _str_
        '''
        url = f"https://tools.keycdn.com/geo.json?host={ip_address}"
        headers = {"User-Agent": "keycdn-tools:https://example.com"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            geo_data = data.get('data', {}).get('geo', {})
            city = geo_data.get('city')
            region = geo_data.get('region_name')
            country = geo_data.get('country_name')
            return str(city), str(region), str(country)
        else:
            return None, None, None

    def insert_user(self, username:str, password:str, ip_address:str, account_type:str):
        """_summary_
        Function to insert user data into the database
        Args:
            username (str): username
            password (str): password
            ip_address (str): ip_address
            account_type (str): account_type
        """
        city, region, country = self.fetch_geo_location(ip_address)
        conn = self.create_connection()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, ip_address, account_type, city, region, country) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (username, password, ip_address, account_type, city, region, country))
        conn.commit()
        conn.close()

    def delete_all_users(self):
        """_summary_
        Function to delete all users from the database
        """
        conn = self.create_connection()
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS users")
        self.create_table() # recreates the table
        conn.close()

