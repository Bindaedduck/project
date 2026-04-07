# 📋 IBM Process Mining (IPM) 

본 문서는 데이터 적재 및 SQL 조회 시 발생할 수 있는 구문 오류를 방지하기 위한 컬럼명(Column Name) 설정 표준입니다.

---

## 1. 사용 금지 및 주의 특수문자
데이터베이스 엔진과 IPM 분석 엔진에서 연산자나 구분자로 오인할 수 있는 문자들입니다.

| 특수문자 | 상태 | 이유 및 발생 현상 | 권장 대체 문자 |
| :--- | :---: | :--- | :--- |
| **`.` (Dot)** | **금지** | 테이블명.컬럼명 구분자로 인식 (조회 불가) | `_` (Underscore) |
| **`-` (Dash)** | **금지** | SQL 산술 연산자(Minus)로 인식 | `_` (Underscore) |
| **` ` (Space)** | **금지** | 구문 종료로 인식하여 Syntax Error 발생 | `_` (Underscore) |
| **`/` , `\`** | **주의** | 나눗셈 연산자 또는 경로 구분자로 오인 | `_` 또는 `div` |
| **`@`, `#`, `$`** | **주의** | 특수 변수나 임시 객체 기호와 충돌 가능 | 제거 권장 |
| **`( )`, `[ ]`** | **금지** | 함수 호출 또는 배열 인덱스로 인식 | `_` 로 대체 |

---

## 2. SQL 및 시스템 예약어 (Reserved Words)
컬럼명으로 사용할 경우 쿼리 작성 시 반드시 쌍따옴표(`" "`)를 써야 하거나, 실행이 거부되는 단어들입니다.

### ⚠️ 필수 회피 단어 (조회 및 적재 오류 주범)
* **날짜 관련:** `DATE`, `TIME`, `TIMESTAMP`, `INTERVAL`, `YEAR`, `MONTH`, `DAY`
* **DML/DDL:** `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `TABLE`, `COLUMN`, `INDEX`, `VIEW`
* **조건/논리:** `WHERE`, `AND`, `OR`, `NOT`, `IN`, `LIKE`, `BETWEEN`, `IS`, `NULL`
* **집계/그룹:** `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`, `GROUP`, `ORDER`, `BY`, `HAVING`
* **IPM 엔진 예약어:** `PROCESSID`, `ACTIVITY`, `STARTTIME`, `ENDTIME`, `RESOURCE`, `ROLE`

---

## 3. 권장 명명 규칙 (Best Practices)

1.  **Lower Case Only:** 모든 컬럼명은 **소문자**로 작성한다. (PostgreSQL은 대소문자를 구분하며, 대문자 포함 시 쿼리가 복잡해짐)
2.  **Snake Case:** 단어 사이의 구분은 언더바(`_`)를 사용한다. (예: `user_id`, `event_timestamp`)
3.  **Prefix 활용:** 예약어 충돌을 피하기 위해 의미 있는 접두어를 붙인다.
    * `id_` : 식별자 (예: `id_jira`, `id_swarm`)
    * `ts_` : 타임스탬프 (예: `ts_start`, `ts_end`)
    * `val_`: 수치 데이터 (예: `val_amount`, `val_cost`)
4.  **Length Limit:** 컬럼명은 영문 기준 **30자 이내**를 권장한다. (PostgreSQL 한계는 63자이나 가독성을 위해 단축 권고)
