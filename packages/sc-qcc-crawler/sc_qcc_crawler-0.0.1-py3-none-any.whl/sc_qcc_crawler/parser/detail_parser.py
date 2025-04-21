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

#  The MIT License (MIT)
#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
import json
import logging
import re
from collections import defaultdict
from sc_qcc_crawler.config.config import Config


class DetailParser:

    def __init__(self, *, config: Config):
        self._config = config
        self._encoding = self._config.get("spider.qcc.encoding")
        # 用于记录每个 StockName 是什么公司（company.companyDetail.Name）
        self._stock_name_companies = defaultdict(set)

    def get_stock_name_companies(self):
        return self._stock_name_companies

    def parse_content(self, *, content):
        # 正则提取 window.__INITIAL_STATE__ 后的 JSON 字符串
        match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?})\s*;', content, re.DOTALL)
        if not match:
            logging.getLogger(__name__).error("未找到匹配的 JSON 字符串")
            return False
        json_str = match.group(1)
        try:
            data = json.loads(json_str)

            try:
                company_name = data["company"]["companyDetail"]["Name"]
            except (KeyError, TypeError):
                company_name = None
            if not company_name:
                logging.getLogger(__name__).error("未找到 company.companyDetail.Name")
                return False
            try:
                partners = data["company"]["companyDetail"]["Partners"]
            except (KeyError, TypeError):
                partners = []
            if len(partners) == 0:
                logging.getLogger(__name__).error("company.companyDetail.Partners 为空")
                return False
            for partner in partners:
                stock_name = partner.get("StockName", "")
                if stock_name:
                    self._stock_name_companies[stock_name].add(company_name)
            return True
        except json.JSONDecodeError as e:
            logging.getLogger(__name__).error("JSON 解码失败：", e)
            return False

    def parse_file(self, *, html_file):
        # 读取 HTML 文件内容
        with open(html_file, "r", encoding=self._encoding) as f:
            html_content = f.read()
            self.parse_content(content=html_content)
