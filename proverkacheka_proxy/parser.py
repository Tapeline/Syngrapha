import tempfile
import time
from logging import Logger

from opentelemetry import trace
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import bs4

tracer = trace.get_tracer(__name__)


class ProverkaChekaComClient:
    def __init__(self, logger: Logger):
        self.logger = logger
        opts = Options()
        opts.add_argument("--disable-gpu")
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("start-maximized")
        opts.add_argument("disable-infobars")
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument("--disable-extensions")
        user_data_dir = tempfile.mkdtemp()
        opts.add_argument(f"--user-data-dir={user_data_dir}")
        logger.info("creating chrome webdriver")
        self.driver = webdriver.Chrome(options=opts)

    def get_check_html(self, fn, fd, fp, s, d, t):
        start = time.perf_counter()
        self.logger.info("navigating to proverkachecka.com")
        with tracer.start_as_current_span("navigate"):
            self.driver.get("https://proverkacheka.com/")
        fn_box = self.driver.find_element(By.ID, "b-checkform_fn")
        fd_box = self.driver.find_element(By.ID, "b-checkform_fd")
        fp_box = self.driver.find_element(By.ID, "b-checkform_fp")
        s_box = self.driver.find_element(By.ID, "b-checkform_s")
        d_box = self.driver.find_element(By.ID, "b-checkform_date")
        t_box = self.driver.find_element(By.ID, "b-checkform_time")
        check_typ = Select(self.driver.find_element(
            By.CSS_SELECTOR, "#b-checkform_n"
        ))
        check_typ.select_by_value("1")
        send_btn = self.driver.find_element(
            By.CSS_SELECTOR, "#b-checkform_tab-props button:nth-child(1)"
        )
        self.logger.info("found all elements, sending data")
        fn_box.send_keys(str(fn))
        fd_box.send_keys(str(fd))
        fp_box.send_keys(str(fp))
        d_box.send_keys(d)
        t_box.send_keys(t)
        s_box.send_keys(str(s))
        self.driver.execute_script(
            "document.getElementById('b-checkform_time').scrollIntoView()"
        )
        send_btn.click()
        self.logger.info("waiting for response")
        try:
            with tracer.start_as_current_span("response_wait"):
                element = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.CSS_SELECTOR, "table.b-check_table tbody")
                    )
                )
            end = time.perf_counter()
            self.logger.info(
                "got a response", extra={"time_ms": (end - start) * 1000}
            )
            return element.get_attribute("innerHTML")
        except:
            self.logger.info("timeout!")
            return None

    def parse_html_contents(self, html: str):
        self.logger.info("parsing html")
        soup = bs4.BeautifulSoup(html)
        [
            [store_name],
            [store_addr],
            _,  # INN
            _,  # filler
            [date_time],
            _,  # ch No
            _,  # shift No
            _,  # cashier
            _,
            _,  # filler,
            *items,
            [_, _, total],
            _,  # cash
            _,  # card
            _,  # tax
            _,  # tax
            _,  # kkt No
            _,  # serial No
            _,  # fn
            _,  # fd
            _,  # fp
            _,  # qr
        ] = [list(elem.children) for elem in soup.find_all("tr")]
        self.logger.info("unpacked contents")
        store_name = store_name.get_text()
        store_addr = store_addr.get_text()
        total = total.get_text()
        items = [
            (
                item[1].get_text(),
                item[2].get_text(),
                item[3].get_text(),
                item[4].get_text()
            )
            for item in items
        ]
        self.logger.info("parsed")
        return store_name, store_addr, total, items

    def close(self):
        self.logger.info("driver closing")
        self.driver.close()
        self.driver.quit()


#client = ProverkaChekaComClient()
#_ = client.get_check_html(
#    fn=7281440701375636,
#    fd=76212,
#    fp=3396038878,
#    s="512.40",
#    d="02072024",
#    t="1944"
#)
#html = client.get_check_html(
#    fn=7281440701375636,
#    fd=76212,
#    fp=3396038878,
#    s="512.40",
#    d="02072024",
#    t="1944"
#)
#client.close()
#print(client.parse_html_contents(html))
