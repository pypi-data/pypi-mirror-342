"""执行处理模块
该模块负责安全地处理和展示AI模型的响应结果，主要功能包括：
- 根据响应类型选择不同的执行策略
- 处理命令类型响应（复制到剪贴板）
- 处理文本类型响应（格式化显示）
- 展示警告和提示信息
"""
import click
import pyperclip


class Execution:
    """执行处理类
    
    根据AI响应的类型（Command/Text）选择相应的处理策略，
    确保输出格式统一且用户友好。
    
    Attributes:
        model (str): AI模型标识符
        response_dict (dict): AI响应的结构化数据
        execution_type (str): 执行类型（Command/Text）
    """
    def __init__(self, model: str, response_dict: dict):
        """初始化执行处理器
        
        Args:
            model (str): AI模型标识符
            response_dict (dict): 包含响应信息的字典，必须包含 'conversation_type' 键
        """
        self.model = model
        self.response_dict = response_dict
        self.execution_type = response_dict['conversation_type']

    def execute(self):
        """根据响应类型选择并执行相应的处理策略"""
        if self.execution_type == "Command":
            self.execute_command()
        elif self.execution_type == "Text":
            self.execute_text()

    def execute_command(self):
        """处理命令类型响应"""
        pyperclip.copy(self.response_dict['content'])
        click.echo(f"\n=== {self.model} ===")
        click.echo(f"Command: {self.response_dict['content']}")
        click.echo(f"Warning: {self.response_dict['warning']}")
        if self.response_dict['tip']:
            click.echo(f"Tip: {self.response_dict['tip']}")
        click.echo("\n[ 已复制到剪贴板 ✓ ]\n")

    def execute_text(self):
        """处理文本类型响应"""
        click.echo(f"\n=== {self.model} ===")
        click.echo(f"Content: {self.response_dict['content']}")
        click.echo(f"Warning: {self.response_dict['warning']}")
        if self.response_dict['tip']:
            click.echo(f"Tip: {self.response_dict['tip']}")
        click.echo()