import torch
import torch.nn as nn
import torch.nn.functional as F

class Gomoku_net(nn.Module):
    def __init__(self, board_size=15):
        super(Gomoku_net, self).__init__()
        self.board_size = board_size
        self.input_channels = 3  # e.g. my stones, opponent stones, current player

        # Backbone (5 conv layers)
        self.conv1 = nn.Conv2d(self.input_channels, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.conv5 = nn.Conv2d(128, 256, kernel_size=3, padding=1)

        self.bn1 = nn.BatchNorm2d(64)
        self.bn2 = nn.BatchNorm2d(64)
        self.bn3 = nn.BatchNorm2d(128)
        self.bn4 = nn.BatchNorm2d(128)
        self.bn5 = nn.BatchNorm2d(256)

        # Policy head
        self.policy_conv = nn.Conv2d(256, 2, kernel_size=1)  # output shape: (batch, 2, 15, 15)
        self.policy_fc = nn.Linear(2 * board_size * board_size, board_size * board_size)

        # Value head
        self.value_conv = nn.Conv2d(256, 1, kernel_size=1)  # output shape: (batch, 1, 15, 15)
        self.value_fc1 = nn.Linear(board_size * board_size, 64)
        self.value_fc2 = nn.Linear(64, 1)

    def forward(self, x):
        # Backbone
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.bn4(self.conv4(x)))
        x = F.relu(self.bn5(self.conv5(x)))

        # Policy head
        p = F.relu(self.policy_conv(x))
        p = p.view(p.size(0), -1)
        p = self.policy_fc(p)
        p = F.log_softmax(p, dim=1)  # Log probabilities over 225 positions

        # Value head
        v = F.relu(self.value_conv(x))
        v = v.view(v.size(0), -1)
        v = F.relu(self.value_fc1(v))
        v = torch.tanh(self.value_fc2(v))  # Scalar value in [-1, 1]

        return p, v  # p: (batch, 225), v: (batch, 1)

    def store(self, path):
        torch.save(self.state_dict(), path)


__all__ = ["Gomoku_net"]