# BackEnd

이 프로젝트는 중앙대학교 **캡스톤 디자인(1)** 의 백엔드 서버로, FastAPI를 기반으로 개발되었습니다.  
주요 기능으로 사용자 관리, 버튼 로그 처리, 실시간 채팅, IoT 연동, 추천 문장 기능 등을 제공합니다.

---

## 📋 주요 기능

1. **사용자 관리**
   - 사용자 추가, 조회, NOK(Next of Kin) 설정 및 조회 API 제공

2. **버튼 로그 및 카테고리 추천**
   - 버튼 클릭 로그 추가
   - 버튼 카테고리별 사용량 집계 및 추천 기능 제공

3. **실시간 채팅**
   - WebSocket을 이용한 실시간 1:1 채팅 기능
   - 메시지 저장, 읽음 상태 관리, 채팅방 메시지 조회 API 제공

4. **추천 문장 기능**
   - 입력 텍스트(한글 자모, 영어 등) 기반 추천 문장 반환 API 제공

5. **IoT 연동**
   - IoT 기기와의 WebSocket 통신 지원 (`/ws/iot`, `/ws/iot-light`)
   - IoT 메시지 브로드캐스트 기능

6. **FCM 푸시 알림**
   - FCM을 통한 푸시 알림 전송 API 제공

---

## 🛠️ 기술 스택

- **언어**: Python
- **프레임워크**: FastAPI
- **데이터베이스**: MySQL
- **ORM**: SQLAlchemy
- **웹소켓**: FastAPI WebSocket
- **템플릿 엔진**: Jinja2
- **기타**: FCM, jamo(한글 자모 분리)

---

## 🚀 실행 방법

1. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

2. **서버 실행**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
   - --host: 서버 컴퓨터의 네트워크 주소
   - --port: 서버 컴퓨터의 네트워크 포트

3. **브라우저 접속**
- 기본 홈페이지
   - localhost:8000
- Swagger 문서 (API 명세서)
   - localhost:8000/docs

## 📝 기타
- DB 연결 정보는 .env 파일을 통해 환경변수로 관리합니다. 
   - DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME (MySQL)
   - FCM_KEY, PROJECT_ID (Firebase)
   