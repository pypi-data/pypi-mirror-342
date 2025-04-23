from mcp.server.fastmcp import FastMCP
import os
import logging
import httpx
from dataclasses import dataclass, asdict
from typing import Any, Optional, List, Dict

# 创建日志器
logger = logging.getLogger()
# 设置日志级别
logger.setLevel(logging.INFO)

# 创建控制台处理器（StreamHandler）
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

# 创建文件处理器（FileHandler）
fileHandler = logging.FileHandler('./tmp/mcp-server-python.log', mode='a')
fileHandler.setLevel(logging.INFO)

# 创建日志格式器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 将格式器添加到处理器
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

# 将处理器添加到日志器
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)

# Initialize FastMCP server
mcp = FastMCP(
    "tool-mcp-server"
)

apiKey = os.getenv("API_KEY")

headers = {
    "X-Source": "web",
    "Content-Type": "application/json",
    "Authorization": apiKey
}


@mcp.tool()
async def getToolsList() -> dict:
    """
    获取当前支持的工具接口列表和参数

    Args:
        None
    """

    getToolsUrl = "https://yuanqi.tencent.com/openapi/v1/tools/list"

    payload = {
        "jsonrpc": "2.0",
        "id": "11111",
        "method": "tools/list",
        "params": {}
    }

    logging.info(f"开始获取工具列表")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(getToolsUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"其他错误: {str(e)}")


@mcp.tool()
async def imageClarity(imageUrl: str) -> dict:
    """
    针对低清、模糊图片进行处理，调用该插件后可输出高清的图片效果。使用示例：直接上传一个图片，输出后得到一个清晰图

    Args:
        imageUrl: 图片URL
    """

    imageClarityUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"imageClarity",
            "arguments": {
                "image_url": imageUrl
            }
        }
    }

    logging.info(f"开始调用图片清晰化工具")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(imageClarityUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"其他错误: {str(e)}")


@mcp.tool()
async def musicGeneration(musicDescription: str, requestId: str) -> dict:
    """
    根据描述生成音乐
    
    Args:
        musicDescription: 音乐描述
        requestId: 请求ID
    """

    musicGenerationUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"musicGeneration",
            "arguments": {
                "description": musicDescription,
                "request_id": requestId
            }
        }
    }
    
    logging.info(f"开始调用音乐生成工具")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(musicGenerationUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"其他错误: {str(e)}")


@mcp.tool()
async def writingAssistant(genre: str, prompt: str) -> dict:  # 已经是驼峰命名，无需修改
    """
    写作助手

    Args:
        genre: 文体类型（如小说、散文、诗歌等）
        prompt: 用户输入的提示词或主题
    """

    writingAssistantUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"writingAssistant",
            "arguments": {
                "genre": genre,
                "prompt": prompt
            }
        }
    }

    logging.info(f"开始调用写作助手")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(writingAssistantUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        logging.info(f"写作助手返回结果：{response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"其他错误: {str(e)}")


@mcp.tool()
async def imageCanny(imageUrl: str, prompt: str) -> dict:
    """
    线稿生图
    
    Args:
        imageUrl: 用户上传的线稿图url
        prompt: 可以文字定义想要生成的特定风格
    """

    imageCannyUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"imageCanny",
            "arguments": {
                "image_url": imageUrl,
                "prompt": prompt
            }
        }
    }

    logging.info(f"开始调用Canny算法处理图片")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(imageCannyUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"其他错误: {str(e)}")


@mcp.tool()
async def hunyuanSearch(keyword: str) -> dict:
    """
    混元搜索
    
    Args:
        keyword: 搜索关键词
    """
    hunyuanSearchUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"hunyuanSearch",
            "arguments": {
                "keyword": keyword
            }
        }
    }

    logging.info(f"开始调用混元搜索")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(hunyuanSearchUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"其他错误: {str(e)}")


@mcp.tool()
async def imageSearch(word: str, limit: int, size: str) -> dict:
    """
    图片检索接口允许用户通过自然语言描述在一个海量精美图库里查找AI图片。使用示例：1.帮我搜一张橘猫的照片；2.帮我搜两张春节的照片；3.找一张海边的照片
    
    Args:
        word: 搜索关键词
        limit: 返回结果数量
        size: 图片大小（{width}x{height}，如200x80）
    """

    imageSearchUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"imageSearch",
            "arguments": {
                "word": word,
                "limit": limit,
                "size": size
            }
        }
    }

    logging.info(f"开始调用图片搜索")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(imageSearchUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"其他错误: {str(e)}")


