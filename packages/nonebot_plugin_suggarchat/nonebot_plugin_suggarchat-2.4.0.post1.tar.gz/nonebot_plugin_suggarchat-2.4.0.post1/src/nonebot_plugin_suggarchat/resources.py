import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import chardet
import jieba
import pytz
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import (
    Event,
    GroupMessageEvent,
    Message,
    PokeNotifyEvent,
    PrivateMessageEvent,
)
from nonebot.log import logger

from .config import config_manager


def format_datetime_timestamp(time: int) -> str:
    """将时间戳格式化为日期、星期和时间字符串"""
    now = datetime.fromtimestamp(time)
    formatted_date = now.strftime("%Y-%m-%d")
    formatted_weekday = now.strftime("%A")
    formatted_time = now.strftime("%I:%M:%S %p")
    return f"[{formatted_date} {formatted_weekday} {formatted_time}]"


def hybrid_token_count(text: str, mode: str = "word") -> int:
    """
    计算中英文混合文本的 Token 数量，支持词、子词、字符模式
    """
    chinese_parts = re.findall(r"[\u4e00-\u9fff]+", text)
    non_chinese_parts = re.split(r"([\u4e00-\u9fff]+)", text)
    tokens = []

    # 处理中文部分
    for part in chinese_parts:
        tokens.extend(list(jieba.cut(part, cut_all=False)))

    # 处理非中文部分
    for part in non_chinese_parts:
        if not part.strip() or part in chinese_parts:
            continue
        if mode == "word":
            tokens.extend(re.findall(r"\b\w+\b|\S", part))
        elif mode == "char":
            tokens.extend(list(part))
        elif mode == "bpe":
            tokens.extend([part[i : i + 2] for i in range(0, len(part), 2)])
        else:
            raise ValueError("Invalid tokens-counting mode")
    return len(tokens)


def split_message_into_chats(text):
    """根据标点符号分割文本为句子"""
    sentence_delimiters = re.compile(r'([。！？!?~]+)[”"’\']*', re.UNICODE)
    sentences = []
    start = 0
    for match in sentence_delimiters.finditer(text):
        end = match.end()
        if sentence := text[start:end].strip():
            sentences.append(sentence)
        start = end
    if start < len(text):
        if remaining := text[start:].strip():
            sentences.append(remaining)
    return sentences


def convert_to_utf8(file_path) -> bool:
    """将文件编码转换为 UTF-8"""
    file_path = str(file_path)
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"]
    if encoding is None:
        try:
            with open(file_path) as f:
                contents = f.read()
                if contents.strip() == "":
                    return True
        except Exception:
            logger.warning(f"无法读取文件{file_path}")
            return False
        logger.warning(f"无法检测到编码{file_path}")
        return False
    with open(file_path, encoding=encoding) as file:
        content = file.read()
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    return True


async def synthesize_message(message: Message, bot: Bot) -> str:
    """合成消息内容为字符串"""
    content = ""
    for segment in message:
        if segment.type == "text":
            content += segment.data["text"]
        elif segment.type == "at":
            content += f"\\（at: @{segment.data.get('name')}(QQ:{segment.data['qq']}))"
        elif segment.type == "forward":
            forward = await bot.get_forward_msg(id=segment.data["id"])
            logger.debug(forward)
            content += (
                " \\（合并转发\n" + await synthesize_forward_message(forward) + "）\\\n"
            )
    return content


