from ptt_crawler import PTT_CRAWLER
from output import output_excel, output_json
from PyPtt import PTT


def main():
    print('-------------------------------------')
    print('please input your id/password of ptt!')
    print('-------------------------------------')
    userId = input('>id: ')
    userPassword = input('>password: ')
    crawler = PTT_CRAWLER(userId, userPassword, 'movie')
    crawler.login()
    print('start to crawl...')

    constraint = [
        (PTT.data_type.post_search_type.KEYWORD, '蜘蛛人'),
        # (PTT.data_type.post_search_type.PUSH, '20')
    ]
    # result = crawler.parse_article_constraint(constraint)

    # you can specify the number of result through:
    result = crawler.parse_article_constraint(constraint, 1000)

    # another function with no constraint you can sepecify the amount
    # result = crawler.parse_article_newest(3000, 160150)

    print('start to output json file...')
    path_json = '../result/movie_蜘蛛人_1000.json'
    output_json(result, path_json)

    # print('start to output excel file...')
    # path_excel = './result/movie_國片.excel'
    # output_excel(result, path_excel)

    print('start to log out...')
    crawler.logout()
    print('log out successfully')


if __name__ == '__main__':
    main()
