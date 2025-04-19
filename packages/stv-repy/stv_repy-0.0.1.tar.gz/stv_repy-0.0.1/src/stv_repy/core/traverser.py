import sys
import os


def traverse_dirs(current_dir, pattern_layers, layer_idx, args, matches):
    if layer_idx >= len(pattern_layers):
        return

    current_layer = pattern_layers[layer_idx]
    is_last = layer_idx == len(pattern_layers) - 1

    try:
        entries = os.listdir(current_dir)
    except (PermissionError, FileNotFoundError):
        return

    matched = []
    for entry in entries:
        entry_path = os.path.join(current_dir, entry)
        entry_name = os.path.basename(entry_path)

        if not current_layer.match(entry_name):
            continue

        if is_last:
            if os.path.isfile(entry_path):
                matches.append(os.path.normpath(entry_path))
        else:
            if os.path.isdir(entry_path):
                matched.append(entry_path)

    if not is_last:
        if len(matched) > 1 and not args.rp_allow_multiple:
            print(f"错误：目录 '{current_dir}' 匹配到多个子目录：{matched}")
            print("提示：使用 --rp-allow-multiple 允许继续匹配")
            sys.exit(1)
        for dir_path in matched:
            traverse_dirs(dir_path, pattern_layers, layer_idx + 1, args, matches)