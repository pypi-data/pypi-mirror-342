"""LightPDF AI助手 MCP Server模块"""
# 标准库导入
import asyncio
import os
import sys
import argparse
import json
from typing import List, Dict, Any, Callable, TypeVar, Optional, Union

# 第三方库导入
from dotenv import load_dotenv

# MCP相关导入
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types

# 本地导入
from .common import BaseResult, Logger, FileHandler
from .converter import Converter, ConversionResult
from .editor import Editor, EditResult

# 加载环境变量
load_dotenv()

# 类型定义
T = TypeVar('T', bound=BaseResult)
ProcessFunc = Callable[[str], Any]

def generate_result_report(
    results: List[BaseResult], 
    operation_name: str
) -> str:
    """生成通用结果报告
    
    Args:
        results: 结果列表
        operation_name: 操作名称
        
    Returns:
        str: JSON格式的报告文本
    """
    # 统计结果
    success_count = sum(1 for r in results if r.success)
    failed_count = len(results) - success_count
    
    # 构建结果JSON对象
    report_obj = {
        "operation": operation_name,
        "total": len(results),
        "success_count": success_count,
        "failed_count": failed_count,
        "success_files": [],
        "failed_files": []
    }
    
    for result in results:
        if result.success:
            # 添加成功的文件信息
            report_obj["success_files"].append({
                "file_path": result.file_path,
                "original_name": result.original_name,
                "download_url": result.download_url
            })
        else:
            # 添加失败的文件信息
            report_obj["failed_files"].append({
                "file_path": result.file_path,
                "original_name": result.original_name,
                "error_message": result.error_message
            })
    
    # 返回JSON字符串
    return json.dumps(report_obj, ensure_ascii=False)

async def process_batch_files(
    file_objects: List[Dict[str, str]], 
    logger: Logger, 
    process_func: Callable[[str, Optional[str], Optional[str]], T],
    operation_desc: Optional[str] = None
) -> List[T]:
    """通用批处理文件函数
    
    Args:
        file_objects: 文件对象列表，每个对象包含path和可选的password及name
        logger: 日志记录器
        process_func: 处理单个文件的异步函数，接收file_path、password和original_name参数
        operation_desc: 操作描述，用于日志记录
    
    Returns:
        List[T]: 处理结果列表
    """
    if len(file_objects) > 1 and operation_desc:
        await logger.log("info", f"开始批量{operation_desc}，共 {len(file_objects)} 个文件")
        
        # 并发处理文件，限制并发数为5
        semaphore = asyncio.Semaphore(5)
        
        async def process_with_semaphore(file_obj: Dict[str, str]) -> T:
            async with semaphore:
                file_path = file_obj["path"]
                password = file_obj.get("password")
                original_name = file_obj.get("name")
                return await process_func(file_path, password, original_name)
        
        # 创建任务列表
        tasks = [process_with_semaphore(file_obj) for file_obj in file_objects]
        return await asyncio.gather(*tasks)
    else:
        # 单文件处理
        file_path = file_objects[0]["path"]
        password = file_objects[0].get("password")
        original_name = file_objects[0].get("name")
        return [await process_func(file_path, password, original_name)]

async def process_conversion_file(
    file_path: str, 
    format: str, 
    converter: Converter, 
    extra_params: Optional[Dict[str, Any]] = None, 
    password: Optional[str] = None,
    original_name: Optional[str] = None
) -> ConversionResult:
    """处理单个文件转换"""
    is_page_numbering = format == "number-pdf"
    
    if is_page_numbering and extra_params:
        # 对于添加页码，使用add_page_numbers方法
        return await converter.add_page_numbers(
            file_path, 
            extra_params.get("start_num", 1),
            extra_params.get("position", "5"),
            extra_params.get("margin", 30),
            password,
            original_name
        )
    else:
        # 对于其他操作，使用convert_file方法
        return await converter.convert_file(file_path, format, extra_params, password, original_name)

