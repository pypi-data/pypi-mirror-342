import os
import typer
import json
from rich import print_json # 예쁜 JSON 출력을 위해 rich 사용

# 필요한 클래스 임포트
from kiwoom_rest_api.koreanstock.stockinfo import StockInfo
from kiwoom_rest_api.auth.token import TokenManager
from kiwoom_rest_api.core.base import APIError # APIError 위치 확인 필요

# Typer 앱 인스턴스 생성
app = typer.Typer()

# --- 환경 변수 또는 옵션으로 API 키/시크릿 가져오기 ---
# 사용자는 환경 변수(KIWOOM_API_KEY, KIWOOM_API_SECRET)를 설정하거나
# CLI 옵션 (--api-key, --api-secret)을 사용해야 합니다.

@app.command()
def ka10001(
    stock_code: str = typer.Argument(..., help="조회할 주식 종목 코드 (예: 005930)"),
    api_key: str = typer.Option(
        None, "--api-key", "-k",
        help="키움증권 API Key (환경 변수 KIWOOM_API_KEY로 설정 가능)",
        envvar="KIWOOM_API_KEY",
        show_envvar=True, # 도움말에 환경 변수 이름 표시
    ),
    api_secret: str = typer.Option(
        None, "--api-secret", "-s",
        help="키움증권 API Secret (환경 변수 KIWOOM_API_SECRET로 설정 가능)",
        envvar="KIWOOM_API_SECRET",
        show_envvar=True,
    ),
    base_url: str = typer.Option(
        "https://openapi.kiwoom.com", # 올바른 Open API URL 사용
        "--base-url", "-u",
        help="API 기본 URL"
    ),
):
    """
    주식 기본 정보 요청 (KA10001) API를 호출합니다.
    """
    # API 키/시크릿 확인
    if not api_key:
        typer.echo("오류: API Key가 제공되지 않았습니다. --api-key 옵션 또는 KIWOOM_API_KEY 환경 변수를 사용하세요.", err=True)
        raise typer.Exit(code=1)
    if not api_secret:
        typer.echo("오류: API Secret이 제공되지 않았습니다. --api-secret 옵션 또는 KIWOOM_API_SECRET 환경 변수를 사용하세요.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"종목 코드 {stock_code}에 대한 기본 정보 요청 시작...")
    typer.echo(f"사용 API URL: {base_url}")

    try:
        # TokenManager 초기화 (가져온 키/시크릿 사용)
        # base_url은 TokenManager가 내부 config에서 가져올 수도 있음
        token_manager = TokenManager(api_key=api_key, api_secret=api_secret)

        # StockInfo 인스턴스 생성 (동기 방식)
        stock_info = StockInfo(base_url=base_url, token_manager=token_manager, use_async=False)

        # API 호출
        result = stock_info.basic_stock_information_request_ka10001(stock_code)

        typer.echo("\n--- API 응답 ---")
        # 결과를 예쁘게 JSON 형식으로 출력
        print_json(data=result)
        typer.echo("----------------")

    except APIError as e:
        typer.echo(f"\nAPI 오류 발생 (HTTP {e.status_code}): {e.message}", err=True)
        if e.error_data:
            typer.echo("오류 데이터:", err=True)
            print_json(data=e.error_data)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"\n예상치 못한 오류 발생: {type(e).__name__}", err=True)
        typer.echo(f"오류 메시지: {e}", err=True)
        raise typer.Exit(code=1)

# 다른 API 호출을 위한 명령어를 여기에 추가할 수 있습니다.
# 예: @app.command() def another_api(...): ...

if __name__ == "__main__":
    app()
