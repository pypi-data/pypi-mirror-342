import numpy as np
import torch
from classes.Gomoku_env import Gomoku_env

def play_with_human(net, device):
    
    env = Gomoku_env()
    print(env)

    while True:
        if env.turn():
            try:
                move = input("Your move (format: x y): ")
                x, y = map(int, move.strip().split())
                env.move(x, y, positive=True)
            except Exception as e:
                print("Invalid move:", e)
                continue
        else:
            state = env.state().to(device)
            with torch.no_grad():
                policy, _ = net(state)
                probs = torch.softmax(policy, dim=1).cpu().numpy().flatten()
                sorted_indices = probs.argsort()[::-1]
                for idx in sorted_indices:
                    x, y = divmod(idx, 15)
                    if env.board[x][y] == 0:
                        env.move(x, y, positive=False)
                        break

        print(env)
        winner = env.win()
        if winner != 0:
            print("Game Over! Winner:", "You (●)" if winner == 1 else "AI (○)")
            break
        elif np.all(env.board != 0):
            print("Draw!")
            break

__all__ = ["play_with_human"]