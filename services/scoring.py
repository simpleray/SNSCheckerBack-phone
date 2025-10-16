
# 直接的スコア計算
def direct_scores(nlp_result):
    weights = {
        "phone": 35,
        "email": 30,
        "person": 15,
        "postal": 40,
        "date": 10,
        "age": 5
    }
    target_labels = ["phone", "email", "person", "postal", "date", "age"]
    total_raw_score = 0
    
    # --- デバッグ用PRINT ---
    print("--- direct_scores デバッグ開始 ---")
    print(f"入力データ: {nlp_result}")
    
    for label in target_labels:
        result_value = nlp_result.get(label)
        
        if result_value and isinstance(result_value, list) and len(result_value) >= 2:
            count = result_value[1]
        else:
            count = 0
            
        weight = weights.get(label, 0)
        total_raw_score += count * weight
        
        # --- デバッグ用PRINT ---
        print(f"ラベル: '{label}', 個数: {count}, 重み: {weight}, 現在の合計スコア: {total_raw_score}")

    final_score = min(total_raw_score, 100)
    
    # --- デバッグ用PRINT ---
    print(f"最終的な生スコア: {total_raw_score}")
    print(f"最終スコア (上限100): {final_score}")
    print("--- direct_scores デバッグ終了 ---\n")
    
    return final_score

# 間接的スコア計算
def indirect_scores(nlp_result):
    base_weight = 10
    exponent = 1.5
    target_labels = ["station", "hospital", "tourristspot", "place", "date"]
    
    total_indirect_count = 0
    
    # --- デバッグ用PRINT ---
    print("--- indirect_scores デバッグ開始 ---")
    print(f"入力データ: {nlp_result}")
    
    for label in target_labels:
        result_value = nlp_result.get(label)
        
        if result_value and isinstance(result_value, list) and len(result_value) >= 2:
            count = result_value[1]
        else:
            count = 0
            
        total_indirect_count += count
        
        # --- デバッグ用PRINT ---
        print(f"ラベル: '{label}', 個数: {count}, 現在の合計個数: {total_indirect_count}")

    # --- デバッグ用PRINT ---
    print(f"最終的な合計個数: {total_indirect_count}")

    if total_indirect_count == 0:
        print("--- indirect_scores デバッグ終了 ---\n")
        return 0
    
    raw_score = base_weight * (total_indirect_count ** exponent)
    final_score = min(raw_score, 100) # スコアの上限を100に設定

    # --- デバッグ用PRINT ---
    print(f"最終的な生スコア: {raw_score}")
    print(f"最終スコア (上限100): {final_score}")
    print("--- indirect_scores デバッグ終了 ---\n")
    
    return int(final_score)