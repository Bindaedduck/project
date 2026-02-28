
## IBM Process Mining management
> Admin 권한 부여
```
# account_groups: 계정의 권한 관리 테이블
INSERT INTO public.account_groups(id, groupid, userid, lastmoddate)
VALUES(25, '관리자 그룹 id', '계정 id', '2026-02-24 23:04:10.594');  
```

<br/>

> 로그인 접속 시 403 에러
- Admin 권한이 있는 계정이 해당 계정에게 아무 권한 부여
    - Accounts list > 해당 계정 선택 > Member of > 아무 권한 부여

<br/>

> Organization 수정
- 모든 프로젝트(All projects) > Organization 수정

<br/>

> python 패키지 경로
```
opt/processmining/respository/temp/accel/venv/lib/python3.12/site-packages/
```

<br/>

> PostgreSQL 접속
```
# PostgreSQL 접속
sudo -u postgres psql

# PostgreSQL > processmining 스키마 접속 1
sudo -u postgres psql -d processmining

# PostgreSQL > processmining 스키마 접속 2
sudo -u postgres /usr/bin/psql -d eventlog
```

<br/>

> 에어갭 환경에서 python 패키지 설치
- RHEL ISO 자체에 python만이 아니라 python패키지도 어느정도 포함되어 있으며, 설치할 패키지가 포함되어 있다는 가정하에 진행
```
# psycopg2 패키지 설치
sudo dnf install python3.12-psycopg2

# 의존성 패키지 설치
# gcc: c컴파일러, postgresql-devel: postgresql 클라이언트 헤더 파일 제공, python3-devel: python 개발 헤더 파일 제공 
sudo dnf install gcc postgresql-devel python3-devel

# 패키지 옮기기
cp /usr/lib64/python3.12/site-packages/패키지폴더 /opt/processmining/repository/temp/accel/venv/lib/python3.12/site-packages

# 폴더 권한 부서서
chown -R user:user /

# 패키지가 제대로 적용됐는지 확인
# -> 설치한 패키지를 사용하는 python moudle을 업로드해서 processApp 실행
```

<br/>

> User groups authority
- Analyst Users
    - Create a process-mining project [o]
    - Start from a process application [o]

- Business Users
    - projcets only view [o]

- Multi TenantAdministrators
    - 다른 Tenant를 관리할 수 있다.

<br/>

> Organizations
- 같은 organizations에서는 project, processApp이 공유된다.

- 같은 tenants 안에서는 organization이 중복으로 만들어질 수 없다.

<br/>

> Tenants
- tenants가 다르면 organizations가 공유되지 않아 동일이름으로 생성도 가능하다.

<br/>

> Projects
- Process > Model > Box
    - Anonymous: Role을 부여하지 않았을 때 표시
    - Box 클릭 후 show activity statistics > 필드 > compute statistics > 필드에 대한 통계

- Table Join을 하면 object table 컬럼으로 role을 부여할 수 있다.
    - Attributes > Role attribute > Edit role attribute > 컬럼 지정

- 필터 지정
    - Process > Manage filters > Add filters
        - Timespan: 기간별로 조회
        - Process Flow: 횟수별로 조회
    
    - Save as template: 필터 즐겨찾기

<br/>

> Project / ProcessApp 역할
- Project: 설계/분석 -> 설계도

- ProcessApp: 운영/모니터링 -> 설계도를 가지고 실제 운영
