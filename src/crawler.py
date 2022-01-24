# import module
from PyPtt import PTT
import sys


class PTT_CRAWLER:
    def __init__(self, ptt_id, ptt_password, board, *infoIndex):
        self.id = ptt_id
        self.password = ptt_password
        self.board = board
        self.bot = PTT.API()
        if len(infoIndex) == 2:
            self.output_post_info = True
            self.post_indexes = infoIndex[0]
            self.output_push_info = True
            self.push_indexes = infoIndex[1]
        else:  # len(infoIndex == 1)
            if infoIndex[0][0] <= 11:
                self.output_post_info = True
                self.post_indexes = infoIndex[0]
                self.output_push_info = False
            else:
                self.output_push_info = True
                self.push_indexes = infoIndex[0]
                self.output_post_info = False


    def login(self):
        try:
            self.bot.login(self.id, self.password)
        except PTT.exceptions.LoginError:
            self.bot.log('warning: fail to log in')
            sys.exit()
        except PTT.exceptions.WrongIDorPassword:
            self.bot.log('warning: wrong password or id')
            sys.exit()
        except PTT.exceptions.LoginTooOften:
            self.bot.log('try too often, please wait for a moment to log in')
            sys.exit()
        except self.bot.unregistered_user:
            self.bot.log('warning: the user is not registered')
        self.bot.log('log in successfully!')


    def logout(self):
        self.bot.logout()


    def find_index(self, *constraint):
        if len(constraint) != 0:
            index = self.bot.get_newest_index(
                PTT.data_type.index_type.BBS,
                self.board,
                search_list=constraint[0]
            )
        else:  # get the newest
            index = self.bot.get_newest_index(
                PTT.data_type.index_type.BBS,
                self.board,
            )

        return index


    def get_push_info(self, post):
        push_info_dict = {}
        count_push = count_boo = count_arrow = get_push_content = get_boo_content = get_arrow_content = False
        for index in self.push_indexes:
            if index == 12:
                count_push = True
                push_info_dict['push_count'] = 0
            elif index == 13:
                count_boo = True
                push_info_dict['boo_count'] = 0
            elif index == 14:
                count_arrow = True
                push_info_dict['arrow_count'] = 0
            elif index == 15:
                get_push_content = True
                push_info_dict['push_coontent'] = []
            elif index == 16:
                get_boo_content = True
                push_info_dict['boo_content'] = []
            elif index == 17:
                get_arrow_content = True
                push_info_dict['arrow_content'] = []

        for push in post.push_list:
            if push.type == PTT.data_type.push_type.PUSH and count_push:
                push_info_dict['push_count'] += 1
            if push.type == PTT.data_type.push_type.PUSH and get_push_content:
                push_info_dict['push_coontent'].append(push.content.replace(' ', ''))
            if push.type == PTT.data_type.push_type.BOO and count_boo:
                push_info_dict['boo_count'] += 1
            if push.type == PTT.data_type.push_type.BOO and get_boo_content:
                push_info_dict['boo_content'].append(push.content.replace(' ', ''))
            if push.type == PTT.data_type.push_type.ARROW and count_arrow:
                push_info_dict['arrow_count'] += 1
            if push.type == PTT.data_type.push_type.ARROW and get_arrow_content:
                push_info_dict['arrow_content'].append(push.content.replace(' ', ''))

        return push_info_dict


    def output(self, postList):
        output_List = []
        for post in postList:
            if self.output_post_info:
                post_info_dict = {'title': post.title}
                for index in self.post_indexes:
                    if index == 1: post_info_dict['aid'] = post.aid
                    elif index == 2: post_info_dict['index'] = post.index
                    elif index == 3: post_info_dict['date'] = post.date
                    elif index == 4: post_info_dict['board'] = post.board
                    elif index == 5:
                        content = str(post.content).replace(' ', '')
                        post_info_dict['content'] = content
                    elif index == 6: post_info_dict['author'] = post.author
                    elif index == 7: post_info_dict['money'] = post.money
                    elif index == 8: post_info_dict['url'] = post.web_url
                    elif index == 9: post_info_dict['ip'] = post.ip
                    elif index == 10: post_info_dict['list_date'] = post.list_date
                    elif index == 11: post_info_dict['locatoin'] = post.location
                if self.output_push_info:
                    post_dict = post_info_dict | self.get_push_info(post)
                else:
                    post_dict = post_info_dict
            else:
                post_dict = self.get_push_info(post)
            
            output_List.append(post_dict)
        
        return output_List


    def parse_article_constraint(self, *constraint):
        index = self.find_index(constraint[0])
        postList = []
        if len(constraint) == 1:
            end = index
            for index in range(1, end+1):
                post = self.bot.get_post(
                    self.board,
                    post_index=index,
                    search_list=constraint[0]
                )
                if post.delete_status == PTT.data_type.post_delete_status.NOT_DELETED:
                    postList.append(post)
            postList.reverse()
        else:
            start = index
            target_article_num = constraint[1]
            current_article_num = 0
            while current_article_num < target_article_num:
                post = self.bot.get_post(
                    self.board,
                    post_index=start,
                    search_list=constraint[0]
                )
                if post.delete_status == PTT.data_type.post_delete_status.NOT_DELETED:
                    postList.append(post)
                    current_article_num += 1
                start -= 1
        return self.output(postList)


    def parse_article_newest(self, *args):
        postList = []
        if len(args) == 0:
            self.bot.log('please try again and give an index...')
        else:
            start = self.find_index() if len(args) == 1 else args[1]
            loop = 0
            article_num = args[0]
            while loop < article_num:
                post = self.bot.get_post(
                    self.board,
                    post_index=start
                )
                if post.delete_status == PTT.data_type.post_delete_status.NOT_DELETED:
                    postList.append(post)
                    loop += 1
                start -= 1
        
        return self.output(postList)
