
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

# PostgreSQL > processmining 스키마 접속
sudo -u postgres psql -d processmining
```
