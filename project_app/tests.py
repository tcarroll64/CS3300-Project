# tests.py

from django.test import TestCase, LiveServerTestCase
from django.urls import reverse, resolve
from .models import Sheet, Store, Item
from django.contrib.auth.models import User, Group
from .forms import CreateUserForm, SheetForm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import time

# UNIT TESTS
class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Non-modified objects used by all model test methods
        cls.test_store = Store.objects.create(
            name='Test Store',
            store_img='store_images/Chad.png',
            about='Test About Info'
            )
        
        cls.test_item = Item.objects.create(
            name='Test Item',
            barcode='barcode_images/chicksand_bc.png',
            code='ABC123',
            quant_bag='34',
            quant_box='5',
            about='Test About'
            )
        
        cls.test_sheet = Sheet.objects.create(
            name='Test Sheet',
            author='Test Author',
            notes='Test Notes',
            store=cls.test_store
        )
        cls.test_sheet.items.add(cls.test_item)

    def testSheet(self):
        expected_sheet_url = reverse('sheet-detail', args=[self.test_sheet.store.id, self.test_sheet.id])
        expected_sheet_str = 'Test Sheet - ' + str(self.test_sheet.pub_date)
        associated_items = self.test_sheet.items.all()
        associated_store = self.test_sheet.store
        
        # Check sheet details
        self.assertEqual(self.test_sheet.name, 'Test Sheet')
        self.assertEqual(self.test_sheet.author, 'Test Author')
        self.assertEqual(self.test_sheet.notes, 'Test Notes')

        # Check url/str rep. - This test made me learn that my get_absolute_url() was written wrong!!!
        self.assertEqual(self.test_sheet.get_absolute_url(), expected_sheet_url)
        self.assertEqual(str(self.test_sheet), expected_sheet_str)

        # Check sheet-store relationship works
        self.assertEqual(associated_store.name, 'Test Store')

        # Check sheet-item relationship works
        self.assertEqual(associated_items.exists(), True)
        self.assertEqual(associated_items.count(), 1)
        self.assertEqual(associated_items.first().name, 'Test Item')
    
    def testStore(self):
        expected_store_url = reverse('store-detail', args=[self.test_store.id])
        expected_store_str = 'Test Store'

        # Check store details
        self.assertEqual(self.test_store.name, 'Test Store')
        self.assertEqual(self.test_store.about, 'Test About Info')
        self.assertEqual(self.test_store.store_img, 'store_images/Chad.png')

        # Check url/str rep.
        self.assertEqual(self.test_store.get_absolute_url(), expected_store_url)
        self.assertEqual(str(self.test_store), expected_store_str)
    
    def testItem(self):
        expected_item_url = reverse('item-detail', args=[self.test_item.id])
        expected_item_str = 'Test Item'

        # Check item details
        self.assertEqual(self.test_item.name, 'Test Item')
        self.assertEqual(self.test_item.barcode, 'barcode_images/chicksand_bc.png')
        self.assertEqual(self.test_item.code, 'ABC123')
        self.assertEqual(self.test_item.quant_bag, '34')
        self.assertEqual(self.test_item.quant_box, '5')
        self.assertEqual(self.test_item.about, 'Test About')

        # Check item url and str rep.
        self.assertEqual(self.test_item.get_absolute_url(), expected_item_url)
        self.assertEqual(str(self.test_item), expected_item_str)

class FormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_store = Store.objects.create(
            name='Test Store',
            store_img='store_images/Chad.png',
            about='Test About Info'
        )

        cls.test_item = Item.objects.create(
            name='Test Item',
            barcode='barcode_images/chicksand_bc.png',
            code='ABC123',
            quant_bag='34',
            quant_box='5',
            about='Test About'
        )

        cls.test_user = User.objects.create_user(
            username='testuser',
            password='passworddd',
        )

    def testValidSheetForm(self):
        data = {
            'name': 'Test Sheet',
            'author': 'Test Author',
            'notes': 'Test Notes',
        }

        form = SheetForm(data)
        self.assertTrue(form.is_valid())
        

    def testInvalidSheetForm(self):
        data = {
            'name': '',  # Required field left blank so form should be invalid
            'author': 'Test Author',
            'notes': 'Test Notes',
        }

        form = SheetForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())  # Check if the 'name' field has an error

    def testCreateSheetFormPost(self):
        # An attempt where I filled out the form to create a user then tried to login, this didnt work
        # userData = {
        #     'username': 'testUser',
        #     'email': 'no@email.com',
        #     'password1': 'passworddd',
        #     'password2': 'passworddd',
        #     'pin': '1234',
        # }
        # userForm = CreateUserForm(userData)
        # #print("Form errors:", userForm.errors)
        # self.assertTrue(userForm.is_valid())
        # userForm.save()
        # #print(User.objects.all())
        # self.assertTrue(User.objects.filter(username='testUser').exists())

        # Logging client in
        login_successful = self.client.login(username='testuser', password='passworddd')
        self.assertTrue(login_successful)
        #print("All users:", User.objects.all())
        
        # Assigning the user the 'supervisor' group which is needed to access view
        # https://docs.djangoproject.com/en/4.1/ref/contrib/auth/#group-model
        superGroup, created = Group.objects.get_or_create(name='supervisor')
        self.test_user.groups.add(superGroup)
        self.test_user.save()
        self.assertTrue(self.test_user.groups.filter(name='supervisor').exists())   # Ensuring user added to group

        # Creating test data for a sheet
        sheetData = {
            'name': 'Test Sheet',
            'author': 'Test Author',
            'notes': 'Test Notes',
        }

        url = f'/store/{self.test_store.id}/create_sheet'
        response = self.client.post(url, sheetData, follow=True)    # POST sheet to database
        self.assertEqual(response.status_code, 200) # Successfull status code

        created_sheet= Sheet.objects.filter(name='Test Sheet')
        #print(created_sheet)
        self.assertTrue(created_sheet.exists())

        # Debug prints
        # print("Form errors:", response.context['form'].errors)
        # print("Response content:", response.content.decode())
        # print("Sheets after form submission:", Sheet.objects.all())

