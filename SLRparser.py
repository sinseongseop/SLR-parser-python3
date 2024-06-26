import sys
from treelib import Node, Tree

# Nonterminal과 Terminal 값을 가지는 클래스
class nodeValue(object): 
    def __init__(self, value): 
        self.value = value

# Terminal/Non-terminal을 index랑 매칭 (딕션너리 이용)
SLRIndex = {
    'vtype': 0, 'id': 1, 'semi': 2, 'assign': 3, 'literal': 4, 'character': 5, 'boolstr': 6, 'addsub': 7, 
    'multdiv': 8, 'lparen': 9, 'rparen': 10, 'num': 11, 'lbrace': 12, 'rbrace': 13, 'comma': 14, 'if': 15, 
    'while': 16, 'comp': 17, 'else': 18, 'return': 19, '$': 20, 'CODE': 21, 'VDECL': 22, 'ASSIGN': 23, 
    'RHS': 24, 'EXPR': 25, 'T': 26, 'F': 27, 'FDECL': 28, 'ARG': 29, 'MOREARGS': 30, 'BLOCK': 31, 
    'STMT': 32, 'COND': 33, 'Q': 34, 'ELSE': 35, 'RETURN': 36
}

# CFG info
#CFG=[['E','T * E', 3],[],[],[],[],[],[]] # 0: E -> T * E 인 경우 왼쪽과 같이 저장 (LHS , RHS, RHS의 길이) 형식
CFG = [
    ['S', 'CODE', 1],               # 0 S -> CODE
    ['CODE', 'VDECL CODE', 2],      # 1 CODE -> VDECL CODE
    ['CODE', 'FDECL CODE', 2],      # 2 CODE -> FDECL CODE
    ['CODE', '', 0],               # 3 CODE -> ''
    ['VDECL', 'vtype id semi', 3],  # 4 VDECL -> vtype id semi
    ['VDECL', 'vtype ASSIGN semi', 3],  # 5 VDECL -> vtype ASSIGN semi
    ['ASSIGN', 'id assign RHS', 3],    # 6 ASSIGN -> id assign RHS
    ['RHS', 'EXPR', 1],             # 7 RHS -> EXPR
    ['RHS', 'literal', 1],          # 8 RHS -> literal
    ['RHS', 'character', 1],        # 9 RHS -> character
    ['RHS', 'boolstr', 1],          # 10 RHS -> boolstr
    ['EXPR', 'T addsub EXPR', 3],   # 11 EXPR -> T addsub EXPR
    ['EXPR', 'T', 1],               # 12 EXPR -> T
    ['T', 'F multdiv T', 3],        # 13 T -> F multdiv T
    ['T', 'F', 1],                  # 14 T -> F
    ['F', 'lparen EXPR rparen', 3], # 15 F -> lparen EXPR rparen
    ['F', 'id', 1],                 # 16 F -> id
    ['F', 'num', 1],                # 17 F -> num
    ['FDECL', 'vtype id lparen ARG rparen lbrace BLOCK RETURN rbrace', 9],  # 18 FDECL -> vtype id lparen ARG rparen lbrace BLOCK RETURN rbrace
    ['ARG', 'vtype id MOREARGS', 3],   # 19 ARG -> vtype id MOREARGS
    ['ARG', '', 0],                # 20 ARG -> ''
    ['MOREARGS', 'comma vtype id MOREARGS', 4],  # 21 MOREARGS -> comma vtype id MOREARGS
    ['MOREARGS', '', 0],           # 22 MOREARGS -> ''
    ['BLOCK', 'STMT BLOCK', 2],     # 23 BLOCK -> STMT BLOCK
    ['BLOCK', '', 0],              # 24 BLOCK -> ''
    ['STMT', 'VDECL', 1],           # 25 STMT -> VDECL
    ['STMT', 'ASSIGN semi', 2],     # 26 STMT -> ASSIGN semi
    ['STMT', 'if lparen COND rparen lbrace BLOCK rbrace ELSE', 8],   # 27 STMT -> if lparen COND rparen lbrace BLOCK rbrace ELSE
    ['STMT', 'while lparen COND rparen lbrace BLOCK rbrace', 7],    # 28 STMT -> while lparen COND rparen lbrace BLOCK rbrace
    ['COND', 'Q comp COND', 3],    # 29 COND -> Q comp COND
    ['Q', 'boolstr', 1],           # 30 Q -> boolstr
    ['COND', 'Q', 1],              # 31 COND -> Q
    ['ELSE', 'else lbrace BLOCK rbrace', 4],  # 32 ELSE -> else lbrace BLOCK rbrace
    ['ELSE', '', 0],               # 33 ELSE -> ''
    ['RETURN', 'return RHS semi', 3]  # 34 RETURN -> return RHS semi
]

# SLR Table 저장
def parse_cell(cell):
    if cell == '0':
        return []
    elif cell.startswith('s'):
        return ['S', int(cell[1:])]
    elif cell.startswith('r'):
        return ['R', int(cell[1:])]
    elif cell.isdigit():
        return ['G', int(cell)]
    elif cell == 'acc':
        return ['A', 0]
    else:
        return []

