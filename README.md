# MANDATORY

#### 1. credentials.env

1.  credentials.env.example을 credentials.env 로 변경
2.  USERNAME, PASSWORD 입력

##### 실행권한 부여

- `chmod +x install_and_schedule.sh`

#### 스크립트 실행

- `./install_and_schedule.sh`
- sudo 권한 필요 (절전모드를 해제하기 위해 pmset 설정)

---

## FOR TEST

#### 크론잡 확인

- crontab -l

#### 브라우저 숨김 설정

- ./get_cabi_coin.py 의
  `options.add_argument('--headless') # 브라우저를 숨김 모드로 실행`

#### 동전줍기 한번 실행 (쉘스크립트를 통해 설치한 후 해야합니다.)

$(pwd)/venv/bin/python3 $(pwd)/get_cabi_coin.py

#### 절전모드 해제 확인

- pmset -g sched

#### 절전모드 해제 반복 해제

- sudo pmset repeat cancel
