import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from ..main import get_db_connection, create, update, delete, LOGIN, PASSWORD, clients, create2, update2, delete2
from flask import url_for

class TestMain(unittest.TestCase):

    @patch('main.mysql.connector.connect')
    def test_get_db_connection(self, mock_connect):
        mock_connect.return_value = MagicMock()
        db_connection = get_db_connection()
        self.assertIsInstance(db_connection, mysql.connector.MySQLConnection)

    @patch('main.get_db_connection')
    def test_create(self, mock_get_db_connection):
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None

        result = create(name='Test Good', description='Test Description', price=100, availability_in_stock='In stock', quantity_in_stock=5)

        mock_cursor.execute.assert_called_once_with("INSERT INTO Goods (Name, Description, Price, Availability_in_stock, Quantity_in_stock) VALUES (%s, %s, %s, %s, %s)", ('Test Good', 'Test Description', 100, 'In stock', 5))
        mock_get_db_connection.return_value.commit.assert_called_once()

    @patch('main.get_db_connection')
    def test_update(self, mock_get_db_connection):
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None

        result = update(1, name='Updated Good', description='Updated Description', price=150, availability_in_stock='In stock', quantity_in_stock=8)

        mock_cursor.execute.assert_called_once_with("UPDATE Goods SET Name=%s, Description=%s, Price=%s, Availability_in_stock=%s, Quantity_in_stock=%s WHERE ID=%s", ('Updated Good', 'Updated Description', 150, 'In stock', 8, 1))
        mock_get_db_connection.return_value.commit.assert_called_once()

    @patch('main.get_db_connection')
    def test_delete(self, mock_get_db_connection):
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None

        result = delete(1)

        mock_cursor.execute.assert_called_once_with("DELETE FROM Goods WHERE ID=%s", (1,))
        mock_get_db_connection.return_value.commit.assert_called_once()




    @patch('main.get_db_connection')
    def test_clients(self, mock_get_db_connection):
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [
            ('Иван Иванов', 'г. Москва', '+79991234567', 'ivan@example.com', 'Заказ 1, Заказ 2', 'ivan', 'password')]

        response = self.main.get('/clients')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Иван Иванов', response.data)

    @patch('main.get_db_connection')
    def test_create2(self, mock_get_db_connection):
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None

        response = self.main.post('/create2', data={'full_name': 'Петр Петров', 'address': 'г. Санкт-Петербург',
                                                   'telephone': '+78121234567', 'email': 'petr@example.com',
                                                   'order_history': 'Заказ 1', 'login': 'petr', 'password': 'password'},
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO Clients (full_name, address, telephone, email, order_history, login, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            ('Петр Петров', 'г. Санкт-Петербург', '+78121234567', 'petr@example.com', 'Заказ 1', 'petr', 'password'))
        mock_get_db_connection.return_value.commit.assert_called_once()

    @patch('main.get_db_connection')
    def test_update2(self, mock_get_db_connection):
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None
        mock_cursor.fetchone.return_value = (
        'Старый клиент', 'Старый адрес', '+79991234567', 'old@example.com', 'Заказ 1', 'old', 'password')

        response = self.main.post('/update2/1', data={'full_name': 'Обновленный клиент', 'address': 'Обновленный адрес',
                                                     'telephone': '+79999999999', 'email': 'new@example.com',
                                                     'order_history': 'Заказ 2', 'login': 'new',
                                                     'password': 'newpassword'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        mock_cursor.execute.assert_called_once_with(
            "UPDATE Clients SET Full_name=%s, Address=%s, Telephone=%s, Email=%s, Order_history=%s, Login=%s, Password=%s WHERE ID=%s",
            ('Обновленный клиент', 'Обновленный адрес', '+79999999999', 'new@example.com', 'Заказ 2', 'new',
             'newpassword', 1))
        mock_get_db_connection.return_value.commit.assert_called_once()

    @patch('main.get_db_connection')
    def test_delete2(self, mock_get_db_connection):
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None

        response = self.main.post('/delete2/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        mock_cursor.execute.assert_called_once_with("DELETE FROM Clients WHERE ID=%s", (1,))
        mock_get_db_connection.return_value.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
