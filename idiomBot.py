import asyncio
import json
import os.path
import threading
import time
from multiprocessing import Process
from typing import Dict, List

import qqbot
import pandas as pd
import numpy as np

from qqbot.core.util.yaml_util import YamlUtil


m_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))

idiom = pd.read_json("idiom.json")
t = idiom.pinyin.str.split()
idiom["firstChar"] = t.str[0]
idiom["lastChar"] = t.str[-1]
idiom = idiom.set_index("word")[["firstChar", "lastChar"]]
is_begin = False
word2 = ""
lastChar = ""
resp_sentence = ["太厉害了",
                "竟然被你答上来了",
                "你简直是个文学家",
                "你很棒哦",
                "开始佩服你了呢"]

async def _message_handler(event, message: qqbot.Message):
    """
    定义事件回调的处理
    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """

    # 根据指令触发不同的推送消息
    global idiom
    global is_begin
    global word2
    global lastChar
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    content = message.content
    qqbot.logger.info("event %s" % event + ",receive message %s" % content)

    # @function 收到开始接龙的指令，且之前[未开始]接龙游戏
    # @action   开始游戏，给出第一个成语
    if "/接龙" in content and is_begin == False:
        is_begin = True
        word2 = np.random.choice(idiom.index)
        lastChar = idiom.loc[word2, "lastChar"]
        message_to_send = qqbot.MessageSendRequest(content='那我就先开始啦，接招：【' + word2 + '】，认输或者不想玩了记得告诉我:“不玩了”哦！', msg_id=message.id)
        await msg_api.post_message(message.channel_id, message_to_send)
        
    # @function 收到开始接龙的指令，且之前[已开始]接龙游戏
    # @action   提示用户之前游戏还在继续
    elif "/接龙" in content and is_begin == True:
        message_to_send = qqbot.MessageSendRequest(content='【'+ word2 + '】你还没接出来呢，加油再想想呀~~~ 认输或者不想玩了记得告诉我:“不玩了”哦！', msg_id=message.id)
        await msg_api.post_message(message.channel_id, message_to_send)
    
    # @function 收到结束游戏的指令
    # @action   结束游戏
    elif "不玩了" in content and is_begin == True:
        is_begin = False
        message_to_send = qqbot.MessageSendRequest(content="好的，游戏结束啦，欢迎下次来玩哦~", msg_id=message.id)
        await msg_api.post_message(message.channel_id, message_to_send)

    # @function 游戏进行中，用户和电脑正在对战
    elif is_begin == True:
        word = message.content
        word = content.split(" ")
        word = word[1]
        qqbot.logger.info("word: %s" % word)

        # @action 用户输入的成语不在“字典”中，提示重新输入有效成语
        if word not in idiom.index:
            qqbot.logger.info("not a idiom")
            message_to_send = qqbot.MessageSendRequest(content="你输入的不是一个成语，请重新输入！", msg_id=message.id)
            await msg_api.post_message(message.channel_id, message_to_send)

        # @action 用户输入了错误的答案，提示答案错误 游戏结束
        elif lastChar and idiom.loc[word, 'firstChar'] != lastChar:
            qqbot.logger.info("wrong answer")
            is_begin = False
            message_to_send = qqbot.MessageSendRequest(content="哈哈，你的答案错了，我赢啦，游戏结束！！！", msg_id=message.id)
            await msg_api.post_message(message.channel_id, message_to_send)

        # @action 用户输入的答案无解，提示用户胜利
        elif idiom.index[idiom.firstChar == idiom.loc[word, "lastChar"]].shape[0] == 0:
            qqbot.logger.info("win!")
            is_begin = False
            message_to_send = qqbot.MessageSendRequest(content="恭喜你赢了！你太厉害了，我被你打败！！！", msg_id=message.id)
            await msg_api.post_message(message.channel_id, message_to_send)

        # @function 用户输入了正确答案，且机器人能继续接龙
        # @action   输出对用户成语的回答
        else:
            qqbot.logger.info("right answer and response")
            words = idiom.index[idiom.firstChar == idiom.loc[word, "lastChar"]]
            word2 = np.random.choice(words)
            message_to_send = qqbot.MessageSendRequest(content= np.random.choice(resp_sentence) + "，我的答案是【" + word2 + "】", msg_id=message.id)
            await msg_api.post_message(message.channel_id, message_to_send)
            lastChar = idiom.loc[word2, "lastChar"]
        
    # @function 用户输入了非法内容
    # @action   提示用户重新按提示输入
    else:
        message_to_send = qqbot.MessageSendRequest(content="你输入的消息小Q看不懂呢~ 试试输入“/接龙”", msg_id=message.id)
        await msg_api.post_message(message.channel_id, message_to_send)


# 主函数
if __name__ == "__main__":
    # @机器人后推送被动消息
    t_token = qqbot.Token(m_config["token"]["appid"], m_config["token"]["token"])
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(t_token, False, qqbot_handler)