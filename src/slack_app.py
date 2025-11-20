import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

# chatbot_engine からのインポートはそのままで、
# 必要に応じてこのファイルを更新するか、またはこのインポートが正しいことを確認します。
from chatbot_engine import chat, create_index
from langchain.memory import ChatMessageHistory
# langchain-community への更新が必要な場合、以下のように変更します。
# この例では、langchain.memory の具体的な更新方法は示されていませんが、
# 必要に応じて langchain-community から適切なモジュールをインポートします。
# from langchain_community.memory import ChatMessageHistory



load_dotenv()

index=create_index()
# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

def fetch_history(channel:str)->ChatMessageHistory:
    bot_user_id=app.client.auth_test()["user_id"]
    conversation_history=app.client.conversation_history(channel=channel,limit=3)
    
    history=ChatMessageHistory()
    
    for message in reversed(conversation_history["message"]):
        text=message["text"]
        
        if message["user"]==bot_user_id:
            history.add_ai_message(text)
        else:
            history.add_user_message(text)
    return history    

@app.event("app_mention")
def handle_mention(event,say):
    channel=event["channel"]
    history=fetch_history(channel)
    
    message=event["text"]
    bot_message=chat(message,history,index)
    say(bot_message)
# アプリを起動します
if __name__ == "__main__":
    app_env=os.environ.get("APP_ENV","production")
    
  