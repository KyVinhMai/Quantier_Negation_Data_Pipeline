# website_exceptions = []
# with open("cursed_websites.txt", "r") as f:
#     for line in f:
#         website_exceptions.append(line.rstrip())
#
# filetype_exceptions = []
# with open("cursed_filetypes.txt", "r") as f:
#     for line in f:
#         filetype_exceptions.append(line.rstrip())
#
#
# def check_url(url:str) -> bool:
#     for web_exc in website_exceptions:
#         if web_exc in url:
#             return False
#
#     return True
#
# def check_filetype(url: str) -> bool:
#     for exc in filetype_exceptions:
#         if exc in url:
#             return False
#
#     return True