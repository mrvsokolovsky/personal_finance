from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import mysql.connector
from mysql.connector import Error

chrome_options = Options()
chrome_options.add_argument("--headless")
PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH , options=chrome_options)


class Receipt:
    def __init__(self, fn, fd, fpd, date, time, paid):
        self.fn = fn
        self.fd = fd
        self.fpd = fpd
        self.date = date
        self.time = time
        self.paid = paid

    def get_receipt(self):
        driver.get('https://proverkacheka.com/')
        fn = driver.find_element_by_id('b-checkform_fn')
        fd = driver.find_element_by_id('b-checkform_fd')
        fpd = driver.find_element_by_id('b-checkform_fp')
        dt = driver.find_element_by_id('b-checkform_date')
        tm = driver.find_element_by_id('b-checkform_time')
        cost = driver.find_element_by_id('b-checkform_s')
        op_type = driver.find_element_by_id('b-checkform_n')

        fn.send_keys(self.fn)
        fd.send_keys(self.fd)
        fpd.send_keys(self.fpd)
        cost.send_keys(self.paid)
        dt.send_keys(self.date)
        tm.send_keys(self.time)

        op_type.send_keys(Keys.ARROW_DOWN)

        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.PAGE_DOWN)

        button = driver.find_element_by_class_name('b-checkform_btn-send')
        button.click()

        wait = WebDriverWait(driver, 20, 0.3, ignored_exceptions=[EC.NoSuchElementException])
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'b-check_item')))
        prods = driver.find_elements_by_class_name('b-check_item')
        # driver.close()
        return prods

    def file_append(self, prods):
        with open('products.txt', 'a+') as products:
            products.write(self.date[:2] + '.' + self.date[2:4] + '.' + self.date[4:] + '\n')
            products.write(self.time[:2] + ':' + self.time[2:] + '\n\n')
            for prod in prods:
                products.write(prod.text + '\n')
            products.write('\n' + '____________________' + '\n\n')
        driver.close()

    def db_connect(self, prods):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='my_db',
                                                 user='root',
                                                 password='')

            if connection.is_connected():
                print("You're connected to database")
                cursor = connection.cursor()
                string = open('barcode_result.txt', 'r').read()
                sep = '-'
                insert_query = 'INSERT INTO my_db.receipt(Purchase_date, Name, Price) VALUES (%s, %s, %s)'
                date = string[2:6] + sep + string[6:8] + sep + string[8:10]
                for prod in prods:
                    prod = prod.text.split(' ')
                    price = prod[-1]
                    prod[0] = ''
                    prod[-3:] = ['', '', '']
                    prod = ' '.join(prod)
                    record = (date, prod, float(price))
                    cursor.execute(insert_query, record)
                    connection.commit()

                print(str(len(prods)), "product(s) added successfully")
                driver.close()
                cursor.close()
                connection.close()

        except Error as e:
            print("Error while connecting to MySQL", e)
