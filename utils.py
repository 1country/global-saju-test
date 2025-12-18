import requests
import streamlit as st
from datetime import date

# 1. 만세력 엔진 (일주 계산기 - 영문 설명 추가됨)
def calculate_day_gan(birth_date):
    base_date = date(1900, 1, 1)
    delta = birth_date - base_date
    if delta.days < 0: return 0
    gan_index = delta.days % 10
    gans = [
        {"ko": "갑목(甲)", "desc": "곧게 뻗은 거목", "desc_en": "Straight and tall tree", "element": "Wood", "en": "Gap (Wood)"},
        {"ko": "을목(乙)", "desc": "적응력 강한 화초", "desc_en": "Adaptable and resilient flower", "element": "Wood", "en": "Eul (Wood)"},
        {"ko": "병화(丙)", "desc": "태양 같은 열정", "desc_en": "Passion like the blazing sun", "element": "Fire", "en": "Byeong (Fire)"},
        {"ko": "정화(丁)", "desc": "촛불 같은 온기", "desc_en": "Warmth of a gentle candle", "element": "Fire", "en": "Jeong (Fire)"},
        {"ko": "무토(戊)", "desc": "묵직한 태산", "desc_en": "Heavy and majestic mountain", "element": "Earth", "en": "Mu (Earth)"},
        {"ko": "기토(己)", "desc": "생명을 품은 텃밭", "desc_en": "Fertile soil embracing life", "element": "Earth", "en": "Gi (Earth)"},
        {"ko": "경금(庚)", "desc": "단단한 원석", "desc_en": "Solid and unrefined iron ore", "element": "Metal", "en": "Gyeong (Metal)"},
        {"ko": "신금(辛)", "desc": "빛나는 보석", "desc_en": "Shining and precious gemstone", "element": "Metal", "en": "Sin (Metal)"},
        {"ko": "임수(壬)", "desc": "포용하는 바다", "desc_en": "Vast and embracing ocean", "element": "Water", "en": "Im (Water)"},
        {"ko": "계수(癸)", "desc": "스며드는 빗물", "desc_en": "Gentle and permeating rain", "element": "Water", "en": "Gye (Water)"}
    ]
    return gans[gan_index]

# 2. 라이센스 검증기 (마스터키 지원)
def verify_license_flexible(key, current_product_id, all_access_id="all_access_pass"):
    if key == "test": return True, "테스트 통과 (개발자 모드)"
    
    if _check_gumroad(key, current_product_id):
        return True, "✅ 정품 인증 완료! (개별 구매)"
        
    if _check_gumroad(key, all_access_id):
        return True, "👑 프리패스 회원님 환영합니다! (전체 이용 가능)"
        
    return False, "🚫 유효하지 않은 키입니다."

# (내부용) 실제 검로드 통신 함수
def _check_gumroad(key, permalink):
    try:
        response = requests.post(
            "https://api.gumroad.com/v2/licenses/verify",
            data={"product_permalink": permalink, "license_key": key, "increment_uses_count": "true"}
        )
        data = response.json()
        if data.get("success") and not data["license_key"]["refunded"] and not data["license_key"]["chargebacked"]:
            return True
        return False
    except:
        return False
