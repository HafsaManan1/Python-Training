class UserManager:
    def __init__(self, database):
        self.db = database

    def add_user(self, username, password, level, active=0):
        self.db.execute('INSERT INTO users (username, password, level, active) VALUES (?, ?, ?,?)', (username, password, level, active))

    def validate_user(self, username, password):
        return self.db.fetchone('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    
    def update_user(self, user_id, username, password, level, active=0):
        self.db.execute('UPDATE users SET username=?, password=?, level=?, active=? WHERE id=?', (username, password, level, active, user_id))

    def delete_user(self, user_id):
        self.db.execute('DELETE FROM users WHERE id=?', (user_id,))

    def get_all_users(self):
        return self.db.fetchall('SELECT * FROM users')
    
    def update_user_active_status(self, user_id, active):
        self.db.execute('UPDATE users SET active=? WHERE id=?', (active, user_id))

    def get_active_users(self):
        return self.db.fetchall('SELECT * FROM users WHERE active=?', (1,))

class InventoryManager:
    def __init__(self, database):
        self.db = database

    def add_item(self,item_id, name, quantity, price):
        self.db.execute('INSERT INTO inventory (id, name, quantity, price) VALUES (?, ?, ?, ?)', (item_id, name, quantity, price))

    def update_item(self, item_id, name, quantity, price):
        self.db.execute('UPDATE inventory SET name=?, quantity=?, price=? WHERE id=?', (name, quantity, price, item_id))

    def delete_item(self, item_id):
        self.db.execute('DELETE FROM inventory WHERE id=?', (item_id,))

    def get_all_items(self):
        return self.db.fetchall('SELECT * FROM inventory')
    
    def get_item_name(self,name):
        return self.db.fetchone('SELECT * FROM inventory WHERE name=?',(name,))
    
    def get_item_sku(self,item_id):
        return self.db.fetchone('SELECT * FROM inventory WHERE id=?',(item_id,))

