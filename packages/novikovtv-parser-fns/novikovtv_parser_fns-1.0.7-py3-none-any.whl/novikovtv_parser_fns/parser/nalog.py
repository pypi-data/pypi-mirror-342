import asyncio
from typing import Optional, Callable, Tuple

import aiohttp
from bs4 import BeautifulSoup, Tag
from typing_extensions import deprecated

from novikovtv_parser_fns.parser.captcha.solver import CaptchaSolver
from novikovtv_parser_fns.parser.config import get_parse_ext_config, get_excel_config
from novikovtv_parser_fns.parser.constants import RPS, SEARCH_PAGE_RANGE, ITERATION_DELAY_IN_SECONDS
from novikovtv_parser_fns.parser.exceptions import SearchBadParsing, SearchIDCaptchaError, SearchIDInvalidError, \
    SkipIterationError
from novikovtv_parser_fns.parser.models.search import SearchRequest, SearchResult, Organization


class NalogParserBase(object):
    MAX_ATTEMPTS = 20

    def __init__(self):
        self.semaphore = asyncio.Semaphore(RPS)
        self.max_attempts = self.__class__.MAX_ATTEMPTS


class NalogSearchParserWithCaptchaSolver(NalogParserBase):
    API_FNS_CAPTCHA_URL = "https://pb.nalog.ru/captcha-dialog.html"

    def __init__(self, api_url: str, get_params_function: Callable):
        super().__init__()
        self.captcha_url = self.__class__.API_FNS_CAPTCHA_URL

        self.get_params_function: Callable = get_params_function
        self.api_url = api_url

    async def _solve_captcha(self, **kwargs) -> str:
        attempt = 0
        while attempt < self.max_attempts:
            attempt += 1
            print(f"attempt: {attempt}")
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.captcha_url) as resp:
                        html_text = await resp.text()

                        soup = BeautifulSoup(html_text, 'html.parser')
                        captcha: Tag = soup.find('img')
                        if captcha is None:
                            print("captcha not found")
                            return

                        captcha_token: str = captcha['src'].split('&')[0].replace('/static/captcha.bin?a=', '')

                async with aiohttp.ClientSession() as session:
                    async with session.get("https://pb.nalog.ru" + captcha['src']) as resp:
                        captcha_img = await resp.read()
                        captcha_solver = CaptchaSolver(captcha_img)
                        captcha_recognition = captcha_solver.solve()

                if not captcha_token or not captcha_recognition:
                    raise SkipIterationError

                async with aiohttp.ClientSession() as session:
                    async with session.post("https://pb.nalog.ru/captcha-proc.json", params={
                        'captcha': captcha_recognition,
                        "captchaToken": captcha_token,
                    }) as resp:
                        if not resp.ok:
                            raise SkipIterationError
                        captcha_text = await resp.text()
                        captcha_text = captcha_text.replace('\"', '')

                search_id = await self._get_search_id(**kwargs, captcha=captcha_text)
                return search_id
            except SkipIterationError as sie:
                pass
            except Exception as e:
                print("NalogParserApi._solve_captcha", e.__class__, e)

            await asyncio.sleep(ITERATION_DELAY_IN_SECONDS)

    async def try_get_search_id_through_captcha(self, **kwargs) -> Optional[Tuple[str, dict]]:
        try:
            search_id, params = await self._get_search_id(**kwargs)
            return search_id, params
        except SearchIDCaptchaError as e:
            return await self._solve_captcha(**kwargs)

    async def _get_search_id(self, **kwargs) -> Optional[Tuple[str, dict]]:
        params: dict = self.get_params_function(**kwargs)
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, params=params) as resp:
                    search: SearchRequest = SearchRequest(**await resp.json())
                    if search.ERROR is not None:
                        raise SearchIDCaptchaError(search)

                    return search.id, params


