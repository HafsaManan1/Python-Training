class UserManager:
    def __init__(self, database):
        self.db = database

    def add_user(self, username, password, level):
        self.db.execute('INSERT INTO users (username, password, level) VALUES (?, ?, ?)', (username, password, level))

    def validate_user(self, username, password):
        return self.db.fetchone('SELECT * FROM users WHERE username=? AND password=?', (username, password))


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
