import re


class Extractors:
    @staticmethod
    def get_last_page(s):
        match = re.search(r'page=(\d+)', s)

        if match:
            page_number = int(match.group(1))
            return page_number
        else:
            return None


if __name__ == "__main__":
    s = "/browse/frozen?page=24'"
    extractor = Extractors()
    page_no = extractor.get_last_page(s)
    print(page_no)