class NalogParser(NalogParserBase):
    API_FNS_URL = "https://pb.nalog.ru/search-proc.json"

    def __init__(self):
        super().__init__()
        self.api_url = self.__class__.API_FNS_URL
        self.results: list[SearchResult] = []

    async def search(self, query: str) -> list[SearchResult]:
        nalog_search_parser = NalogSearchParserWithCaptchaSolver(self.api_url, get_parse_ext_config)
        task_ids: list = [
            asyncio.create_task(nalog_search_parser.try_get_search_id_through_captcha(query=query, page=page)) for page
            in SEARCH_PAGE_RANGE
        ]
        search_id_list_plain: list[Optional[Tuple[str, dict]]] = await asyncio.gather(*task_ids)
        search_id_list = [_search_id[0] for _search_id in search_id_list_plain if id]
        if not search_id_list:
            raise SearchIDInvalidError()

        task: list = [asyncio.create_task(self.__try_search(_search_id)) for _search_id in search_id_list]
        results: list[Optional[SearchResult]] = await asyncio.gather(*task)

        self.results: list[SearchResult] = [res_ for res_ in results if res_ is not None]
        return self.results

    async def __try_search(self, search_id: str) -> Optional[SearchResult]:
        try:
            res: SearchResult = await self.__search(search_id)
            if not res:
                print(f"No results for {search_id}")
            return res
        except Exception as e:
            print("NalogParser.__try_search", e.__class__.__name__, e)

    async def __search(self, search_id: str) -> Optional[SearchResult]:
        params = {
            "id": search_id,
            "method": "get-response",
        }

        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                iterations: int = 0
                while iterations <= self.max_attempts:
                    iterations += 1
                    try:
                        async with session.post(self.api_url,
                                                params=params,
                                                headers={
                                                    "Connection": "keep-alive",
                                                    "Content-Type": "application/json",
                                                    "Keep-Alive": "timeout=20"
                                                }) as resp:
                            search_res_plain = await resp.json()
                            if search_res_plain:
                                break
                    except Exception as e:
                        print("NalogParser.__search", e)

                    await asyncio.sleep(ITERATION_DELAY_IN_SECONDS)

                if iterations > self.max_attempts:
                    raise SearchBadParsing("Iteration limit reached")

                search_res: SearchResult = SearchResult(**search_res_plain)
                return search_res


@deprecated("Experimental. Now use NalogParser")
class NalogExcelParser(NalogParserBase):
    MAX_ITERATIONS = 10
    API_DOWNLOAD_FNS_URL = "https://pb.nalog.ru/download-proc.json"

    def __init__(self):
        super().__init__()
        self.api_url = self.__class__.API_DOWNLOAD_FNS_URL
        self.max_iterations = self.__class__.MAX_ITERATIONS
        self.results: list[SearchResult] = []

    async def search(self, query: str) -> list[SearchResult]:
        nalog_search_parser_ext = NalogSearchParserWithCaptchaSolver(NalogParser.API_FNS_URL, get_parse_ext_config)
        ext_search_id, ext_params = await nalog_search_parser_ext.try_get_search_id_through_captcha(query=query,
                                                                                                    page="1")

        nalog_search_parser = NalogSearchParserWithCaptchaSolver(self.api_url, get_excel_config)
        search_id, params = await nalog_search_parser.try_get_search_id_through_captcha(ext_params=ext_params)
        if not search_id:
            return []

        download_params = {
            "id": search_id,
            "method": "check-search-excel-response",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url,
                                    params=download_params,
                                    headers={"Content-Type": "application/x-www-form-urlencoded"}) as resp:
                print(await resp.json())

    async def __try_search(self, search_id: str) -> Optional[SearchResult]:
        try:
            res: SearchResult = await self.__search(search_id)
            if not res:
                print(f"No results for {search_id}")
            return res
        except Exception as e:
            print("NalogParser.__try_search", e.__class__.__name__, e)

    async def __search(self, search_id: str) -> Optional[SearchResult]:
        params = {
            "id": search_id,
            "method": "get-response",
        }

        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                iterations: int = 0
                while iterations <= self.max_iterations:
                    iterations += 1
                    try:
                        async with session.post(self.api_url,
                                                params=params,
                                                headers={"Content-Type": "application/json"}) as resp:
                            search_res_plain = await resp.json()
                            if search_res_plain:
                                break
                    except Exception as e:
                        print("NalogParser.__search", e)

                    await asyncio.sleep(ITERATION_DELAY_IN_SECONDS)

                if iterations >= self.max_iterations:
                    raise SearchBadParsing()

                search_res: SearchResult = SearchResult(**search_res_plain)
                return search_res


def make_csv_text(results: list[SearchResult]) -> str:
    csv_text: str = Organization.get_headers() + "\n"
    for result in results:
        for organization in result.ul.data:
            csv_text += organization.get_csv() + "\n"

    return csv_text


async def main():
    parser = NalogParser()
    res = await parser.search("")
    with open("out.csv", "w", encoding="utf-8") as file:
        file.write(make_csv_text(res))


if __name__ == '__main__':
    asyncio.run(main())
