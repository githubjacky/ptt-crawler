# import module
from PyPtt import PTT
import sys


class PTT_CRAWLER:
    def __init__(self, ptt_id, ptt_password, board):
        self.id = ptt_id
        self.password = ptt_password
        self.board = board
        self.bot = PTT.API()

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

    def response(self, post):
        push_count = 0
        boo_count = 0
        arrow_count = 0
        for push in post.push_list:
            if push.type == PTT.data_type.push_type.PUSH:
                push_count += 1
            elif push.type == PTT.data_type.push_type.BOO:
                boo_count += 1
            elif push.type == PTT.data_type.push_type.ARROW:
                arrow_count += 1
        return push_count, boo_count, arrow_count

    def outputList(self, postList):
        outputList = []
        for post in postList:
            content = str(post.content).replace(' ', '')
            content = content.replace('\n', '')
            data = {
                'date': post.date,
                'title': post.title,
                'content': content,
                'push': self.response(post)[0],
                'boo': self.response(post)[1],
                'arrow': self.response(post)[2],
                'total_comment': self.response(post)[0]+self.response(post)[1]+self.response(post)[2],
                'not-boo': self.response(post)[0]+self.response(post)[2]
            }
            outputList.append(data)
        return outputList

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

        return self.outputList(postList)

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

        return self.outputList(postList)
