실행권한 부여
chmod +x install_and_schedule.sh

스크립트 실행
./install_and_schedule.sh

크론잡 확인
crontab -l

동전줍기 한번 실행 (쉘스크립트로 설치한 후 해야합니다.)
$(pwd)/venv/bin/python3 $(pwd)/get_cabi_coin.py
