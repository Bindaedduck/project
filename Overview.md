## Solution

**IBM Process Mining(IPM)**, **Business Automation Workflow(BAW)**, **Watsonx Orchestrate**

## Concept

- **IBM Process Mining:** 시스템 로그를 바탕으로 시스템 간 흐름 파악
- **IBM Task Mining:** 사람의 PC작업을 바탕으로 개별작업 파악
- **BAW:** 비즈니스 프로세스 자동화 도구, 업무를 자동으로 처리하는 플랫폼, [BAW / RPA 차이?](#baw--rpa-차이)
- **Air-gapped:** 외부환경과 물리적, 논리적으로 차단된 환경
- **Node:** 서버
- **Non-GPU Worker Node:** GPU가 없는 워커 노드
- **Plugin:** 기존 도구의 기능을 덧붙여 확장하는 모듈
- **RPM:** 패키지 설치, [RPM / YUM 차이?](#rpm--yum-차이)
- **ETL:** Extract, Transform, Load, 데이터를 추출해서 변환하고 저장하는 과정
- **MVP(Minimum Variable Project):** 최소한의 핵심기능만 갖춘 완성된 상태 
- **BPMN(Business Process Modeling Notation):** 비즈니스 프로세스를 시각적으로 설계하고 모델링하기 위한 국제 표준 그래픽 기법
- **Compute:** 계산하다
- **Statistics:** 통계학

##  Quick Links

- **[IBM Process Mining (IPM)](https://www.ibm.com/docs/ko/process-mining)**
        
- **[Business Automation Workflow (BAW)](https://www.ibm.com/docs/ko/baw)**

- **[IBM watsonx Orchestrate ADK](https://developer.watson-orchestrate.ibm.com/agents/descriptions)**

##  Resource Access

- **Partner Portal:** [IBM Partner Plus](https://partnerportal.ibm.com/s/)
    
##  Tech Stack & Environment
- **Basestructure:**
    - master node(제어, 스케줄링, 상태관리) - worker node(실행) - storage node(저장)

- **Infrastructure:** 
    - Red Hat (RHEL) : 9.6
    - Red Hat OpenShift (OCP) : 4.18
    - Master #1,2,3 - Non-GPU Worker #1,2,3 - GPU Worker #1 - Storage #1,2,3
    - CP4BA 25.0.0, 25.0.1 버전과 호환 

- **Solution Version:** Latest (최신 버전)
- **Air-gapped** 
- **Non-conatianer: IPM?**
- **Conatianer: BAW, Watsonx Orchestrate**

## Role
```
IPM = 원재료 정제 공장
     └─ 로그 데이터를 깔끔하게 정리

BAW = 자동화 공장
     └─ IPM 데이터로 자동 작업 실행

Watsonx = AI 분석실
         └─ IPM 데이터로 AI 분석
```

## Linux(Ubuntu) 설치
1. 관리자 권한으로 PowerShell 실행
    ```
    wsl --install 
    wsl --status # Default Version: 2
    ```

2. 재부팅 후 Ubuntu실행 
    - 사용자명/ 비밀번호 설정

## BAW / RPA 차이
|구분|내용|
|------|---|
|BAW|시스템 간의 API호출로 자동화, UI를 거치지 않는다.|
|RPA|사람이 직접 UI를 클릭해서 자동화|

## RPM / YUM 차이
|구분|내용|인터넷 필요|
|------|---|:---:|
|RPM|Linux프로그램 설치, 의존성 설치 X|X|
|YUM|Linux프로그램 설치, 의존성 설치 O|O|

## PostgreSQL
```
# pg_hba.conf 파일 위치
# pg_hba.conf 파일: 외부 접근 제어 및 인증 관리
/var/lib/pgsql/16/data/pg_hba.conf

# 서비스 상태 확인
system status postgresql-16

# PostgreSQL 접속
sudo -u postgres psql

# PostgreSQL > processmining 스키마 접속 1
sudo -u postgres psql -d processmining

# PostgreSQL > processmining 스키마 접속 2
sudo -u postgres /usr/bin/psql -d eventlog

# PostgreSQL 데이터베이스 생성
# usr/psql-16/bin 위치에서 생성하기
export POSTGRES_PROCESSMINER_PWD="<YOUR_PASSWORD>"
export POSTGRES_PROCESSMINER_USER="processmining"
export POSTGRES_PROCESSMINER_DATABASE="processmining"

pushd /tmp
sudo -E -u postgres createuser ${POSTGRES_PROCESSMINER_USER}
sudo -E -u postgres createdb ${POSTGRES_PROCESSMINER_DATABASE}
sudo -E -u postgres psql -c "alter user ${POSTGRES_PROCESSMINER_USER} with encrypted password '${POSTGRES_PROCESSMINER_PWD}';"
sudo -E -u postgres psql -c "grant all privileges on database ${POSTGRES_PROCESSMINER_DATABASE} to ${POSTGRES_PROCESSMINER_USER};"
sudo -E -u postgres psql -c "GRANT ALL ON ALL TABLES IN SCHEMA public TO ${POSTGRES_PROCESSMINER_USER}";
sudo -E -u postgres psql -c "ALTER DATABASE ${POSTGRES_PROCESSMINER_DATABASE} OWNER TO ${POSTGRES_PROCESSMINER_USER}";
popd
```


