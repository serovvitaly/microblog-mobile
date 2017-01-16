#!/usr/bin/python3
import sys
import vk_api


def get_members_by_group_id(group_id):
    request = vk_api.request('groups.getMembers')
    request.set_param('group_id', group_id)
    request.set_param('count', 1000)
    request.set_param('offset', 0)
    request_list = vk_api.list(request)
    #request_list.set_count(2000)
    request_list.exec()
    items = request_list.get_items()
    return items


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You must specify the parameters')
        exit()
    members = get_members_by_group_id(sys.argv[1])
    if members is None:
        exit()
    for member_id in members:
        print(member_id)
