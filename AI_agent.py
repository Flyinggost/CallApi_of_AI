from openai import OpenAI
import time
#hhh openai
client = OpenAI(
  base_url="https://api.tokenpony.cn/v1",#free token website
  api_key="your key",
)

# 初始化对话历史
conversation_history = [
    {
        "role": "system", 
        "content": "你是一个小说家,你最喜欢写小说"#sys prompt
    }
]

print("💬 连续对话模式已启动（输入'退出'或'exit'结束对话）")
print("=" * 50)

# 连续对话循环
while True:
    # 获取用户输入
    user_input = input("\n👤 你: ").strip()
    
    # 检查是否退出
    if user_input.lower() in ['退出', 'exit', 'quit']:
        print("👋 对话结束，再见！")
        break
    
    if not user_input:
        print("⚠️ 请输入有效内容")
        continue
    
    # 添加用户消息到对话历史
    conversation_history.append({"role": "user", "content": user_input})
    
    # 使用流式响应e
    try:
        response = client.chat.completions.create(
            model="qwen3-32b",
            messages=conversation_history,
            temperature=2,
            max_tokens=1024,
            stream=True  # 启用流式响应
        )
        
        # 初始化变量
        thinking_content = ""
        final_answer = ""
        in_thinking = False
        in_answer = False
        
        # 处理流式响应
        print("\n🤔 AI思考中:", end=" ")
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta:
                delta = chunk.choices[0].delta
                
                # 检测思考过程开始
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                    if not in_thinking:
                        in_thinking = True
                    thinking_content += delta.reasoning_content
                    print(delta.reasoning_content, end='', flush=True)
                
                # 检测最终答案开始
                elif hasattr(delta, 'content') and delta.content:
                    if not in_answer:
                        in_answer = True
                        # 如果之前有思考过程，换行显示答案
                        if in_thinking:
                            print("\n\n🤖 AI回答:", end=" ")
                        else:
                            print("🤖 AI回答:", end=" ")
                    final_answer += delta.content
                    print(delta.content, end='', flush=True)
        
        print("\n" + "-" * 50)
        
        # 将AI回复添加到对话历史（只添加最终答案）
        if final_answer:
            conversation_history.append({"role": "assistant", "content": final_answer})
        elif thinking_content and not final_answer:
            # 如果没有最终答案但有思考过程，将思考过程作为回答
            conversation_history.append({"role": "assistant", "content": thinking_content})
    
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("🔄 重新连接中...")
        time.sleep(1)