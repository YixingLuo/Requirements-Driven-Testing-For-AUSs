
from lxml import etree
import requests


# 根据关键词获取项目列表
def get_repos_list(key_words):
    # 初始化列表
    repos_list = []
    # 默认
    for i in range(1, 100):
        url = 'https://github.com/search?p=' + str(i) + '&q=' + key_words + '&type=repositories'
        response = requests.get(url)
        # 获取页面源码
        page_source = response.text
        # print(page_source)
        tree = etree.HTML(page_source)
        # 获取项目超链接
        arr = tree.xpath('//*[@class="f4 text-normal"]/a/@href')
        repos_list += arr
        return repos_list


# 获取一个项目的issues列表
def get_issues_list(repo_url):
    issues_list = []
    # url = 'https://github.com' + repo_name + '/issues'
    # 'https://github.com/ApolloAuto/apollo/issues?q=is%3Aissue+is%3Aclosed'
    # https: // github.com / ApolloAuto / apollo / pulls
    url = repo_url + '/pulls?q=is%3Apr+is%3Aclosed'
    print(url)
    response = requests.get(url)
    # 获取源码
    page_source = response.text
    tree = etree.HTML(page_source)
    # 获取issues数量
    number = tree.xpath('//*[@id="js-repo-pjax-container"]/div[1]/nav/ul/li[2]/a/span[2]')
    # print(len(number))
    if len(number) == 0:
        number = '0'
    else:
        number = number[0].text
    # 超过1K就爬取1000条（够用了）
    if number.isdigit():
        number = int(number)
    else:
        number = 10000

    # print(number)
    ## apollo
    # number = 10082
    ## apollo-plan
    # number = 2832
    ## carla
    # number = 770
    ## airsim
    number = 512
    # autoware
    # number = 1318
    # 计算分页数量，每页25个issues
    page = 0
    if number % 25 == 0:
        page = int(number / 25)
    else:
        page = int(number / 25) + 1
    for i in range(1, page + 1):
        'https://github.com/ApolloAuto/apollo/pulls?page=1&q=is%3Apr+is%3Aclosed'
        'https://github.com/carla-simulator/carla/pulls?q=is%3Apr+is%3Aclose'
        'https://github.com/ApolloAuto/apollo/pulls?q=is%3Apr+is%3Aclosed+plan'
        url = repo_url + '/pulls?page=' + str(i) + '&q=is%3Apr+is%3Aclosed'
        print(url)
        response = requests.get(url)
        # 获取源码
        page_source = response.text
        tree = etree.HTML(page_source)
        print(tree)
        # 获取issues超链接
        arr = tree.xpath('//*[@class="d-block d-md-none position-absolute top-0 bottom-0 left-0 right-0"]/@href')
        issues_list += arr
        # print(issues_list)
        # /combust/mleap/issues/716
    # 返回issues数量和列表

    return number, issues_list


# 获取一个issue的内容及评论
def get_issue_content(issue_name):
    # 拼接issue地址
    url = 'https://github.com' + issue_name
    # print(url)
    response = requests.get(url)
    page_source = response.text
    print(page_source)
    tree = etree.HTML(page_source)
    print(tree)
    # 获取issue内容
    # issue_content = tree.xpath('//table//td')[0].xpath('string(.)')
    issue_content = tree.xpath('//title/text()')[0].xpath('string(.)')
    print(issue_content)

    return issue_content


if __name__ == '__main__':
    # 测试
    # get_repos_list('ML pipeline')
    # get_issues('/combust/mleap')
    # get_issue_content('/combust/mleap/issues/716')
    '''
    issue="/rust-lang/rust/issues/76833"
    content=get_issue_content(issue)
    print(content)

    '''
    with open(r'airsim-result.md', 'w+', encoding='utf-8') as f:
        # key_words = input('please input a keyword：')
        # 获取项目列表
        # repos_list = get_repos_list(key_words)
        # 格式：/combust/mleap
        # for repo in repos_list:
            # 拼接项目url
            # repos_url = 'https://github.com' + repo
            # repo_url = 'https://github.com/ApolloAuto/apollo'
            # repo_url = 'https://github.com/carla-simulator/carla'
            repo_url = 'https://github.com/microsoft/AirSim'
            # repo_url = 'https://github.com/Autoware-AI/autoware.ai'
            print(repo_url)
            f.write('\n\n')
            f.write(repo_url)
            f.write('\n')
            # 获取项目的issues列表
            number, issues_list = get_issues_list(repo_url)
            f.write(str(number))
            f.write('\n')
            # 格式：/combust/mleap/issues/716
            for issue in issues_list:
                # 获取issue的内容
                issue_url = 'https://github.com' + issue
                content = get_issue_content(issue)
                print(issue_url)
                f.write(issue_url)
                f.write('\n')
                f.write('>' * 100)
                f.write('\n')
                f.write(str(content).strip())
                f.write('\n')
                f.write('<' * 100)
                f.write('\n')
                f.flush()
                # print(content)
                # print(issue)
    print('The end!')
