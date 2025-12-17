import requests
import streamlit as st
from datetime import date

# 1. 만세력 엔진 (일주 계산기)
def calculate_day_gan(birth_date):
    base_date = date(1900, 1, 1)
    delta = birth_date - base_date
    if delta.days < 0: return 0
    gan_index = delta.days % 10
    gans = [
        {"ko": "갑목(甲)", "desc": "곧게 뻗은 거목", "element": "Wood", "en": "Gap (Wood)"},
        {"ko": "을목(乙)", "desc": "적응력 강한 화초", "element": "Wood", "en": "Eul (Wood)"},
        {"ko": "병화(丙)", "desc": "태양 같은 열정", "element": "Fire", "en": "Byeong (Fire)"},
        {"ko": "정화(丁)", "desc": "촛불 같은 온기", "element": "Fire", "en": "Jeong (Fire)"},
        {"ko": "무토(戊)", "desc": "묵직한 태산", "element": "Earth", "en": "Mu (Earth)"},
        {"ko": "기토(己)", "desc": "비옥한 텃밭", "element": "Earth", "en": "Gi (Earth)"},
        {"ko": "경금(庚)", "desc": "단단한 원석", "element": "Metal", "en": "Gyeong (Metal)"},
        {"ko": "신금(辛)", "desc": "빛나는 보석", "element": "Metal", "en": "Sin (Metal)"},
        {"ko": "임수(壬)", "desc": "도도한 바다", "element": "Water", "en": "Im (Water)"},
        {"ko": "계수(癸)", "desc": "스며드는 빗물", "element": "Water", "en": "Gye (Water)"}
    ]
    return gans[gan_index]

# 2. 라이센스 검증기 (마스터키 지원)
# current_product_id: 지금 페이지 상품 ID
# all_access_id: 20불짜리 프리패스 상품 ID (기본값: all_access_pass)
def verify_license_flexible(key, current_product_id, all_access_id="all_access_pass"):
    # 테스트용
    if key == "test": return True, "테스트 통과 (개발자 모드)"
    
    # 1차 시도: "이거 혹시 '이 페이지 전용' 키야?"
    if _check_gumroad(key, current_product_id):
        return True, "✅ 정품 인증 완료! (개별 구매)"
        
    # 2차 시도: "아니면 혹시 '프리패스(20불)' 키야?"
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
        # 성공했고 + 환불되지 않았고 + 취소되지 않았으면 OK
        if data.get("success") and not data["license_key"]["refunded"] and not data["license_key"]["chargebacked"]:
            return True
        return False
    except:
        return False
