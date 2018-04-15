from __future__ import print_function
import copy
import random
import datetime

MAX = 1e10
class Team43:

    def __init__(self):
        self.termVal = MAX
        self.limit = 5
        self.count = 0
        self.gameweight = [[6,4,4,6],[4,3,3,4],[4,3,3,4],[6,4,4,6]]
        self.weight = [[2,3,3,2],[3,4,4,3],[3,4,4,3],[2,3,3,2]]
        self.trans = {}
        self.timeLimit = datetime.timedelta(seconds = 15)
        self.begin = MAX
        self.limitReach = 0


    def ifwin(self,board,x,y,mark,anti_mark):

        scorewin=MAX/20

        for i in xrange(4):
            if (board.board_status[4*x+i][4*y]==mark):
                if (board.board_status[4*x+i][4*y+1]==mark):
                    if (board.board_status[4*x+i][4*y+2]==mark):
                        if (board.board_status[4*x+i][4*y+3]==mark):
                            return (scorewin)

        # Vertical win
        for i in xrange(4):
            if (board.board_status[4*x][4*y+i]==mark):
                if (board.board_status[4*x+1][4*y+i]==mark):
                    if (board.board_status[4*x+2][4*y+i]==mark):
                        if (board.board_status[4*x+3][4*y+i]==mark):
                            return (scorewin)
        # Diamond win
        for i in xrange(2):
            for j in xrange(2):
                if (board.board_status[4*x+i][4*y+j+1]==mark):
                    if (board.board_status[4*x+i+1][4*y+j+2]==mark):
                        if (board.board_status[4*x+i+2][4*y+j+1]==mark):
                            if( board.board_status[4*x+i+1][4*y+j]==mark):
                                return (scorewin)
        return 0

    def block_ev(self,board,x,y,mark,anti_mark):

        score=self.ifwin(board,x,y,mark,anti_mark)
        if (score != 0):
            return score

        hor_table=[[0.5 for i in range(4)]for j in range (4)]
        for i in range(4):
            temp=0
            product=1
            weigh=0
            for j in range(4):
                if board.board_status[4*x + i][4*y + j]==mark:
                    temp=temp+1
                    hor_table[i][j]=temp
                elif board.board_status[4*x + i][4*y + j]==anti_mark:
                    temp=0
                    hor_table[i][j]=temp
                product=product*hor_table[i][j]
                weigh+=self.weight[i][j]
            score+=product*weigh

        ver_table=[[0.5 for i in range(4)]for j in range (4)]
        for j in range(4):
            temp=0
            product=1
            weigh=0
            for i in range(4):
                if board.board_status[4*x + i][4*y + j]==mark:
                    temp=temp+1
                    ver_table[i][j]=temp
                elif board.board_status[4*x + i][4*y + j]==anti_mark:
                    temp=0
                    ver_table[i][j]=temp
                product=product*hor_table[i][j]
                weigh+=self.weight[i][j]
            score+=product*weigh
        
        ldi_table=[[0.5 for i in range(4)]for j in range (4)]
        for i in range(2):
            j=1
            temp=0
            product=1
            weigh=0
            for k in range(2):
                if board.board_status[4*x + i+k][4*y + j+k]==mark:
                    temp=temp+1
                    ldi_table[i+k][j+k]=temp
                elif board.board_status[4*x + i+k][4*y + j+k]==anti_mark:
                    temp=0
                    ldi_table[i+k][j+k]=temp
                product=product*ldi_table[i+k][j+k]
                weigh+=self.weight[i+k][j+k]
            offi=i+1;
            offj=j-1;
            for k in range(2):
                if board.board_status[4*x + offi+k][4*y + offj+k]==mark:
                    ldi_table[offi+k][offj+k]=temp+1
                    temp=temp+1
                elif board.board_status[4*x + offi+k][4*y + offj+k]==anti_mark:
                    temp=0
                    ldi_table[offi+k][offj+k]=temp

                product=product*ldi_table[offi+k][offj+k]
                weigh+=self.weight[offi+k][offj+k]
            score+=product*weigh

        rdi_table=[[0.5 for i in range(4)]for j in range (4)]
        for i in range(2):
            j=2
            temp=0
            product=1
            weigh=0
            for k in range(2):
                if board.board_status[4*x + i+k][4*y + j+k]==mark:
                    temp=temp+1
                    rdi_table[i+k][j+k]=temp
                elif board.board_status[4*x + i+k][4*y + j+k]==anti_mark:
                    temp=0
                    rdi_table[i+k][j+k]=temp
                product=product*rdi_table[i+k][j+k]
                weigh+=self.weight[i+k][j+k]
            offi=i+1;
            offj=j-1;
            for k in range(2):
                if board.board_status[4*x + offi+k][4*y + offj+k]==mark:
                    rdi_table[offi+k][offj+k]=temp+1
                    temp=temp+1
                elif board.board_status[4*x + offi+k][4*y + offj+k]==anti_mark:
                    temp=0
                    rdi_table[offi+k][offj+k]=temp

                product=product*rdi_table[offi+k][offj+k]
                weigh+=self.weight[offi+k][offj+k]
            score+=product*weigh

        # for i in range(4):
        #   for j in range(4):
        #       print board[4*x + i][4*y + j],
        #   print
        # print

        return score

    def game_ev(self,board,tmpBlock,mark,anti_mark):
        score=0
        scorewin=MAX*10
        for i in xrange(4):
            if (board.block_status[i][0]==mark):
                if (board.block_status[i][1]==mark):
                    if (board.block_status[i][2]==mark):
                        if (board.block_status[i][3]==mark):
                            return (scorewin)

        # Vertical win
        for i in xrange(4):
            if (board.block_status[0][i]==mark):
                if (board.block_status[1][i]==mark):
                    if (board.block_status[2][i]==mark):
                        if (board.block_status[3][i]==mark):
                            return (scorewin)
        # Diamond win
        for i in xrange(2):
            for j in xrange(2):
                if (board.block_status[i][j+1]==mark):
                    if (board.block_status[i+1][j+2]==mark):
                        if (board.block_status[i+2][j+1]==mark):
                            if( board.block_status[i+1][j]==mark):
                                return (scorewin)
        x=0
        y=0
        hor_table=[[0.5 for i in range(4)]for j in range (4)]
        for i in range(4):
            temp=0
            product=1
            weigh=0
            for j in range(4):
                if board.block_status[i][j]==mark:
                    temp=temp+1
                    hor_table[i][j]=temp
                elif board.block_status[4*x + i][4*y + j]==anti_mark:
                    temp=0
                    hor_table[i][j]=temp
                product=product*hor_table[i][j]
                weigh+=self.gameweight[i][j]
            score+=product*weigh

        ver_table=[[0.5 for i in range(4)]for j in range (4)]
        for j in range(4):
            temp=0
            product=1
            weigh=0
            for i in range(4):
                if board.block_status[4*x + i][4*y + j]==mark:
                    temp=temp+1
                    ver_table[i][j]=temp
                elif board.block_status[4*x + i][4*y + j]==anti_mark:
                    temp=0
                    ver_table[i][j]=temp
                product=product*hor_table[i][j]
                weigh+=self.gameweight[i][j]
            score+=product*weigh
        
        ldi_table=[[0.5 for i in range(4)]for j in range (4)]
        for i in range(2):
            j=1
            temp=0
            product=1
            weigh=0
            for k in range(2):
                if board.block_status[4*x + i+k][4*y + j+k]==mark:
                    temp=temp+1
                    ldi_table[i+k][j+k]=temp
                elif board.block_status[4*x + i+k][4*y + j+k]==anti_mark:
                    temp=0
                    ldi_table[i+k][j+k]=temp
                product=product*ldi_table[i+k][j+k]
                weigh+=self.gameweight[i+k][j+k]
            offi=i+1;
            offj=j-1;
            for k in range(2):
                if board.block_status[4*x + offi+k][4*y + offj+k]==mark:
                    ldi_table[offi+k][offj+k]=temp+1
                    temp=temp+1
                elif board.block_status[4*x + offi+k][4*y + offj+k]==anti_mark:
                    temp=0
                    ldi_table[offi+k][offj+k]=temp

                product=product*ldi_table[offi+k][offj+k]
                weigh+=self.gameweight[offi+k][offj+k]
            score+=product*weigh

        rdi_table=[[0.5 for i in range(4)]for j in range (4)]
        for i in range(2):
            j=2
            temp=0
            product=1
            weigh=0
            for k in range(2):
                if board.block_status[4*x + i+k][4*y + j+k]==mark:
                    temp=temp+1
                    rdi_table[i+k][j+k]=temp
                elif board.block_status[4*x + i+k][4*y + j+k]==anti_mark:
                    temp=0
                    rdi_table[i+k][j+k]=temp
                product=product*rdi_table[i+k][j+k]
                weigh+=self.gameweight[i+k][j+k]
            offi=i+1;
            offj=j-1;
            for k in range(2):
                if board.block_status[4*x + offi+k][4*y + offj+k]==mark:
                    rdi_table[offi+k][offj+k]=temp+1
                    temp=temp+1
                elif board.block_status[4*x + offi+k][4*y + offj+k]==anti_mark:
                    temp=0
                    rdi_table[offi+k][offj+k]=temp

                product=product*rdi_table[offi+k][offj+k]
                weigh+=self.gameweight[offi+k][offj+k]
            score+=product*weigh

        return score*100

    def heuristic(self, board,mark,anti_mark):
        tmpBlock = copy.deepcopy(board.block_status)
        final = 0
        for i in xrange(4):
            for j in xrange(4):
                blvalue = self.block_ev(board,i,j,mark,anti_mark)
                # print(aaja,i,j)
                final += blvalue

        final += self.game_ev(board,tmpBlock,mark,anti_mark)
        #final+=random.randint(500,1000)
        del(tmpBlock)
        return final

    def alphaBeta(self, board, old_move, flag, depth, alpha, beta, cntwin):
        # Taking 'x' as the maximising player
        # nodeval[0]=heurestic value of the node/board state , nodeval[1]=chosen position of the marker

        # CACHING
        hashval = hash(str(board.board_status))
        if(self.trans.has_key(hashval)):
            # print("hash exists")
            bounds = self.trans[hashval]
            if(bounds[0] >= beta):
                return bounds[0],old_move
            if(bounds[1] <= alpha):
                return bounds[1],old_move
            # print("also returning")
            alpha = max(alpha,bounds[0])
            beta = min(beta,bounds[1])

        cells = board.find_valid_move_cells(old_move)
        random.shuffle(cells)

        if (flag == 'x'):
            nodeVal = -MAX, cells[0]
            tmp = copy.deepcopy(board.block_status)
            a = alpha

            for chosen in cells :
                if datetime.datetime.utcnow() - self.begin >= self.timeLimit :
                    # print("breaking at depth ",depth)
                    self.limitReach = 1
                    break
                board.update(old_move, chosen, flag)
                # print("chosen ",chosen)
                if (board.find_terminal_state()[0] == 'o'):
                	# O WINS THE BOARD
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    board.block_status = copy.deepcopy(tmp)
                    continue
                elif (board.find_terminal_state()[0] == 'x'):
                    # X WINS THE BOARD
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    board.block_status = copy.deepcopy(tmp)
                    nodeVal = self.termVal,chosen
                    break
                elif(board.find_terminal_state()[0] == 'NONE'):
                	# DRAW OF THE FINAL BOARD
                    x = 0
                    d = 0
                    o = 0
                    tmp1 = 0
                    for i2 in xrange(4):
                        for j2 in xrange(4):
                            if(board.block_status[i2][j2] == 'x'):
                                x += 1*(self.gameweight[i2][j2])
                            if(board.block_status[i2][j2] == 'o'):
                                o += 1*(self.gameweight[i2][j2])
                            if(board.block_status[i2][j2] == 'd'):
                                d += 1
                    if(x==o):
                        tmp1 = 0
                    elif(x>o):
                        tmp1 = MAX/4 + 80*(x-o)
                    else:
                        tmp1 = -MAX/4 - 80*(o-x)
                    # print(tmp1)
                elif( depth >= self.limit):
                    tmp1 = self.heuristic(board,'x','o')
                    # print("Heuristic value for ",chosen," is ",tmp1)
                else:
                    checkwin=self.ifwin(board,chosen[0]/4,chosen[1]/4,'x','o')
                    if (checkwin==MAX/20 and cntwin==0):
                        # print ('depth is ',depth,' and pos is ',chosen[0],' ',chosen[1],' for ',flag)
                        tmp1 = self.alphaBeta(board, chosen, 'x', depth+1, a, beta,1)[0]
                    else:
                    	# block win on bonus move
                        tmp1 = self.alphaBeta(board, chosen, 'o', depth+1, a, beta,0)[0]

                board.board_status[chosen[0]][chosen[1]] = '-'
                board.block_status = copy.deepcopy(tmp)
                if(nodeVal[0] < tmp1):
                    nodeVal = tmp1,chosen
                # print("The nodeval is ",nodeVal)
                a = max(a, tmp1)
                if beta <= nodeVal[0] :
                    break
            del(tmp)

        if (flag == 'o'):
            nodeVal = MAX, cells[0]
            tmp = copy.deepcopy(board.block_status)
            b = beta

            for chosen in cells :
                if datetime.datetime.utcnow() - self.begin >= self.timeLimit :
                    # print("breaking")
                    self.limitReach = 1
                    break
                board.update(old_move, chosen, flag)

                if(board.find_terminal_state()[0] == 'o'):
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    board.block_status = copy.deepcopy(tmp)
                    nodeVal = -1*self.termVal,chosen
                    break
                elif(board.find_terminal_state()[0] == 'x'):
                    board.board_status[chosen[0]][chosen[1]] = '-'
                    board.block_status = copy.deepcopy(tmp)
                    continue
                elif(board.find_terminal_state()[0] == 'NONE'):
                    x = 0
                    d = 0
                    o = 0
                    tmp1 = 0

                    for i2 in range(4):
                        for j2 in range(4):
                            if board.block_status[i2][j2] == 'x':
                                x += 1*(self.gameweight[i2][j2])
                            if board.block_status[i2][j2] == 'o':
                                o += 1*(self.gameweight[i2][j2])
                            if board.block_status[i2][j2] == 'd':
                                d += 1
                    if(x==o):
                        tmp1 = 0
                    elif(x>o):
                        tmp1 = MAX/4 + 80*(x-o)
                    else:
                        tmp1 = -MAX/4 - 80*(o-x)

                elif(depth >= self.limit):
                    tmp1 = -1*self.heuristic(board,'o','x')
                else:
                    checkwin=-self.ifwin(board,chosen[0]/4,chosen[1]/4,'o','x')
                    if (checkwin==-MAX/20 and cntwin==0):
                        # print ('depth is ',depth,' and pos is ',chosen[0],' ',chosen[1],' for ',flag)
                        tmp1 = self.alphaBeta(board, chosen, 'o', depth+1, alpha, b,1)[0]
                    else:
                        # block win on bonus move
                        tmp1 = self.alphaBeta(board, chosen, 'x', depth+1, alpha, b,0)[0]

                board.board_status[chosen[0]][chosen[1]] = '-'
                board.block_status = copy.deepcopy(tmp)
                if(nodeVal[0] > tmp1):
                    nodeVal = tmp1,chosen
                b = min(b, tmp1)
                if alpha >= nodeVal[0] :
                    break
            del(tmp)

        # print("return value is ",nodeVal)
        if(nodeVal[0] <= alpha):
            self.trans[hashval] = [-MAX,nodeVal[0]]
        if(nodeVal[0] > alpha and nodeVal[0] < beta):
            self.trans[hashval] = [nodeVal[0],nodeVal[0]]
        if(nodeVal[0]>=beta):
            self.trans[hashval] = [nodeVal[0],MAX]
        # print(self.trans.items())
        return nodeVal

    def opp_win(self,board,move,mark,anti_mark):
        score=0
        x=move[0]%4
        y=move[1]%4
        for i in xrange(4):
            temp=0
            for j in range(4):
                if (board.board_status[4*x+i][4*y+j]==anti_mark):
                    temp=temp+10
                elif(board.board_status[4*x+i][4*y+j]==mark):
                    temp=temp-20
            score=max(temp,score)
        # Vertical win
        for j in xrange(4):
            temp=0
            for i in range(4):
                if (board.board_status[4*x+i][4*y+j]==anti_mark):
                    temp=temp+10
                elif(board.board_status[4*x+i][4*y+j]==mark):
                    temp=temp-20
            score=max(temp,score)
        # Diamond win

        for i in xrange(2):
            temp=0
            for j in xrange(2):
                if (board.board_status[4*x+i][4*y+j+1]==anti_mark):
                    temp=temp+10
                elif (board.board_status[4*x+i][4*y+j+1]==mark):
                    temp=temp-20
                if (board.board_status[4*x+i+1][4*y+j+2]==anti_mark):
                    temp=temp+10
                elif (board.board_status[4*x+i+1][4*y+j+2]==mark):
                    temp=temp-20
                if (board.board_status[4*x+i+2][4*y+j+1]==anti_mark):
                    temp=temp+10
                elif (board.board_status[4*x+i+2][4*y+j+1]==mark):
                    temp=temp-20
                if( board.board_status[4*x+i+1][4*y+j]==anti_mark):
                    temp=temp+10
                elif( board.board_status[4*x+i+1][4*y+j]==mark):
                    temp=temp-20
            score=max(temp,score)
        
        return score

    def check(self,board,old_move,mymove,mark,anti_mark):
        points=0
        minp=1000000

        board.update(old_move, mymove, mark)
        if(self.ifwin(board,old_move[0]%4,old_move[1]%4,mark,anti_mark) ==MAX/20):
            board.board_status[mymove[0]][mymove[1]]='-'
            board.block_status[mymove[0]/4][mymove[1]/4]='-'
            return mymove
        board.board_status[mymove[0]][mymove[1]]='-'
        board.block_status[mymove[0]/4][mymove[1]/4]='-'

        points=self.opp_win(board,mymove,mark,anti_mark)
        if(points < 30):
            return mymove

        cells=board.find_valid_move_cells(old_move) 
        #print (cells)
        for chosen in cells :
            points=self.opp_win(board,chosen,mark,anti_mark)
            if(points <= minp):
                minp=points
                mymove=chosen
        return mymove

    def move(self, board, old_move, flag):
        self.begin = datetime.datetime.utcnow()
        self.count += 1
        self.limitReach = 0
        self.trans.clear()
        # print(self.trans.items())
        mymove = board.find_valid_move_cells(old_move)[0]
        for i in xrange(3,120):
            self.trans.clear()
            self.limit = i
            # print("in depth ",i)
            bval = self.alphaBeta(board, old_move, flag, 1, -MAX, MAX,0)
            getval = bval[1]
            # print("returned from depth ",i)
            if(self.limitReach == 0):
                mymove = getval
            else:
                break
        if flag=='x':
            anti_flag='o'
        else:
            anti_flag='x'
        mymove=self.check(board,old_move,mymove,flag,anti_flag)
        return mymove[0], mymove[1]