async def process_edit_file(
    file_path: str, 
    edit_type: str, 
    editor: Editor, 
    extra_params: Dict[str, Any] = None,
    password: Optional[str] = None,
    original_name: Optional[str] = None
) -> EditResult:
    """处理单个文件编辑"""
    if edit_type == "decrypt":
        return await editor.decrypt_pdf(file_path, password, original_name)
    elif edit_type == "add_watermark":
        return await editor.add_watermark(
            file_path=file_path,
            text=extra_params.get("text", "水印"),
            position=extra_params.get("position", "center"),
            opacity=extra_params.get("opacity", 0.5),
            range=extra_params.get("range", ""),
            layout=extra_params.get("layout", "on"),
            font_family=extra_params.get("font_family"),
            font_size=extra_params.get("font_size"),
            font_color=extra_params.get("font_color"),
            password=password,
            original_name=original_name
        )
    elif edit_type == "encrypt":
        return await editor.encrypt_pdf(
            file_path=file_path,
            password=extra_params.get("password", ""),
            original_password=password,
            original_name=original_name
        )
    elif edit_type == "compress":
        return await editor.compress_pdf(
            file_path=file_path,
            image_quantity=extra_params.get("image_quantity", 60),
            password=password,
            original_name=original_name
        )
    elif edit_type == "split":
        return await editor.split_pdf(
            file_path=file_path,
            pages=extra_params.get("pages", ""),
            password=password,
            split_type=extra_params.get("split_type", "page"),
            merge_all=extra_params.get("merge_all", 1),
            original_name=original_name
        )
    elif edit_type == "merge":
        # 对于合并操作，我们需要特殊处理，因为它需要处理多个文件
        return EditResult(
            success=False, 
            file_path=file_path, 
            error_message="合并操作需要使用特殊处理流程",
            original_name=original_name
        )
    elif edit_type == "rotate":
        return await editor.rotate_pdf(
            file_path=file_path, 
            angle=extra_params.get("angle", 90),
            pages=extra_params.get("pages", ""),
            password=password,
            original_name=original_name
        )
    else:
        return EditResult(
            success=False, 
            file_path=file_path, 
            error_message=f"不支持的编辑类型: {edit_type}",
            original_name=original_name
        )

async def process_tool_call(
    logger: Logger, 
    file_objects: List[Dict[str, str]], 
    operation_config: Dict[str, Any]
) -> types.TextContent:
    """通用工具调用处理函数
    
    Args:
        logger: 日志记录器
        file_objects: 文件对象列表，每个对象包含path和可选的password
        operation_config: 操作配置，包括操作类型、格式、参数等
        
    Returns:
        types.TextContent: 包含处理结果的文本内容
    """
    file_handler = FileHandler(logger)
    
    # 根据操作类型选择不同的处理逻辑
    if operation_config.get("is_edit_operation"):
        # 编辑操作
        editor = Editor(logger, file_handler)
        edit_type = operation_config.get("edit_type", "")
        extra_params = operation_config.get("extra_params")
        
        # 获取操作描述
        edit_map = {
            "decrypt": "解密", 
            "add_watermark": "添加水印", 
            "encrypt": "加密", 
            "compress": "压缩", 
            "split": "拆分", 
            "merge": "合并", 
            "rotate": "旋转"
        }
        operation_desc = f"PDF{edit_map.get(edit_type, edit_type)}"
        
        # 处理文件
        results = await process_batch_files(
            file_objects, 
            logger,
            lambda file_path, password, original_name: process_edit_file(
                file_path, edit_type, editor, extra_params, password, original_name
            ),
            operation_desc
        )
        
        # 生成报告
        report_msg = generate_result_report(
            results, 
            operation_desc
        )
    else:
        # 转换操作
        converter = Converter(logger, file_handler)
        format = operation_config.get("format", "")
        extra_params = operation_config.get("extra_params")
        is_watermark_removal = operation_config.get("is_watermark_removal", False)
        is_page_numbering = operation_config.get("is_page_numbering", False)
        
        # 获取操作描述
        if is_watermark_removal:
            operation_desc = "去除水印"
            task_type = "水印去除"
        elif is_page_numbering:
            operation_desc = "添加页码"
            task_type = "添加页码"
        else:
            operation_desc = f"转换为 {format} 格式"
            task_type = "转换"
        
        # 处理文件
        results = await process_batch_files(
            file_objects,
            logger,
            lambda file_path, password, original_name: process_conversion_file(
                file_path, format, converter, extra_params, password, original_name
            ),
            operation_desc
        )
        
        # 生成报告
        report_msg = generate_result_report(
            results, 
            task_type
        )
    
    # 如果全部失败，记录错误
    if not any(r.success for r in results):
        await logger.error(report_msg)
    
    return types.TextContent(type="text", text=report_msg)

