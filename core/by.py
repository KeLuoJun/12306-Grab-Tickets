import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
from config.settings import STARTS, ENDS, DTIME, ORDER, USERS, XB, PZ, STUDENT, EXECUTABLE_PATH

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Byticket(object):
    executable_path = EXECUTABLE_PATH
    starts = STARTS
    ends = ENDS
    dtime = DTIME
    order = ORDER
    users = USERS
    xb = XB
    pz = PZ
    student = STUDENT

    # URLs
    ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc"
    login_url = "https://kyfw.12306.cn/otn/resources/login.html"
    initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
    # buy_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

    def __init__(self):
        options = Options()
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        service = Service(self.executable_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        try:
            self.driver.get(self.login_url)

            account = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="login-box"]//li[@class="login-hd-account"]/a')))
            account.click()
            logging.info("请扫码登录！")
            
            # 显式等待登录成功
            WebDriverWait(self.driver, 60).until(
                EC.url_to_be(self.initmy_url)
            )
            logging.info("登录成功！")
        except Exception as e:
            logging.error("登录过程中发生错误: %s", e)
            raise

    def set_cookies(self):
        try:
            self.driver.add_cookie({"name": "_jc_save_fromStation", "value": self.starts})
            self.driver.add_cookie({"name": "_jc_save_toStation", "value": self.ends})
            self.driver.add_cookie({"name": "_jc_save_fromDate", "value": self.dtime})
            self.driver.refresh()
        except Exception as e:
            logging.error("设置Cookie时发生错误: %s", e)
            raise

    def start(self):
        try:
            # self.login()
        
            # 跳转到购票页面
            self.driver.get(self.ticket_url)
            self.set_cookies()

            count = 0
            while True:
                if count > 15:
                    logging.error("超过最大查询次数，退出程序。")
                    return False

                # 点击查询按钮
                try:
                    query_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "query_ticket")))
                    query_btn.click()
                    count += 1
                    logging.info(f"第 {count} 次查询...")

                    # 获取所有预订按钮
                    book_btns = self.wait.until(
                        EC.presence_of_all_elements_located((By.XPATH, '//tbody[@id="queryLeftTable"]/tr/td[@class="no-br"]'))
                    )

                    # 获取所有车次
                    trains = self.wait.until(
                        EC.presence_of_all_elements_located((By.XPATH, '//a[@class="number"]'))
                    )

                    if self.order == 0:
                        for o, btn in enumerate(book_btns):
                            self.order = o + 1
                            btn.find_element(By.XPATH, './a').click()
                            time.sleep(0.5)
                    else:
                        book_btns[self.order-1].find_element(By.XPATH, './a').click()

                    # 切换到新窗口
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    break
                
                except Exception as e:
                    logging.warning("尚未开始预订，继续查询...")
                    time.sleep(0.5)
                    continue

            # 选择乘车人
            try:
                user_checks = self.wait.until(
                    EC.visibility_of_all_elements_located((By.XPATH, '//ul[@id="normal_passenger_id"]/li'))
                )
                for user in self.users:
                    for check in user_checks:
                        label = check.find_element(By.XPATH, './label')
                        if user in label.text:
                            check.find_element(By.XPATH, './input').click()
                            break
            except Exception as e:
                logging.error("选择乘车人时发生错误: %s", e)
                raise

            # 关闭可能遮挡的弹出框
            try:
                if self.student:
                    close_btn = self.wait.until(EC.element_to_be_clickable((By.ID, 'dialog_xsertcj_ok')))
                else:
                    close_btn = self.wait.until(EC.element_to_be_clickable((By.ID, 'dialog_xsertcj_cancel')))
                close_btn.click()
            except Exception as e:
                logging.error("关闭弹出框时发生错误: %s", e)
                raise

            # 选择席别
            try:
                seat_select = Select(self.driver.find_element(By.XPATH, '//select[@id="seatType_1"]'))
                options = seat_select.options
                for option in options:
                    if self.xb in option.text:
                        seat_select.select_by_visible_text(option.text)
                        break
            except Exception as e:
                logging.error("选择席别时发生错误: %s", e)
                raise

            # 提交订单
            try:
                submit_btn = self.driver.find_element(By.ID, "submitOrder_id")
                submit_btn.click()

                # 确认选座
                confirm_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "qr_submit_id")))
                confirm_btn.click()
                time.sleep(2)

                logging.info("抢票成功，请尽快支付！")
                return True
            except Exception as e:
                logging.error("提交订单时发生错误: %s", e)
                raise

        except Exception as e:
            logging.error("主流程发生错误: %s", e)
            return False
        finally:
            self.driver.quit()

if __name__ == '__main__':
    try:
        bt = Byticket()
        bt.start()
    except Exception as e:
        logging.error("程序启动时发生错误: %s", e)
