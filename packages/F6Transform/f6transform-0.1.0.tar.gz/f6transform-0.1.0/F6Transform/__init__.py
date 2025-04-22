import numpy as np

# F6库：空间运动基本操作集
# @ 符号说明：
# - F6理论中，@表示运动combine操作
# - Python中，@表示矩阵乘法（对应运动矩阵叠加）

__all__ = [
    'o2R', 'R2o', 'F62Q', 'Q2F6',
    'invQ', 'invF6', 'combine_F6'
]

def o2R(yaw, roll, pitch):
    Rz = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw),  np.cos(yaw), 0],
        [0,            0,           1]
    ])
    Ry = np.array([
        [np.cos(roll), 0, np.sin(roll)],
        [0,            1, 0],
        [-np.sin(roll),0, np.cos(roll)]
    ])
    Rx = np.array([
        [1, 0,            0],
        [0, np.cos(pitch),-np.sin(pitch)],
        [0, np.sin(pitch), np.cos(pitch)]
    ])
    return Rz @ Ry @ Rx

def R2o(R):
    beta = np.arctan2(-R[2, 0], np.sqrt(R[0, 0]**2 + R[1, 0]**2))
    if np.isclose(beta, np.pi/2):
        alpha = np.arctan2(-R[0, 1], R[1, 1])
        gamma = 0
    elif np.isclose(beta, -np.pi/2):
        alpha = np.arctan2(-R[0, 1], R[1, 1])
        gamma = 0
    else:
        alpha = np.arctan2(R[1, 0], R[0, 0])
        gamma = np.arctan2(R[2, 1], R[2, 2])
    return np.degrees(alpha), np.degrees(beta), np.degrees(gamma)

def F62Q(f6):
    x, y, z, yaw, roll, pitch = f6
    yaw, roll, pitch = np.radians(yaw), np.radians(roll), np.radians(pitch)
    R = o2R(yaw, roll, pitch)
    Q = np.eye(4)
    Q[:3, :3] = R
    Q[:3, 3] = [x, y, z]
    return Q

def Q2F6(Q):
    R = Q[:3, :3]
    t = Q[:3, 3]
    yaw, roll, pitch = R2o(R)
    return [t[0], t[1], t[2], yaw, roll, pitch]

def invQ(Q):
    return np.linalg.inv(Q)

def invF6(f6):
    return Q2F6(invQ(F62Q(f6)))

def combine_F6(f60, f61):
    return Q2F6(F62Q(f60) @ F62Q(f61))
