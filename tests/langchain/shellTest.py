from langchain.callbacks import HumanApprovalCallbackHandler
from langchain.tools import ShellTool

tool = ShellTool(callbacks=[HumanApprovalCallbackHandler()])


print(tool.run(u"net user"))