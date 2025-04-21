"""
onebot v11 自带 Node_custom, 忽略此构造
"""
from nonebot.adapters.onebot.v11 import MessageSegment
from typing import List
from dataclasses import dataclass, field

@dataclass(frozen=True)
class MessageData:
    """
    消息数据载体。

    用于存储单个转发消息节点的用户信息和内容。
    """
    # 消息段列表
    content: List[MessageSegment]
    # 发送者昵称
    nickname: str
    # 发送者 QQ 号 (Uin)
    user_id: str


@dataclass(frozen=True)
class ForwardMessage:
    """
    单个转发消息节点。

    符合 OneBot v11 转发消息格式中的 "node" 类型。
    """
    type: str = field(default="node", init=False)
    # 节点数据
    data: MessageData