def read_txt_to_SLRTable(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    SLRTable = []
    for line in lines:
        row = line.strip().split('\t')
        parsed_row = [parse_cell(cell) for cell in row]
        SLRTable.append(parsed_row)
    
    return SLRTable

# 예제 파일을 읽어서 SLRTable로 변환
filename = 'SLR_table.txt'
SLRTable = read_txt_to_SLRTable(filename)

#SLR parser 함수 구현
def parser(tokens):
    print("SLRpasrser 함수")
    
    parseTree=Tree() #parser Tree
    parseTree.create_node("root",'root',data=nodeValue("dummy-rootNode"))
    parserStack =[] # 파싱용 스택
    tokenPointer= 0 # 몇번째 Token을 가리키는 중인가  
    nodeId=0; # 각 노드의 고유 번호
    
    parserStack.append(0) # 스택에 START STATE 초기화

    # leftSubstring값 저장
    leftSubstring = []
 
    # Step1의 stack, input출력
    cnt = 1
    print("Step", cnt)
    cnt+=1
    print("Stack : [ ", parserStack[0], " ]")
    print("Input : ", tokens)

    while(True):
        state = parserStack[-1]      # 제일 위에 있는 노드 엿보기    
        token = tokens[tokenPointer]  # 포인터가 가리키는 토큰의 종류
        tokenIndex = SLRIndex[token] 

        # error확인 - SLR_table에 state, tokenIndex에 해당하는 시행값 없으면 오류
        if(SLRTable[state][tokenIndex] == []):
            print()
            print("error!")
            print("Step", cnt - 1, "에서 current state가 ", state, "이고 next input symbol이", token, "일 때 해당하는 SLR테이블 값이 존재하지 않음\n")
            print("error 발생 전 까지 형성된 파싱 트리\n")
            treeBytes = parseTree.show(stdout=False,data_property="value") 
            treeDraw = treeBytes.encode('utf-8').decode('utf-8')
            print(treeDraw)  # 트리 출력
            exit()
        
        [instruction , num] = SLRTable[state][tokenIndex] # state 값과 현재 Pointer가 가리키는 Token을 통해 SLR 파싱테이블의 값 가져오기

        if( instruction == 'S' ): # Shift 인 경우
            nextState = num
            newNode = parseTree.create_node(1,nodeId,parent='root',data=nodeValue(token))  # 노드 하나 만들어서 Terminal 값 저장 
            parserStack.append(newNode) # 노드 스택에 추가
            parserStack.append(nextState) # 다음 state 스택에 추가
            nodeId+=1 
            tokenPointer+=1

            # Shift step 출력
            print("Action :", "Shift", num, "시행")
            print()
            print("Step", cnt)
            # parserStack에서 state값만 출력
            print("Stack : [  ", end = "")
            for i in parserStack:
                if(type(i) == Node):
                    continue
                print(i, " ", end = "")
            print("]")
            # leftSubstring 저장
            leftSubstring.append(tokens[tokenPointer - 1])
            # parsing과정 중 input값 출력
            print("Input : ", leftSubstring, " | ", tokens[tokenPointer:])
            cnt+=1
            
        elif(instruction =="R"): # Reduce 인 경우
            childNodes=[] 
            
            for _ in range( CFG[num][2] ): # RHS의 길이 만큼 스택에서 states 팝하기.
                parserStack.pop() #state
                childNodes.append(parserStack.pop()) #Node  
                
            state = parserStack[-1] # 스택의 맨 위 state 값 엿보기
            
            nonTerminal = CFG[num][0] # A -> alpha인 production에서 nonTerminal인 A추출
            nonTermIndex = SLRIndex[nonTerminal]
            [instruction , nextState] = SLRTable[state][nonTermIndex] # <- Goto 시행
            newNode = parseTree.create_node(1, nodeId ,parent='root',data=nodeValue(nonTerminal))  # 노드 하나 만들어서 nonTerminal 값 저장 
            
            for childNode in reversed(childNodes):
                childId = childNode.identifier
                parseTree.move_node(childId, nodeId) # 부모 자식간의 트리 형성

            # Reduce step 출력
            print("Action :", "Reduce(", num, ") 시행")
            print()
            print("Step", cnt)
            # parserStack에서 state값만 출력
            print("Stack : [  ", end = "")
            for i in parserStack:
                if(type(i) == Node):
                    continue
                print(i, " ", end = "")
            print("]")
            cnt+=1
            # leftSubstring에 Reduce시행 과정 반영
            for _ in range( CFG[num][2] ): # RHS의 길이 만큼 leftSubstring에서  팝하기.
                leftSubstring.pop() #state
            leftSubstring.append(nonTerminal)
            # parsing과정 중 input값 출력
            print("Input : ", leftSubstring, " | ", tokens[tokenPointer:])

            parserStack.append(newNode) # 노드 스택에 추가
            parserStack.append(nextState) # 다음 state 스택에 추가 <- Goto 시행한 결과 stack에 추가
            nodeId+=1   

            # Goto step 출력
            print("Action :", "Goto", nextState, " 시행")
            print()
            print("Step", cnt)
            # parserStack에서 state값만 출력
            print("Stack : [  ", end = "")
            for i in parserStack:
                if(type(i) == Node):
                    continue
                print(i, " ", end = "")
            print("]")
            cnt+=1
            # parsing과정 중 input값 출력
            print("Input : ", leftSubstring, " | ", tokens[tokenPointer:])
            
        elif(instruction == "A"): #Accept 인 경우
            print("Action :", "acc 시행\n")
            print("parsing 성공!\n")
            print("형성된 parse Tree \n")
            tree=parseTree.subtree(nodeId-1) # 불필요한 루트 노드 제거
            treeBytes = tree.show(stdout=False,data_property="value") 
            treeDraw = treeBytes.encode('utf-8').decode('utf-8')
            print(treeDraw)  # 트리 출력         
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
#print(tokens) # 디버깅 확인용

parser(tokens) # SLRparser 수행