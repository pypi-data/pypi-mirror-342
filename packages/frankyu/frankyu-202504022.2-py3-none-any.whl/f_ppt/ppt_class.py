import win32com.client
import datetime
import os
import pythoncom
from typing import Optional

class PPTCreator:
    def __init__(
        self, 
        output_dir: str = "T:\\ppt", 
        visible: bool = True
    ):
        """初始化PPT创建器
        
        Args:
            output_dir: PPT保存目录 
            visible: 是否前台显示PowerPoint
        """
        self.output_dir = output_dir
        self.visible = visible
        self.ppt_app = None
        self.presentation = None

    def initialize_ppt(self) -> None:
        """初始化PowerPoint应用"""
        pythoncom.CoInitialize()
        self.ppt_app = win32com.client.Dispatch(
            "PowerPoint.Application"
        )
        self.ppt_app.Visible = self.visible
        self.ppt_app.DisplayAlerts = False

    def create_new_presentation(self) -> None:
        """创建新的演示文稿"""
        self.presentation = (
            self.ppt_app.Presentations.Add()
        )

    def add_slide_with_content(
        self, 
        title: str, 
        content: str, 
        layout: int = 5
    ) -> None:
        """添加带内容的幻灯片
        
        Args:
            title: 幻灯片标题
            content: 幻灯片内容
            layout: 幻灯片版式 
                (默认5=标题+内容)
        """
        slide = self.presentation.Slides.Add(1, layout)
        slide.Shapes.Title.TextFrame.TextRange.Text = title
        
        if slide.Shapes.Count >= 2:
            content_shape = slide.Shapes(2)
            content_shape.TextFrame.TextRange.Text = (
                content
            )

    def setup_page_numbers(self) -> None:
        """设置幻灯片页码"""
        slide_master = (
            self.presentation.SlideMaster
        )
        headers_footers = (
            slide_master.HeadersFooters
        )
        headers_footers.Footer.Visible = True
        headers_footers.SlideNumber.Visible = True
        
        for slide in self.presentation.Slides:
            slide.DisplayMasterShapes = True

    def save_presentation(
        self, 
        filename: Optional[str] = None, 
        timestamp_format: str = "%Y%m%d_%H%M%S"
    ) -> str:
        """保存演示文稿
        
        Args:
            filename: 自定义文件名 
                (None则自动生成)
            timestamp_format: 时间戳格式
            
        Returns:
            保存的文件完整路径
        """
        os.makedirs(
            self.output_dir, 
            exist_ok=True
        )
        
        if filename is None:
            timestamp = (
                datetime.datetime.now()
                .strftime(timestamp_format)
            )
            filename = (
                f"PPT_{timestamp}.pptx"
            )
        
        save_path = os.path.join(
            self.output_dir, 
            filename
        )
        self.presentation.SaveAs(save_path)
        return save_path

    def close(self) -> None:
        """清理资源"""
        if self.presentation:
            self.presentation.Close()
        if self.ppt_app:
            try:
                self.ppt_app.Quit()
            except:
                pass
        pythoncom.CoUninitialize()

    def __enter__(self):
        """支持with语句"""
        self.initialize_ppt()
        self.create_new_presentation()
        return self

    def __exit__(
        self, 
        exc_type, 
        exc_val, 
        exc_tb
    ):
        """退出with语句时自动清理"""
        self.close()


def create_sample_ppt():
    """创建示例PPT的完整流程"""
    with PPTCreator(
        output_dir="T:\\ppt", 
        visible=True
    ) as creator:
        # 添加幻灯片内容
        creator.add_slide_with_content(
            title="12345",
            content="45678"
        )
        
        # 设置页码
        creator.setup_page_numbers()
        
        # 保存并打印路径
        saved_path = (
            creator.save_presentation()
        )
        print(
            f"PPT已保存至: {saved_path}"
        )


if __name__ == "__main__":
    create_sample_ppt()