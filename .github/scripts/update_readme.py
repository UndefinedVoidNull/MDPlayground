# .github/scripts/update_readme.py

import os
from datetime import datetime
from urllib.parse import quote
from collections import defaultdict

def main():
    # 定义 posts 目录
    posts_directory = 'posts'
    
    # 排除的文件
    excluded_files = {'README.md', '.github/scripts/update_readme.py'}
    
    # 使用 defaultdict 按修改日期分组文件
    files_by_date = defaultdict(list)
    
    # 遍历 posts 目录
    for root, _, filenames in os.walk(posts_directory):
        for filename in filenames:
            if filename.endswith(('.md', '.pdf')) and filename not in excluded_files:
                filepath = os.path.join(root, filename)
                
                # 获取相对于仓库根目录的路径
                relative_path = os.path.relpath(filepath, '.')  # 例如 'posts/My Post.md'
                relative_path = relative_path.replace('\\', '/')  # 兼容 Windows
                
                # 获取文件的最后修改时间
                timestamp = os.path.getmtime(filepath)
                modified_datetime = datetime.fromtimestamp(timestamp)
                modified_date_str = modified_datetime.strftime('%Y-%m-%d')
                
                # 对路径进行 URL 编码，处理空格和特殊字符
                encoded_path = quote(relative_path)
                
                # 提取文件名（不含扩展名）作为显示名称
                name = os.path.splitext(os.path.basename(filepath))[0]
                
                # 将文件信息添加到对应的日期组
                files_by_date[modified_date_str].append({
                    'name': name,
                    'path': encoded_path
                })
    
    # 按日期降序排序
    sorted_dates = sorted(files_by_date.keys(), reverse=True)
    
    # 生成 README.md 内容
    readme_content = "# Blog Posts\n\n"
    
    for date in sorted_dates:
        readme_content += f"## {date}\n\n"
        
        # 获取当前日期组的所有文件，并按名称字母顺序排序
        sorted_files = sorted(
            files_by_date[date],
            key=lambda x: x['name'].lower()  # 不区分大小写排序
        )
        
        for file in sorted_files:
            readme_content += f"- [{file['name']}]({file['path']})\n"
        
        readme_content += "\n"  # 每个日期组后添加一个空行
    
    # 将内容写入 README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
