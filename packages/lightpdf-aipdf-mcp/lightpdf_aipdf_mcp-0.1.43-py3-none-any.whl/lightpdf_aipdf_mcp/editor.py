"""PDF文档编辑模块"""
import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Any

import httpx

from .common import BaseResult, Logger, FileHandler, BaseApiClient
from .converter import InputFormat

class EditType(str, Enum):
    """支持的PDF编辑操作类型"""
    SPLIT = "split"          # 拆分PDF
    MERGE = "merge"          # 合并PDF
    ROTATE = "rotate"        # 旋转PDF
    COMPRESS = "compress"    # 压缩PDF
    ENCRYPT = "protect"      # 加密PDF
    DECRYPT = "unlock"       # 解密PDF
    ADD_WATERMARK = "watermark"  # 添加水印

@dataclass
class EditResult(BaseResult):
    """编辑结果数据类"""
    pass

class Editor(BaseApiClient):
    """PDF文档编辑器"""
    def __init__(self, logger: Logger, file_handler: FileHandler):
        super().__init__(logger, file_handler)
        self.api_base_url = "https://techsz.aoscdn.com/api/tasks/document/pdfedit"

    async def _validate_pdf_file(self, file_path: str) -> bool:
        """验证文件是否为PDF格式
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 如果是PDF文件则返回True，否则返回False
        """
        # 对于URL或OSS路径，跳过文件格式检查
        if self.file_handler.is_url(file_path) or self.file_handler.is_oss_id(file_path):
            return True
            
        input_format = self.file_handler.get_input_format(file_path)
        if input_format != InputFormat.PDF:
            await self.logger.error(f"此功能仅支持PDF文件，当前文件格式为: {self.file_handler.get_file_extension(file_path)}")
            return False
        return True
    
    async def _log_operation(self, operation: str, details: str = None):
        """记录操作日志
        
        Args:
            operation: 操作描述
            details: 详细信息（可选）
        """
        log_msg = f"正在{operation}"
        if details:
            log_msg += f"（{details}）"
        log_msg += "..."
        await self.logger.log("info", log_msg)
    
    async def split_pdf(self, file_path: str, pages: str = "", password: Optional[str] = None, split_type: str = "page", merge_all: int = 1) -> EditResult:
        """拆分PDF文件
        
        Args:
            file_path: 要拆分的PDF文件路径
            pages: 拆分页面规则，例如 "1,3,5-7" 表示提取第1,3,5,6,7页，""表示所有页面，默认为""
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            split_type: 拆分类型，可选值: "every"=每页拆分为一个文件, "page"=指定页面规则拆分，默认为"page"
            merge_all: 是否合并拆分后的文件，仅在split_type="page"时有效，0=不合并，1=合并，默认为1
            
        Returns:
            EditResult: 拆分结果
        """
        # 验证输入文件是否为PDF
        if not await self._validate_pdf_file(file_path):
            return EditResult(success=False, file_path=file_path, error_message="非PDF文件")
        
        # 验证拆分类型
        valid_split_types = {"every", "page"}
        if split_type not in valid_split_types:
            await self.logger.error(f"无效的拆分类型: {split_type}。有效值为: every, page")
            return EditResult(success=False, file_path=file_path, error_message=f"无效的拆分类型: {split_type}。有效值为: every, page")
        
        # 构建API参数
        extra_params = {
            "split_type": split_type
        }
        
        # 仅在page模式下设置pages和merge_all参数
        if split_type == "page":
            extra_params["pages"] = pages
            extra_params["merge_all"] = merge_all
            
        # 记录操作描述
        operation_details = f"类型: {split_type}"
        if split_type == "page":
            operation_details += f", 页面: {pages}"
        await self._log_operation("拆分PDF文件", operation_details)
        
        # 调用edit_pdf方法处理API请求
        return await self.edit_pdf(file_path, EditType.SPLIT, extra_params, password)

    async def merge_pdfs(self, file_paths: List[str], password: Optional[str] = None) -> EditResult:
        """合并多个PDF文件
        
        Args:
            file_paths: 要合并的PDF文件路径列表
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            
        Returns:
            EditResult: 合并结果
        """
        if len(file_paths) < 2:
            await self.logger.error("合并PDF至少需要两个文件")
            return EditResult(success=False, file_path=','.join(file_paths), error_message="合并PDF至少需要两个文件")
        
        # 验证所有文件是否都是PDF并且存在
        for pdf_file in file_paths:
            if not await self._validate_pdf_file(pdf_file):
                return EditResult(success=False, file_path=pdf_file, error_message="非PDF文件")
            
            exists = await self.file_handler.validate_file_exists(pdf_file)
            if not exists:
                return EditResult(success=False, file_path=pdf_file, error_message="文件不存在")
        
        # 记录操作描述
        await self._log_operation("合并PDF文件", f"{len(file_paths)} 个文件")
        
        # 合并PDF需要特殊处理，因为涉及多个文件
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                # 创建合并任务
                task_id = await self._create_merge_task(client, file_paths, password)
                
                # 等待任务完成
                download_url = await self._wait_for_task(client, task_id, "合并")
                
                # 记录完成信息
                await self.logger.log("info", "PDF合并完成。可通过下载链接获取结果文件。")
                
                return EditResult(
                    success=True,
                    file_path=file_paths[0],  # 使用第一个文件路径作为参考
                    error_message=None,
                    download_url=download_url
                )

            except Exception as e:
                return EditResult(
                    success=False,
                    file_path=file_paths[0],
                    error_message=str(e),
                    download_url=None
                )

    async def rotate_pdf(self, file_path: str, angle: int, pages: str = "", password: Optional[str] = None) -> EditResult:
        """旋转PDF文件的页面
        
        Args:
            file_path: 要旋转的PDF文件路径
            angle: 旋转角度，可选值为90、180、270
            pages: 指定要旋转的页面范围，例如 "1,3,5-7" 或 "" 表示所有页面
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            
        Returns:
            EditResult: 旋转结果
        """
        # 验证输入文件是否为PDF
        if not await self._validate_pdf_file(file_path):
            return EditResult(success=False, file_path=file_path, error_message="非PDF文件")
        
        # 验证旋转角度
        valid_angles = {90, 180, 270}
        if angle not in valid_angles:
            await self.logger.error("无效的旋转角度。角度必须是: 90, 180, 270")
            return EditResult(success=False, file_path=file_path, error_message="无效的旋转角度。角度必须是: 90, 180, 270")
        
        # 构建API参数
        extra_params = {
            "angle": json.dumps({str(angle): pages})
        }
        
        # 记录操作描述
        angle_desc = f"{angle}°" + (f": {pages}" if pages else ": 所有页面")
        await self._log_operation("旋转PDF文件", f"参数: {angle_desc}")
        
        # 调用edit_pdf方法处理API请求
        return await self.edit_pdf(file_path, EditType.ROTATE, extra_params, password)

    async def compress_pdf(self, file_path: str, image_quantity: int = 60, password: Optional[str] = None) -> EditResult:
        """压缩PDF文件
        
        Args:
            file_path: 要压缩的PDF文件路径
            image_quantity: 图片质量，范围1-100，默认为60
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            
        Returns:
            EditResult: 压缩结果
        """
        # 验证输入文件是否为PDF
        if not await self._validate_pdf_file(file_path):
            return EditResult(success=False, file_path=file_path, error_message="非PDF文件")
        
        # 验证图片质量
        if not 1 <= image_quantity <= 100:
            await self.logger.error(f"无效的图片质量: {image_quantity}。有效值范围为: 1-100")
            return EditResult(success=False, file_path=file_path, error_message=f"无效的图片质量: {image_quantity}。有效值范围为: 1-100")
        
        # 构建API参数
        extra_params = {
            "image_quantity": image_quantity
        }
        
        # 记录操作描述
        await self._log_operation("压缩PDF文件", f"图片质量: {image_quantity}")
        
        # 调用edit_pdf方法处理API请求
        return await self.edit_pdf(file_path, EditType.COMPRESS, extra_params, password)

    async def encrypt_pdf(self, file_path: str, password: str, original_password: Optional[str] = None) -> EditResult:
        """加密PDF文件
        
        Args:
            file_path: 要加密的PDF文件路径
            password: 设置的新密码（用于加密PDF）
            original_password: 文档原密码，如果文档已受密码保护，则需要提供（可选）
            
        注意:
            根据API文档，加密操作需要通过password参数指定要设置的新密码。
            如果文档已经受密码保护，则使用original_password参数提供原密码进行解锁。
            
        Returns:
            EditResult: 加密结果
        """
        # 验证输入文件是否为PDF
        if not await self._validate_pdf_file(file_path):
            return EditResult(success=False, file_path=file_path, error_message="非PDF文件")
        
        # 构建API参数
        extra_params = {
            "password": password  # 设置的新密码
        }
        
        # 记录操作描述
        await self._log_operation("加密PDF文件")
        
        # 调用edit_pdf方法处理API请求
        return await self.edit_pdf(file_path, EditType.ENCRYPT, extra_params, original_password)

    async def decrypt_pdf(self, file_path: str, password: Optional[str] = None) -> EditResult:
        """解密PDF文件
        
        Args:
            file_path: 要解密的PDF文件路径
            password: 文档密码，如果文档受密码保护，则需要提供（必须提供正确的密码才能解密）
            
        注意:
            该方法调用API的unlock功能，需要提供正确的PDF密码才能成功解密。
            
        Returns:
            EditResult: 解密结果
        """
        # 验证输入文件是否为PDF
        if not await self._validate_pdf_file(file_path):
            return EditResult(success=False, file_path=file_path, error_message="非PDF文件")
        
        # 记录操作描述
        await self._log_operation("解密PDF文件")
        
        # 调用edit_pdf方法处理API请求
        return await self.edit_pdf(file_path, EditType.DECRYPT, {}, password)

    async def add_watermark(
        self, 
        file_path: str, 
        text: str, 
        position: str,  # 必需参数：位置，如"top", "center", "diagonal"等
        opacity: float = 0.5, 
        deg: str = "-45",  # 直接使用字符串格式的角度
        range: str = "",  # 与API保持一致，使用range而非pages
        layout: Optional[str] = None,  # 可选参数: "on"/"under"
        font_family: Optional[str] = None,
        font_size: Optional[int] = None,
        font_color: Optional[str] = None,
        password: Optional[str] = None
    ) -> EditResult:
        """为PDF文件添加水印
        
        Args:
            file_path: 要添加水印的PDF文件路径
            text: 水印文本内容
            position: 水印位置，可选值:"topleft","top","topright","left","center",
                    "right","bottomleft","bottom","bottomright","diagonal","reverse-diagonal"
            opacity: 透明度，0.0-1.0，默认为0.5
            deg: 倾斜角度，字符串格式，如"-45"，默认为"-45"
            range: 指定页面范围，例如 "1,3,5-7" 或 "" 表示所有页面
            layout: 布局位置，可选值:"on"(在内容上)/"under"(在内容下)
            font_family: 字体
            font_size: 字体大小
            font_color: 字体颜色，如"#ff0000"表示红色
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            
        Returns:
            EditResult: 添加水印结果
        """
        # 验证输入文件是否为PDF
        if not await self._validate_pdf_file(file_path):
            return EditResult(success=False, file_path=file_path, error_message="非PDF文件")
        
        # 验证透明度
        if not 0.0 <= opacity <= 1.0:
            await self.logger.error(f"无效的透明度: {opacity}。有效值范围为: 0.0-1.0")
            return EditResult(success=False, file_path=file_path, error_message=f"无效的透明度: {opacity}。有效值范围为: 0.0-1.0")
        
        # 验证position参数
        valid_positions = {"topleft", "top", "topright", "left", "center", "right", 
                        "bottomleft", "bottom", "bottomright", "diagonal", "reverse-diagonal"}
        if position not in valid_positions:
            await self.logger.error(f"无效的位置: {position}")
            return EditResult(success=False, file_path=file_path, error_message=f"无效的位置: {position}")
        
        # 构建API参数
        extra_params = {
            "edit_type": "text",  # 固定为文本水印
            "text": text,
            "position": position,
            "opacity": opacity,
            "deg": deg,
            "range": range
        }
        
        # 添加可选参数
        if layout:
            extra_params["layout"] = layout
        if font_family:
            extra_params["font_family"] = font_family
        if font_size:
            extra_params["font_size"] = font_size
        if font_color:
            extra_params["font_color"] = font_color
        
        # 记录操作描述
        await self._log_operation("为PDF添加水印", f"文本: {text}, 位置: {position}, 透明度: {opacity}")
        
        # 调用edit_pdf方法处理API请求
        return await self.edit_pdf(file_path, EditType.ADD_WATERMARK, extra_params, password)

    async def edit_pdf(self, file_path: str, edit_type: EditType, extra_params: Dict[str, Any] = None, password: Optional[str] = None) -> EditResult:
        """编辑PDF文件
        
        Args:
            file_path: 要编辑的PDF文件路径
            edit_type: 编辑操作类型
            extra_params: 额外的API参数
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            
        注意:
            1. 对于加密操作(protect)，需要在extra_params中提供新密码
            2. 对于解密操作(unlock)，需要提供正确的password参数
            3. 所有extra_params中的参数将直接传递给API
            
        Returns:
            EditResult: 编辑结果
        """
        if not self.api_key:
            await self.logger.error("未找到API_KEY。请在客户端配置API_KEY环境变量。")
            return EditResult(success=False, file_path=file_path, error_message="未找到API_KEY。请在客户端配置API_KEY环境变量。")

        # 验证文件
        exists = await self.file_handler.validate_file_exists(file_path)
        if not exists:
            return EditResult(success=False, file_path=file_path, error_message="文件不存在")

        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                # 初始化extra_params（如果为None）
                if extra_params is None:
                    extra_params = {}
                
                # 如果提供了密码，将其添加到extra_params
                if password:
                    extra_params["password"] = password
                
                # 创建编辑任务
                task_id = await self._create_task(client, file_path, edit_type, extra_params)
                
                # 等待任务完成
                download_url = await self._wait_for_task(client, task_id, "编辑")
                
                # 记录完成信息
                await self.logger.log("info", "编辑完成。可通过下载链接获取结果文件。")
                
                return EditResult(
                    success=True,
                    file_path=file_path,
                    error_message=None,
                    download_url=download_url
                )

            except Exception as e:
                return EditResult(
                    success=False,
                    file_path=file_path,
                    error_message=str(e),
                    download_url=None
                )

    async def _create_task(self, client: httpx.AsyncClient, file_path: str, edit_type: EditType, extra_params: Dict[str, Any] = None) -> str:
        """创建编辑任务
        
        Args:
            client: HTTP客户端
            file_path: 文件路径
            edit_type: 编辑操作类型
            extra_params: 额外API参数(可选)
        
        Returns:
            str: 任务ID
        """
        await self.logger.log("info", "正在提交PDF编辑任务...")
        
        headers = {"X-API-KEY": self.api_key}
        data = {"type": edit_type.value}
        
        # 添加额外参数
        if extra_params:
            data.update(extra_params)
        
        # 检查是否为OSS路径
        if self.file_handler.is_oss_id(file_path):
            # 使用JSON方式时添加Content-Type
            headers["Content-Type"] = "application/json"
            # OSS路径处理方式，与URL类似，但提取resource_id
            data["resource_id"] = file_path.split("oss_id://")[1]
            response = await client.post(
                self.api_base_url,
                json=data,
                headers=headers
            )
        # 检查是否为URL路径
        elif self.file_handler.is_url(file_path):
            # 使用JSON方式时添加Content-Type
            headers["Content-Type"] = "application/json"
            data["url"] = file_path
            response = await client.post(
                self.api_base_url,
                json=data,
                headers=headers
            )
        else:
            # 对于文件上传，使用表单方式，不需要添加Content-Type
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = await client.post(
                    self.api_base_url,
                    files=files,
                    data=data,
                    headers=headers
                )
        
        # 使用基类的方法处理API响应
        return await self._handle_api_response(response, "创建任务")

    async def _create_merge_task(self, client: httpx.AsyncClient, file_paths: List[str], password: Optional[str] = None) -> str:
        """创建PDF合并任务
        
        Args:
            client: HTTP客户端
            file_paths: 要合并的PDF文件路径列表
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
        
        Returns:
            str: 任务ID
        """
        await self.logger.log("info", "正在提交PDF合并任务...")
        
        headers = {"X-API-KEY": self.api_key}
        data = {"type": EditType.MERGE.value}
        
        # 准备URL格式的输入
        url_inputs = []
        
        # 准备本地文件列表
        local_files = []
        files = {}
        
        for i, file_path in enumerate(file_paths):
            # 检查是否为URL或OSS路径
            if self.file_handler.is_oss_id(file_path):
                # 对于OSS路径，添加到inputs数组
                input_item = {"resource_id": file_path.split("oss_id://")[1]}
                if password:
                    input_item["password"] = password
                url_inputs.append(input_item)
            elif self.file_handler.is_url(file_path):
                # 对于URL或OSS路径，添加到inputs数组
                input_item = {"url": file_path}
                if password:
                    input_item["password"] = password
                url_inputs.append(input_item)
            else:
                # 记录本地文件，需要使用form方式
                local_files.append(file_path)
                
        # 如果全部是URL输入，使用JSON方式
        if url_inputs and not local_files:
            data["inputs"] = url_inputs
            # 使用JSON方式时添加Content-Type
            headers["Content-Type"] = "application/json"
            response = await client.post(
                self.api_base_url,
                json=data,
                headers=headers
            )
        else:
            # 如果有本地文件，使用form方式，不需要添加Content-Type
            # 准备文件
            for i, file_path in enumerate(local_files):
                files[f"file{i+1}"] = open(file_path, "rb")
                
            # 如果有URL输入，添加inputs参数
            if url_inputs:
                data["inputs"] = json.dumps(url_inputs)
            
            try:
                # 发送请求
                response = await client.post(
                    self.api_base_url,
                    data=data,
                    files=files,
                    headers=headers
                )
                
            finally:
                # 确保所有打开的文件都被关闭
                for file_obj in files.values():
                    file_obj.close()
            
        # 使用基类的方法处理API响应
        return await self._handle_api_response(response, "创建合并任务") 