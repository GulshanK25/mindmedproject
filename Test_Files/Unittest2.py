import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
import mysql.connector as con
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication, QMessageBox
from mindmed2 import MainApp

class TestLogin(unittest.TestCase):
    
    def setUp(self):
        self.widget = MagicMock()
        self.widget.tb01.text.return_value = ""
        self.widget.tb02.text.return_value = ""
        
    def test_valid_login(self):
        self.widget.login()
        self.assertTrue(self.widget.menubar.isVisible())
        self.assertEqual(self.widget.tabWidget.currentIndex(), 1)
        self.assertFalse(QMessageBox.information.called)
        self.assertFalse(self.widget.l01.setText.called)
        
    def test_invalid_login(self):
        self.widget.tb01.text.return_value = "admin"
        self.widget.tb02.text.return_value = "password"
        self.widget.login()
        self.assertTrue(self.widget.menubar.isVisible())
        self.assertNotEqual(self.widget.tabWidget.currentIndex(), 1)
        QMessageBox.information.assert_called_once_with(self.widget, "Mental Health Management System", "Invalid admin login details, Try again !")
        self.widget.l01.setText.assert_called_once_with("Invalid admin login details, Try again !")

    @patch('path.to.module.con.connect')
    def test_fill_next_employee_id(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1, 'John', 'Doe', 'Male', '1990-01-01', '1234567890', 'johndoe@test.com', '123 Main St', 'New York', 'IT', 'Some comment')]
        mock_connect.return_value.cursor.return_value = mock_cursor

        employee_management = EmployeeManagement()
        employee_management.fill_next_employee_id()

        self.assertEqual(employee_management.l111.text(), '2')


    @patch('path.to.module.QMessageBox.information')
    @patch('path.to.module.con.connect')
    def test_save_employee_id_information(self, mock_connect, mock_messagebox_information):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        employee_management = EmployeeManagement()
        employee_management.l111.setText('1')
        employee_management.tb112.setText('John')
        employee_management.tb113.setText('Doe')
        employee_management.cb114.setCurrentText('Male')
        employee_management.tb115_1.setText('1990')
        employee_management.tb115_2.setText('01')
        employee_management.tb115_3.setText('01')
        employee_management.tb116.setText('1234567890')
        employee_management.tb117.setText('johndoe@test.com')
        employee_management.tb118.setText('123 Main St')
        employee_management.tb119.setText('New York')
        employee_management.cb120.setCurrentText('IT')
        employee_management.tb121.setText('Some comment')

        employee_management.save_employee_id_information()

        mock_cursor.execute.assert_called_with(
        "insert into employee (employeeID,first_name,last_name,gender,date_of_birth,mobail_number,email,address,city,department,comment) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        ('1', 'John', 'Doe', 'Male', '1990-01-01', '1234567890', 'johndoe@test.com', '123 Main St', 'New York', 'IT', 'Some comment')
    )
        mock_messagebox_information.assert_called_with(employee_management, "Mental health management system", "Employee information added successfully!")

    def test_show_edit_employee_tab(self):
        self.employee.l5000 = Mock()
        self.employee.tabWidget = Mock()

        self.employee.show_edit_employee_tab()

        self.assertEqual(self.employee.tabWidget.setCurrentIndex.call_count, 1)
        self.assertEqual(self.employee.choose_employee_id_from_textbox.call_count, 1)

    def test_choose_employee_id_from_textbox(self):
        self.employee.l5000 = Mock()
        self.employee.tb401 = Mock()

        mydb_mock = Mock()
        cursor_mock = Mock()
        self.employee.con.connect.return_value = mydb_mock
        mydb_mock.cursor.return_value = cursor_mock
        cursor_mock.fetchall.return_value = [("001", "John", "Smith", "Male", "1990-01-01", "5551234", "jsmith@example.com", "123 Main St", "Anytown", "IT", "Comment")]

        self.employee.choose_employee_id_from_textbox()

        self.assertEqual(cursor_mock.execute.call_count, 1)
        cursor_mock.execute.assert_called_with("select * from employee where employeeID ='"+ self.employee.l5000.text() +"'")
        self.assertEqual(cursor_mock.fetchall.call_count, 1)
        self.assertEqual(self.employee.tb401.clear.call_count, 1)
        self.assertEqual(self.employee.tb401.addItem.call_count, 1)
        self.employee.tb401.addItem.assert_called_with("001")

    def test_fill_information_of_the_selected_employee(self):
        self.employee.tb401 = Mock()
        self.employee.tb122 = Mock()
        self.employee.tb123 = Mock()
        self.employee.cb124 = Mock()
        self.employee.tb125_1 = Mock()
        self.employee.tb125_2 = Mock()
        self.employee.tb125_3 = Mock()
        self.employee.tb126 = Mock()
        self.employee.tb127 = Mock()
        self.employee.tb128 = Mock()
        self.employee.tb129 = Mock()
        self.employee.cb130 = Mock()
        self.employee.tb131 = Mock()

        mydb_mock = Mock()
        cursor_mock = Mock()
        self.employee.con.connect.return_value = mydb_mock
        mydb_mock.cursor.return_value = cursor_mock
        cursor_mock.fetchone.return_value = ("001", "John", "Smith", "Male", "1990-01-01", "5551234", "jsmith@example.com", "123 Main St", "Anytown", "IT", "Comment")

        self.employee.fill_information_of_the_selected_employee()

        self.assertEqual(cursor_mock.execute.call_count, 1)
        cursor_mock.execute.assert_called_with("SELECT * FROM employee WHERE employeeID = %s", (self.employee.tb401.text(),))
        self.assertEqual(cursor_mock.fetchone.call_count, 1)
        self.assertEqual(self.employee.tb122.setText.call_count, 1)
        self.employee.tb122.setText.assert_called_with("John")
        self.assertEqual(self.employee.tb123.setText.call_count, 1)
        self.employee.tb123.setText.assert_called_with("Smith")
        self.assertEqual(self.employee.cb124.setCurrentText.call_count, 1)
        self.employee.cb124.setCurrentText.assert_called_with("Male")
        self.assertEqual(self.employee.tb125_1.setText.call_count, 1)
        self.employee.tb125_1.setText.assert_called_with("1990")
        self.assertEqual(self.employee.tb125_2.setText.call_count, 1)
        self.employee.tb125_2.setText.assert_called_with("01")
        self.assertEqual(self.employee.tb125_3.setText.call_count, 1)
        self.employee.tb125_3.setText.assert_called_with("01")
        self.assertEqual(self.employee.tb126.setText.call_count)
    
    def test_fill_next_member_id(self):
        expected_output = 3
        
        with patch('mysql.connector.connect') as mock_connect:
            mock_cursor = mock_connect.return_value.cursor.return_value
            mock_cursor.fetchall.return_value = [(1, ), (2, )]
            
            self.main_window.fill_next_member_id()
            self.assertEqual(int(self.main_window.l211.text()), expected_output)
            
    def test_fill_information_of_the_selected_member(self):
        self.main_window.tb501.addItem('1')
        
        with patch('mysql.connector.connect') as mock_connect:
            mock_cursor = mock_connect.return_value.cursor.return_value
            mock_cursor.fetchone.return_value = (1, 'John', 'Doe', 'Male', '1990-01-01', '1234567890', 'johndoe@mail.com', '123 Main St', 'New York', 'Psychology', 'Member comment')
            
            self.main_window.fill_information_of_the_selected_member()
            self.assertEqual(self.main_window.tb222.text(), 'John')
            self.assertEqual(self.main_window.tb223.text(), 'Doe')
            self.assertEqual(self.main_window.cb224.currentText(), 'Male')
            self.assertEqual(self.main_window.tb225_1.text(), '1990')
            self.assertEqual(self.main_window.tb225_2.text(), '01')
            self.assertEqual(self.main_window.tb225_3.text(), '01')
            self.assertEqual(self.main_window.tb226.text(), '1234567890')
            self.assertEqual(self.main_window.tb227.text(), 'johndoe@mail.com')
            self.assertEqual(self.main_window.tb228.text(), '123 Main St')
            self.assertEqual(self.main_window.tb229.text(), 'New York')
            self.assertEqual(self.main_window.cb230.currentText(), 'Psychology')
            self.assertEqual(self.main_window.tb231.text(), 'Member comment')
            
    def test_edit_member_information(self):
        self.main_window.tb501.addItem('2')
        self.main_window.tb222.setText('New')
        self.main_window.tb223.setText('Name')
        
        with patch('mysql.connector.connect') as mock_connect:
            mock_cursor = mock_connect.return_value.cursor.return_value
            
            self.main_window.edit_member_information()
            mock_cursor.execute.assert_called_once()
            mock_connect.return_value.commit.assert_called_once()
            QMessageBox.information.assert_called_once()

        
if __name__ == '__main__':
    unittest.main()