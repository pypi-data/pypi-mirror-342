from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from .conversion import list_conversion

import time


class JobScraper:

    def __init__(
            self,
            domain: str,
            archive_name: str,
            query: list,
            location: str
    ):
        self.domain = domain
        self.archive_name = archive_name
        self.sheet_name = domain
        self.query = query
        self.location = location
        self.__job_archive: list = []
        self.processed_archive: list = []

        self.__options = Options()
        self.__options.add_argument('--ignore-certificate-errors')
        self.__options.add_argument('--ignore-ssl-errors')
        self.__options.add_argument('--log-level=3')
        # self.__options.add_argument('--headless')
        self.__options.add_argument('--start-maximized')
        self.__navigator = webdriver.Chrome(
            options=self.__options,
            service=Service(ChromeDriverManager().install())
        )
        self.__wait = WebDriverWait(self.__navigator, 5)
        self.__wait_linkedin = WebDriverWait(self.__navigator, 30)

    def __domain_selector(self):

        if self.domain == "linkedin":
            self.domain = "https://www.linkedin.com/jobs/"
            self.__access_linkedin()
            return
        elif self.domain == "vagas.com":
            self.domain = "https://www.vagas.com.br/"
            self.__access_vagas()
            return
        elif self.domain == "catho":
            self.domain = "https://www.catho.com.br"
            self.__access_catho()
            return
        elif self.domain == "glassdoor":
            self.domain = "https://www.glassdoor.com.br/Vaga/index.htm"
            self.__access_glassdoor()
            return
        else:
            raise SyntaxError(
                "Você não usou uma palavra-chave apropriada,"
                " consulte a documentação."
            )

    def __dupe_removal(self, archive):

        double_check_list = []

        for i in archive:
            if i[0] in double_check_list:
                pass
            else:
                self.processed_archive.append(i)
                double_check_list.append(i[0])

    def __access_linkedin(self):
        self.__navigator.get(self.domain)

        for i in self.query:
            query_input = self.__wait_linkedin.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, "div > div > div.relative > input")))
            query_input.send_keys(i)
            query_input.send_keys(Keys.ENTER)

            time.sleep(3)  # Safety timer to load elements

            # LinkedIn Lazy Load check
            while True:
                try:
                    job_list = self.__navigator.find_elements(
                        By.CSS_SELECTOR, "li div > div > a")

                    footer_element = self.__navigator.find_element(
                        By.XPATH, '//*[@id="compactfooter-about"]')

                    if footer_element:
                        break

                except NoSuchElementException:
                    self.__navigator.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'})",
                        job_list[-1])

            for j in range(len(job_list)):

                individual_job_label = job_list[j].get_attribute(
                    "aria-label")
                individual_job_link = job_list[j].get_attribute("href")
                self.__job_archive.append(
                    [individual_job_label, individual_job_link])

            self.__navigator.back()

        self.__dupe_removal(self.__job_archive)

    def __access_vagas(self):

        self.__navigator.get(self.domain)

        for i in self.query:
            query_input = self.__wait.until(EC.presence_of_element_located(
                (By.ID, "nova-home-search")))
            query_input.send_keys(i + " " + self.location)
            query_input.send_keys(Keys.ENTER)

            time.sleep(3)  # Safety timer to load elements

            try:
                job_list = self.__wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "link-detalhes-vaga")))
            except TimeoutException:
                job_list = False

            if job_list:
                for j in range(len(job_list)):
                    self.__navigator.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'})",
                        job_list[j]
                    )
                    individual_job_label = job_list[j].get_attribute("title")
                    individual_job_link = job_list[j].get_attribute("href")
                    self.__job_archive.append(
                        [individual_job_label, individual_job_link])

                self.__navigator.get(self.domain)

            else:
                self.__navigator.get(self.domain)

        self.__dupe_removal(self.__job_archive)

    def __access_catho(self):

        self.__navigator.get(self.domain)

        for i in self.query:
            query_input = self.__wait.until(EC.presence_of_element_located(
                (By.ID, "input-0")))
            query_input.send_keys(i)
            query_input.send_keys(Keys.ENTER)

            # Treating location for url manipulation
            treated_location = "-".join(self.location.split()).lower()
            self.__navigator.get(
                self.__navigator.current_url + treated_location)

            time.sleep(3)  # Safety timer to load elements

            try:
                job_list = self.__wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR,
                            "#search-result > ul > li div > h2 > a")))
            except TimeoutException:
                job_list = False

            if job_list:
                for j in range(len(job_list)):
                    self.__navigator.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'})",
                        job_list[j]
                    )
                    individual_job_title = job_list[j].get_attribute("text")
                    individual_job_link = job_list[j].get_attribute("href")
                    self.__job_archive.append(
                        [individual_job_title, individual_job_link])

                self.__navigator.get(self.domain)

            else:
                self.__navigator.get(self.domain)

        self.__dupe_removal(self.__job_archive)

    def __access_glassdoor(self):

        self.__navigator.get(self.domain)

        for i in self.query:
            query_input = self.__wait.until(EC.presence_of_element_located(
                (By.ID, "searchBar-jobTitle")))
            query_input.send_keys(i)
            location_input = self.__wait.until(EC.presence_of_element_located(
                (By.ID, "searchBar-location")))
            location_input.send_keys(self.location)
            location_input.send_keys(Keys.ENTER)

            time.sleep(3)  # Safety timer to load elements

            try:
                job_list = self.__wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "a.JobCard_jobTitle__GLyJ1")))
            except TimeoutException:
                job_list = False

            if job_list:
                for j in range(len(job_list)):
                    self.__navigator.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'})",
                        job_list[j]
                    )
                    individual_job_title = job_list[j].get_attribute("text")
                    individual_job_link = job_list[j].get_attribute("href")
                    self.__job_archive.append(
                        [individual_job_title, individual_job_link])

                self.__navigator.back()

            else:
                self.__navigator.back()

        self.__dupe_removal(self.__job_archive)

    def create_archive(self):
        self.__domain_selector()
        list_conversion(
            self.processed_archive,
            self.archive_name,
            self.sheet_name
        )
