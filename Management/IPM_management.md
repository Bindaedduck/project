
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

> python 패키지
```
# 경로
opt/processmining/respository/temp/accel/venv/lib/python3.12/site-packages

# 실제 실행 위치
## RHEL
/usr/bin/python 3.12

## IPM
/opt/processmining/repository/temp/accel/venv/bin/python 3.12
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

> Project
- Eventlog upload
    - 최적화
        - csv -> csv.gz
        - 한 번에 업로드하는 양은 최대 200만줄 정도만  

    - 누적해서 파일 업로드 가능
    - 업로드 300MB, 누적 용량 47GB 제한
    - 여러파일을 읽어들이기 가능 but 여러파일을 zip파일로 묶어서 업로드 할 시 하나의 파일만 읽는다
    - ETL
        - TEXT 문자열은 255자 이하
        - processid, activity, starttime은 빈칸 X
        - timestamp 형식은 starttime 호환 X
        - 컬럼이름의 .이 들어가면 안된다.
    - error: 발견한 상황만 기재, 다른 문제일수도 있다.
        - Invalid csv field {0}: TEXT 문자열 길이가 255자를 넘어간 경우
        - Generic error: 컬럼명이 예약어를 쓰고 있는 경우
        - Case id...: processid값이 빈칸
        - starttime...: starttime 형식 or 빈칸
        - %Y-%m-%d %H:%M:%S.%f 형식을 사용하여 '2025-03-11 15:04:00'형식 날짜를 구문 분석할 수 없음: 2025-03-11 15:04:00 값을 %Y-%m-%d %H:%M:%S.%f 형식에 맞지 않아서 발생


- Process > Model
  - Box
    - Anonymous: Role을 부여하지 않았을 때 표시
    - Box 클릭 후 show activity statistics > 필드 > compute statistics > 필드에 대한 통계
    - endtime 컬럼 값을 설정하지 않으면 box에 duration 값은 0으로 표시
  
  - BPMN download: Download > Model(BPMN2.0) > Download

- Table Join을 하면 object table 컬럼으로 role을 부여할 수 있다.
    - Attributes > Role attribute > Edit role attribute > 컬럼 지정

- View option
    - 활동복잡도: activity 백분율 / 높일수록 activity가 개수가 늘어난다.
    - 관계복잡도: activtiy간의 관계 백분율 / 높일수록 관계(선)가 더 많이 보인다.

- 필터 지정
    - Process > Manage filters > Add filters
        - Timespan: 기간별로 조회
        - Process Flow: 횟수별로 조회
    
    - Save as template: 필터 즐겨찾기

- Multi projcet: 같은 organization안에 같은 object table로 묶여있는 경우에 같이 묶어서 최대 5개까지 보여진다.

- Backup
    - project의 meta data, 설정, 대시보드만 가져오며 data는 백업하지 않는다.
    - data를 업로드 할시 meta data, 설정, 대시보드 값을 backup파일의 값 그대로 가져온다.

- 특이점
    - 다른 사용자가 Projcet의 옵션들을 조정하여 일정시간 보고 있으면 해당 옵션들을 projcet가 기억하여 다른 사람들이 project를 보려고 할때 해당 옵션으로 보여지게 된다.
    - project는 소유자가 아니면 관리자나 rest api호출로도 삭제할 수 없다.

> ProcessApp
- error: 발견한 상황만 기재, 다른 문제일수도 있다.
    - [Object object]: timeout 에러, 재시도를 하게 되면 성공하는 경우가 있다.

<br/>

> Project / ProcessApp 역할
- Project: 설계/분석 -> 설계도

- ProcessApp: 운영/모니터링 -> 설계도를 가지고 실제 운영

> DB
- project-operations: 에러 로그
- accelatortype, accelatortypedetails: processapp

<br/>

> Rest api
- 기본적으로 계정의 apiKey를 통해 JWT token(Bearer token) 값을 받아 호출
    - apiKey 활성화: 계정 > User profile > Enable API Key
    - JWT token 값 받아오기
        - 계정 > User profile > Rest-API and MCP - Generate token
        - rest api 호출
    - Bearer token: 보안 토큰의 일종, 소지자(Bearer)가 추가 인증 없이 토큰만 있으면 접근하는 방식

```
# sign(POST): JWT token 값 받아오기

# request
/ingergration/sign
{
    "uid":계정
    "apiKey":apiKey
}

# response
{
    "sign":JWT token
    "success":true
}
```

```
# settings(PATCH): project의 세팅 값 변경
# Ex. project의 복잡도 옵션을 초기화할때 사용(복잡도가 올라가면 project의 로딩시간이 길어지므로)

# request
# projectKey: project 이름
# org: project의 소유자 권한인 상태에서 Project > Options > Process Details > Organization key
/integration/processes/{projectKey}/setting
auth: JWT token
param: org
{
  "generalSettings": {
    "computeDurationInBusinessHours": true,
    "excludeWeekends": true,
    "businessHours": "9-11",
    "selectedCalendars": [
      {
        "id": "3rvsu7367378823gdbnfb",
        "name": "Production Team",
        "dates": [
          "2019-11-14T00:55:31.820Z",
          "2016-09-13T23:30:52.123Z"
        ],
        "vacationType": [
          "sample"
        ]
      }
    ],
    "automatedFieldTruthValue": "Robot",
    "automatedActivityAttribute": "Opp Band",
    "customExcludedFields": [
      "Opp band",
      "Opp tree"
    ],
    "timeZoneOffset": "+0200",
    "defaultPage": "Analytics",
    "displayReferenceActivities": true,
    "keepDefinedRoles": true,
    "defaultMetric": "median",
    "projectCurrency": "USD",
    "modelRelationDetails": 1,                           #관계 복잡도
    "modelActivityDetail": 100,                          #활동 복잡도
    "blueWorksliveProcess": "sample",
    "defaultBucketLimit": 23
  },
  "activityCosts": [
    {
      "activity": "Amend Purchase Requisition",
      "cost": 1,
      "type": "Manual",
      "endDate": "2019-11-14T00:00:00.000Z"
    }
  ],
  "activityWorkingTimes": [
    {
      "activity": "Amend Purchase Requisition",
      "type": "Automatic",
      "value": 110,
      "endDate": "2019-11-14T00:00:00.000Z"
    }
  ],
  "roleCosts": [
    {
      "role": "Requester",
      "hourlyCost": 2,
      "endDate": "2019-11-14T00:00:00.000Z"
    }
  ],
  "resourceCosts": [
    {
      "resource": "Anna kaulfman",
      "type": "Automatic",
      "hourlyCost": 6,
      "endDate": "2019-11-14T00:00:00.000Z"
    }
  ]
}
```
