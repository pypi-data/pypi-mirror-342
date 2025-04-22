import sys

from arxiv_mcp.app import mcp

from arxiv_mcp.resources import resources
from arxiv_mcp.tools import tools
from arxiv_mcp.prompts import prompts

def main():

    print("서버 시작 전...", file=sys.stderr) 

    port_to_use = 8000 
    print(f"서버를 포트 {port_to_use}에서 실행합니다.", file=sys.stderr)
    
    mcp.run()
    
    print("서버 종료됨.", file=sys.stderr)

if __name__ == "__main__":
    main() 