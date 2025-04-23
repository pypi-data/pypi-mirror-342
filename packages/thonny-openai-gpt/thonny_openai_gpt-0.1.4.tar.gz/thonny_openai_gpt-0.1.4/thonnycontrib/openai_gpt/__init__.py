"""
Thonny OpenAI GPT 助手插件 - 提供聊天面板和程式碼分析功能
"""

from thonny import get_workbench
from thonnycontrib.openai_gpt.gpt_tool import GPTChatView, gpt_assistant

def load_plugin():
    """載入插件，註冊命令和工具列按鈕"""
    print("Loading thonny-openai-gpt plugin...")  # 加入日誌輸出
    
    try:
        wb = get_workbench()
        
        # 註冊視圖
        wb.add_view(GPTChatView, "GPT聊天", "se")
        
        # 註冊命令 (同時加入選單和工具列)
        wb.add_command(
            command_id="gpt_assistant",
            menu_name="工具",
            command_label="GPT助手", # 稍微簡化標籤
            handler=gpt_assistant,
            include_in_toolbar=True,
            image="question",  # 使用內建圖示
            caption="GPT助手" # 工具列提示
        )
        
        print("thonny-openai-gpt plugin loaded successfully.") # 確認載入完成
    except Exception as e:
        print(f"Error loading thonny-openai-gpt plugin: {e}")
        import traceback
        traceback.print_exc()