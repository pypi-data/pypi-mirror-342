from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from conversion import list_conversion  # type: ignore

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
        self.job_archive: list = []
        self.processed_archive: list = []

        self.options = Options()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_argument('--log-level=3')
        self.navigator = webdriver.Chrome(
            options=self.options,
            service=Service(ChromeDriverManager().install())
        )
        self.wait = WebDriverWait(self.navigator, 18)

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
            raise NotImplementedError(
                "Você não usou uma palavra-chave apropriada."
            )

    def __dupe_removal(self, archive):

        self.processed_archive = list(
            set(list(tuple(x) for x in archive)))

    def __access_linkedin(self):
        self.navigator.get(self.domain)

        for i in self.query:
            query_input = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div > div > div.relative > input")))
            query_input.send_keys(i)
            query_input.send_keys(Keys.ENTER)

            time.sleep(3)  # Safety timer to load elements

            try:
                job_list = self.navigator.find_elements(
                    By.CSS_SELECTOR, "li div > div > a")
            except TimeoutException:
                job_list = False

            if job_list:
                for j in range(len(job_list)):
                    self.navigator.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'})",
                        job_list[j]
                    )
                    individual_job_label = job_list[j].get_attribute(
                        "aria-label")
                    individual_job_link = job_list[j].get_attribute("href")
                    self.job_archive.append(
                        [individual_job_label, individual_job_link])

                self.navigator.back()

            else:
                self.navigator.back()

        self.__dupe_removal(self.job_archive)

    def __access_vagas(self):

        self.navigator.get(self.domain)

        for i in self.query:
            query_input = self.wait.until(EC.presence_of_element_located(
                (By.ID, "nova-home-search")))
            query_input.send_keys(i + " " + self.location)
            query_input.send_keys(Keys.ENTER)

            time.sleep(3)  # Safety timer to load elements

            try:
                job_list = self.wait.until(EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "link-detalhes-vaga")
                ))
            except TimeoutException:
                job_list = False

            if job_list:
                for j in range(len(job_list)):
                    self.navigator.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'})",
                        job_list[j]
                    )
                    individual_job_label = job_list[j].get_attribute("title")
                    individual_job_link = job_list[j].get_attribute("href")
                    self.job_archive.append(
                        [individual_job_label, individual_job_link])

                self.navigator.get(self.domain)

            else:
                self.navigator.get(self.domain)

        self.__dupe_removal(self.job_archive)

    def __access_catho(self):

        self.navigator.get(self.domain)

        for i in self.query:
            query_input = self.wait.until(EC.presence_of_element_located(
                (By.ID, "input-0")))
            query_input.send_keys(i)
            query_input.send_keys(Keys.ENTER)

            # Treating location for url manipulation
            treated_location = "-".join(self.location.split()).lower()
            self.navigator.get(self.navigator.current_url + treated_location)

            time.sleep(3)  # Safety timer to load elements

            try:
                job_list = self.wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "#search-result > ul > li div > h2 > a")
                ))
            except TimeoutException:
                job_list = False

            if job_list:
                for j in range(len(job_list)):
                    self.navigator.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'})",
                        job_list[j]
                    )
                    individual_job_title = job_list[j].get_attribute("text")
                    individual_job_link = job_list[j].get_attribute("href")
                    self.job_archive.append(
                        [individual_job_title, individual_job_link])

                self.navigator.get(self.domain)

            else:
                self.navigator.get(self.domain)

        self.__dupe_removal(self.job_archive)

    def __access_glassdoor(self):

        self.navigator.get(self.domain)

        for i in self.query:
            query_input = self.wait.until(EC.presence_of_element_located(
                (By.ID, "searchBar-jobTitle")))
            query_input.send_keys(i)
            location_input = self.wait.until(EC.presence_of_element_located(
                (By.ID, "searchBar-location")))
            location_input.send_keys(self.location)
            location_input.send_keys(Keys.ENTER)

            time.sleep(3)  # Safety timer to load elements

            try:
                job_list = self.wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "a.JobCard_jobTitle__GLyJ1")))
            except TimeoutException:
                job_list = False

            if job_list:
                for j in range(len(job_list)):
                    self.navigator.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'})",
                        job_list[j]
                    )
                    individual_job_title = job_list[j].get_attribute("text")
                    individual_job_link = job_list[j].get_attribute("href")
                    self.job_archive.append(
                        [individual_job_title, individual_job_link])

                self.navigator.back()

            else:
                self.navigator.back()

        self.__dupe_removal(self.job_archive)

    def create_archive(self):
        self.__domain_selector()
        list_conversion(
            self.processed_archive,
            self.archive_name,
            self.sheet_name
        )
