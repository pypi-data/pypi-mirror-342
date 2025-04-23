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
            menu_name="tools", # 使用英文選單名稱，避免本地化問題
            command_label="GPT 助手",
            handler=gpt_assistant,
            include_in_toolbar=False, # 暫時不包含在工具列，避免問題
            caption="GPT 助手" 
        )
        
        print("thonny-openai-gpt plugin loaded successfully.") # 確認載入完成
    except Exception as e:
        print(f"Error loading thonny-openai-gpt plugin: {e}")
        import traceback
        traceback.print_exc()