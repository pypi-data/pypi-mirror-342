import os
from PIL import Image
from typing import Tuple, Dict, List, Union
from wechat_draft.utils import log


def calculate_crop_parameters(image_file_path: str,
                              start_point: Tuple[int, int],
                              crop_width_px: int,
                              auto_adjust_if_exceed: bool = True) -> Dict[str, Union[str, List[Dict]]]:
    """
    根据用户设定的图片文件路径、截图起点和横轴方向剪切像素，返回微信公众号草稿箱接口所需的裁剪参数。
    新增 auto_adjust_if_exceed 参数，控制当裁剪尺寸超出图片边界时是否自动调整。

    :param image_file_path: 图片文件路径，字符串类型。
    :param start_point: 截图的起点坐标 (x, y)，元组类型，元素为整数。
    :param crop_width_px: 横轴方向剪切的像素宽度，整数类型。
    :param auto_adjust_if_exceed: 布尔类型，默认为 True。
                                  True: 当裁剪尺寸超出图片边界时，自动调整 crop_width_px 和 crop_height_px 到最大可能值，保持比例。
                                  False: 当裁剪尺寸超出图片边界时，抛出 ValueError 异常。
    :return: 包含 pic_crop_235_1, pic_crop_1_1, crop_percent_list 参数的字典。
             pic_crop_235_1 和 pic_crop_1_1 的值为字符串类型，crop_percent_list 的值为列表类型。
             如果发生错误 (FileNotFoundError 或 ValueError 且 auto_adjust_if_exceed 为 False)，返回空字典。
    :raises ValueError: 当 auto_adjust_if_exceed 为 False 且裁剪尺寸超出图片边界时。
    """
    try:
        image = Image.open(image_file_path)
        original_width, original_height = image.size
        log.debug(f"图片原始尺寸：宽度={original_width}px, 高度={original_height}px")

        start_x_px, start_y_px = start_point
        log.debug(f"截图起点（像素坐标）：x={start_x_px}px, y={start_y_px}px")
        log.debug(f"横轴剪切宽度（像素）：{crop_width_px}px")
        log.debug(f"自动调整超出边界参数：{'开启' if auto_adjust_if_exceed else '关闭'}")

        crop_params_dict = {}
        ratios = {"2.35_1": 1 / 2.35, "1_1": 1, "16_9": 9 / 16}  # 存储比例和对应的height/width比值
        crop_percent_list = []

        for ratio_name, ratio_hw in ratios.items():
            current_crop_width_px = crop_width_px  # 使用一个变量在循环内调整，避免影响外层 crop_width_px
            crop_height_px = int(current_crop_width_px * ratio_hw)
            end_x_px = start_x_px + current_crop_width_px
            end_y_px = start_y_px + crop_height_px

            # 检查是否超出边界并进行调整或报错
            if end_x_px > original_width or end_y_px > original_height:
                if auto_adjust_if_exceed:
                    log.warning(f"比例 {ratio_name} 裁剪尺寸超出图片边界，尝试自动调整...")
                    # 优先调整宽度，确保宽度不超过边界
                    if end_x_px > original_width:
                        current_crop_width_px = original_width - start_x_px
                        if current_crop_width_px < 0:
                            current_crop_width_px = 0  # 避免起点超出图片导致宽度为负数
                        crop_height_px = int(current_crop_width_px * ratio_hw)
                        end_x_px = start_x_px + current_crop_width_px
                        end_y_px = start_y_px + crop_height_px
                        log.warning(f"宽度超出边界，已调整 crop_width_px 为 {current_crop_width_px}px")

                    # 调整宽度后，再次检查高度，并调整高度 (实际上宽度调整已经大概率可以解决高度问题，但再次检查更稳妥)
                    if end_y_px > original_height:
                        crop_height_px = original_height - start_y_px
                        if crop_height_px < 0:
                            crop_height_px = 0  # 避免起点超出图片导致高度为负数
                        current_crop_width_px = int(crop_height_px / ratio_hw)  # 根据调整后的高度反算宽度，保证比例
                        end_x_px = start_x_px + current_crop_width_px
                        end_y_px = start_y_px + crop_height_px
                        log.warning(
                            f"高度超出边界，已调整 crop_height_px 为 {crop_height_px}px，并同步调整 crop_width_px 为 {current_crop_width_px}px 以保持比例")

                    log.debug(f"比例 {ratio_name} 自动调整后裁剪参数:")
                    log.debug(
                        f"  调整后裁剪区域（像素坐标）：左上角=({start_x_px}px, {start_y_px}px), 右下角=({end_x_px}px, {end_y_px}px)")

                else:
                    raise ValueError(f"比例 {ratio_name} 裁剪参数超出图片边界。"
                                     f"起点 ({start_x_px}, {start_y_px}), 剪切宽度 {crop_width_px}px，计算出的裁剪区域右下角坐标为 ({end_x_px}, {end_y_px})"
                                     f"，超出图片尺寸 (宽度={original_width}px, 高度={original_height}px)。"
                                     f"请调整 start_point 或 crop_width_px 参数，或开启 auto_adjust_if_exceed 参数以自动调整。")

            # 归一化坐标
            x1_normalized = start_x_px / original_width
            y1_normalized = start_y_px / original_height
            x2_normalized = end_x_px / original_width
            y2_normalized = end_y_px / original_height

            # 格式化为字符串，保留6位小数
            x1_str = f"{x1_normalized:.6f}"
            y1_str = f"{y1_normalized:.6f}"
            x2_str = f"{x2_normalized:.6f}"
            y2_str = f"{y2_normalized:.6f}"

            log.debug(f"比例 {ratio_name} 裁剪参数:")
            log.debug(
                f"  裁剪区域（像素坐标）：左上角=({start_x_px}px, {start_y_px}px), 右下角=({end_x_px}px, {end_y_px}px)")
            log.debug(f"  归一化坐标：x1={x1_str}, y1={y1_str}, x2={x2_str}, y2={y2_str}")

            if ratio_name == "2.35_1":
                crop_params_dict["pic_crop_235_1"] = f"{x1_str}_{y1_str}_{x2_str}_{y2_str}"
            elif ratio_name == "1_1":
                crop_params_dict["pic_crop_1_1"] = f"{x1_str}_{y1_str}_{x2_str}_{y2_str}"
            elif ratio_name == "16_9":
                crop_params_dict["pic_crop_16_9"] = f"{x1_str}_{y1_str}_{x2_str}_{y2_str}"

            crop_percent_list.append({
                "ratio": ratio_name.replace("_", "_"),  # 保持ratio参数为 "1_1", "16_9", "2.35_1" 符合文档
                "x1": float(x1_str),
                "y1": float(y1_str),
                "x2": float(x2_str),
                "y2": float(y2_str)
            })

        crop_params_dict["crop_percent_list"] = crop_percent_list
        return crop_params_dict

    except FileNotFoundError:
        log.error(f"错误：图片文件未找到：{image_file_path}")
        return {}  # 返回空字典表示错误
    except ValueError as ve:
        if not auto_adjust_if_exceed:
            log.error(f"参数错误: {ve}")  # 只有在不自动调整时才记录 ValueError，否则自动调整已经warning了
            return {}  # 返回空字典表示错误
        else:  # 如果开启了自动调整，但还是有其他ValueError，例如 Pillow 库的错误，也需要捕获并返回空字典
            log.error(f"处理图片时发生错误: {ve}")
            return {}
    except Exception as e:
        log.error(f"处理图片时发生未知错误: {e}")
        return {}  # 返回空字典表示错误


if __name__ == '__main__':
    # 示例用法 (请替换为实际的图片路径和参数)
    image_path = "test.jpeg"  # 替换为你的图片路径, 请确保存在 test.jpg 文件

    # 示例 1:  crop_width_px 超出图片宽度，auto_adjust_if_exceed=True (默认)
    start_point_1 = (100, 50)
    crop_width_px_1 = 5000  # 宽度会超出，因为图片宽度只有 200px
    crop_parameters_1 = calculate_crop_parameters(image_path, start_point_1, crop_width_px_1,
                                                  auto_adjust_if_exceed=True)
    print(crop_parameters_1)
