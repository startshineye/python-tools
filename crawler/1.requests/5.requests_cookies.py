import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
}

url = "https://github.com/startshineye"

# cookie_str
cookies_str = "_ga=GA1.2.150843220.1593087436; _octo=GH1.1.1661912861.1656428524; _device_id=8655e7a2207006161e4c236120b39e84; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; preferred_color_mode=light; tz=Asia%2FShanghai; user_session=4hLXjFwJvyMeNKw09K1g-tQ1TKUL5IXxjAVw-EOhi9QVyh0U; __Host-user_session_same_site=4hLXjFwJvyMeNKw09K1g-tQ1TKUL5IXxjAVw-EOhi9QVyh0U; tz=Asia%2FShanghai; logged_in=yes; dotcom_user=startshineye; has_recent_activity=1; _gh_sess=GP3Xf%2BGsjP0hFpI%2B5FhW%2BpWu28%2BvIOgqvXOMAPgHx8NpEc%2FRMVlobIu%2FwZ3GzD7vNPXB67vWkckQll9ers3jGu2OmJlR2qtUVRhsuQmzPRF7dF0QQf2Pa0Q%2FO4HcRwg2yY06M3G%2B%2FM2CyI%2FY8kJWAjHqpi0PkouTmwl1aWgSI693iKYhG9%2FM4iWT3pNnVLA2wRbnt6HVwmOPKqdmWazmQTqQDc5jBQNoptemv2UbimWLG%2FWorAgIpQ0%2FELIoZKmcWCFd07vbeKzScI1Tkz9TcHILreg%2BDG2mx%2BrOwEqqZNV4glHvaRL%2Bes4u%2BJLzi4o8UDDL5u1UPg07rgcgcCpPYIQlA%2FkS4dLD7sSFPGeGHvmOx4t8sm9pz%2BOWE6JBhL%2FJ7o3fAEcXOrl9QQ%2F1IIsGY2yyt%2FwXSVnN7HvE98SOCPKvDGNZK2tyNSov077VD%2BhUPUGVKbbYBeA3BELUeeqtl7U3QNU%2BUP1wctnwb9Q7ao6nNit289eLfahTExuz%2FwyLwoPmmMNVCNpc0GWrxyKE6p%2B8laPS63gLdtxZTPs5pHV6Zya%2B0r3emhwcNlqFGTkUb5xkSNC2ueYNILutuaGHI7tkZ0aLy1ykrlUkk76DowdmvEMlMHzHn5%2FAod3Van09pxJ1jwjrL9qF2q%2BFmV8DFd8EpjGksglQH%2BHWrjaqkWRhDe9zq99DOoRPO4PbzUwPMVysSN0I9dM%2B2KTQI1ihwGMbeMwnUIEAHKm1bbMn9VXA5%2BPfcP%2BB%2BD9lxgWU0xSpEgw12NMSQTN3MyGI9Bf5K12iTo2iXQLs1Rp%2FZKrNnFvJwEgBwkz8SMzPrqroFdrbIsL%2BjA6zXEKc8tuQnVFrUXWmm5UyWebmoRm04SI%2B4dYIl0VUBYIZCLIkGYNGKfy6alvIz20qfmswKbnIEBNX46OLXFr0BXnA8BDgwqU%2BjvTjtHnUVa1x7doFWtJD2W15p4hXfBprUfHwUuRNkx4arl0zG%2BKcH4Eur085Y%2BMP6zcEWJ%2FbecYTAwezS7Wb0jOlvZVYmsmIyJ6LQXl8kB3yhgm5%2FJHQHtGwnN09Yo7W4zyijR7dAlG5wAU%2B%2BJZWfMIFodIUEukNXF1nRXHJ2u8TXrOvhua14PIJ6cQCZwTRWpFwbY9z--To4%2Bn6fmogIVXjJV--Ju9kJHbmu11GsQ7mkE2gnw%3D%3D"

# 构造cookies字典
cookies_dict = {}

cookies_list = cookies_str.split('; ')

cookies_dict = {cookie.split("=")[0]: cookie.split("=")[-1] for cookie in cookies_list}

'''
for cookie in cookies_list:
    # _ga=GA1.2.150843220.1593087436
    cookies_dict[cookie.split("=")[0]] = cookie.split("=")[-1]
'''

print(cookies_dict)
res = requests.get(url, headers=headers, cookies=cookies_dict)

with open("../cookies.html", "wb") as f:
    f.write(res.content)
