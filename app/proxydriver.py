from selenium import webdriver
from random import choice
from webdriver_manager.chrome import ChromeDriverManager
import zipfile,os
from selenium import webdriver

def get_chromedriver(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS, use_proxy=False, user_agent=None):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    if use_proxy:
        pluginfile = f'proxy_auth_plugin{PROXY_HOST}.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json",  manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    return driver

def convert_table(lines):
    def from_ascii():
        out = []
        first, header, third, *body, last = lines
        first = first.translate(str.maketrans({'-': '━', '+': '┯'}))
        out.append(f'┏{first[1:-1]}┓')
        header = header.translate(str.maketrans({'|': '│'}))
        out.append(f'┃{header[1:-1]}┃')
        third = third.translate(str.maketrans({'-': '─', '+': '┼'}))
        out.append(f'┠{third[1:-1]}┨')
        for line in body:
            line = line.translate(str.maketrans({'|': '│'}))
            line = line.replace('yes', ' ✓ ')
            out.append(f'┃{line[1:-1]}┃')
        last = last.translate(str.maketrans({'-': '━', '+': '┷'}))
        out.append(f'┗{last[1:-1]}┛')
        return '\n'.join(out)

if __name__ == '__main__':
    input_lines = []
    try:
        while True:
            input_lines.append(input())
    except EOFError:
        pass
    print(convert_table(input_lines))