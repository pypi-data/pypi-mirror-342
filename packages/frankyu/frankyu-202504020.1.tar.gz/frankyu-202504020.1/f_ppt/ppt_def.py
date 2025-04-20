# 导入系统模块
import win32com.client  # 用于操作PowerPoint的COM接口
import datetime        # 用于生成时间戳
import os              # 用于路径操作
import pythoncom       # 用于COM初始化
from typing import Optional  # 类型提示支持


def init_ppt_app(visible: bool = True) -> object:
    """初始化PowerPoint应用实例"""
    
    # 初始化COM组件
    # 必须最先调用，否则无法使用COM接口
    pythoncom.CoInitialize()
    
    # 创建PowerPoint应用对象
    # 使用Dispatch连接已安装的PowerPoint
    ppt_app = win32com.client.Dispatch(
        "PowerPoint.Application"
    )
    
    # 控制程序可见性
    # True=显示界面，False=后台运行
    ppt_app.Visible = visible
    
    # 关闭所有警告弹窗
    # 避免保存等操作时弹出确认对话框
    ppt_app.DisplayAlerts = False
    
    return ppt_app


def create_presentation(ppt_app: object) -> object:
    """创建空白演示文稿"""
    
    # 新建演示文稿对象
    # 相当于点击PowerPoint的"新建"按钮
    presentation = ppt_app.Presentations.Add()
    
    return presentation


def add_slide(
    presentation: object,
    title: str,
    content: str,
    layout: int = 5
) -> None:
    """添加内容幻灯片"""
    
    # 添加新幻灯片
    # 参数1=插入位置，参数2=版式类型
    slide = presentation.Slides.Add(1, layout)
    
    # 设置标题文字
    # 通过Shapes集合访问标题框
    slide.Shapes.Title.TextFrame.TextRange.Text = title
    
    # 检查是否存在内容占位符
    # 索引1是标题，索引2开始是内容
    if slide.Shapes.Count >= 2:
        
        # 获取内容占位符对象
        # 通常是幻灯片上的文本框
        content_shape = slide.Shapes(2)
        
        # 设置内容文字
        content_shape.TextFrame.TextRange.Text = content


def enable_page_numbers(presentation: object) -> None:
    """启用幻灯片页码"""
    
    # 获取幻灯片母版对象
    # 控制所有幻灯片的统一样式
    slide_master = presentation.SlideMaster
    
    # 获取页眉页脚设置对象
    # 包含页码、日期等设置
    headers_footers = slide_master.HeadersFooters
    
    # 显示底部页脚区域
    # 但不一定显示文字内容
    headers_footers.Footer.Visible = True
    
    # 显示幻灯片编号
    # 通常在右下角显示数字
    headers_footers.SlideNumber.Visible = True
    
    # 应用到所有现有幻灯片
    for slide in presentation.Slides:
        
        # 强制显示母版元素
        # 确保页码可见
        slide.DisplayMasterShapes = True


def save_ppt(
    presentation: object,
    output_dir: str,
    filename: Optional[str] = None,
    timestamp_format: str = "%Y%m%d_%H%M%S"
) -> str:
    """保存演示文稿文件"""
    
    # 创建输出目录（如果不存在）
    # exist_ok=True避免目录已存在时报错
    os.makedirs(output_dir, exist_ok=True)
    
    # 自动生成文件名逻辑
    if not filename:
        
        # 获取当前系统时间
        # 格式化为指定字符串格式
        timestamp = datetime.datetime.now().strftime(
            timestamp_format
        )
        
        # 组合标准文件名
        # 示例：PPT_20230822_143022.pptx
        filename = f"PPT_{timestamp}.pptx"
    
    # 拼接完整文件路径
    # 使用os.path保证跨平台兼容性
    save_path = os.path.join(output_dir, filename)
    
    # 执行保存操作
    # 会覆盖同名文件（因DisplayAlerts=False）
    presentation.SaveAs(save_path)
    
    return save_path


def close_ppt(
    ppt_app: object,
    presentation: object
) -> None:
    """安全关闭PPT资源"""
    
    # 关闭演示文稿文档
    # 相当于点击"关闭"按钮
    if presentation:
        presentation.Close()
    
    # 退出PowerPoint程序
    # 释放内存资源
    if ppt_app:
        try:
            ppt_app.Quit()
        except:
            pass
    
    # 必须调用的COM清理
    # 与CoInitialize()配对使用
    pythoncom.CoUninitialize()


def create_sample_ppt():
    """完整的PPT创建示例"""
    
    # 声明变量（带类型注释）
    ppt_app = None      # type: Optional[object]
    presentation = None # type: Optional[object]
    
    try:
        # === 初始化阶段 ===
        # 创建PowerPoint进程
        ppt_app = init_ppt_app(visible=True)
        
        # 新建空白文档
        presentation = create_presentation(ppt_app)
        
        # === 内容编辑 ===
        # 添加首页幻灯片
        add_slide(
            presentation,
            title="项目汇报",  # 主标题文字
            content="2023年度总结",  # 内容文字
            layout=5  # 标准标题+内容版式
        )
        
        # 启用页码功能
        enable_page_numbers(presentation)
        
        # === 输出结果 ===
        # 保存到指定目录
        saved_path = save_ppt(
            presentation,
            output_dir="T:\\ppt",  # 保存路径
            filename=None  # 自动生成文件名
        )
        
        # 打印保存结果
        print(f"文件已保存到：{saved_path}")
    
    finally:
        # === 资源清理 ===
        # 确保无论如何都会执行清理
        if ppt_app or presentation:
            close_ppt(ppt_app, presentation)


# 程序入口
if __name__ == "__main__":
    
    # 执行示例创建流程
    create_sample_ppt()