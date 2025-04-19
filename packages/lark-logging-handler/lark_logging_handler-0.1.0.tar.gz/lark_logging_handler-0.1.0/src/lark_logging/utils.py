import json
import logging
from typing import Dict, Any

# 定义 Build 返回类型
from typing import TypedDict, Literal


class BuildResult(TypedDict):
    """飞书消息构建结果类型"""
    msg_type: Literal["post", "interactive"]
    content: str  # JSON 字符串


def _build_log_message(data: Dict[str, Any]) -> BuildResult:
    """构建飞书消息内容"""
    level = logging.getLevelName(data.get("level", logging.NOTSET))
    time_str = data.get("time", "")
    message = data.get("message", "")

    # 创建标题和emoji
    title_emoji = "🔔"
    title_text = "系统通知"

    if level == "info":
        title_emoji = "ℹ️"
        title_text = "信息通知"
    elif level == "warning":
        title_emoji = "⚠️"
        title_text = "警告通知"
    elif level == "error" or level == "critical":
        title_emoji = "❌"
        title_text = "错误通知"

    # 构建富文本内容
    post = {
        "zh_cn": {
            "title": f"{title_emoji} {title_text} [{data.get("name", "APP")}]",
            "content": []
        }
    }

    post["zh_cn"]["content"].append([{"tag": "text", "text": " "}])

    # 添加时间和级别
    post["zh_cn"]["content"].append([
        {"tag": "text", "text": "⏰ 时间 : "},
        {"tag": "text", "text": time_str}])
    post["zh_cn"]["content"].append([
        {"tag": "text", "text": "📊 级别 : "},
        {"tag": "text", "text": level.capitalize()}
    ])

    # 添加空行
    post["zh_cn"]["content"].append([{"tag": "text", "text": " "}])

    # 添加消息内容
    post["zh_cn"]["content"].append([
        {"tag": "text", "text": "📝 内容 : "},
        {"tag": "text", "text": message}
    ])

    # 剔除掉 data 的 ["level", "time", "message", "notify","name"]:
    data = {k: v for k, v in data.items() if k not in ["level", "time", "message", "notify", "name"]}
    # 如果没有其他字段，则不添加空行
    if data:
        # 添加空行
        post["zh_cn"]["content"].append([{"tag": "text", "text": " "}])

        # 添加其他字段
        for key, value in data.items():
            # 为特定字段选择emoji
            emoji = "📎"
            if key == "task":
                emoji = "🔄"
            elif key == "component":
                emoji = "🧩"
            elif key == "error":
                emoji = "❌"

            post["zh_cn"]["content"].append([
                {"tag": "text", "text": f"{emoji} {key.upper()} : "},
                {"tag": "text", "text": str(value)}
            ])

    return {"msg_type": "post", "content": json.dumps(post)}


def _build_log_card_message(data: Dict[str, Any]) -> BuildResult:
    """构建飞书卡片消息内容"""
    level = logging.getLevelName(data.get("level", logging.NOTSET)).upper()
    time_str = data.get("time", "")
    message = data.get("message", "")
    app_name = data.get("name", "APP")

    # 根据级别设置卡片颜色和图标
    card_color = "default"
    icon_token = "bell_outlined"
    title_text = "系统通知"

    if level == "INFO":
        card_color = "blue"
        icon_token = "info_outlined"
        title_text = "信息通知"
    elif level == "WARNING":
        card_color = "orange"
        icon_token = "warning_outlined"
        title_text = "警告通知"
    elif level == "ERROR" or level == "CRITICAL":
        card_color = "red"
        icon_token = "error_filled"
        title_text = "错误通知"

    # 移除卡片中不需要单独显示的字段
    extra_data = {k: v for k, v in data.items() if k not in ["level", "time", "message", "notify", "name"]}

    # 构建卡片内容
    card = {
        "schema": "2.0",
        "config": {
            "width_mode": "compact"  # 使卡片宽度撑满聊天窗口，更现代的布局
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": f"{title_text}"
            },
            "subtitle": {
                "tag": "plain_text",
                "content": app_name
            },
            "icon": {
                "tag": "standard_icon",
                "token": icon_token
            },
            "template": card_color
        },
        "body": {
            "elements": []
        }
    }

    # 添加时间和级别信息 - 使用column_set实现水平布局
    card["body"]["elements"].append({
        "tag": "column_set",
        "columns": [
            {
                "tag": "column",
                "width": "weighted",
                "weight": 1,
                "vertical_align": "top",
                "elements": [
                    {
                        "tag": "markdown",
                        "content": "**⏰ 时间**"
                    },
                    {
                        "tag": "markdown",
                        "content": f"{time_str}"
                    }
                ]
            },
            {
                "tag": "column",
                "width": "weighted",
                "weight": 1,
                "vertical_align": "top",
                "elements": [
                    {
                        "tag": "markdown",
                        "content": "**📊 级别**"
                    },
                    {
                        "tag": "markdown",
                        "content": f"**{level}**"
                    }
                ]
            }
        ]
    })

    # 添加消息内容 - 使用div
    card["body"]["elements"].append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"**📝 内容**\n{message}"
        }
    })

    # 添加分割线
    card["body"]["elements"].append({
        "tag": "hr"
    })

    # 如果有额外字段，添加额外信息部分
    if extra_data:
        # 添加额外信息标题
        card["body"]["elements"].append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": "**📋 额外信息**"
            }
        })

        # 为每个额外字段创建一个卡片样式区域
        for key, value in extra_data.items():
            card["body"]["elements"].append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**{key.upper()}**：\n{str(value)}\n"
                }
            })

        card["body"]["elements"].append({
            "tag": "hr"
        })

    # 添加底部时间戳
    card["body"]["elements"].append({
        "tag": "div",
        "text": {
            "tag": "plain_text",
            "content": f"生成于 {time_str}",
            "text_size": "small",
            "text_color": "grey-700",
            "text_align": "right"
        }

    })

    return {"msg_type": "interactive", "content": json.dumps(card)}
