# Dockerfile (Django 애플리케이션용)                                                        

# 1. 기반 이미지 설정                                                                       
FROM python:3.10-slim-bookworm
 
# 2. 환경 변수 설정                                                                         
ENV PYTHONDONTWRITEBYTECODE 1                                                               
ENV PYTHONUNBUFFERED 1                                                                      
WORKDIR /app                                                                                

COPY .env /app/.env
# 3. 시스템 의존성 및 Node.js 설치                                                          
RUN apt-get update && \                                                                     
apt-get install -y --no-install-recommends \                                            
default-libmysqlclient-dev \                                                            
gcc \                                                                                   
pkg-config \                                                                            
curl \                                                                                  
&& curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \                         
&& apt-get install -y nodejs \                                                          
&& rm -rf /var/lib/apt/lists/*                                                          

# 4. Python 의존성 설치 (캐시 활용)                                                         
COPY requirements.txt /app/                                                                 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt                                          

# 5. Node.js 의존성 설치 (캐시 활용)                                                        
#COPY package.json package-lock.json /app/                                                   
#RUN npm install                                                                             
 
# 6. 프로젝트 전체 소스 코드 복사                                                           
COPY . /app/                                                                                

#7. Django 정적 파일 수집                                                                  
RUN python manage.py collectstatic --noinput                                                

# 8 포트 노출 및 애플리케이션 실행                                                         
EXPOSE 7000 
