# -*- coding: utf-8 -*-
import os
import logging
from functools import partial
from pluginbase import PluginBase

# 配置日志显示
logging.basicConfig(level=logging.DEBUG,
                    format="[%(asctime)s] %(filename)s[%(lineno)d]:"
                           "%(levelname)s: %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')
# 得到此文件所在文件夹，包装 get_path ，使容易获得插件位置
here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)


# 设置"example.modules"为插件库，并加载 builtin_plugins 文件夹的插件做为默认插件。
plugin_base = PluginBase(package='example.plugins',
                         searchpath=[get_path('./builtin_plugins')])


class Application(object):
    """一个简单的示例应用程序类."""

    def __init__(self, name):
        # 设置应用名称
        self.name = name

        # 添加“字符串格式化程序”字典。格式化字符串函数由插件提供。
        # key: 函数名 value: 格式化函数
        self.formatters = {}

        # 从 "app_name/plugins" 文件夹加载插件的源代码。
        # 我们还传递应用程序名称作为标识符。
        # 这是可选的，但通过这样做插件将具有一致的内部模块名称，并允许pickle工作。
        self.source = plugin_base.make_plugin_source(
            searchpath=[get_path('./%s/plugins' % name)],
            identifier=self.name)

        # 在这里我们列出了所有源代码知道的插件，加载它们并使用插件提供的“setup”函数来初始化插件。
        for plugin_name in self.source.list_plugins():
            logging.debug(name +' ' + plugin_name)
            plugin = self.source.load_plugin(plugin_name)
            plugin.setup(self)

    def register_formatter(self, name, formatter):
        """可用于为插件注册格式化程序功能。"""
        self.formatters[name] = formatter


def run_demo(app, source):
    """显示应用程序演示模式下的所有格式化程序。"""
    print('Formatters for %s:' % app.name)
    print('       input: %s' % source)
    for name, fmt in sorted(app.formatters.items()):
        print('  %10s: %s' % (name, fmt(source)))
    print('')


def main():
    # 这是一个格式化字符串的示例。
    source = 'This is a cool demo text to show this functionality.'

    # 设置两个应用程序。
    # 一个从./app1/plugins加载插件，另一个从./app2/plugins加载。
    # 两者都将加载默认的./builtin_plugins。
    app1 = Application('app1')
    app2 = Application('app2')

    # 运行这两个demo
    run_demo(app1, source)
    run_demo(app2, source)

    # 为了展示导入系统的工作原理，我们也将展示 导入插件
    # importing plugins regularly:
    with app1.source:
        from example.plugins import secret
        print('Plugin module: %s' % secret)


if __name__ == '__main__':
    main()
