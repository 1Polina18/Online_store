import unittest
import mysql.connector
from main import get_db_connection, create, update, delete, LOGIN, PASSWORD

class TestMainIntegration(unittest.TestCase):

    def setUp(self):
        # Подключение к тестовой базе данных
        self.db = mysql.connector.connect(
            host='localhost',
            user='ppolinash',
            password='ZjBmPtk8aJ7',
            database='Online_store'
        )
        self.cursor = self.db.cursor()

    def tearDown(self):
        # Закрытие соединения с базой данных
        self.cursor.close()
        self.db.close()

    def test_create_good_integration(self):
        # Создание тестового товара
        create(name='Новый товар', description='Описание товара', price=150, availability_in_stock='В наличии', quantity_in_stock=3)

        # Проверка, что товар был добавлен в базу данных
        self.cursor.execute("SELECT * FROM Goods WHERE Name='Новый товар'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result) # Проверяем, что запись существует
        self.assertEqual(result[2], 150) # Проверяем значение Price

    def test_update_good_integration(self):
        # Создание тестового товара
        self.cursor.execute("INSERT INTO Goods (Name, Description, Price, Availability_in_stock, Quantity_in_stock)"
                            "VALUES ('Старый товар', 'Старое описание', 100, 'В наличии', 5)")
        self.db.commit()

        # Обновление товара
        update(1, name='Обновленный товар', description='Обновленное описание', price=200, availability_in_stock='В наличии', quantity_in_stock=7)

        # Проверка обновления
        self.cursor.execute("SELECT * FROM Goods WHERE ID=1")
        result = self.cursor.fetchone()
        self.assertEqual(result[1], 'Обновленное описание')
        self.assertEqual(result[2], 200)

    def test_delete_good_integration(self):
        # Создание тестового товара
        self.cursor.execute("INSERT INTO Goods (Name, Description, Price, Availability_in_stock, Quantity_in_stock)"
                            "VALUES ('Товар для удаления', 'Описание', 100, 'В наличии', 5)")
        self.db.commit()

        # Удаление товара
        delete(1)

        # Проверка удаления
        self.cursor.execute("SELECT * FROM Goods WHERE ID=1")
        result = self.cursor.fetchone()
        self.assertIsNone(result)

    def test_create_client_integration(self):
        # Создание тестового клиента
        create(full_name='Петр Петров', address='г. Санкт-Петербург', telephone='+78121234567', email='petr@example.com',
               order_history='Заказ 1', login='petr', password='password')

        # Проверка, что клиент был добавлен в базу данных
        self.cursor.execute("SELECT * FROM Clients WHERE Full_name='Петр Петров'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[2], '+78121234567')

    def test_update_client_integration(self):
        # Создание тестового клиента
        self.cursor.execute("INSERT INTO Clients (full_name, address, telephone, email, order_history, login,"
                            "password) VALUES ('Старый клиент', 'Старый адрес', '+79991234567', 'old@example.com', 'Заказ 1', 'old', 'password')")
        self.db.commit()

        # Обновление клиента
        update(1, full_name='Обновленный клиент', address='Обновленный адрес', telephone='+79999999999',
               email='new@example.com', order_history='Заказ 2', login='new', password='newpassword')

        # Проверка обновления
        self.cursor.execute("SELECT * FROM Clients WHERE ID=1")
        result = self.cursor.fetchone()
        self.assertEqual(result[1], 'Обновленный адрес')
        self.assertEqual(result[4], 'Заказ 2')

    def test_delete_client_integration(self):
        # Создание тестового клиента
        self.cursor.execute("INSERT INTO Clients (full_name, address, telephone, email, order_history, login,"
                            "password) VALUES ('Клиент для удаления', 'Адрес', '+79991234567', 'client@example.com', 'Заказ 1', 'client', 'password')")
        self.db.commit()

        # Удаление клиента
        delete(1)

        # Проверка удаления
        self.cursor.execute("SELECT * FROM Clients WHERE ID=1")
        result = self.cursor.fetchone()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
