def combined_function(question: str) -> str:
    # まず基本的な回答を生成します
    basic_answer = create_answer(question)
    
    # 次に、質問に関連する参考文献を検索し、質問と回答に追加します
    detailed_answer_with_references = add_sentense(question)
    
    # 最後に、基本的な回答と参考文献を含む詳細な回答を組み合わせます
    final_answer = f"{basic_answer}\n\n参考文献:\n{detailed_answer_with_references}"
    return final_answer

# テスト
question = "Pythonのリストとタプルの違いは？"
final_answer = combined_function(question)
print(final_answer)
