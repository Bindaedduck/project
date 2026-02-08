## Solution

**IBM Process Mining(IPM)**, **Business Automation Workflow(BAW)**, **Watsonx**

## Concept

- **IBM Process Mining:** 시스템 로그를 바탕으로 시스템 간 흐름 파악
- **IrBM Task Mining:** 사람의 PC작업을 바탕으로 개별작업 파악
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
> 도구
1. [OCP(Openshift Container Platform) CLI 도구, oc-mirror CLI 플러그인](https://www.ibm.com/links?url=https%3A%2F%2Fmirror.openshift.com%2Fpub%2Fopenshift-v4%2Fclients%2Focp%2F) 
    - 4.18.x(OpenShift 버전)
    - openshift-client-linux.tar.gz, oc-mirror.tar.gz
2. [IBM/ibm-pak](https://github.com/IBM/ibm-pak) 
    - Tags -> v1.21.1(최신 버전)
    - oc-ibm_pak-linux-amd64.tar.gz
3. [Podman(컨테이너를 실행하고 관리하는 도구)](https://www.ibm.com/links?url=https%3A%2F%2Fpodman.io%2Fgetting-started%2Finstallation.html)

> 파일
1. CASE 파일: ~/.ibm-pak/data/cases/
2. 매니페스트 파일: ~/.ibm-pak/data/mirror/$CASE_NAME/$VERSION/
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
