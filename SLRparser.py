import sys
from treelib import Node, Tree

# Nonterminal과 Terminal 값을 가지는 클래스
class nodeValue(object): 
    def __init__(self, value): 
        self.value = value

# Terminal/Non-terminal을 index랑 매칭 (딕션너리 이용)
#SLRIndex={'vtype':0 ,'num':1 , 'character': 2 , 'CODE': 21} # SLR Table column 값에 맞추어 수정 
SLRIndex={'*': 0 , '(':1, ')':2, 'id': 3, '$': 4 , 'E':5, 'T':6}

# CFG info
#CFG=[['E','T * E', 3],[],[],[],[],[],[]] # 0: E -> T * E 인 경우 왼쪽과 같이 저장 (LHS , RHS, RHS의 길이) 형식

CFG=[["S'",'E',1],['E','T * E',3],['E','T',1],['T','(E)',3],['T','id',1]]

# SLR Table 영역
#SLRTable=[[[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]],
#          [[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]],
#          [[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]],
#         [[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]],
#          [[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]],
#          [[]],[[]],[[]],[[]],[[]],[[]],[[]],[[]]
#          ]

SLRTable=[[[],['S',3],[],['S',4],[],['G',1],['G',2]],
           [[],[],[],[],['A',0],[],[]],
           [['S',5],[],['R',2],[],['R',2],[],[]],
           [[],['S',3],[],['S',4],[],['G',6],['G',2]],
           [['R',4],[],['R',4],[],['R',4],[],[]],
           [[],['S',3],[],['S',4],[],['G',7],['G',2]],
           [[],[],['S',8],[],[],[],[]],
           [[],[],['R',1],[],['R',1],[],[]],
           [['R',3],[],['R',3],[],['R',3],[],[]]]

#에러 처리 정보 영역
Error = [[],[],[],[]] # Error 어떻게 할지 생각 해보기 


#SLR parser 함수 구현
def parser(tokens):
    print("SLRpasrser 함수")
    
    parseTree=Tree() #parser Tree
    parseTree.create_node("root",'root',data=nodeValue("rootNode"))
    parserStack =[] # 파싱용 스택
    tokenPointer= 0 # 몇번째 Token을 가리키는 중인가  
    nodeId=0; # 각 노드의 고유 번호
    
    parserStack.append(0) # 스택에 START STAE 초기화
 
    while(True):
        state = parserStack[-1]      # 제일 위에 있는 노드 엿보기
        
        token = tokens[tokenPointer]  # 포인터가 가리키는 토큰의 종류
        tokenIndex = SLRIndex[token] 
        [instruction , num] = SLRTable[state][tokenIndex] # state 값과 현재 Pointer가 가리키는 Token을 통해 SLR 파싱테이블의 값 가져오기 

        if( instruction == 'S' ): # Shift 인 경우
            nextState = num
            newNode = parseTree.create_node(1,nodeId,parent='root',data=nodeValue(token))  # 노드 하나 만들어서 Terminal 값 저장 
            parserStack.append(newNode) # 노드 스택에 추가
            parserStack.append(nextState) # 다음 state 스택에 추가
            nodeId+=1 
            tokenPointer+=1
            
        elif(instruction =="R"): # Reduce 인 경우
            childNodes=[] 
            
            for _ in range( CFG[num][2] ): # RHS의 길이 만큼 팝하기.
                parserStack.pop() #state
                childNodes.append(parserStack.pop()) #Node  
                
            state = parserStack[-1] # 스택의 맨 위 state 값 엿보기
            
            nonTerminal = CFG[num][0]
            nonTermIndex = SLRIndex[nonTerminal]
            [instruction , nextState] = SLRTable[state][nonTermIndex]
            newNode = parseTree.create_node(1, nodeId ,parent='root',data=nodeValue(nonTerminal))  # 노드 하나 만들어서 nonTerminal 값 저장 
            
            for childNode in reversed(childNodes):
                childId = childNode.identifier
                parseTree.move_node(childId, nodeId) # 부모 자식간의 트리 형성
            
            parserStack.append(newNode) # 노드 스택에 추가
            parserStack.append(nextState) # 다음 state 스택에 추가 
            nodeId+=1   
            
        elif(instruction == "A"): #Accept 인 경우
            print("parsing 성공!")
            tree=parseTree.subtree(nodeId-1) # 불필요한 루트 노드 제거
            treeBytes = tree.show(stdout=False,data_property="value") 
            treeDraw = treeBytes.encode('utf-8').decode('utf-8')
            print(treeDraw)  # 트리 출력         
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
tokens.append('$') # EndMarker($) 추가
print(tokens) # 디버깅 확인용

parser(tokens) # SLRparser 수행
