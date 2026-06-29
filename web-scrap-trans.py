import os
import requests
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def get_raw_html(url):
    print(f"กำลังดึงเนื้อหาจากเว็บ: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # เช็ก Error
        
        print(f"✅ โหลดเว็บสำเร็จ ขนาด {len(response.text)} ตัวอักษร")
        return response.text
    except Exception as e:
        print(f"❌ ไม่สามารถโหลดเว็บได้: {str(e)}")
        return None
    
# Scraping และ Translate
def ai_scrape_and_translate(raw_html):
    print("ส่ง HTML ให้ Gemini Scraping และแปลไทย")
    
    prompt = f"""
    คุณคือ 'Advanced Web Scraper & AI Translator' 
    หน้าที่ของคุณคืออ่านซอร์สโค้ด HTML ดิบที่อยู่ด้านล่างนี้ จากนั้น:
    
    1. ทำการ Scraping: ตัดแท็ก HTML, เมนูบาร์, ฟุตเตอร์, และโฆษณาออกให้หมด เหลือไว้เฉพาะ "เนื้อหาหลักของบทความ" เท่านั้น
    2. ทำการแปลและเรียบเรียง: แปลเนื้อหาหลักที่สแครปได้ออกมาเป็น "ภาษาไทยที่สละสลวย" 
    3. ส่งผลลัพธ์กลับมาในรูปแบบ Markdown ที่อ่านง่าย แยกหัวข้อชัดเจน
    
    นี่คือซอร์สโค้ด HTML ดิบที่ต้องจัดการ:
    ---
    {raw_html[:40000]}
    ---
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        print("✅ สแครปและแปลข้อมูลสำเร็จ\n")
        return response.text
    except Exception as e:
        print(f"❌ พัง: {str(e)}")
        return None

# Main
if __name__ == "__main__":
    target_url = "https://www.nia.nih.gov/health/alzheimers-and-dementia/what-alzheimers-disease"
    
    html_content = get_raw_html(target_url)
    
    if html_content:
        print("-" * 50)
        print(f"ข้อมูลดิบ:\n{html_content[:300]}...\n")
        print("-" * 50)
        
        thai_translation = ai_scrape_and_translate(html_content)
        
        if thai_translation:
            print("แปลไทย:")
            print(thai_translation)