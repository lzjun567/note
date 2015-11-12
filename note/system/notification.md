通知系统设计
=============

通知就是某某东西（Object）被某个人(actor)改变(verb）后需要报告给用户（subject)

notification_id, user_id




actor：角色
    球队：福山金威（把你移出了俱乐部）
    领队：福山金威领队（把你设置为球员10号）
    联赛：和特联赛（邀请你参赛）
    球员：梁月明（已经激活，正式加盟）
    系统：OpenPlay欢迎你加入
    其他：
verb：动作
    设置
    

图标显示的类型就是角色


id
rceiver_id
is_read
sender: actor{id, name , type}
verb: remove/invite/join/
object: 目标对象  球队


赛事组织者 ：需要包含赛事信息


我已加入xxx俱乐部
    receiver_id：我
    verb：加入
    Object_id：xxx俱乐部
    sender：系统

XXX俱乐部加入了xxx联赛（所有球员收到通知）
    receiver_id :所有球员
    object_id :xxx联赛
    "verb": 加入
    sender: xxx俱乐部

XX 球员激活了帐号
    receiver_id:领队
    verb: 激活
    sender: xx球员
    Object_id：账号

赛事组织者公布了赛程
    receiver_id:所有球员
    verb:公布
    sender:赛事组织者
    Object_id：赛程（可以为空）

赛事组织者修改了赛程
    同上

收到 XX 赛事组织者的消息：文字内容
    receiver_id：领队
    verb:收到
    sender:赛事组织者
    Object_id：文字内容

XXX（俱乐部名称）被 XXXX（赛事名称）取消参赛资格
    receiver_id:领队
    verb:取消资格
    sender:赛事组织者
    Object_id ：该赛事

XXX（俱乐部名称）领队把你设置为 领队
    receiver_id：球员
    verb:设置
    sender:领队
    Object_id：俱乐部

你已被 XXX（领队）移出俱乐部
    receiver_id：你
    verb:移出
    object:俱乐部
    sender:领队
 
收到 XXXX（赛事名称）的参赛邀请：同意 / 拒绝
    receiver_id:领队
    verb：收到
    object:邀请（一封邀请的文案）
    sender:赛事组织者
    
文案：XXX（俱乐部名称）邀请你加入俱乐部
    receiver_id:球员
    verb:邀请
    Object:俱乐部
    sender:俱乐部

    
    
    
