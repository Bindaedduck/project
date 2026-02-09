## Solution

**IBM Process Mining(IPM)**, **Business Automation Workflow(BAW)**, **Watsonx**

## Concept

- **IBM Process Mining:** 시스템 로그를 바탕으로 시스템 간 흐름 파악
- **IBM Task Mining:** 사람의 PC작업을 바탕으로 개별작업 파악
- **Air-gapped:** 외부환경과 물리적, 논리적으로 차단된 환경
- **Node:** 서버
- **Non-GPU Worker Node:** GPU가 없는 워커 노드
- **Plugin:** 기존 도구의 기능을 덧붙여 확장하는 모듈

##  Quick Links

- **IBM Process Mining (IPM)**
    - [Official Documentation](https://www.ibm.com/docs/ko/process-mining)
        
- **Business Automation Workflow (BAW)**
    - [Official Documentation](https://www.ibm.com/docs/ko/baw)

##  Resource Access

- **Partner Portal:** [IBM Partner Plus](https://partnerportal.ibm.com/s/)
    
- **Software Download:** [Software Access Catalog](https://partnerportal.ibm.com/s/software-access-catalog)

##  Tech Stack & Environment
- **Basestructure:**
    - master node(제어, 스케줄링, 상태관리) - worker node(실행) - storage node(저장)

- **Infrastructure:** 
    - Red Hat (RHEL) : 9.6
    - Red Hat OpenShift (OCP) : 4.18
    - Master #1,2,3 - Non-GPU Worker #1,2,3 - GPU Worker #1 - Storage #1,2,3
    - CP4BA는 GPU를 사용하지 않는다, GPU Worker의 용도는?
    - CP4BA 25.0.0, 25.0.1 버전과 호환 

- **Solution Version:** Latest (최신 버전)
- **License:** X
- **Air-gapped** 
- **Containerization?**

## Installation Checklist (Preparation)

### IBM Process Mining(IPM)
### [ Non Container ]
> [패키지 다운로드](https://www.ibm.com/software/passportadvantage/pao_customer.html)
1. IBM Process Mining(M0XLBML)   
2. IBM Task Mining(M0XLCML)

> 설치 및 구성하기 IBM Process Mining
1. [기본 설정](https://www.ibm.com/docs/ko/process-mining/2.1.0?topic=mining-basic-setup)
    - [MonetDB](https://www.ibm.com/links?url=https%3A%2F%2Fwww.monetdb.org%2Feasy-setup%2Fredhat-centos%2F) 11.53.9
    - [PostgreSQL](https://www.ibm.com/links?url=https%3A%2F%2Fwww.postgresql.org%2Fdownload%2Flinux%2Fredhat%2F) 16
    - python3.12
    - nginx
2. 고급 설정
    - [JWT 서명 키 생성](https://www.ibm.com/docs/ko/process-mining/2.1.0?topic=configurations-advanced-setup)

> [확장 및 고가용성](https://www.ibm.com/docs/ko/process-mining/2.1.0?topic=configuration-scaling-high-availability)
1. [Redis](https://www.ibm.com/links?url=https%3A%2F%2Fredis.io%2Fdocs%2Flatest%2Foperate%2Frs%2Finstalling-upgrading%2F)

### [ Container ]
> Linux 환경에 사전 다운로드
0. [Linux(Ubuntu) 설치](#linuxubuntu-설치)
1. 도구 설치- 관리자 권한으로 PowerShell 실행<br/><br/>
    `oc - OCP(Openshift Container Platform) CLI` 
    ```
    # ocp v4.18.x(OpenShift 버전)
    curl -L https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest-4.18/openshift-client-linux.tar.gz | tar -xz  
    
    # /user/local/bin/폴더에 다운받은 결과물 이동, kubectl도 같이 다운받기 때문에 같이 이동
    sudo mv oc kubectl /usr/local/bin/ 
    ``` 

    `oc-mirror plugin`
    ```
    # oc-mirror v4.18.x
    curl -L https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest-4.18/oc-mirror.tar.gz | tar -xz
  
    sudo mv oc-mirror /usr/local/bin/
    ```

    `ibm-pak plugin`
    ```
    # ibm-pak v1.21.1
    curl -L https://github.com/IBM/ibm-pak/releases/download/v1.21.1/oc-ibm_pak-linux-amd64.tar.gz -o oc-ibm_pak-linux-amd64.tar.gz
    tar -xvzf oc-ibm_pak-linux-amd64.tar.gz

    sudo mv oc-ibm_pak-linux-amd64 /usr/local/bin/oc-ibm_pak
    ```
2. CASE 파일 다운로드
    ```
    # ibm-pak 실행 권한 부여
    sudo chmod +x /usr/local/bin/oc-ibm_pak 
    oc-ibm_pak --version

    #CASE_NAME, CAE_VERSION 설정
    export CASE_NAME=ibm-process-mining
    export CASE_VERSION=4.0.0  

    # CASE
    oc ibm-pak get $CASE_NAME --version $CASE_VERSION
    ```
3. Manifest 파일 다운로드
    ```
    # TARGET_REGISTRY 임시 설정
    export TARGET_REGISTRY=cp.local.registry:5000

    #Manifest
    oc ibm-pak generate mirror-manifests $CASE_NAME file://local --version $CASE_VERSION --final-registry $TARGET_REGISTRY
    ```

4. 이미지 데이터 다운로드
--------여기서부터 수정--------------

00. 파일 경로
    - CASE: ~/.ibm-pak/data/cases/
    - Manifest: ~/.ibm-pak/data/mirror/


> 도구

3. [Podman(컨테이너를 실행하고 관리하는 도구)](https://www.ibm.com/links?url=https%3A%2F%2Fpodman.io%2Fgetting-started%2Finstallation.html)

> 파일
3. 이미지 데이터: ~/mirror-data

### Business Automation Workflow(BAW)
### [ Container ]
> [컨테이너에 설치 준비](https://www.ibm.com/docs/ko/baw/25.0.x?topic=configuring-preparing-install-business-automation-workflow-containers)
1. Storage class 파일 작성?
2. [git: cert-kubernetes-baw 25.0.1 다운로드](https://github.com/ibmbpm/cert-kubernetes-baw)

> [에어갭 배포를 위한 클러스터 준비](https://www.ibm.com/docs/ko/baw/25.0.x?topic=configuring-preparing-your-cluster-air-gapped-offline-deployment)
1. [OCP(Openshift Container Platform) CLI 도구](https://www.ibm.com/links?url=https%3A%2F%2Fmirror.openshift.com%2Fpub%2Fopenshift-v4%2Fclients%2Focp%2F)
2. [Podman(컨테이너를 실행하고 관리하는 도구)](https://www.ibm.com/links?url=https%3A%2F%2Fpodman.io%2Fgetting-started%2Finstallation.html)
3. [IBM Catalog Mangement Plug-in(V1.18.2 또는 그 이상)](https://www.ibm.com/links?url=https%3A%2F%2Fgithub.com%2FIBM%2Fibm-pak%2Freleases)
4. [oc mirroroc](https://www.ibm.com/links?url=https%3A%2F%2Fmirror.openshift.com%2Fpub%2Fopenshift-v4%2Fx86_64%2Fclients%2Focp%2F)
5. [baw-case-to-be-mirrored-25.0.1. txt](https://www.ibm.com/links?url=https%3A%2F%2Fgithub.com%2Fibmbpm%2Fcert-kubernetes-baw%2Fblob%2F25.0.1%2Fscripts%2Fairgap%2Fbaw-case-to-be-mirrored-25.0.1.txt)

> 컨테이너에 IBM Business Automation Workflow 전제 조건 설치하기
1. Java 17 이상, keytool
2. [OpenSSL](https://www.ibm.com/links?url=https%3A%2F%2Fwww.openssl.org%2F)

## Linux(Ubuntu) 설치
1. 관리자 권한으로 PowerShell 실행
    ```
    wsl --install 
    wsl --status # Default Version: 2
    ```

2. 재부팅 후 Ubuntu실행 
    - 사용자명/ 비밀번호 설정

## Free trial
- [IPM](https://ibm-process-mining-trial.automationcloud.ibm.com/signin)
- [Watsonx](https://dl.watson-orchestrate.ibm.com/?mcsp_metadata=eyJjcm4iOiJjcm46djE6YXdzOnB1YmxpYzp3eG86dXMtZWFzdC0xOnN1Yi8yMDI2MDIwOS0wNDI0LTM1OTgtOTAxZi1mNzE2MGI1M2Q2YjE6MjAyNjAyMDktMDQyNC01MTIzLTkwY2YtMjBhZWM4M2Q5OGU5OjoifQ)
- [CP4BA](https://www.automationcloud.ibm.com/auth/index.jsp)