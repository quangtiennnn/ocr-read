import sys
import json
import os
import re
from bson import ObjectId
# from process_pdf import process_pdf
from mistral_ocr import *


def process_pdf(file_path):
    api_key = os.environ['MISTRAL_API_KEY']
    mistral_ocr = MistralOCR(api_key)

    uploaded_pdf = mistral_ocr.upload_pdf(file_path)
    signed_url = mistral_ocr.get_signed_url(uploaded_pdf.id)
    ocr_response = mistral_ocr.process_ocr(signed_url.url)

    response_dict = json.loads(ocr_response.json())
    # Merge Markdown text from all pages into a single string
    text = '\n'.join(page['markdown'] for page in response_dict['pages'])

    # Regular expressions for Chapters (Chương) and Articles (Điều)
    chapter_pattern = re.findall(r"(Chương\s+[IVXLCDM]+)\s*(.*?)(?=Chương\s+[IVXLCDM]+|$)", text, re.DOTALL)
    article_pattern = re.findall(r"#\s*Điều\s(\d+)\.\s(.*?)(?=#\s*Điều\s\d+\.|$)", text, re.DOTALL)

    # Function to parse article content into sections and subsections
    def parse_article_content(content):
        sections = []
        
        # Regular expressions for sections (e.g., "1.") and subsections (e.g., "a)")
        section_pattern = re.compile(r'^\d+\.\s', re.MULTILINE)
        subsection_pattern = re.compile(r'^[a-z]\)\s', re.MULTILINE)

        # Split content into sections
        section_splits = section_pattern.split(content.strip())
        section_headers = section_pattern.findall(content)

        if not section_headers:  # If no sections, treat entire content as a single section
            if content.strip():
                sections.append({"so_muc": 1, "noi_dung": content.strip(), "muc_con": []})
            return sections

        for i, section in enumerate(section_splits):
            if i == 0:  # Skip content before the first section
                continue
            
            section_header = section_headers[i - 1]  # e.g., "1. "
            section_content = section.strip()
            current_section = {
                "so_muc": int(section_header.split('.')[0]),
                "noi_dung": section_header + section_content.split('\n', 1)[0].strip(),
                "muc_con": []
            }

            # Split section content into subsections
            subsection_splits = subsection_pattern.split(section_content)
            subsection_headers = subsection_pattern.findall(section_content)

            if subsection_headers:
                for j, subsection in enumerate(subsection_splits):
                    if j == 0:  # Skip content before the first subsection
                        continue
                    subsection_header = subsection_headers[j - 1]  # e.g., "a) "
                    subsection_content = subsection.strip()
                    current_section["muc_con"].append({
                        "ky_hieu": subsection_header.split(')')[0],
                        "noi_dung": subsection_header + subsection_content
                    })
            else:
                current_section["noi_dung"] = section_header + section_content.strip()

            sections.append(current_section)

        return sections

    # Construct the JSON structure
    data = {
        "_id": str(ObjectId()),
        "ten_luat": "Thông tư 151/2010/TT-BTC",
        "ngay_ban_hanh": "27/09/2010",
        "ngay_hieu_luc": "11/11/2010",  # 45 days after signing (27/09/2010 + 45 days)
        "chuong": []
    }

    # If no chapters are found, treat the entire document as a single implicit chapter
    if not chapter_pattern:
        chapter = {
            "so_chuong": "I",
            "ten_chuong": "Quy định chung",
            "dieu": []
        }
        for num, content in article_pattern:
            lines = content.strip().split('\n', 1)
            title = lines[0].strip()
            body = lines[1].strip() if len(lines) > 1 else ''
            article = {
                "so_dieu": int(num),
                "ten_dieu": title,
                "noi_dung": parse_article_content(body)
            }
            chapter["dieu"].append(article)
        data["chuong"].append(chapter)
    else:
        for chapter_title, chapter_content in chapter_pattern:
            chapter = {
                "so_chuong": chapter_title.split()[1],
                "ten_chuong": chapter_title.strip(),
                "dieu": []
            }
            articles = re.findall(r"#\s*Điều\s(\d+)\.\s(.*?)(?=#\s*Điều\s\d+\.|$)", chapter_content, re.DOTALL)
            for num, content in articles:
                lines = content.strip().split('\n', 1)
                title = lines[0].strip()
                body = lines[1].strip() if len(lines) > 1 else ''
                article = {
                    "so_dieu": int(num),
                    "ten_dieu": title,
                    "noi_dung": parse_article_content(body)
                }
                chapter["dieu"].append(article)
            data["chuong"].append(chapter)

    return data