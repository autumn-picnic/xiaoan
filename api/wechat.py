"""WeChat Official Account webhook — handles text message XML and replies."""
import hashlib
import time
import xml.etree.ElementTree as ET
from lxml import etree


def verify_signature(token: str, timestamp: str, nonce: str, signature: str) -> bool:
    items = sorted([token, timestamp, nonce])
    computed = hashlib.sha1("".join(items).encode()).hexdigest()
    return computed == signature


def parse_message(body: bytes) -> dict:
    root = ET.fromstring(body)
    return {
        "openid": root.findtext("FromUserName", ""),
        "to": root.findtext("ToUserName", ""),
        "msg_type": root.findtext("MsgType", ""),
        "content": root.findtext("Content", ""),
        "msg_id": root.findtext("MsgId", ""),
    }


def build_reply(to_user: str, from_user: str, content: str) -> str:
    return (
        "<xml>"
        f"<ToUserName><![CDATA[{to_user}]]></ToUserName>"
        f"<FromUserName><![CDATA[{from_user}]]></FromUserName>"
        f"<CreateTime>{int(time.time())}</CreateTime>"
        "<MsgType><![CDATA[text]]></MsgType>"
        f"<Content><![CDATA[{content}]]></Content>"
        "</xml>"
    )
