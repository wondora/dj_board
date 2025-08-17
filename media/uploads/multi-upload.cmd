@echo off
:: 서버 주소
set server=http://192.168.0.100:3000/upload

:: 파일이 있는지 확인
if "%~1"=="" (
    echo 드래그한 파일이 없습니다.
    pause
    exit /b
)

echo 선택한 파일들을 업로드합니다...
echo 서버 주소: %server%
echo.

:: 모든 인자 반복 (%1, %2, ..., %n)
:loop
if "%~1"=="" goto done

echo 업로드 중: %~nx1
curl -s -X POST %server% -F "file=@%~1"

shift
goto loop

:done
echo.
echo 모든 파일 업로드 완료
pause