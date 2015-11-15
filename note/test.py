a = {u'status': 1, u'passport': u'', u'weight': 95.0,
     u'area': {u'province': u'\u6d69\u5e02', u'country': u'\u6fb3\u5927\u5229\u4e9a', u'district': u'\u5f6c\u5e02',
               u'city': u'\u535a\u5e02'}, u'gender': 0, u'id_card': u'440105198107105116',
     u'birth': u'2006-09-19 08:20:06', u'token': u'27b55fcf10c54b5cb7da90e8d543d76f', u'height': 216.0,
     u'phone': u'18873390760', u'op_id': 239559, u'roles': [], u'avatar_uri': u'http://www.baidu.com',
     u'team': {u'name': u'\u516c\u79c0\u6885', u'short_name': u'\u8042\u5efa\u534e',
               u'area': {u'province': u'\u91d1\u51e4\u5e02', u'country': u'\u4e9a\u7f8e\u5c3c\u4e9a',
                         u'district': u'\u5b81\u5e02', u'city': u'\u7ea2\u5e02'}, u'op_id': u'T376542',
               u'id': u'5628778414028f4c0d405f0c', u'logo_uri': u'http://www..com/'},
     u'id': u'5628778414028f4c0d405f0f', u'nationality': u'\u5189\u6d9b', u'country_code': u'+852',
     u'email': u'dylanninin@gmail.com', u'account_roles': [u'player'], u'name': u'zhang si'}


b = {'status': 1, 'avatar_uri': u'http://www.baidu.com', 'weight': 95.0, 'sender_id': '5628778414028f4c0d405f15',
     'height': 216.0, 'phone': u'18873390760', 'op_id': 239559, 'birth': '2006-09-19 08:20:06',
     'nationality': u'\u5189\u6d9b', 'country_code': u'+852', 'id': '5628778414028f4c0d405f0f',
     'competition_id': 'None', 'name': u'zhang si', 'roles': [],
     'area': {u'province': u'\u6d69\u5e02', u'country': u'\u6fb3\u5927\u5229\u4e9a', u'district': u'\u5f6c\u5e02',
              u'city': u'\u535a\u5e02'}, 'gender': 0, 'id_card': u'440105198107105116',
     'token': '27b55fcf10c54b5cb7da90e8d543d76f', 'passport': u'',
     'team': {'name': u'\u516c\u79c0\u6885', 'short_name': u'\u8042\u5efa\u534e',
              'area': {u'province': u'\u91d1\u51e4\u5e02', u'country': u'\u4e9a\u7f8e\u5c3c\u4e9a',
                       u'district': u'\u5b81\u5e02', u'city': u'\u7ea2\u5e02'}, 'op_id': u'T376542',
              'id': '5628778414028f4c0d405f0c', 'logo_uri': u'http://www..com/'}, 'email': u'dylanninin@gmail.com',
     'account_roles': [u'player']}

print sorted(a.keys())
print sorted(b.keys())
