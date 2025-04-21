#  The MIT License (MIT)
#
#  Copyright (c) 2025. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
import json
import logging
import os
import random
from time import sleep

import pandas as pd
import requests
from playwright.sync_api import sync_playwright

from sc_qcc_crawler.config.config import Config
from sc_qcc_crawler.parser.detail_parser import DetailParser
from sc_qcc_crawler.parser.summary_parser import SummaryParser


class HtmlSearcher:

    def __init__(self, *, config: Config):
        self._config = config
        self._encoding = self._config.get("spider.qcc.encoding")
        self._login_url = self._config.get("spider.qcc.login_url")
        self._search_url = self._config.get("spider.qcc.search_url")
        self._search_param_key = self._config.get("spider.qcc.search_param_key")
        self._firm_detail_url = self._config.get("spider.qcc.firm_detail_url")
        self._user_agent_key = self._config.get("spider.qcc.user_agent_key")
        self._user_agent_url = self._config.get("spider.qcc.user_agent_url")
        self._user_agent_expression = self._config.get("spider.qcc.user_agent_expression")
        self._cookie_filename = self._config.get("spider.qcc.cookie_filename")
        self._test_company_id = self._config.get("spider.qcc.test_company_id")
        self._delay = int(self._config.get("spider.qcc.delay"))
        self._login_success_selector = self._config.get("spider.qcc.login_success_selector")
        self._timeout = int(self._config.get("spider.qcc.timeout"))
        self._company_filename = self._config.get("spider.qcc.company_filename")

        self._result_directory = self._config.get("spider.qcc.result_directory")
        if not os.path.exists(self._result_directory):
            os.makedirs(self._result_directory)
        self._result_file_search_result = self._config.get("spider.qcc.result_file_search_result")
        self._result_file_detail = self._config.get("spider.qcc.result_file_detail")
        self._result_file_analysis = self._config.get("spider.qcc.result_file_analysis")
        self._sheet_name_analysis = self._config.get("spider.qcc.sheet_name_analysis")
        self._col_name_shareholder = self._config.get("spider.qcc.col_name_shareholder")
        self._col_name_company = self._config.get("spider.qcc.col_name_company")

        self._summary_parser = SummaryParser(config=self._config)
        self._detail_parser = DetailParser(config=self._config)

        self._session = requests.Session()

        self._saved_cookies = list()
        saved_cookies = self._config.get("spider.qcc.saved_cookies")
        if saved_cookies and type(saved_cookies) is list:
            self._saved_cookies.extend(saved_cookies)

        self._load_cookies()
        self._headers = dict()
        # 读取配置文件的headers，如果不为空，则更新配置
        headers_dict = self._config.get("spider.qcc.headers")
        if headers_dict and type(headers_dict) is dict:
            self._headers.update(headers_dict)

    def _load_cookies(self):
        cookies = list()
        if os.path.exists(self._cookie_filename):
            with open(self._cookie_filename, "r", encoding=self._encoding) as f:
                cookies = json.load(f)

        # 将cookie保存到session中
        for cookie in cookies:
            if cookie['name'] in self._saved_cookies:
                self._session.cookies.set(cookie['name'], cookie['value'])

    def _check_cookie_status(self):
        response = self._session.get(
            self._firm_detail_url.format(self._test_company_id),
            headers=self._headers,
        )
        logging.getLogger(__name__).info(f"测试Cookie状态码: {response.status_code}")
        return response.status_code == 200

    def load_user_agent(self, p):
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        # 获取浏览器的 UA
        page = context.new_page()
        page.goto(self._user_agent_url)
        self._headers[self._user_agent_key] = page.evaluate(self._user_agent_expression)
        # 写回配置文件
        self._config.save()

    def login_and_save_cookies(self):
        if os.path.exists(self._cookie_filename) and self._check_cookie_status():
            logging.getLogger(__name__).info(f"{self._cookie_filename} 文件存在且有效，无需重新登录")
            return
        logging.getLogger(__name__).info(f"{self._cookie_filename} 文件失效，需重新登录")
        # 如果cookie文件不存在，则登录并保存cookie文件
        with sync_playwright() as p:
            # self.load_user_agent(p)

            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            logging.getLogger(__name__).info(f"打开登录页面：{self._login_url}")
            page.goto(self._login_url)

            # 等待登录成功，出现“消息数量”元素
            page.wait_for_selector(selector=self._login_success_selector, timeout=self._timeout, state="attached")

            cookies = list()
            for cookie in context.cookies():
                if cookie.get("name") in self._saved_cookies:
                    cookies.append(cookie)
            # 将cookie保存到文件
            with open(self._cookie_filename, "w") as f:
                json.dump(cookies, f, indent=2)

            self._load_cookies()

            logging.getLogger(__name__).info(f"登录完成，cookie 已保存到：{self._cookie_filename}")
            browser.close()

    def _download_delay(self) -> float:
        return random.uniform(0.5 * self._delay, 1.5 * self._delay)

    def search_company(self, *, company_name):
        target_filename = os.path.join(self._result_directory, f"{company_name}-{self._result_file_detail}.html")
        if os.path.exists(target_filename):
            logging.getLogger(__name__).info(f"{target_filename} 文件已存在，无需查询")
            self._detail_parser.parse_file(html_file=target_filename)
            return
        params = {
            self._search_param_key: company_name,
        }
        response = self._session.get(
            self._search_url,
            params=params,
            headers=self._headers,
        )
        logging.getLogger(__name__).info(f"搜索公司信息状态码: {response.status_code}")
        if response.status_code != 200:
            return
        # 将响应内容保存到文件
        target_filename = os.path.join(self._result_directory, f"{company_name}-{self._result_file_search_result}.html")
        with open(target_filename, "w", encoding=self._encoding) as f:
            f.write(response.text)
        self._summary_parser.parse_content(content=response.text)
        if company_name in self._summary_parser.get_companies():
            logging.getLogger(__name__).info(f"{company_name} 存在")
            key_no = self._summary_parser.get_key_no(company_name=company_name)
            sleep(self._download_delay())
            self.get_company_detail(company_name=company_name, key_no=key_no)

    def get_company_detail(self, *, company_name, key_no):
        response = self._session.get(
            self._firm_detail_url.format(key_no),
            headers=self._headers,
        )
        logging.getLogger(__name__).info(f"查询公司详情状态码: {response.status_code}")
        if response.status_code != 200:
            return
        # 将响应内容保存到文件
        target_filename = os.path.join(self._result_directory, f"{company_name}-{self._result_file_detail}.html")
        with open(target_filename, "w", encoding=self._encoding) as f:
            f.write(response.text)
        self._detail_parser.parse_content(content=response.text)

    def search(self):
        if not os.path.exists(self._company_filename):
            logging.getLogger(__name__).info(f"{self._company_filename} 文件不存在，请确认")
            return
        with open(self._company_filename, 'r', encoding=self._encoding) as f:
            for line in f:
                company = line.strip()
                if len(company) == 0:
                    continue
                self.search_company(company_name=company)
                sleep(self._download_delay())

        logging.getLogger(__name__).info("公司列表 {}".format(self._summary_parser.get_companies()))
        logging.getLogger(__name__).info("股东持股情况 {}".format(self._detail_parser.get_stock_name_companies()))
        # 查找重复的 StockName
        target_filename = os.path.join(self._result_directory, self._result_file_analysis)
        df = pd.DataFrame(columns=[
            self._col_name_shareholder,
            self._col_name_company,
        ])
        for stock_name, companies in self._detail_parser.get_stock_name_companies().items():
            if len(companies) > 1:
                for company_name in companies:
                    row = {
                        self._col_name_shareholder: stock_name,
                        self._col_name_company: company_name,
                    }
                    df.loc[len(df)] = row
        # 写入文件
        if not df.empty:
            with pd.ExcelWriter(target_filename) as excel_writer:
                df.to_excel(
                    excel_writer,
                    sheet_name=self._sheet_name_analysis,
                    index=False
                )
        else:
            logging.getLogger(__name__).info("没有股东持股多家公司的情况")
