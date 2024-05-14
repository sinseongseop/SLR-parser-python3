import sys
from treelib import Node


# Terminal/Non-terminal을 index랑 매칭 (딕션너리 이용)
SLRIndex={'vtype':0 ,'num':1 , 'character': 2 , 'CODE': 21} # SLR Table column 값에 맞추어 수정 


# CFG info
CFG=[['E','T * E', 3],[],[],[],[],[],[]] # 0: E -> T * E 인 경우 왼쪽과 같이 저장 (LHS , RHS, RHS의 길이) 형식


# SLR Table 영역
SLRTable=[[[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]],
          [[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]],
          [[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]],
          [[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]],
          [[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]],
          [[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]]
          ]

#에러 처리 정보 영역
Error = [[],[],[],[]] # Error 어떻게 할지 생각 해보기 


#SLR parser 함수 구현
def parser(tokens):
    print("SLRpasrser 함수")
       
    parserStack =[] # 파싱용 스택
    pointer= 0 # 몇번째 Token을 가리키는 중인가
    
                # 스택에 START STAE 초기화
    while(True):
                # 제일 위에 있는 노드 엿보기
                # 제일 위에 있는 노드의 state 값과 현재 Pointer가 가리키는 Token을 통해 SLR 파싱테이블의 값 가져오기 
                

        # 0번째 인덱스 비교
        if(SLRTable =="S"): # Shift 인 경우
                # 노드 하나 만들어서 state 값과 Terminal 값 저장 (tree.create_node() 이용)
                # 위의 노드 스택에 추가
                # pointer 1 증가
            pass
        elif(SLRTable =="R"): # Reduce 인 경우
                # CFG 3번쨰 정보 이용해 길이 만큼 팝하기.
                # Goto 테이블에 있는 state 값과 NonTerminal 값을 가지는 새로운 노드 만들기
                # 새로만든 노드를 부모로 해서 위에서 팝한 노드를 부모자식 관계 만들어 주기 ( tree.move_node() 이용)
                # 새로 만든 노드 스택에 푸쉬 
            pass
        elif(SLRTable == "A"): #Accept 인 경우
                                #Tree 정보 보여주기. (tree.show() 이용)
            pass                
            break
        else: # Error 인경우
            pass
            break


# main() 프로그램 시작
if( len(sys.argv)==1 ): #파일 입력이 안 주어진 경우
    fileName=input("사용할 파일의 이름을 입력하세요:")
else:
    fileName=sys.argv[1] #command line parameter로 입력된 파일 이름 1개

file=open(fileName,"r",encoding="UTF8")

code=file.read() # 파일에서 적혀 있는 모든 내용을 읽어옴.
tokens=code.split() # token 분리
print(tokens) # 디버깅 확인용
parser(tokens) # SLRparser 수행
