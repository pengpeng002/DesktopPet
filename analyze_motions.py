import json
import os
import glob

def analyze_model_files():
    """
    Analyzes a Live2D model's .model3.json file to find motion-to-sound mappings
    and checks for missing sound files.
    """
    # 1. Get model directory from user
    while True:
        model_dir = input("请输入要分析的模型文件夹名 (例如 lafei_4, lafeiII_3): ").strip()
        if not model_dir:
            print("输入不能为空，请重试。")
            continue
        if not os.path.isdir(model_dir):
            print(f"错误：找不到名为 '{model_dir}' 的文件夹，请确保文件夹在当前目录下。")
        else:
            break

    # 2. Find and parse the .model3.json file
    json_path_list = glob.glob(os.path.join(model_dir, '*.model3.json'))
    if not json_path_list:
        print(f"错误：在 '{model_dir}' 文件夹中没有找到 .model3.json 文件。")
        return

    json_path = json_path_list[0]
    print(f"\n正在分析: {json_path}\n")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            model_data = json.load(f)
    except Exception as e:
        print(f"错误：读取或解析JSON文件失败: {e}")
        return

    # 3. Extract motion-to-sound mappings
    motions_map = model_data.get('FileReferences', {}).get('Motions')
    if not motions_map:
        print("在此模型文件中没有找到 'Motions' 定义。")
        return

    report = []
    missing_sounds = []
    voice_map = {}
    
    print("-" * 50)
    print(f"{ '动作组':<20} | { '动作文件':<35} | { '语音文件':<35} | { '状态'}")
    print("-" * 50)

    # 4. Iterate through all motion groups and definitions
    for group_name, motion_defs in motions_map.items():
        if not motion_defs:
            continue
        
        for i, motion_def in enumerate(motion_defs):
            motion_file = motion_def.get('File', 'N/A')
            sound_file_path = motion_def.get('Sound')
            
            status = ""
            sound_file_display = "无"
            
            if sound_file_path:
                sound_file_display = sound_file_path
                # Normalize path for checking existence
                full_sound_path = os.path.join(model_dir, sound_file_path)
                
                if os.path.exists(full_sound_path):
                    status = "✅ 正常"
                else:
                    status = "❌ 语音文件缺失"
                    missing_sounds.append(sound_file_path)
                
                # Add to voice_map for potential JSON generation
                # If a group has multiple motions, we'll name them group_name_0, group_name_1, etc.
                key_name = f"{group_name}_{i}" if len(motion_defs) > 1 else group_name
                voice_map[key_name] = os.path.basename(sound_file_path)

            report.append({
                "group": group_name,
                "motion": motion_file,
                "sound": sound_file_display,
                "status": status
            })
            print(f"{group_name:<20} | {motion_file:<35} | {sound_file_display:<35} | {status}")

    print("-" * 50)
    
    if not report:
        print("\n分析完成，但没有找到任何有效的动作定义。")
        return

    if missing_sounds:
        print("\n⚠️ 发现以下语音文件缺失:")
        for sound in missing_sounds:
            print(f"  - {sound}")
    else:
        print("\n✅ 所有在 .model3.json 中定义的语音文件都存在。")
        
    # 5. Offer to generate character_data.json
    print("\n")
    while True:
        choice = input("是否要根据以上分析结果，为此模型生成或更新 'character_data.json' 文件? (y/n): ").lower()
        if choice in ['y', 'n']:
            break

    if choice == 'y':
        output_path = os.path.join(model_dir, 'character_data.json')
        
        # Prepare voiceTextMap, preserving existing texts if possible
        voice_text_map = {}
        if os.path.exists(output_path):
            try:
                with open(output_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    voice_text_map = existing_data.get('voiceTextMap', {})
            except Exception as e:
                print(f"读取现有 character_data.json 失败，将创建新的文本映射: {e}")

        for sound_filename in voice_map.values():
            if sound_filename not in voice_text_map:
                voice_text_map[sound_filename] = "" # Add placeholder for new sounds
                
        output_data = {
            "voiceMap": voice_map,
            "voiceTextMap": voice_text_map
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=4)
            print(f"\n成功写入文件: {output_path}")
        except Exception as e:
            print(f"\n错误：写入文件 {output_path} 失败: {e}")

if __name__ == '__main__':
    analyze_model_files()
