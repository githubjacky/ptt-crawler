from crawler import PTT_CRAWLER
from output import output_excel, output_json, output_pdf
from PyPtt import PTT


def main():
    # print('-------------------------------------')
    # print('please input your id/password of ptt!')
    #
    # print('-------------------------------------')
    # userId = input('>id: ')
    # userPassword = input('>password: ')
    userId = "opottghjk00"
    userPassword = "opottghjk00"


    print('-------------------------------------')
    board_name = input('what board do you want to crawl?\n> ')

    while True:
        print('-------------------------------------')
        post_infos = input('select the information that you want to know about the post(separate the indexes by space)\n' +
            '0)pdf default  1)aid  2)index  3)date  4)board  5)content  6)author\n' +
            '7)money  8)url  9)ip  10)list_date  11)location  12)push_count\n' +
            '13)boo_count  14)arrow_count  15)push_content  16)boo_content  17)arrow_content\n> ')
        if post_infos == '0':
            post_infos = [3, 5, 15, 16, 17]
            break
        else:
            post_infos = list(map(int, post_infos.split()))
            post_infos.sort()
            if post_infos[-1] > 17:
                print('type the index out of range, please type again')
            elif post_infos[1] < 0:
                print('type the index out of range, please type again')
            else:
                break
    push_infos = []
    while True:
        current = post_infos[-1]
        if current > 11:
            push_infos.append(current)
            post_infos.pop(-1)
        else:
            break
    postLength = len(post_infos)
    pushLength = len(push_infos)
    if postLength != 0 and pushLength == 0:
        del push_infos
        crawler = PTT_CRAWLER(userId, userPassword, board_name, post_infos)
    elif postLength !=0 and pushLength != 0:
        push_infos.sort()
        crawler = PTT_CRAWLER(userId, userPassword, board_name, post_infos, push_infos)
    elif postLength == 0 and pushLength != 0:
        push_infos.sort()
        del post_infos
        crawler = PTT_CRAWLER(userId, userPassword, board_name, push_infos)
    else:
        print('push and post arrangement error')
    crawler.login()


    while True:
        print('-------------------------------------')
        crawler_type = input('choose the crawler type: 0)constraint 1)without constraint\n> ')
        if crawler_type != '0' and crawler_type != '1':
            print('type wrong index, please type again!')
        else:
            break
    fileName = ''
    if crawler_type == '0':
        fileName += f'{board_name}'
        finish = False
        while not finish:
            print('-------------------------------------')
            constraints = input('type the constraint as the example show(multiple constrains separated by "/")\n'+
                'ex: keyword python/push 20/author code\n> ')
            constraints = constraints.split('/')
            constraintList = []
            for constraint in constraints:
                constraint = constraint.split()
                constraint_type = constraint[0]
                constraint_value = constraint[1]
                fileName += f'_{constraint_type}'
                fileName += f'_{constraint_value}'
                if constraint_type == 'keyword':
                    constraint_tuple = (PTT.data_type.post_search_type.KEYWORD, constraint_value)
                    constraintList.append(constraint_tuple)
                    finish = True
                elif constraint_type == 'push':
                    constraint_tuple = (PTT.data_type.post_search_type.PUSH, constraint_value)
                    constraintList.append(constraint_tuple)
                    finish = True
                elif constraint_type == 'author':
                    constraint_tuple = (PTT.data_type.post_search_type.AUTHOR, constraint_value)
                    constraintList.append(constraint_tuple)
                    finish = True
                else:
                    fileName.replace(f'_{constraint_type}', '')
                    fileName.replace(f'_{constraint_value}', '')
                    print('-------------------------------------')
                    print('type wrong constrains, please type again')
                    finish = False
                    break

        print('-------------------------------------')
        limited_post = int(input('please type the number of posts that you want to limit(type 0 if you do not want to limit)\n> '))
        if limited_post != 0: fileName += f'_{limited_post}'

        print('-------------------------------------')
        print('start crawling...')
        result = crawler.parse_article_constraint(constraintList) if limited_post == 0 else crawler.parse_article_constraint(constraintList, limited_post)
    elif crawler_type == '1':
        fileName += f'{board_name}_n'
        print('-------------------------------------')
        newest = int(input('what amount of the newest post do you want to crawl?\n> '))
        fileName += f'_{newest}'

        print('-------------------------------------')
        index = int(input('please type the starting index(type 0 if you do not want to specify)\n> '))

        print('-------------------------------------')
        print('start crawling...')
        result = crawler.parse_article_newest(newest) if index == 0 else crawler.parse_article_newest(newest, index)
        if index != 0: fileName += f'_{index}'

    print('-------------------------------------')
    output_type = input('crawler end...what type of file do you wnat to output 0)json  1)excel  2)pdf\n> ')
    if output_type == '0':
        path_json = f'../crawler_result/json/{fileName}.json'
        output_json(result, path_json)
    elif output_type == '1':
        path_excel = f'../crawler_result/excel/{fileName}.xlsx'
        output_excel(result, path_excel)
    else:
        path_pdf = f'../crawler_result/pdf/{fileName}.pdf'
        output_pdf(result, path_pdf)

    print('start to log out...')
    crawler.logout()
    print('log out successfully')


if __name__ == '__main__':
    main()

