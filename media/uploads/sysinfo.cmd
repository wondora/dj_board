: 배치파일 (collect_info.bat)

@echo off
:: 1. 사용자 이름 입력 받기
set /p username=성명을 입력하세요: 

:: 2. 날짜 가져오기 (YYYYMMDD-HHMMSS)
for /f "tokens=1-3 delims=/ " %%a in ("%date%") do (
    set mm=%%a
    set dd=%%b
    set yyyy=%%c
)
for /f "tokens=1-2 delims=: " %%a in ("%time%") do (
    set hh=%%a
    set min=%%b
)
set timestamp=%yyyy%%mm%%dd%-%hh%%min%

:: 3. 파일 이름 생성
set filename=%username%_%timestamp%.txt

:: 4. 시스템 정보 수집
echo 사용자: %username% > %filename%
echo 날짜: %timestamp% >> %filename%
echo --------------------------- >> %filename%
echo 운영체제 버전: >> %filename%
ver >> %filename%

echo. >> %filename%
echo IP 주소: >> %filename%
ipconfig | findstr /i "IPv4" >> %filename%

echo 윈도우 버전: >> %filename%
wmic os get Caption >> %filename%

echo. >> %filename%
echo CPU 정보: >> %filename%
wmic cpu get name >> %filename%

echo. >> %filename%
echo 그래픽 카드 정보: >> %filename%
wmic path win32_VideoController get name >> %filename%

echo. >> %filename%
echo RAM (MB): >> %filename%
wmic computersystem get totalphysicalmemory >> %filename%

echo. >> %filename%
echo HDD 정보: >> %filename%
wmic logicaldisk get size,freespace,caption >> %filename%

echo 완료: %filename%

:: 5. 파일 업로드 (Node.js 서버로 전송)
::curl -X POST http://192.168.0.100:3000/upload -F "file=@%filename%"