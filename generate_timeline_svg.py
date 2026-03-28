import json
import os

# --- 配置 ---
DATA_FILE = "daily_data.json"
OUTPUT_SVG = "daily_timeline.svg"

# --- SVG 基础模板和全局样式 ---
SVG_HEADER = """
<svg width="840" height="660" viewBox="0 0 840 660" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.5" y="0.5" width="839" height="659" rx="12" fill="white" stroke="#e1e4e8"/>
  
  <g transform="translate(40, 40)">
    <path d="M11 2a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v28a1 1 0 0 1-1 1H12a1 1 0 0 1-1-1V2Z" fill="#F0F1F1" stroke="#ABB3BD" stroke-width="1.5"/>
    <path d="M11 8.5h18" stroke="#ABB3BD" stroke-width="1.5"/>
    <text x="20" y="23" text-anchor="middle" fill="#8b949e" font-family="Arial, system-ui" font-size="14" font-weight="600">17</text>
    
    <text x="45" y="24" fill="#000000" font-family="Arial, system-ui" font-size="28" font-weight="bold">每日记录</text>
    <text x="1" y="60" fill="#586069" font-family="Menlo, monospace" font-size="16">My Daily Log · 持续更新中</text>
  </g>
  
  <line x1="60.5" y1="180" x2="60.5" y2="600" stroke="#e1e4e8" stroke-width="2"/>
"""

SVG_FOOTER = "</svg>"

def create_entry_svg(entry, y_pos):
    """生成单个时间轴条目的 SVG 代码"""
    color = entry.get("color", "#8b949e")
    date_text = entry["date"]
    if entry.get("is_today"):
        date_text += " · 今天"
    
    # 颜色变量
    dot_color = color
    date_color = "#9b8bf1" if entry.get("is_today") else "#8b949e"
    title_color = "#000000"
    desc_color = "#586069"
    tag_bg_color = "#f6f8fa"
    tag_border_color = "#eaecef"

    svg_entry = f"""
  <g transform="translate(0, {y_pos})">
    <circle cx="60.5" cy="18" r="6" fill="{dot_color}"/>
    
    <g transform="translate(80, 0)">
      <text x="0" y="20" fill="{date_color}" font-family="Arial, system-ui" font-size="18" font-weight="500">{date_text}</text>
      
      <text x="0" y="55" fill="{title_color}" font-family="Arial, system-ui" font-size="20" font-weight="bold">{entry["title"]}</text>
      
      <foreignObject x="0" y="70" width="700" height="100">
        <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, system-ui; font-size: 16px; color: {desc_color}; line-height: 1.6; word-wrap: break-word;">
          {entry["description"]}
        </div>
      </foreignObject>
"""

    # 渲染标签
    if entry.get("tags"):
        tag_x = 0
        tag_y = 120 # 根据描述文本的预估高度
        svg_entry += f'<g transform="translate({tag_x}, {tag_y})">'
        
        current_x = 0
        for tag in entry["tags"]:
            # 预估标签宽度
            tag_text_width = len(tag) * 10 
            tag_full_width = tag_text_width + 16 # 左右 padding
            
            svg_entry += f"""
        <rect x="{current_x}" y="0" width="{tag_full_width}" height="28" rx="6" fill="{tag_bg_color}" stroke="{tag_border_color}"/>
        <text x="{current_x + tag_full_width / 2}" y="19" text-anchor="middle" fill="{color}" font-family="Arial, system-ui" font-size="14" font-weight="500">{tag}</text>
"""
            current_x += tag_full_width + 10 # 标签间距
            
        svg_entry += '</g>' # tag group end

    svg_entry += """
    </g> </g> """
    return svg_entry

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 计算全局高度（根据条目数量和估计高度动态调整）
    # 这里我们固定死 840x660，如果条目太多需要增加这个高度。
    
    full_svg = SVG_HEADER
    
    current_y = 170
    ENTRY_HEIGHT = 160 # 标签组存在时的预估高度

    # 只取最近3条，防止图片太长
    for entry in data[:3]:
        full_svg += create_entry_svg(entry, current_y)
        current_y += ENTRY_HEIGHT
        
    full_svg += SVG_FOOTER

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(full_svg)
    print(f"SVG generated successfully: {OUTPUT_SVG}")

if __name__ == "__main__":
    main()