@mcp.tool()
async def pdfParse(sourceTitle: str, sourceUrl: str) -> dict:
    """
    当用户的问题是总结pdf文件内容，或问题跟pdf文件相关，且需要获取pdf文件的完整内容时，使用此工具
    
    Args:
        sourceTitle: 跟用户问题相关的，需要获取内容的PDF文件名
        sourceUrl: 跟用户问题相关的，需要获取内容的PDF文件的URL链接
    """
    pdfParseUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"pdfParse",
            "arguments": {
                "source_title": sourceTitle,
                "source_url": sourceUrl
            }
        }
    }

    logging.info(f"开始调用PDF解析")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(pdfParseUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


@mcp.tool()
async def sogouSearch(keyword: str, returnCount: int, searchSite: str, timeFilter: int) -> dict:
    """
    建议在工作流模式下使用该插件，自定义模版图。如果在提示词模式下使用该插件，请输入以下prompt模版，并更换链接以替换模版图：1. 你是一个图像换脸工具；2. 你的模版图（template_image_url）链接是：https://www.helloimg.com/i/2025/02/18/67b4004cc4284.jpg ；3. 你需要提取用户上传图（image_url）的脸部特征，将上传图里的人脸更换到模版图里
    
    Args:
        keyword: 搜索关键词
        returnCount: 返回结果数量
        searchSite: 搜索站点（如baidu.com）
        timeFilter: 搜索过滤时间，0-不限制、1-1天内、2-1周内、3-1月内、4-1年内、5-半年内、6-3年内
    """

    sogouSearchUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"sogouSearch",
            "arguments": {
                "keyword": keyword,
                "returnCount": returnCount,
                "searchSite": searchSite,
                "timeFilter": timeFilter
            }
        }
    }

    logging.info(f"开始调用搜狗搜索引擎")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(sogouSearchUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


@mcp.tool()
async def faceMerge(imageUrl: str, ipWeight: float, style: str, templateImageUrl: str) -> dict:
    """
    搜狗搜索引擎，当你需要搜索你不知道的信息，比如天气、汇率、时事等，这个工具非常有用。但是绝对不要在用户想要翻译的时候使用它
    
    Args:
        imageUrl: 用户提供的人像图片url
        ipWeight: 范围（0-1），融合相似度，数字越大越像用户图，保留一位小数
        style: real(真实优先)、balanced(平衡优先)、textured(质感优先)、beautiful(美颜优先)
        templateImageUrl: 1.模版图大小不超过4M，支持jpg/jpeg/png格式；2.模版图分辨率至少300x300的清晰图片；3.请保证人脸完整，画面占比>50%，且不能闭眼；4.目前仅支持单人换脸
    """

    faceMergeUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"faceMerge",
            "arguments": {
                "image_url": imageUrl,
                "ip_weight": ipWeight,
                "style": style,
                "template_image_url": templateImageUrl
            }
        }
    }
    
    logging.info(f"开始调用人脸融合")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(faceMergeUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


@mcp.tool()
async def ocr(imageUrl: str, prompt: str) -> dict:
    """
    图片识别文字 OCR
    
    Args:
        imageUrl: 用户上传图片的url地址
        prompt: 用户描述想要识别的内容
    """

    ocr_url = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"ocr",
            "arguments": {
                "image_url": imageUrl,
                "prompt": prompt
            }
        }
    }
    
    logging.info(f"开始调用OCR识别")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(ocr_url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


@mcp.tool()
async def documentDeepRead(fileUrl: str, prompt: str, type: str) -> dict:
    """
    学生阅读论文、需要论文助手进行速览、总结
    
    Args:
        fileUrl: 仅支持以下格式的文档：pdf,txt,doc,docx,ppt,pptx
        prompt: 可以指定对文档的类型和要执行的阅读任务进行定义
        type: 指定文档类型：学术论文、研报、其他
    """

    documentDeepReadUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"documentDeepRead",
            "arguments": {
                "file_url": fileUrl,
                "prompt": prompt,
                "type": type
            }
        }
    }

    logging.info(f"开始调用文档深度阅读")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(documentDeepReadUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


@mcp.tool()
async def imageReplaceBackground(imageUrl: str, prompt: str) -> str:
    """
    用户上传图片后，可通过自然语言描述更换图片的背景
    
    Args:
        imageUrl: 用户上传图片url
        prompt: 可以直接定义一种风格的特定prompt
    """

    imageReplaceBackgroundUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"imageReplaceBackground",
            "arguments": {
                "image_url": imageUrl,
                "prompt": prompt
            }
        }
    }

    logging.info(f"开始调用图片替换背景")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(imageReplaceBackgroundUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


@mcp.tool()
async def webBrowser(url: str) -> dict:
    """
    从url链接提取网页中的标题、正文，当您需要获取网页内容时非常有用。

    Args:
        url: 用户期望获取网页内容的url
    """

    webBrowserUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"webBrowser",
            "arguments": {
                "url": url
            }
        }
    }

    logging.info(f"开始调用网页浏览器")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(webBrowserUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


@mcp.tool()
async def hunyuanText2Image(imageUrl: str, prompt: str) -> dict:
    """
    通过文字描述生成图片，或者根据要求修改图片
    
    Args:
        imageUrl: 需要修改的图片url地址
        prompt: 用于生成图片或者修改图片的提示词
    """
    
    hunyuanText2ImageUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"hunyuanText2Image",
            "arguments": {
                "image_url": imageUrl,
                "prompt": prompt
            }
        }
    }

    logging.info(f"开始调用混元文本转图像")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(hunyuanText2ImageUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


@mcp.tool()
async def photoStylize(imageUrl: str, style: str) -> dict:
    """
    人像风格化API允许用户上传一张人像图片，并选择一种风格，结果是将改人像图片转化成对应风格的人像图片
    
    Args:
        imageUrl: 上传图片大小不超过4.5M，支持jpg/jpeg格式
        style: 可选的风格：夏日水镜风格，小星星风格，皮克斯卡通风格，多巴胺风格，复古港漫风格，日漫风格，婚礼人像风，金币环绕风格，3d职场，3d古风，3d游乐场，3d宇航员，3d芭比，3d复古，度假漫画风。
    """

    photoStylizeUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"photoStylize",
            "arguments": {
                "image_url": imageUrl,
                "style": style
            }
        }
    }

    logging.info(f"开始调用人像风格化")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(photoStylizeUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


@mcp.tool()
async def textTranslation(field: str, source: str, target: str, text: str) -> dict:
    """将文本从一种语言翻译成另一种语言。
    
    Args:
        field: 开发者可以自己指定翻译文本所属领域，例如学术、游戏等
        source: 源语言的支持类型，支持简体中文：zh，英语：en，法语：fr；葡萄牙语：pt，西班牙语：es，日语：ja，俄语：ru，阿拉伯语：ar，韩语：ko，意大利语：it，德语：de
        target: 目标语言的支持类型，支持简体中文：zh，英语：en，法语：fr；葡萄牙语：pt，西班牙语：es，日语：ja，俄语：ru，阿拉伯语：ar，韩语：ko，意大利语：it，德语：de
        text: 待翻译的文本
    """

    textTranslationUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"textTranslation",
            "arguments": {
                "field": field,
                "source": source,
                "target": target,
                "text": text
            }
        }
    }

    logging.info(f"开始调用文本翻译")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(textTranslationUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


@mcp.tool()
async def imageRetouchSwitch(imageUrl: str, style: str) -> dict:
    """
    图片风格转换
    
    Args:
        imageUrl: 用户上传的图片url
        style: 可选的风格：宫崎骏、水彩、像素、极简、胶片电影、素描、水墨画、油画、粘土、彩铅
    """

    imageRetouchSwitchUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"imageRetouchSwitch",
            "arguments": {
                "image_url": imageUrl,
                "style": style
            }
        }
    }

    logging.info(f"开始调用图像修型开关")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(imageRetouchSwitchUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


@mcp.tool()
async def pdfContentSearch(sourceUrl: str, sourceTitle: str, prompt: str) -> str:
    """
    当用户的问题需要检索pdf文件中的指定内容时，使用此工具
    
    Args:
        sourceUrl: 跟用户问题相关的，需要检索内容的PDF文件的URL链接
        sourceTitle: 跟用户问题相关的，需要检索内容的PDF文件名
        prompt: 需要在pdf文件中检索的内容
    """

    pdfContentSearchUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"pdfContentSearch",
            "arguments": {
                "source_url": sourceUrl,
                "source_title": sourceTitle,
                "prompt": prompt
            }
        }
    }

    logging.info(f"开始调用PDF内容搜索")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(pdfContentSearchUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


@mcp.tool()
async def hunyuanImage2Text(prompt: str, resourceUrl: str) -> str:
    """
    用户上传的图片后，对图片中的内容进行分析和理解

    Args:
        prompt: 用于辅助理解图片内容的提示词
        resourceUrl: 需要被理解的图片url地址
    """

    hunyuanImage2TextUrl = "https://yuanqi.tencent.com/openapi/v1/tools/call"

    payload = {
        "jsonrpc": "2.0",
        "id": "22222",
        "method": "tools/call",
        "params": {
            "name":"hunyuanImage2Text",
            "arguments": {
                "prompt": prompt,
                "resource_url": resourceUrl
            }
        }
    }

    logging.info(f"开始调用混元图像转文本")

    try:
        timeout = httpx.Timeout(60.0, connect=30.0)
        response = httpx.post(hunyuanImage2TextUrl, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # 自动处理4xx/5xx错误
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")


def run_mcp():
    mcp.run(transport='stdio')

if __name__ == '__main__':
    run_mcp()
