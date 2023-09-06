# %%
import chess
import chess.svg
import chess.pgn
import chess.engine
from IPython.display import SVG
import datetime 
import time

PIECES=[chess.PAWN,chess.KNIGHT,chess.BISHOP,chess.ROOK,chess.QUEEN,chess.KING ]
PLAYERS= [chess.WHITE,chess.BLACK]
from flask import Flask, Response, request
import webbrowser
import traceback
# %%


# %%


# %%

STOCKFISH_PATH="C:\projects\human\chess\stockfish\stockfish-windows-x86-64-avx2.exe"
pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]
bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]
queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]
kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

# %%
def basic_hurstic_func(board):
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

    if board.turn:
        return material
    else:
        return -material
def hurstic_func(board):
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                        for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                            for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                            for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                        for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                            for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                        for i in board.pieces(chess.KING, chess.BLACK)])
    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval

# %%
def minimax(board, depth, maximizing_player):
    if depth == 0 or board.is_game_over():
        return hurstic_func(board)
    if maximizing_player:
        value = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = max(value, minimax(board, depth - 1, False))
            board.pop()
        return value
    else:
        value = float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = min(value, minimax(board, depth - 1, True))
            board.pop()
        return value

# %%
def alphabeta(board,alpha=-100, beta=100 ,depthleft=1):
    bestscore = -9999
    bestmove= []
    if (depthleft == 0):
        return {"score": hurstic_func(board)}
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(board,-beta, -alpha, depthleft - 1)["score"]
        
        board.pop()
        if (score >= beta):
            return {"score":score, "move":move}
        if (score > bestscore):
            bestscore = score
            bestmove= move
            
        if (score > alpha):
            alpha = score
    return {"score":bestscore, "move":bestmove}

def quiesce(board,alpha, beta ):
    stand_pat = hurstic_func(board)
    score=0
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat
    for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                score = -quiesce(board,-beta, -alpha)
                board.pop()
    if (score >= beta):
        return beta
    if (score > alpha):
        alpha = score
        return alpha




def main2():
    board = chess.Board()
    count = 0
    movehistory = []
    game = chess.pgn.Game()
    board = chess.Board()
    while not board.is_game_over(claim_draw=True):
        if board.turn:
            count += 1
            print(f'\n{count}]\n')
            move = alphabeta(board)["move"]
            board.push(move)
            print(board)
            print()
        else:
            move = alphabeta(board)["move"]
            board.push(move)
            print(board)
        
        movehistory.append(move)
    game.add_line(movehistory)
    game.headers["Event"] = "Self Tournament 2020"
    game.headers["Site"] = "Pune"
    game.headers["Date"] = str(datetime.datetime.now().date())
    game.headers["Round"] = 1
    game.headers["White"] = "Ai"
    game.headers["Black"] = "Ai"
    game.headers["Result"] = str(board.result(claim_draw=True))
    print(game)
    SVG(chess.svg.board(board=board,size=400))


# %%
board=chess.Board()
moves_hist=[]
stockFishEngine=chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

def aiMove():
    move = alphabeta(board)["move"]
    moves_hist.append(str(move))

    board.push(move)


def stockFishMove():

    move = stockFishEngine.play(board, chess.engine.Limit(time=0.1))
    print(move)
    board.push(move.move)
    moves_hist.append(str(move.move))

    board.push(move)



app = Flask(__name__)
# Front Page of the Flask Web Page
@app.route("/")
def main():
    global count, board,moves_hist
    ret = '<html><head>'
    ret += '<style>input {font-size: 20px; } button { font-size: 20px; }</style>'
    ret += '</head><body>'
    hist =",".join(moves_hist)
    ret += '<div id="moves">moves:[%s] </div>' % hist
    ret += '<img width=510 height=510 src="/board.svg?%f"></img></br></br>' % time.time()
    ret += '<form action="/game/" method="post"><button name="New Game" type="submit">New Game</button></form>'
    ret += '<form action="/undo/" method="post"><button name="Undo" type="submit">Undo Last Move</button></form>'
    ret += '<form action="/move/"><input type="submit" value="Make Human Move:"><input name="move" type="text"></input></form>'
    ret += '<form action="/dev/" method="post"><button name="Comp Move" type="submit">Make Ai Move</button></form>'
    
    ret += '<form action="/stmove/" method="post"><button name="move">Make StockFish Move</button></form>'

    #ret += '<form action="/engine/" method="post"><button name="Stockfish Move" type="submit">Make Stockfish Move</button></form>'
    return ret
# Display Board
@app.route("/board.svg/")
def board():
    return Response(chess.svg.board(board=board, size=700), mimetype='image/svg+xml')
# Human Move
@app.route("/move/")
def move():
    try:
        move = request.args.get('move', default="")
        board.push_san(move)
        moves_hist.append(str(move))
    except Exception as  e:
        print(e)
    return main()
# Make Ai’s Move
@app.route("/stmove/", methods=['POST'])
def stmove():
    try:
        print("hey")
        stockFishMove()

    except Exception:
        traceback.print_exc()
    return main()


@app.route("/dev/", methods=['POST'])
def dev():
    try:
        aiMove()

    except Exception:
        traceback.print_exc()
    return main()
# Make UCI Compatible engine's move
# @app.route("/engine/", methods=['POST'])
# def engine():
#     try:
#         stockfish()
#     except Exception:
#         traceback.print_exc()
#     return main()
# New Game
@app.route("/game/", methods=['POST'])
def game():
    moves_hist=[]
    board.reset()
    return main()
# Undo
@app.route("/undo/", methods=['POST'])
def undo():
    try:
        moves_hist.pop()
        board.pop()
    except Exception:
        traceback.print_exc()
    return main()

    
board = chess.Board()
webbrowser.open("http://127.0.0.1:5000/")
app.run()