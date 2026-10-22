# -*- coding: utf-8 -*-

# 小龙智脑 (XiaoLong Brain) - 全新原创项目

# 作者 / 版权人: 小龙 (XiaoLong)

# License: MIT。本项目所有代码均为原创，保留署名即可自由使用。



import inspect





class Tool:

    def __init__(self, name, func, description=""):

        self.name = name

        self.func = func

        self.description = description or (func.__doc__ or "").strip()



    def run(self, **kwargs):

        return self.func(**kwargs)



    def spec(self):

        return {"name": self.name, "description": self.description,

                "parameters": list(inspect.signature(self.func).parameters)}





class ToolRegistry:

    def __init__(self):

        self.tools = {}



    def register(self, tool):

        self.tools[tool.name] = tool

        return tool



    def register_fn(self, name, func, description=""):

        return self.register(Tool(name, func, description))



    def get(self, name):

        return self.tools.get(name)



    def list(self):

        return [t.spec() for t in self.tools.values()]



    def call(self, name, **kwargs):

        tool = self.tools.get(name)

        if not tool:

            raise KeyError("Unknown tool: %s" % name)

        return tool.run(**kwargs)





# 全局默认工具注册表

_default_registry = ToolRegistry()





def tool(name=None, description=""):

    # 装饰器：把函数注册为工具

    def deco(func):

        tname = name or func.__name__

        _default_registry.register(Tool(tname, func, description))

        return func

    return deco





def get_default_registry():

    return _default_registry

