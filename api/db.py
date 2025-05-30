# ------------------------------------------------------------------
# 파일명: db.py
# 위치: api/db.py
# 이 파일은 FastAPI 앱에서 사용할 데이터베이스와 연결하고,
# 테이블 정의 및 세션 관리를 위한 설정을 담고 있다.
# - PostgreSQL을 비동기 방식으로 연결하여 사용할 수 있도록 구성함
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# [ import 구문 ]
# SQLAlchemy를 비동기 방식으로 사용할 수 있도록 관련 도구들을 불러온다.
# ------------------------------------------------------------------

# * create_async_engine:
#  - PostgreSQL과 연결을 만들기 위한 도구 (비동기 방식)
#  - DB 주소를 넣어서 '엔진'이라는 연결 도구를 만든다.
# * AsyncSession:
#  - DB에 연결한 후 데이터를 조회하거나 저장할 때 사용하느 ㄴ세션
#  - 비동기 방식으로 작동하는 세션이다.
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# * sessionmaker:
#  - 위에서 만든 엔진을 이용해서 실제 DB 작업을 할 수 있는 '세션'을 만든다.
#  - 쉽게 말하면 "DB 작업을 할 수 있는 연결 준비 도구"
# * declarative_base:
#  - 테이블을을 만들기 위해 사용하는 기본 클래스
#  - 우리가 만들 테이블들은 이 클래스를 '기반으로' 정의하게 된다.
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------------------------------------------------
# [1] PostgreSQL에 연결할 주소 설정 (DB 정속 정보)
# 형식: postgresql+asyncpg://사용자:비밀번호@호스트/데이터베이스이름
# - postgresql+asyncpg: 비동기 방식으로 PostgreSQL에 접속할 수 있게 해주는 형식
# - todo_user : DB 사용자 이름
# - 1234 : 사용자 비밀번호
# - localhost : 현재 컴퓨터에서 실행 중인 DB 서버
# - todo_db : 사용할 데이터베이스 이름
# ------------------------------------------------------------------
DB_URL = "postgresql+asyncpg://todo_user:1234@localhost/todo_db"

# ------------------------------------------------------------------
# [2] DB 엔진 생성
# - 엔진은 FastAPI와 PostgreSQL 사이클 연결해주는 역활을 한다.
# - echo=True : SQL 실행 내용을 터미널에 출력해줌 (디버깅에 유용)
# ------------------------------------------------------------------
db_engine = create_async_engine(DB_URL, echo=True)

# ------------------------------------------------------------------
# [3] 세션(session) 설정
# - 세션은 DB와 데이터를 주고받을 수 있게 도와주는 통로이다.
# - autocommit=False : 자동 저장하지 않음 (commit()을 직접 호출해야 저장됨)
# - autoflush=False : 성능 향상을 위해 자동 반영하지 않음
# - class_=AsyncSession : 비동기 방식의 세션을 사용함
# ------------------------------------------------------------------
db_session = sessionmaker(
    bind=db_engine, class_=AsyncSession, autocommit=False, autoflush=False
)


# ------------------------------------------------------------------
# [4] 테이블 생성을 위한 기본 클래스 정의
# - 이후에 만들 모든 테이블 클래스들은 이 Base를 상속받아 정의한다.
# - 이 Base를 기준으로 실제 DB에 테이블을 만들 수 있다.
# ------------------------------------------------------------------
Base = declarative_base()


# ------------------------------------------------------------------
# [5] FastAPI에서 사용할 DB 세션 생성 함수
# - get-db() 함수는 '의존성  주입(Dependency Injection)'에 사용된다.
# - 즉, 우리가 직접 세션을 만들지 않아도,
#   FastAPI가 이 함수를 실행해서 필요한 DB 세션을 자동으로 넣어준다.
# - 예 : 함수 정의에서 DB=Depends(get_db)라고 쓰면 FastAPI가 알아서 실행해준다.
# - async with : 비동기 방식으로 세션을 열고 닫아준다.
# - yield : session을 외부로 넘겨주고, 함수가 끝나면 자동으로 정리된다.
# ------------------------------------------------------------------
async def get_db():
    async with db_session() as session:
        yield session
