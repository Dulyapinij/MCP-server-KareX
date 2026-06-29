import os
import trafilatura
import requests
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Scraping
def scrape_article(url):
    print(f"กำลังดึงเนื้อหาจากเว็บ: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # เช็ก Error
        
        # trafilatura จะช่วยตัด HTML ขยะออกให้ เหลือแต่ Text
        text = trafilatura.extract(response.text)
        
        if text:
            print(f"✅ ดึงข้อมูลสำเร็จ ได้เนื้อหา {len(text)} ตัวอักษร")
            return text
        else:
            print("❌ trafilatura หาเนื้อหาหลักไม่เจอ")
            return None
            
    except Exception as e:
        print(f"❌ ไม่สามารถดึงข้อมูลได้: {str(e)}")
        return None

# Translation
def translate_to_thai(raw_text):
    print("กำลังส่งให้ AI แปลไทย")
    
    prompt = f"""
    คุณคือ 'ผู้เชี่ยวชาญด้านการแปลเอกสารทางการแพทย์และการดูแลสุขภาพ' 
    หน้าที่ของคุณคือแปลข้อความภาษาอังกฤษด้านล่างนี้เป็นภาษาไทย
    
    เงื่อนไขการแปล:
    1. แปลให้สละสลวย อ่านง่าย เป็นธรรมชาติแบบที่คนไทยอ่าน
    2. หากมีศัพท์เฉพาะทางการแพทย์ ให้แปลเป็นไทยและวงเล็บภาษาอังกฤษไว้ด้วย
    3. จัดย่อหน้าให้เป็นระเบียบ อ่านง่าย
    
    ข้อความที่ต้องการแปล:
    ---
    {raw_text[:3000]}
    ---
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        print("✅ แปลภาษาสำเร็จ\n")
        return response.text
    except Exception as e:
        print(f"❌ แปลภาษาไม่สำเร็จ: {str(e)}")
        return None

# Main
if __name__ == "__main__":
    target_url = "https://www.nia.nih.gov/health/alzheimers-and-dementia/what-alzheimers-disease"
    
    scraped_text = scrape_article(target_url)
    
    if scraped_text:
        print("-" * 50)
        print(f"ข้อมูลดิบ:\n{scraped_text[:300]}...\n")
        print("-" * 50)
        
        thai_translation = translate_to_thai(scraped_text)
        
        if thai_translation:
            print("แปลไทย:")
            print(thai_translation)