# 创建Server实例
app = Server(
    name="LightPDF_AI_tools",
    instructions="轻闪文档处理工具。",
)

# 定义工具
@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="convert_document",
            description="文档格式转换工具。\n\nPDF可转换为：DOCX/XLSX/PPTX/图片/HTML/TXT；\n其他格式可转换为PDF：DOCX/XLSX/PPTX/图片/CAD/CAJ/OFD",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "文件路径或URL"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "文档密码，如果文档受密码保护，则需要提供此参数"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "文件的原始文件名"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "要转换的文件列表，每个文件包含路径和可选的密码"
                    },
                    "format": {
                        "type": "string",
                        "description": "目标格式",
                        "enum": ["pdf", "docx", "xlsx", "pptx", "jpg", "jpeg", "png", "bmp", "gif", "html", "txt"]
                    }
                },
                "required": ["files", "format"]
            }
        ),
        types.Tool(
            name="add_page_numbers",
            description="在PDF文档的每一页上添加页码。",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF文件路径或URL"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF文档密码，如果文档受密码保护，则需要提供此参数"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "文件的原始文件名"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "要添加页码的PDF文件列表，每个文件包含路径和可选的密码"
                    },
                    "start_num": {
                        "type": "integer",
                        "description": "起始页码",
                        "default": 1,
                        "minimum": 1
                    },
                    "position": {
                        "type": "string",
                        "description": "页码位置：1(左上), 2(上中), 3(右上), 4(左下), 5(下中), 6(右下)",
                        "enum": ["1", "2", "3", "4", "5", "6"],
                        "default": "5"
                    },
                    "margin": {
                        "type": "integer",
                        "description": "页码边距",
                        "enum": [10, 30, 60],
                        "default": 30
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="remove_watermark",
            description="去除PDF文件中的水印，将文件处理后返回无水印的PDF版本。",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF文件路径或URL"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF文档密码，如果文档受密码保护，则需要提供此参数"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "文件的原始文件名"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "要去除水印的PDF文件列表，每个文件包含路径和可选的密码"
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="add_watermark",
            description="为PDF文件添加文本水印。",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "需要添加水印的PDF文件路径或URL"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF文档密码，如果文档受密码保护，则需要提供此参数"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "文件的原始文件名"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "需要添加水印的PDF文件列表，每个文件包含路径和可选的密码"
                    },
                    "text": {
                        "type": "string",
                        "description": "水印文本内容"
                    },
                    "position": {
                        "type": "string",
                        "description": "水印位置: 左上(topleft), 上中(top), 右上(topright), 左(left), 中(center), 右(right), 左下(bottomleft), 下(bottom), 右下(bottomright), 对角线(diagonal，-45度), 反对角线(reverse-diagonal，45度)",
                        "enum": ["topleft", "top", "topright", "left", "center", "right", 
                                "bottomleft", "bottom", "bottomright", "diagonal", "reverse-diagonal"],
                        "default": "center"
                    },
                    "opacity": {
                        "type": "number",
                        "description": "透明度，0.0-1.0",
                        "default": 1.0,
                        "minimum": 0.0,
                        "maximum": 1.0
                    },
                    "range": {
                        "type": "string",
                        "description": "页面范围，例如 '1,3,5-7' 或 ''（空字符串或不设置）表示所有页面"
                    },
                    "layout": {
                        "type": "string",
                        "description": "布局位置：在内容上(on)或在内容下(under)",
                        "enum": ["on", "under"],
                        "default": "on"
                    },
                    "font_family": {
                        "type": "string",
                        "description": "字体"
                    },
                    "font_size": {
                        "type": "integer",
                        "description": "字体大小"
                    },
                    "font_color": {
                        "type": "string",
                        "description": "字体颜色，如 '#ff0000' 表示红色"
                    }
                },
                "required": ["files", "text", "position"]
            }
        ),
        types.Tool(
            name="unlock_pdf",
            description="移除PDF文件的密码保护，生成无密码版本的PDF文件。",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "需要解密的PDF文件路径或URL"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF文档的密码，用于解锁文档，如果文档受密码保护，则需要提供此参数"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "文件的原始文件名"
                                }
                            },
                            "required": ["path", "password"]
                        },
                        "description": "需要解密的PDF文件列表，每个文件包含路径和密码"
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="protect_pdf",
            description="为PDF文件添加密码保护。",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "需要加密的PDF文件路径或URL"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF文档密码，如果文档受密码保护，则需要提供此参数"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "文件的原始文件名"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "需要加密的PDF文件列表，每个文件包含路径和可选的原密码"
                    },
                    "password": {
                        "type": "string",
                        "description": "要设置的新密码"
                    }
                },
                "required": ["files", "password"]
            }
        ),
        types.Tool(
            name="compress_pdf",
            description="压缩PDF文件大小。",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "需要压缩的PDF文件路径或URL"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF文档密码，如果文档受密码保护，则需要提供此参数"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "文件的原始文件名"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "需要压缩的PDF文件列表，每个文件包含路径和可选的密码"
                    },
                    "image_quantity": {
                        "type": "integer",
                        "description": "图像质量，1-100，值越低压缩率越高",
                        "default": 60,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="split_pdf",
            description="拆分PDF文件到多个文件。",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "需要拆分的PDF文件路径或URL"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF文档密码，如果文档受密码保护，则需要提供此参数"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "文件的原始文件名"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "需要拆分的PDF文件列表，每个文件包含路径和可选的密码"
                    },
                    "split_type": {
                        "type": "string",
                        "description": "拆分类型: 每个页面拆分成一个文件(every)或按pages范围拆分(page)",
                        "enum": ["every", "page"],
                        "default": "page"
                    },
                    "pages": {
                        "type": "string",
                        "description": "指定要拆分的页面范围，例如 '1,3,5-7' 或 ''（空字符串或不设置）表示所有页面。仅当split_type为page时有效"
                    },
                    "merge_all": {
                        "type": "integer",
                        "description": "是否将结果合并为一个PDF文件: 1=是，0=否（将会返回多个文件的zip包）。仅当split_type为page时有效",
                        "enum": [0, 1],
                        "default": 0
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="merge_pdfs",
            description="合并多个PDF文件。",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "需要合并的PDF文件路径或URL"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF文档密码，如果文档受密码保护，则需要提供此参数"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "文件的原始文件名"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "需要合并的PDF文件列表，每个文件包含路径和可选的密码"
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="rotate_pdf",
            description="旋转PDF文件的页面。",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "需要旋转的PDF文件路径或URL"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF文档密码，如果文档受密码保护，则需要提供此参数"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "文件的原始文件名"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "需要旋转的PDF文件列表，每个文件包含路径和可选的密码"
                    },
                    "angle": {
                        "type": "integer",
                        "description": "旋转角度，可选值为90、180、270",
                        "enum": [90, 180, 270],
                        "default": 90
                    },
                    "pages": {
                        "type": "string",
                        "description": "指定要旋转的页面范围，例如 '1,3,5-7' 或 ''（空字符串或不设置）表示所有页面"
                    }
                },
                "required": ["files", "angle"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    # 创建日志记录器
    logger = Logger(app.request_context)
    
    # 定义工具配置和默认参数值
    TOOL_CONFIG = {
        "convert_document": {
            "format_key": "format",  # 从arguments获取format
            "is_watermark_removal": False,
            "is_page_numbering": False,
            "is_edit_operation": False,
        },
        "remove_watermark": {
            "format": "doc-repair",  # 固定format
            "is_watermark_removal": True,
            "is_page_numbering": False,
            "is_edit_operation": False,
        },
        "add_page_numbers": {
            "format": "number-pdf",  # 固定format
            "is_watermark_removal": False,
            "is_page_numbering": True,
            "is_edit_operation": False,
            "param_keys": ["start_num", "position", "margin"]  # 需要从arguments获取的参数
        },
        "unlock_pdf": {
            "edit_type": "decrypt",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
        },
        "add_watermark": {
            "edit_type": "add_watermark",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
            "param_keys": ["text", "position", "opacity", "range", "layout", 
                          "font_family", "font_size", "font_color"]  # 需要从arguments获取的参数
        },
        "protect_pdf": {
            "edit_type": "encrypt",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
            "param_keys": ["password"]  # 需要从arguments获取的参数
        },
        "compress_pdf": {
            "edit_type": "compress",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
            "param_keys": ["image_quantity"]  # 需要从arguments获取的参数
        },
        "split_pdf": {
            "edit_type": "split",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
            "param_keys": ["pages", "split_type", "merge_all"]  # 需要从arguments获取的参数
        },
        "merge_pdfs": {
            "edit_type": "merge",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
        },
        "rotate_pdf": {
            "edit_type": "rotate",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
            "param_keys": ["angle", "pages"]  # 需要从arguments获取的参数
        }
    }
    
    DEFAULTS = {
        "start_num": 1,
        "position_page_numbers": "5",  # 添加页码的位置默认值
        "position_watermark": "center",  # 水印的位置默认值
        "margin": 30,
        "opacity": 0.5,
        "range": "",
        "layout": "on",  # 添加layout默认值
        "image_quantity": 60,
        "split_type": "page",
        "merge_all": 1,
        "angle": 90,
        "pages": ""
    }
    
    if name in TOOL_CONFIG:
        # 处理文件信息
        file_objects = arguments.get("files", [])
        if not file_objects:
            error_msg = "未提供文件信息"
            await logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]
        
        # 确保file_objects是一个列表
        if isinstance(file_objects, dict):
            file_objects = [file_objects]
            
        config = TOOL_CONFIG[name]
        operation_config = dict(config)  # 复制配置
        
        # 处理格式
        if not operation_config.get("format") and "format_key" in config:
            operation_config["format"] = arguments.get(config["format_key"], "")
        
        # 处理额外参数
        if "param_keys" in config:
            operation_config["extra_params"] = {}
            
            # 处理特殊情况：position参数在不同工具中有不同的默认值
            for key in config["param_keys"]:
                if key == "position":
                    if name == "add_page_numbers":
                        # 添加页码工具使用"5"作为position默认值
                        operation_config["extra_params"][key] = arguments.get(key, DEFAULTS.get("position_page_numbers"))
                    elif name == "add_watermark":
                        # 添加水印工具使用"center"作为position默认值
                        operation_config["extra_params"][key] = arguments.get(key, DEFAULTS.get("position_watermark"))
                    else:
                        # 其他工具使用通用默认值
                        operation_config["extra_params"][key] = arguments.get(key, DEFAULTS.get(key))
                else:
                    # 其他参数正常处理
                    operation_config["extra_params"][key] = arguments.get(key, DEFAULTS.get(key, ""))
            
            # 对于protect_pdf工具，需要处理新密码
            if name == "protect_pdf" and "password" in arguments:
                operation_config["extra_params"]["password"] = arguments.get("password")
        
        # 特殊处理merge_pdfs工具
        if name == "merge_pdfs":
            # 创建编辑器
            file_handler = FileHandler(logger)
            editor = Editor(logger, file_handler)
            
            # 提取文件路径、密码和原始名称
            file_paths = [file_obj["path"] for file_obj in file_objects]
            passwords = [file_obj.get("password") for file_obj in file_objects]
            original_names = [file_obj.get("name") for file_obj in file_objects]
            
            # 由于merge_pdfs方法只接受一个密码参数，如果文件密码不同，可能需要特殊处理
            # 此处简化处理，使用第一个非空密码
            password = next((p for p in passwords if p), None)
            
            # 合并文件名用于结果文件
            merged_name = None
            if any(original_names):
                # 如果有原始文件名，则合并它们（最多使用前两个文件名）
                valid_names = [name for name in original_names if name]
                if valid_names:
                    if len(valid_names) == 1:
                        merged_name = valid_names[0]
                    else:
                        merged_name = f"{valid_names[0]}_{valid_names[1]}_等"
            
            # 直接调用merge_pdfs方法
            result = await editor.merge_pdfs(file_paths, password, merged_name)
            
            # 构建结果报告
            report_msg = generate_result_report(
                [result], 
                "PDF合并"
            )
            
            # 如果失败，记录错误
            if not result.success:
                await logger.error(report_msg)
            
            return [types.TextContent(type="text", text=report_msg)]
        
        # 调用通用处理函数
        result = await process_tool_call(logger, file_objects, operation_config)
        return [result]
    
    error_msg = f"未知工具: {name}"
    await logger.error(error_msg, ValueError)
    return [types.TextContent(type="text", text=error_msg)]

