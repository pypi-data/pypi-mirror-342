import asyncio
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.plugin import on_startswith
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent, Bot

from .get_source import MCModScraper

wiki = on_startswith(("#百科", "#百科模组", "#百科整合包", "#百科资料", "#百科教程"))
cmd_map = {
    "#百科": 0, "#百科模组": 1, "#百科整合包": 2, "#百科资料": 3, "#百科教程": 4
}
mcmod = MCModScraper()


async def timeout_task(matcher: Matcher, timeout: float):
    """一个后台任务，在指定时间后检查并处理超时"""
    await asyncio.sleep(timeout)
    if not matcher.state.get("_finished", False):  # 使用一个内部标志检查
        try:
            matcher.state["_finished"] = True
            await matcher.finish("选择超时，请重新发起查询。")
        except Exception as e:
            logger.error(f"Error in timeout task: {e}")


async def send_content(url: str, bot: Bot):
    content = await mcmod.get_content(url)
    message = []
    text = ''
    # print(content)
    if content:
        message.append(MessageSegment.node_custom(
            user_id=bot.self_id,
            nickname="百科bot",
            content=MessageSegment.text(content[0]+'\n'+url)
        ))
        if len(content) == 3:
            message.append(MessageSegment.node_custom(
                user_id=bot.self_id,
                nickname="百科bot",
                content=MessageSegment.text("支持的MC版本\n"+content[2])
            ))
        for i in content[1]:
            if i.get('type') == 'image':
                if text:
                    message.append(MessageSegment.node_custom(
                        user_id=bot.self_id,
                        nickname="百科bot",
                        content=MessageSegment.text(text)
                    ))
                    text = ''
                if i.get('content'):
                    message.append(MessageSegment.node_custom(
                        user_id=bot.self_id,
                        nickname="百科bot",
                        content=[MessageSegment.image(
                            i.get('url')), MessageSegment.text(i.get('content'))]
                    ))
                else:
                    message.append(MessageSegment.node_custom(
                        user_id=bot.self_id,
                        nickname="百科bot",
                        content=MessageSegment.image(i.get('url'))
                    ))
            elif i.get('type') == 'text':
                text += ('\n' if text else '') + i.get('content')
            elif i.get('type') == 'title':
                if text:
                    message.append(MessageSegment.node_custom(
                        user_id=bot.self_id,
                        nickname="百科bot",
                        content=MessageSegment.text(text)
                    ))
                text = i.get('content')
        if text:
            message.append(MessageSegment.node_custom(
                user_id=bot.self_id,
                nickname="百科bot",
                content=MessageSegment.text(text)
            ))
        return message
    else:
        return None


@wiki.handle()
async def wiki_search(bot: Bot, event: GroupMessageEvent, state: T_State):
    cmdArgs = event.get_plaintext().split()
    if len(cmdArgs) > 2 and cmdArgs[-1].isdigit():
        # 如果最后一个参数是数字，则将其视为序号
        query = ' '.join(cmdArgs[1:-1])
        seq = int(cmdArgs[-1])
    elif len(cmdArgs) >= 2:
        query = ' '.join(cmdArgs[1:])
        seq = None
    else:
        await wiki.finish("请输入要查询的内容")

    # @todo: 如果没找到相关内容，可以切换复杂搜索
    result = await mcmod.search_mcmod(query, cmd_map.get(cmdArgs[0]))
    if not result:
        await wiki.finish("未找到相关内容")

    msgs = []
    # print(cmdArgs)
    if len(result) == 1 or (seq is not None):
        if len(result) == 1:
            link = result[0]['link']
        else:
            if (seq > len(result) or seq < 1):
                await wiki.finish("请输入正确的序号")
            link = result[seq - 1]['link']

        content = await send_content(link, bot)
        if not content:
            await wiki.finish("获取内容失败, 请稍后再试")
        else:
            await bot.send_group_forward_msg(group_id=event.group_id, messages=content)
            await wiki.finish()
    else:
        msgs.append(MessageSegment.node_custom(
            user_id=bot.self_id,
            nickname="百科bot",
            content=MessageSegment.text("请在60s内回复要查询的序号。")
        ))
        for i in range(len(result)):
            msgs.append(MessageSegment.node_custom(
                user_id=bot.self_id,
                nickname=str(i+1),
                content=MessageSegment.text(
                    f'{result[i]["title"]}\n{result[i]["link"]}'
                )
                # {result[i]['description']+'\n' if result[i]['description'] else ''}
            ))
        await bot.send_group_forward_msg(group_id=event.group_id, messages=msgs)
        state['search_result'] = result


@wiki.receive()
async def _(state: T_State, event: GroupMessageEvent, bot: Bot):
    msg = event.get_plaintext()
    if msg.isdigit():
        index = int(msg) - 1
        if 'search_result' in state and 0 <= index < len(state['search_result']):
            url = state['search_result'][index]['link']
            content = await send_content(url, bot)
            if content:
                await bot.send_group_forward_msg(group_id=event.group_id, messages=content)
            else:
                await wiki.finish("获取内容失败")
        else:
            await wiki.finish("无效的序号或搜索结果已过期")
    elif msg.startswith("#百科"):
        await wiki_search(bot, event, state)
        await wiki.reject()
    else:
        await wiki.finish("请输入有效的序号")
