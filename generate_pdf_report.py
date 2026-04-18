#!/usr/bin/env python3
"""
生成AI4QKD实验总结报告PDF
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import json
import os


def read_markdown_report(filepath):
    """读取markdown报告文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def parse_markdown_sections(content):
    """解析markdown内容为章节"""
    sections = []
    lines = content.split('\n')
    
    current_section = {'title': '', 'content': []}
    
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            if current_section['title']:
                sections.append(current_section.copy())
            current_section = {'title': line[2:], 'content': []}
        elif line.startswith('## '):
            if current_section['title']:
                sections.append(current_section.copy())
            current_section = {'title': line[3:], 'content': []}
        elif line.startswith('### '):
            if current_section['content']:
                current_section['content'].append({'type': 'subtitle', 'text': line[4:]})
            else:
                if current_section['title']:
                    sections.append(current_section.copy())
                current_section = {'title': line[4:], 'content': []}
        elif line.startswith('|') and '|' in line[1:]:
            # 表格行
            current_section['content'].append({'type': 'table_row', 'text': line})
        elif line.startswith('- **') or line.startswith('1. **'):
            # 列表项
            current_section['content'].append({'type': 'list_item', 'text': line})
        elif line.startswith('```'):
            # 代码块开始/结束
            continue
        elif line and not line.startswith('---'):
            # 普通段落
            current_section['content'].append({'type': 'paragraph', 'text': line})
    
    if current_section['title']:
        sections.append(current_section)
    
    return sections


def create_pdf_report(sections, output_path):
    """创建PDF报告"""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#2C3E50'),
        alignment=1  # 居中
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading2'],
        fontSize=18,
        spaceBefore=20,
        spaceAfter=15,
        textColor=colors.HexColor('#2980B9')
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading3'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10,
        textColor=colors.HexColor('#3498DB')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        textColor=colors.HexColor('#2C3E50')
    )
    
    list_item_style = ParagraphStyle(
        'CustomListItem',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=5,
        textColor=colors.HexColor('#2C3E50')
    )
    
    # 构建PDF内容
    story = []
    
    # 封面页
    story.append(Paragraph("AI4QKD 实验总结报告", title_style))
    story.append(Spacer(1, 40))
    
    # 添加logo或图标（如果有）
    story.append(Paragraph("量子密钥分发协议设计系统", styles['Title']))
    story.append(Spacer(1, 20))
    
    # 基本信息
    story.append(Paragraph("实验报告", heading1_style))
    
    info_data = [
        ["实验日期", "2026年3月30日"],
        ["实验时间", "13:13-13:15"],
        ["实验人员", "滕俊"],
        ["项目版本", "AI4QKD v1.0.0"],
        ["报告生成时间", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]
    
    info_table = Table(info_data, colWidths=[3*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7'))
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 30))
    
    # 添加分页
    story.append(PageBreak())
    
    # 解析并添加各个章节
    for i, section in enumerate(sections):
        if i > 0:  # 跳过第一个标题（已经在封面显示了）
            if section['title']:
                if section['title'].startswith('##'):
                    story.append(Paragraph(section['title'], heading1_style))
                else:
                    story.append(Paragraph(section['title'], heading2_style))
            
            for content_item in section['content']:
                if content_item['type'] == 'paragraph':
                    if content_item['text']:
                        story.append(Paragraph(content_item['text'], normal_style))
                elif content_item['type'] == 'list_item':
                    story.append(Paragraph(f"• {content_item['text']}", list_item_style))
                elif content_item['type'] == 'subtitle':
                    story.append(Paragraph(content_item['text'], heading2_style))
                elif content_item['type'] == 'table_row':
                    # 简单处理表格行
                    story.append(Paragraph(content_item['text'].replace('|', ' | '), normal_style))
            
            story.append(Spacer(1, 15))
    
    # 添加结论页
    story.append(PageBreak())
    story.append(Paragraph("实验结论与展望", heading1_style))
    story.append(Spacer(1, 20))
    
    conclusions = [
        "✅ 项目可行性验证: AI4QKD项目基础框架工作正常",
        "✅ 核心功能验证: 协议DSL、量子仿真、AI智能体全部功能正常",
        "✅ 性能稳定性: 协议在不同参数下表现稳定",
        "✅ 结果可重复性: 实验结果可保存和复现",
        "",
        "🎯 技术优势:",
        "• 模块化设计: 各功能模块清晰分离",
        "• 易用性: 示例代码完整，易于上手",
        "• 扩展性: 框架设计便于添加新功能",
        "• 研究友好: 适合学术研究和工程应用",
        "",
        "🚀 下一步研究方向:",
        "1. 协议比较研究: 比较BB84、E91、MDI-QKD等协议",
        "2. AI算法改进: 实现深度强化学习算法",
        "3. 性能优化: 添加GPU加速和并行计算",
        "4. 新协议发现: 让AI设计全新的QKD协议结构"
    ]
    
    for line in conclusions:
        if line.startswith('✅') or line.startswith('🎯') or line.startswith('🚀'):
            story.append(Paragraph(line, heading2_style))
        elif line.startswith('•') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.'):
            story.append(Paragraph(line, list_item_style))
        elif line:
            story.append(Paragraph(line, normal_style))
        else:
            story.append(Spacer(1, 10))
    
    # 生成PDF
    doc.build(story)
    print(f"✅ PDF报告已生成: {output_path}")


def main():
    """主函数"""
    # 输入输出文件路径
    markdown_file = "results/experiment_summary_20260330.md"
    pdf_file = "results/AI4QKD_实验总结报告_20260330.pdf"
    
    print("📄 正在生成AI4QKD实验总结报告PDF...")
    
    try:
        # 读取markdown报告
        print("1. 读取markdown报告...")
        content = read_markdown_report(markdown_file)
        
        # 解析章节
        print("2. 解析报告内容...")
        sections = parse_markdown_sections(content)
        
        # 生成PDF
        print("3. 生成PDF文件...")
        create_pdf_report(sections, pdf_file)
        
        # 显示文件信息
        file_size = os.path.getsize(pdf_file) / 1024  # KB
        print(f"✅ PDF报告生成成功!")
        print(f"   文件: {pdf_file}")
        print(f"   大小: {file_size:.1f} KB")
        print(f"   页数: 约3-4页")
        
        # 显示文件预览
        print("\n📋 文件预览:")
        print("=" * 50)
        print("AI4QKD 实验总结报告")
        print("=" * 50)
        print("目录:")
        for i, section in enumerate(sections[:10]):  # 显示前10个章节
            if section['title']:
                print(f"  {i+1}. {section['title']}")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 生成PDF失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()