# SELENIUM TESTS
class HostTest(LiveServerTestCase):
    def testhomepage(self):
        # Specifying webdriver to use (chrome webdriver)
        driver = webdriver.Chrome()
        # Navigating to local host to access Django app
        driver.get('http://127.0.0.1:8000/')
        # Adding a delay to ensure page loads correctly
        time.sleep(1)
        # Verifying the home page has the title 'WIS Scan SheetsS'
        assert "WIS Scan Sheets" in driver.title

class LoginFormTest(LiveServerTestCase):
    def testform(self):
        driver = webdriver.Chrome()

        # Navigting to log in page
        driver.get('http://127.0.0.1:8000/accounts/login/?next=/')

        # Finding the username/password fields on the login page
        user_name = driver.find_element(By.NAME, "username")
        user_password = driver.find_element(By.NAME, "password")

        # Finding the login button on the login page
        submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
        
        # Entering in login information in the username/password fields
        user_name.send_keys('testAdmin2')
        user_password.send_keys('testP@S$')

        # Clicking the submit button on the page after the fields have been filled out
        submit.click()
        # Added delay to see if redirect works
        time.sleep(2)

        # Ensuring that the user is logged in and their username is found on the page
        assert 'testAdmin' in driver.page_source

        driver.quit()

# Testing complete process of adding a pre-existing item to a sheet
class AddItemToSheetTest(LiveServerTestCase):
    def testAddItem(self):
        def should_select_item(index):
            return index % 2 == 0
        
        driver = webdriver.Chrome()

        # Go to home page
        driver.get('http://127.0.0.1:8000/')

        # Click on element to see scan sheets of a store (specifically clicks on store logo)
        view_store_sheets = driver.find_element(By.LINK_TEXT, 'View Scan Sheets')
        view_store_sheets.click()

        view_sheet = driver.find_element(By.LINK_TEXT, 'View')
        view_sheet.click()

        add_items = driver.find_element(By.LINK_TEXT, 'Add/Remove Items')
        add_items.click()

        # Finding the username/password fields on the login page
        user_name = driver.find_element(By.NAME, "username")
        user_password = driver.find_element(By.NAME, "password")

        # Finding the login button on the login page
        submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
        
        # Entering in login information in the username/password fields
        user_name.send_keys('testAdmin2')
        user_password.send_keys('testP@S$')

        # Clicking the submit button on the page after the fields have been filled out
        submit.click()
        # Added delay to see if redirect works
        time.sleep(2)

        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[name='items']")
        # Creating empty list to track the ID's of the items that were checked
        checked_item_ids = []
        
        time.sleep(2)

        for index, checkbox in enumerate(checkboxes):
            if should_select_item(index):
                checkbox.click()
                checked_item_ids.append(int(checkbox.get_attribute("value")))
        #print(checked_item_ids)
        

        submit_button = driver.find_element(By.NAME, "Add items")
        submit_button.click()

        # Parsing the URL
        url_path = urlparse(driver.current_url).path
        #print("URL Path:", url_path)

        # Resolving the url to a valid path in urls.py
        match = resolve(url_path)
        #print("Match:", match)

        # Extracting the sheet ID from the url
        sheet_id = match.kwargs.get('sheet_id')
        #print("Sheet ID:", sheet_id)

        '''
        PRINTS CORRECT SHEET "ID = 1" - BUT, the code below results in an error that the sheet could not be found.
        I am not sure how to fix this. I assume it is because tests.py is not interacting with the database fully and I tried some things,
        but none of them worked. If I have time I will revisit this before turn-in.
        '''
        
        sheet = Sheet.objects.get(pk=sheet_id)
        items_in_sheet = sheet.items.all()
        #print(items_in_sheet)

        # Convert the items in the sheet to a list of item IDs
        items_in_sheet_ids = [item.id for item in items_in_sheet]

        # Assert that the checked items are in the sheet
        for checked_item_id in checked_item_ids:
            self.assertIn(checked_item_id, items_in_sheet_ids)

        # Assert that all items in the sheet are in the checked items
        for item_id in items_in_sheet_ids:
            self.assertIn(item_id, checked_item_ids)

        # Close the driver
        driver.quit()