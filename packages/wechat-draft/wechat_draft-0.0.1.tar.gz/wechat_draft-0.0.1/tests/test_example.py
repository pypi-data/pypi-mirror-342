# 开发人员： Xiaoqiang
# 微信公众号:  XiaoqiangClub
# 开发时间： 2025-04-19
# 文件名称： tests/test_example.py
# 项目描述： 测试示例文件
# 开发工具： PyCharm
from dataclasses import dataclass
from wechat_draft import WechatDraft


@dataclass
class WechatConfig:
    """微信公众号配置"""
    test_app_id: str = "wx9031a672052b7eb5"
    test_app_secret: str = "30437646c0feea497fdbf30074a1a1fb"
    test_token: str = "xiaoqiangclub520520xiaoqiangclub"
    test_open_id: str = "gh_97e22ebdf5bc"  # 测试公众号原始ID

    app_id: str = "wx44bb72cca0ea65d6"
    app_secret: str = "c9f743480b9debcda8440c4b06c33253"
    token: str = "xiaoqiangclub520520xiaoqiangclub"
    open_id: str = "gh_15e613666293"  # 正式公众号原始ID


def test_sample():
    # wechat = WechatDraft(WechatConfig.test_app_id, WechatConfig.test_app_secret)
    wechat = WechatDraft(WechatConfig.app_id, WechatConfig.app_secret)
    # 示例：新增永久图片素材
    # {"media_id": "7W9OX-_svPHG2Ejnx73Q23fwHJnx4cqYhtA1lAVGNxfzZGvXN571zdKnqO2MxKyU", "url": "http://mmbiz.qpic.cn/sz_mmbiz_jpg/OAeCMzEJygKtKZYe6Z247zMsOl4lbXAicdmHibrF23yBPGocLYXBjfZ1UJYx0XYwqic3RMmPCPnicEp7FEicoWmxicCw/0?wx_fmt=jpeg", "item": []}
    # 上传图片响应：{"url": "http://mmbiz.qpic.cn/sz_mmbiz_jpg/OAeCMzEJygKtKZYe6Z247zMsOl4lbXAicBFUOICzKqLHrboGoPvjZvjZC8a2sK75FzzIWTboRgMxBaddGIIiargg/0?from=appmsg"}
    # image_info = wechat.upload_news_image(image_path="./test.jpg")
    # print(image_info)
    # return
    # if image_info:
    #     image_media_id = image_info[0]
    image_media_id = "7W9OX-_svPHG2Ejnx73Q23fwHJnx4cqYhtA1lAVGNxfzZGvXN571zdKnqO2MxKyU"
    crop_percent_list = wechat.get_crop_params('test.jpeg', (100, 150), 2500).get('crop_percent_list')

    # 示例：创建图文消息草稿，使用新增的图片素材作为封面
    if image_media_id:
        wechat.create_draft(
            title="测试图文消息",
            content="<p>这是图文消息内容，包含<em>富文本</em>和图片</p><img src=\"图片URL\">",
            article_type="news",
            thumb_media_id=image_media_id,
            author="小强",
            digest="这是图文消息摘要",
            # pic_crop_235_1="0.1_0_0.9_0.8",
            # pic_crop_235_1=[{"ratio": "16_9", "x1": 0.1, "y1": 0, "x2": 0.9, "y2": 0.8}],
            # pic_crop_1_1="0.1_0_0.9_0.8",
            # crop_percent_list=[{'ratio': '2.35_1', 'x1': 0.024414, 'y1': 0.012207, 'x2': 0.097656, 'y2': 0.043213}, {'ratio': '1_1', 'x1': 0.024414, 'y1': 0.012207, 'x2': 0.097656, 'y2': 0.085449}, {'ratio': '16_9', 'x1': 0.024414, 'y1': 0.012207, 'x2': 0.097656, 'y2': 0.053223}],
            crop_percent_list=crop_percent_list,
            need_open_comment=1,
            only_fans_can_comment=0
        )
    #
    # # 示例：临时切换公众号
    # target_appid = "目标公众号的appid"  # 替换为实际要切换到的公众号的appid
    # switch_result = wechat.temporary_switch_mp(target_appid)
    # if switch_result == 0:
    #     print("临时切换公众号成功")
    # else:
    #     print("临时切换公众号失败")
    #
    # # 检测草稿箱开关状态
    # is_open = wechat.check_draft_switch_state()
    # if is_open is not None:
    #     print(f"草稿箱开关状态：{'开启' if is_open else '关闭'}")
    #
    # # 开启草稿箱功能（谨慎操作！）
    # if not is_open:
    #     confirm = input("是否确认开启草稿箱功能？(y/n): ")
    #     if confirm.lower() == "y":
    #         success = wechat.switch_to_draft_box()
    #         if success:
    #             print("操作完成，等待后台生效。")
    #         else:
    #             print("开启失败，请检查原因")
    # else:
    #     print("草稿箱功能已开启，无需重复操作")

    # 示例：获取永久素材
    # material = wechat.get_permanent_material(media_id=image_media_id)

    # 示例：删除永久素材
    # if image_media_id:
    #     wechat.delete_permanent_material(media_id=image_media_id)


if __name__ == "__main__":
    test_sample()
