## Project Version

- python 3.9.16
  - 파이썬 상위 버전에서는 OpenCV가 정상적으로 작동하지 않는 문제가 있습니다!
  - _꼭 3.9.16 버전으로 설치 부탁드립니다._

<br>
<br>

---

## How to Run

1. 파이썬 가상환경에서 돌리는 걸 추천드립니다.
   - 파이썬 가상환경 구동 명령어

```bash
>> python3 -m venv .venv
>> cd .venv
>> source bin/activate
```



- 파이썬 특정 버전으로 가상환경 실행하기 (e.g.)

```bash
>> /opt/homebrew/bin/python3.9 -m venv .venv
# {원하는 버전의 파이썬이 설치된 경로} -m {가상환경 이름} {가상환경 디렉토리명}
```



2. 가상 환경 디렉토리내로 모든 소스파일 복사

```bash
>> cp -r {mosaicec 경로} .
```

- 또는 파일 편집기 내에서 파일을 복사해오는 것도 가능합니다!



3. 쉘 스크립트 파일 구동

```bash
>> cd mosaicec
>> sh mosaicec.sh
```
