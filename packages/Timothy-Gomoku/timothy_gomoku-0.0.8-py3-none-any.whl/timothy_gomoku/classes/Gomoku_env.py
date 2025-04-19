import numpy as np
import torch


def board_symbol(value):
    if value == 1:
        return "● "
    elif value == -1:
        return "○ "
    else:
        return "· "


class Gomoku_env:

    def __init__(self):
        self.board = np.zeros((15, 15), dtype=np.int8)
        self.step = [0, 0]

    def __str__(self):
        output = "┌───────────────────────────────┐\n"
        for i in range(15):
            output += "│ "
            for j in range(15):
                output += board_symbol(self.board[i][j])
            output += "│\n"
        output += "└───────────────────────────────┘"
        output += "\n"
        output += f"Player A: {self.step[0]} steps\n"
        output += f"Player B: {self.step[1]} steps\n"
        output += f"Turn: {'A' if self.turn() else 'B'}\n"
        output += f"Win: {self.win()}"
        return output

    def move(self, x, y, positive):
        if x < 0 or x >= 15:
            raise ValueError("Invalid move")
        if y < 0 or y >= 16:
            raise ValueError("Invalid move")
        if self.board[x][y] != 0:
            raise ValueError("Invalid move")

        if positive == 1:
            self.step[0] += 1
            self.board[x][y] = 1
        else:
            self.step[1] += 1
            self.board[x][y] = -1

    def turn(self):
        return self.step[0] <= self.step[1]

    __win_cols = [[[x + k, y] for k in range(5)] for x in range(11) for y in range(15)]
    __win_rows = [[[x, y + k] for k in range(5)] for x in range(15) for y in range(11)]
    __win_diags_1 = [
        [[x + k, y + k] for k in range(5)] for x in range(11) for y in range(11)
    ]
    __win_diags_2 = [
        [[x + k, y - k] for k in range(5)] for x in range(11) for y in range(4, 15)
    ]
    win_combos = __win_cols + __win_rows + __win_diags_1 + __win_diags_2

    def win(self):
        for win_combo in Gomoku_env.win_combos:
            ok = True
            coordinate_0 = win_combo[0]
            x_0 = coordinate_0[0]
            y_0 = coordinate_0[1]
            if self.board[x_0][y_0] == 0:
                continue
            for coordinate in win_combo[1:]:
                x = coordinate[0]
                y = coordinate[1]
                if self.board[x][y] == 0:
                    ok = False
                    break
                if self.board[x][y] != self.board[x_0][y_0]:
                    ok = False
                    break
            if ok:
                return self.board[x_0][y_0]
        if self.step[0] + self.step[1] == 225:
            return 2
        return 0

    def state(self):
        """
        将当前棋盘状态编码为 3x15x15 的 PyTorch Tensor
        通道：
            0: 当前玩家的棋子
            1: 对手的棋子
            2: 当前玩家是谁（全是 1 或 0）
        """
        board = self.board
        current_player = 1 if self.turn() else -1

        my_stones = (board == current_player).astype(np.float32)
        opp_stones = (board == -current_player).astype(np.float32)
        current_plane = np.full(
            (15, 15), 1.0 if current_player == 1 else 0.0, dtype=np.float32
        )

        state = np.stack([my_stones, opp_stones, current_plane])
        return torch.tensor(state, dtype=torch.float32).unsqueeze(0)


__all__ = ["Gomoku_env"]
