import httpx
from lxml.etree import HTML as parse_html
import conippets.json as json

_repo_data_xpath_ = '//react-partial[@partial-name="repos-overview"]/script[@data-target="react-partial.embeddedData"]'
_code_data_xpath_ = '//react-app[@app-name="react-code-view"]/script[@data-target="react-app.embeddedData"]'

def get_repo_data(user, repo):
    url = f'https://github.com/{user}/{repo}'
    r = httpx.get(url, follow_redirects=True)
    html = parse_html(r.text)
    repo_data = html.xpath(_repo_data_xpath_)[0]
    repo_data = json.loads(repo_data.text)
    return repo_data

def createAt(user, repo):
    repo_data = get_repo_data(user, repo)
    create_time = repo_data['props']['initialPayload']['repo']['createdAt']
    return create_time

def currentOid(user, repo):
    repo_data = get_repo_data(user, repo)
    commit_id = repo_data['props']['initialPayload']['refInfo']['currentOid']
    return commit_id

def get_code_data(url):
    r = httpx.get(url, follow_redirects=True)
    html = parse_html(r.text)
    code_data = html.xpath(_code_data_xpath_)[0]
    code_data = json.loads(code_data.text)
    return code_data

def rawLines(url):
    code_data = get_code_data(url)
    code = code_data['payload']['blob']['rawLines']
    return code

def list_dir(url):
    dir_data = get_code_data(url)
    items = dir_data['payload']['tree']['items']
    return items
