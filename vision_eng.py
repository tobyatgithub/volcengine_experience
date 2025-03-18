import base64
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from volcengine.visual.VisualService import VisualService

# 加载 .env 文件
load_dotenv()


def ocr_recognition(image_path: str, mode: Literal["normal", "accurate"] = "normal"):
    """
    执行OCR文字识别
    
    Args:
        image_path: 图片路径
        mode: OCR模式，可选 "normal"（通用文字识别）或 "accurate"（高精度文字识别）
    """
    # 创建 VisualService 实例
    visual_service = VisualService()

    # 从环境变量获取并设置 AK/SK
    visual_service.set_ak(os.getenv("AccessKeyId"))
    visual_service.set_sk(os.getenv("SecretAccessKey"))

    try:
        # 读取图片文件
        with open(image_path, "rb") as f:
            image_data = f.read()

        # 将图片转base64编码
        base64_data = base64.b64encode(image_data)
        
        if mode == "accurate":
            # 构造高精度识别请求参数
            body = {
                "image_base64": base64_data,
                "scene": "high_accuracy"  # 明确指定高精度场景
            }
            # 调用高精度识别接口
            resp = visual_service.ocr_accurate(body)
        else:
            # 构造通用识别请求参数
            body = {
                "image_base64": base64_data
            }
            # 调用通用文字识别接口
            resp = visual_service.ocr_normal(body)
        
        # 准备保存结果
        result = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "image_path": image_path,
            "ocr_mode": mode,
            "ocr_result": resp
        }
        
        # 创建results目录（如果不存在）
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        # 生成输出文件名（使用时间戳和模式）
        output_file = results_dir / f"ocr_result_{mode}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # 保存结果到JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print(f"\nOCR Recognition Results ({mode} mode) saved to: {output_file}")
        print("\nRecognized text:")
        for line in resp.get('data', {}).get('line_texts', []):
            print(f"- {line}")
            
        return result

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None


if __name__ == "__main__":
    # 使用示例
    image_path = "images/1742216223472.jpg"  # 替换为你的图片路径
    
    # # 使用通用文字识别
    # print("\n=== Running Normal OCR ===")
    # ocr_recognition(image_path, mode="normal")
    
    # 使用高精度文字识别
    print("\n=== Running Accurate OCR ===")
    ocr_recognition(image_path, mode="accurate")
