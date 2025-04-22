import click
from ai_command_master import core

@click.group(context_settings={
    "ignore_unknown_options": True,
    "allow_extra_args": True,
    "help_option_names": ['-h', '--help'],
    "terminal_width": 120
})
def cli():
    """
    ai-command-master: 通过自然语言生成并执行终端命令
    """
    pass

@cli.command(name="ask")
@click.argument('description', nargs=-1, required=True)
def ask_command(description):
    """
    根据自然语言描述生成并执行命令
    """
    description_str = ' '.join(description)
    core.start_request(description_str)

@cli.group(name="config")
def config_group():
    """配置管理功能"""
    pass

@config_group.command(name="show")
def show_config():
    """显示当前配置"""
    core.show_config()

@config_group.command(name="list")
def list_config():
    """列出全部配置"""
    core.list_all_profiles()

@config_group.command(name="switch")
@click.argument('profile_name')
def switch_config(profile_name):
    """切换指定配置"""
    core.switch_config(profile_name)

@config_group.command(name="create")
@click.argument('profile_name')
def create_config(profile_name):
    """新建配置文件"""
    core.create_profile(profile_name)

@cli.result_callback()
def handle_default_command(result, **kwargs):
    ctx = click.get_current_context()
    if not ctx.invoked_subcommand and ctx.protected_args:
        description = ' '.join(ctx.protected_args)
        if ctx.args:
            description += ' ' + ' '.join(ctx.args)
        core.start_request(description)
        ctx.exit()