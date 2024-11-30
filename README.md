# MANDATORY

#### 1. credentials.env

1.  credentials.env.example을 credentials.env 로 변경
2.  USERNAME, PASSWORD 입력

#### 시간 주기 설정

- install_and_schedule.sh 의
  `CRON_JOB="* 12 * * * $(pwd)/venv/bin/python3 $(pwd)/get_cabi_coin.py"`
  현재 매일 12시에 실행
- 절전모드시 실행이 안되니 주의

##### 실행권한 부여

- chmod +x install_and_schedule.sh

#### 스크립트 실행

- ./install_and_schedule.sh

---

## FOR TEST

#### 크론잡 확인

- crontab -l

#### 브라우저 숨김 설정

- ./get_cabi_coin.py 의
  `options.add_argument('--headless') # 브라우저를 숨김 모드로 실행`

#### 동전줍기 한번 실행 (쉘스크립트를 통해 설치한 후 해야합니다.)

$(pwd)/venv/bin/python3 $(pwd)/get_cabi_coin.py
