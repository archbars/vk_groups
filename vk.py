import requests
import json
import time


class VKUser:
    def __init__(self, user_id, app_token):
        self.app_token = app_token
        if isinstance(user_id, int):
            self.user_id = str(user_id)
        else:
            url = 'https://api.vk.com/method/users.get?user_ids=' + user_id + '&v=5.85&access_token=' + app_token
            result = requests.get(url)
            self.user_id = str(json.loads(result.text).get("response")[0].get('id'))

    def get_friends(self):
        url = 'https://api.vk.com/method/friends.get?user_id=' + self.user_id + '&v=5.85&access_token=' + self.app_token
        result = requests.get(url)
        friends_dict = json.loads(result.text)
        friends_list = friends_dict.get('response').get('items')
        return friends_list

    def get_groups(self):
        url = 'https://api.vk.com/method/groups.get?user_id=' + self.user_id + '&v=5.85&access_token=' + self.app_token
        result = requests.get(url)

        groups_dict = json.loads(result.text)
        if groups_dict.get('error'):
            return 'error ' + str(groups_dict.get('error').get('error_code'))
        else:
            member_count = groups_dict.get('response').get('items')
            return member_count


class VKGroup:
    def __init__(self, group_id, app_token):
        self.group_id = str(group_id)
        self.app_token = app_token

    def get_group_info(self):
        url = 'https://api.vk.com/method/groups.getById?group_id=' + self.group_id + '&v=5.85&access_token=' +\
              self.app_token
        result = requests.get(url)
        groups_dict = json.loads(result.text)
        groups_list = groups_dict.get('response')[0]
        return [groups_list.get('id'), groups_list.get('name')]

    def get_group_members(self):
        url = 'https://api.vk.com/method/groups.getMembers?group_id=' + self.group_id + '&v=5.85&access_token=' +\
              self.app_token
        result = requests.get(url)
        groups_dict = json.loads(result.text)
        if groups_dict.get('error'):
            print('Error', groups_dict.get('error').get('error_code'))
        else:
            member_count = groups_dict.get('response').get('count')
            return member_count

    def get_all_info_in_dict(self):
        group_id_and_name = self.get_group_info()
        member_count = self.get_group_members()
        group_info_dict = {'name': group_id_and_name[1], 'gid': group_id_and_name[0],  'members_count': member_count}
        return group_info_dict


def find_unique(user, app_token):
    current_unique_set = VKUser(user, app_token).get_groups()
    all_friends = VKUser(user, app_token).get_friends()
    for friend in all_friends:
        if len(current_unique_set) > 0:
            print('.')
            time.sleep(0.4)
            current_friend_group_set = VKUser(str(friend), app_token).get_groups()
            current_unique_set = list(set(current_unique_set) - set(current_friend_group_set))
        else:
            break
    return current_unique_set


def main(our_user, app_token):
    list_of_unique_group = find_unique(our_user, app_token)
    result_group_info_list = []
    for group in list_of_unique_group:
        time.sleep(0.4)
        result_group_info_list.append(VKGroup(group, app_token).get_all_info_in_dict())
    if len(result_group_info_list) == 0:
        print("У пользователя нет уникальных групп")
    else:
        print(json.dumps(result_group_info_list, indent=2))


main('eshmargunov', 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae')
