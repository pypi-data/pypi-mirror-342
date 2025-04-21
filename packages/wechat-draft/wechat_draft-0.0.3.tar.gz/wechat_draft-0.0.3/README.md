# WechatDraft: 微信公众号草稿与永久素材管理工具

## 项目简介

WechatDraft 是一个基于 Python
的微信公众号开发工具，提供草稿箱管理、永久素材操作等功能，支持图文消息、图片消息的创建、上传、裁剪及状态管理。适用于需要批量管理公众号内容的开发者，简化素材操作流程，提升内容发布效率。

## 特性

- **草稿箱管理**：创建、管理公众号草稿，支持图文/图片消息，包含封面裁剪、评论设置等功能。
- **永久素材操作**：上传、获取、删除图片、视频、语音等永久素材，支持素材校验和格式转换。
- **自动缓存**：自动管理 Access Token 缓存，避免频繁请求带来的性能损耗。
- **错误处理**：内置详细错误码解析，覆盖微信官方接口错误，提供清晰的问题定位信息。
- **图片裁剪**：基于图片坐标自动生成微信所需的裁剪参数，支持多种比例（2.35:1、1:1、16:9）。

## 准备工作

1. 使用该功能需要先准备微信公众号账号，并获取 AppID 和 AppSecret。

   - 进入[微信公众号后台页面](https://mp.weixin.qq.com/)，依次进入 `设置与开发 > 开发接口管理 > 基本设置` 获取 `AppID` 和
     `AppSecret`。

2. 将服务器IP地址（测试环境的IP地址）加入`IP白名单`。

## 安装

```bash
pip install wechat_draft
```

## 快速开始

### 初始化

```python
from wechat_draft import WechatDraft

# 初始化客户端
app = WechatDraft(
    app_id="你的公众号APP ID",
    app_secret="你的公众号APP Secret"
)
```

### 权限检测

> 根据[官方文档](https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Temporary_MP_Switch.html)
> 介绍：目前草稿功能还在内测阶段，有些账号并没有开通该功能，你可以调用以下2个方法进行检测或开通`草稿`功能。注意该功能开启后不能关闭。

```python
# 检测草稿箱开关状态
app.check_draft_switch_state()

# 开通草稿箱功能，开通该功能后，服务器需要等待几分钟才能真实生效！
app.open_draft()
```

### 创建图文草稿

```python
# 上传封面图片获取永久素材ID
cover_media_id = app.add_permanent_material(
    material_type="image",
    file_path="cover.jpg"
)[0]

# 创建草稿
draft_id = app.create_draft(
    title="测试图文",
    content="<p>图文内容</p>",
    article_type="news",
    thumb_media_id=cover_media_id,
    need_open_comment=1,
    only_fans_can_comment=0,
    # 自动生成裁剪参数（示例：从图片(100, 50)坐标开始，横向裁剪500像素）
    **app.get_crop_params(
        image_file_path="cover.jpg",
        start_point=(100, 50),
        crop_width_px=500
    )
)

print(f"草稿创建成功，ID：{draft_id}")
```

注意：微信公众号对永久素材上传数量有限制，建议图文文章中的图片使用 `app.upload_news_image()`
方法来上传，因为通过这个接口上传的图片不会计入素材数量限制，详情请阅读 [官方文档](https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Adding_Permanent_Assets.html)。

### 上传永久图片素材

```python
# 上传图片素材
media_info = app.add_permanent_material(
    material_type="image",
    file_path="image.jpg"
)
if media_info:
    media_id, url = media_info
    print(f"素材ID：{media_id}，URL：{url}")
```

### 删除永久素材

```python
result = app.delete_permanent_material(media_id="xxx")
if result:
    print("素材删除成功")
else:
    print("删除失败")
```

### 检测草稿箱开关状态

```python
status = app.check_draft_switch_state()
if status is not None:
    print(f"草稿箱状态：{'开启' if status else '关闭'}")
```

## API 参考

### 类初始化参数

| 参数                  | 类型    | 说明                                                            |
|---------------------|-------|---------------------------------------------------------------|
| `app_id`            | `str` | 公众号 AppID                                                     |
| `app_secret`        | `str` | 公众号 AppSecret                                                 |
| `access_token_file` | `str` | Access Token 缓存文件路径（默认：系统临时目录/wechat_draft_access_token.json） |

### 核心方法

#### `get_access_token()`

- **功能**：自动获取并管理 Access Token，优先使用本地缓存，过期后自动刷新。
- **返回**：`str` - 有效的 Access Token，失败时返回 `None`。

#### `add_permanent_material(material_type, file_path, title=None, introduction=None)`

- **功能**：上传永久素材（图片、视频、语音等）。
- **参数**：
    - `material_type`：素材类型（`image`/`video`/`voice`/`thumb`）。
    - `file_path`：本地文件路径。
    - `title`：视频素材标题（仅 `video` 类型需要）。
    - `introduction`：视频素材描述（仅 `video` 类型需要）。
- **返回**：`list` - `[media_id, url]`（成功），失败返回 `None`。

#### `create_draft(title, content, ...)`

- **功能**：创建公众号草稿（支持图文/图片消息）。
- **关键参数**：
    - `title`：标题（≤64字，必填）。
    - `content`：内容（支持 HTML，必填）。
    - `thumb_media_id`：封面素材 ID（图文消息必填）。
    - `crop_percent_list`：通用裁剪参数（替代传统坐标参数，优先级更高）。
- **返回**：`str` - 草稿 ID（`media_id`），失败返回 `None`。

#### `get_crop_params(image_file_path, start_point, crop_width_px, auto_adjust_if_exceed=True)`

- **功能**：根据图片坐标自动生成微信所需的裁剪参数（支持 2.35:1、1:1、16:9 比例）。
- **参数**：
    - `image_file_path`：图片路径。
    - `start_point`：裁剪起点坐标 `(x, y)`（像素）。
    - `crop_width_px`：横向裁剪宽度（像素）。
    - `auto_adjust_if_exceed`：超出边界时自动调整（默认 `True`）。
- **返回**：`dict` - 包含裁剪参数的字典，失败返回空字典。

## 错误码说明

内置错误码解析映射，覆盖微信官方错误（部分示例）：

| 错误码    | 说明                            |
|--------|-------------------------------|
| 40001  | AppSecret 错误或 Access Token 无效 |
| 45003  | 标题长度超过限制（最多64字）               |
| 53401  | 封面图片尺寸不符合要求（建议900x500px）      |
| -41000 | Access Token 过期或无效，需重新获取      |

完整错误码见代码内 `_error_map` 常量。

## 注意事项

1. **草稿箱开关**：`open_draft()` 为不可逆操作，开启后需等待服务器生效。
2. **素材限制**：
    - 永久图片素材大小 ≤10MB，支持 `bmp/png/jpeg/jpg/gif`。
    - 图文消息正文图片需通过 `upload_news_image()` 上传（≤1MB，JPEG格式）。
3. **裁剪参数**：优先使用 `crop_percent_list` 通用参数，传统坐标参数（如 `pic_crop_235_1`）将逐步淘汰。
4. **权限问题**：部分接口（如商品功能）需公众号开通对应权限。

## 贡献与反馈

- 项目地址：[https://gitee.com/xiaoqiangclub/wechat_draft](https://gitee.com/xiaoqiangclub/wechat_draft)
- 问题反馈：通过微信公众号 `xiaoqiangclub` 联系开发者。

## 开发者信息

- **开发者**：Xiaoqiang
- **微信公众号**：xiaoqiangclub
- **开发时间**：2025年4月

---

使用过程中如有问题，请参考代码内注释或联系开发者获取支持。