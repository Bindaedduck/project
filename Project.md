## Solution

**IBM Process Mining(IPM)**, **Business Automation Workflow(BAW)**, **Watsonx**

## Concept

- **IBM Process Mining:** 시스템 로그를 바탕으로 시스템 간 흐름 파악
- **IBM Task Mining:** 사람의 PC작업을 바탕으로 개별작업 파악
- **Air-gapped:** 외부환경과 물리적, 논리적으로 차단된 환경
- **Node:** 서버
- **Non-GPU Worker Node:** GPU가 없는 워커 노드

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
    - BAW 25.0.1 버전과 호환 
- **Solution Version:** Latest (최신 버전 사용)
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
    - [MonetDB](https://www.ibm.com/links?url=https%3A%2F%2Fwww.monetdb.org%2Feasy-setup%2Fredhat-centos%2F)
    - [PostgreSQL](https://www.ibm.com/links?url=https%3A%2F%2Fwww.postgresql.org%2Fdownload%2Flinux%2Fredhat%2F)
    - python3.12
    - nginx

### [ Container ]
> 호스트 준비하기
1. [OCP(Openshift Container Platform) CLI 도구](https://www.ibm.com/links?url=https%3A%2F%2Fmirror.openshift.com%2Fpub%2Fopenshift-v4%2Fclients%2Focp%2F)
2. [Podman(컨테이너를 실행하고 관리하는 도구)](https://www.ibm.com/links?url=https%3A%2F%2Fpodman.io%2Fgetting-started%2Finstallation.html)
3. [IBM/ibm-pak](https://github.com/IBM/ibm-pak)
4. [oc-mirror CLI 플러그인](https://www.ibm.com/links?url=https%3A%2F%2Fmirror.openshift.com%2Fpub%2Fopenshift-v4%2Fx86_64%2Fclients%2Focp%2Fstable-4.17%2Foc-mirror.tar.gz)

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