def get_memory_data(event: Event) -> dict[str, Any]:
    """获取事件对应的记忆数据，如果不存在则创建初始数据"""
    logger.debug(f"获取{event.get_type()} {event.get_session_id()} 的记忆数据")
    private_memory = config_manager.private_memory
    group_memory = config_manager.group_memory

    if not Path(private_memory).exists() or not Path(private_memory).is_dir():
        Path.mkdir(private_memory)
    if not Path(group_memory).exists() or not Path(group_memory).is_dir():
        Path.mkdir(group_memory)

    if (
        not isinstance(event, PrivateMessageEvent)
        and not isinstance(event, GroupMessageEvent)
        and isinstance(event, PokeNotifyEvent)
        and event.group_id
    ) or (
        not isinstance(event, PrivateMessageEvent)
        and isinstance(event, GroupMessageEvent)
    ):
        group_id = event.group_id
        conf_path = Path(group_memory / f"{group_id}.json")
        if not conf_path.exists():
            with open(str(conf_path), "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "id": group_id,
                        "enable": True,
                        "memory": {"messages": []},
                        "full": False,
                    },
                    f,
                    ensure_ascii=True,
                    indent=0,
                )
    elif (
        not isinstance(event, PrivateMessageEvent)
        and isinstance(event, PokeNotifyEvent)
    ) or isinstance(event, PrivateMessageEvent):
        user_id = event.user_id
        conf_path = Path(private_memory / f"{user_id}.json")
        if not conf_path.exists():
            with open(str(conf_path), "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "id": user_id,
                        "enable": True,
                        "memory": {"messages": []},
                        "full": False,
                    },
                    f,
                    ensure_ascii=True,
                    indent=0,
                )
    convert_to_utf8(conf_path)
    with open(str(conf_path), encoding="utf-8") as f:
        conf = json.load(f)
        logger.debug(f"读取到记忆数据{conf}")
        return conf


def write_memory_data(event: Event, data: dict) -> None:
    """将记忆数据写入对应的文件"""
    logger.debug(f"写入记忆数据{data}")
    logger.debug(f"事件：{type(event)}")
    group_memory = config_manager.group_memory
    private_memory = config_manager.private_memory

    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
        conf_path = Path(group_memory / f"{group_id}.json")
    elif isinstance(event, PrivateMessageEvent):
        user_id = event.user_id
        conf_path = Path(private_memory / f"{user_id}.json")
    elif isinstance(event, PokeNotifyEvent):
        if event.group_id:
            group_id = event.group_id
            conf_path = Path(group_memory / f"{group_id}.json")
            if not conf_path.exists():
                with open(str(conf_path), "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "id": group_id,
                            "enable": True,
                            "memory": {"messages": []},
                            "full": False,
                        },
                        f,
                        ensure_ascii=True,
                        indent=0,
                    )
        else:
            user_id = event.user_id
            conf_path = Path(private_memory / f"{user_id}.json")
            if not conf_path.exists():
                with open(str(conf_path), "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "id": user_id,
                            "enable": True,
                            "memory": {"messages": []},
                            "full": False,
                        },
                        f,
                        ensure_ascii=True,
                        indent=0,
                    )
    with open(str(conf_path), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=True)


async def get_friend_info(qq_number: int, bot: Bot) -> str:
    """获取好友昵称"""
    friend_list = await bot.get_friend_list()
    return next(
        (
            friend["nickname"]
            for friend in friend_list
            if friend["user_id"] == qq_number
        ),
        "",
    )


def split_list(lst: list, threshold: int) -> list[Any]:
    """将列表分割为多个子列表，每个子列表长度不超过阈值"""
    if len(lst) <= threshold:
        return [lst]
    return [lst[i : i + threshold] for i in range(0, len(lst), threshold)]


async def is_same_day(timestamp1: int, timestamp2: int) -> bool:
    """判断两个时间戳是否为同一天"""
    date1 = datetime.fromtimestamp(timestamp1).date()
    date2 = datetime.fromtimestamp(timestamp2).date()
    return date1 == date2


async def synthesize_forward_message(forward_msg: dict) -> str:
    """合成转发消息内容为字符串"""
    result = ""
    for segment in forward_msg["messages"]:
        nickname = segment["sender"]["nickname"]
        qq = segment["sender"]["user_id"]
        time = f"[{datetime.fromtimestamp(segment['time']).strftime('%Y-%m-%d %I:%M:%S %p')}]"
        result += f"{time}[{nickname}({qq})]说："
        for segments in segment["content"]:
            segments_type = segments["type"]
            if segments_type == "text":
                result += f"{segments['data']['text']}"
            elif segments_type == "at":
                result += f" [@{segments['data']['qq']}]"
        result += "\n"
    return result


def get_current_datetime_timestamp():
    """获取当前时间并格式化为日期、星期和时间字符串"""
    utc_time = datetime.now(pytz.utc)
    asia_shanghai = pytz.timezone("Asia/Shanghai")
    now = utc_time.astimezone(asia_shanghai)
    formatted_date = now.strftime("%Y-%m-%d")
    formatted_weekday = now.strftime("%A")
    formatted_time = now.strftime("%H:%M:%S")
    return f"[{formatted_date} {formatted_weekday} {formatted_time}]"