async def main():
    """应用主入口"""
    # 打印版本号
    try:
        import importlib.metadata
        version = importlib.metadata.version("lightpdf-aipdf-mcp")
        print(f"LightPDF AI-PDF MCP Server v{version}", file=sys.stderr)
    except Exception as e:
        print("LightPDF AI-PDF MCP Server (版本信息获取失败)", file=sys.stderr)
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="LightPDF AI-PDF MCP Server")
    parser.add_argument("-p", "--port", type=int, default=0, help="指定SSE服务器的端口号，如果提供则使用SSE模式，否则使用stdio模式")
    args = parser.parse_args()
    
    initialization_options = app.create_initialization_options(
        notification_options=NotificationOptions()
    )
    
    if args.port:
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route
        import uvicorn
            
        # 使用SSE服务器
        print(f"启动SSE服务器，端口号：{args.port}", file=sys.stderr)
        
        # 创建SSE传输
        transport = SseServerTransport("/messages/")
        
        # 定义SSE连接处理函数
        async def handle_sse(request):
            async with transport.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], initialization_options
                )
        
        # 创建Starlette应用
        sse_app = Starlette(routes=[
            Route("/sse/", endpoint=handle_sse),
            Mount("/messages/", app=transport.handle_post_message),
        ])
        
        # 使用异步方式启动服务器
        server = uvicorn.Server(uvicorn.Config(
            app=sse_app,
            host="0.0.0.0",
            port=args.port,
            log_level="warning"
        ))
        await server.serve()
    else:
        import mcp.server.stdio as stdio

        # 使用stdio服务器
        print("启动stdio服务器", file=sys.stderr)
        async with stdio.stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                initialization_options
            )

def cli_main():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("服务器被用户中断", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"服务器发生错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    cli_main()
