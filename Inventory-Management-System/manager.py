class UserManager:
    def __init__(self, database):
        self.db = database

    def add_user(self, username, password, level):
        self.db.execute('INSERT INTO users (username, password, level) VALUES (?, ?, ?)', (username, password, level))

    def validate_user(self, username, password):
        return self.db.fetchone('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    
    def update_user(self, user_id, username, password, level):
        self.db.execute('UPDATE users SET username=?, password=?, level=? WHERE id=?', (username, password, level, user_id))

    def delete_user(self, user_id):
        self.db.execute('DELETE FROM users WHERE id=?', (user_id,))

    def get_all_users(self):
        return self.db.fetchall('SELECT * FROM users')



class InventoryManager:
    def __init__(self, database):
        self.db = database

    def add_item(self, name, quantity, price):
        self.db.execute('INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))

    def update_item(self, item_id, name, quantity, price):
        self.db.execute('UPDATE inventory SET name=?, quantity=?, price=? WHERE id=?', (name, quantity, price, item_id))

    def delete_item(self, item_id):
        self.db.execute('DELETE FROM inventory WHERE id=?', (item_id,))

    def get_all_items(self):
        return self.db.fetchall('SELECT * FROM inventory')
