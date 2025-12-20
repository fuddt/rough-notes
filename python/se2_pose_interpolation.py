import math
from typing import Tuple

# --- ユーティリティ ---
def wrap_to_pi(a: float) -> float:
    """角度aを (-π, π] に正規化。ヨー差分の連続性確保に必須。"""
    return (a + math.pi) % (2.0 * math.pi) - math.pi

def rot(theta: float):
    """2x2回転行列 R(theta) を返す。"""
    c, s = math.cos(theta), math.sin(theta)
    return ((c, -s), (s, c))

def matvec2(M, v):
    """2x2行列Mと2次元ベクトルvの積。"""
    return (M[0][0]*v[0] + M[0][1]*v[1],
            M[1][0]*v[0] + M[1][1]*v[1])

def se2_from_xyyaw(x: float, y: float, yaw: float):
    """姿勢 (x,y,yaw) を SE(2) 変換（R,t）へ。"""
    R = rot(yaw)
    t = (x, y)
    return R, t

def se2_inv(R, t):
    """SE(2) の逆変換。"""
    Rt = ((R[0][0], R[1][0]), (R[0][1], R[1][1]))  # R^T
    tinv = matvec2(Rt, (-t[0], -t[1]))
    return Rt, tinv

def se2_mul(R1, t1, R2, t2):
    """SE(2) の合成。 (R1,t1) * (R2,t2)"""
    R = ((R1[0][0]*R2[0][0] + R1[0][1]*R2[1][0],
          R1[0][0]*R2[0][1] + R1[0][1]*R2[1][1]),
         (R1[1][0]*R2[0][0] + R1[1][1]*R2[1][0],
          R1[1][0]*R2[0][1] + R1[1][1]*R2[1][1]))
    t = (t1[0] + R1[0][0]*t2[0] + R1[0][1]*t2[1],
         t1[1] + R1[1][0]*t2[0] + R1[1][1]*t2[1])
    return R, t

# --- SE(2) の exp/log マップ ---
def se2_V(theta: float):
    """
    V(θ) = [[sinθ/θ, -(1-cosθ)/θ],
            [(1-cosθ)/θ,  sinθ/θ]]
    小角ではテイラー展開で安定化。
    """
    eps = 1e-9
    if abs(theta) < eps:
        # sinθ ≈ θ - θ^3/6, 1-cosθ ≈ θ^2/2
        a = 1.0 - (theta**2)/6.0
        b = 0.5*theta
        return ((a, -b), (b, a))
    s = math.sin(theta)/theta
    c = (1.0 - math.cos(theta))/theta
    return ((s, -c), (c, s))

def se2_V_inv(theta: float):
    """
    V(θ) の逆行列。閉形式で安定化。
    det = (sinθ/θ)^2 + ((1-cosθ)/θ)^2 = 2*(1-cosθ)/θ^2
    小角では series で処理。
    """
    eps = 1e-9
    if abs(theta) < eps:
        # V ≈ [[1 - θ^2/6, -θ/2],
        #      [θ/2,        1 - θ^2/6]]
        # 逆行列を1次近似で：V^{-1} ≈ [[1 + θ^2/6, +θ/2],
        #                              [-θ/2,       1 + θ^2/6]]
        a = 1.0 + (theta**2)/6.0
        b = 0.5*theta
        return ((a, b), (-b, a))
    s = math.sin(theta)/theta
    c = (1.0 - math.cos(theta))/theta
    det = s*s + c*c  # > 0
    inv = (( s/det,  c/det),
           (-c/det,  s/det))
    return inv

def se2_log(R, t):
    """
    相対変換 (R,t) の対数：twist ξ = (vx, vy, ω) を返す。
    R は回転、t は平行移動。  t = V(ω) * v
    """
    # 角度を取り出す（Rは正規の回転を想定）
    yaw = math.atan2(R[1][0], R[0][0])  # Δψ
    Vinv = se2_V_inv(yaw)
    vx, vy = matvec2(Vinv, t)
    return (vx, vy, yaw)

def se2_exp(vx: float, vy: float, omega: float):
    """
    twist ξ=(vx,vy,ω) の指数： (R, t) を返す。
    t = V(ω) * v,  R = Rot(ω)
    """
    R = rot(omega)
    V = se2_V(omega)
    tx, ty = matvec2(V, (vx, vy))
    return R, (tx, ty)

# --- 0.3フレーム補間の本体 ---
def interpolate_pose_se2(
    x0: float, y0: float, yaw0: float,
    x1: float, y1: float, yaw1: float,
    alpha: float = 0.3
) -> Tuple[float, float, float]:
    """
    フレーム i の姿勢 (x0,y0,yaw0) からフレーム i+1 の姿勢 (x1,y1,yaw1) までの間を、
    SE(2) の対数・指数で補間して、alpha(=0.3) フレーム後の姿勢を返す。

    流れ：
      1) 相対変換 T_rel = T0^{-1} * T1 を作る
      2) ξ = log(T_rel) を取り、α倍する（一定twist仮定）
      3) T_alpha = T0 * exp(α ξ)
    """
    # 角度差はラップして連続性を保つ（重要）
    dyaw = wrap_to_pi(yaw1 - yaw0)

    # 姿勢をSE(2)へ
    R0, t0 = se2_from_xyyaw(x0, y0, yaw0)
    R1, t1 = se2_from_xyyaw(x0 + (x1 - x0), y0 + (y1 - y0), yaw0 + dyaw)  # yawだけはwrap後を反映

    # 相対変換 T_rel = T0^{-1} * T1
    R0inv, t0inv = se2_inv(R0, t0)
    Rrel, trel = se2_mul(R0inv, t0inv, R1, t1)

    # 対数（twist）→ α 倍 → 指数
    vx, vy, omega = se2_log(Rrel, trel)
    Ralpha, talpha = se2_exp(alpha*vx, alpha*vy, alpha*omega)

    # T_alpha = T0 * exp(α ξ)
    Ralpha_g, talpha_g = se2_mul(R0, t0, Ralpha, talpha)

    # 出力姿勢（角度も wrap しておく）
    x_alpha, y_alpha = talpha_g
    yaw_alpha = wrap_to_pi(yaw0 + alpha*dyaw)
    return x_alpha, y_alpha, yaw_alpha


# --- 簡易版：線形補間（近似。曲率が小さいとき用） ---
def interpolate_pose_lerp(
    x0: float, y0: float, yaw0: float,
    x1: float, y1: float, yaw1: float,
    alpha: float = 0.3
) -> Tuple[float, float, float]:
    """
    位置は線形補間、角度はラップ付き線形補間（近似）。
    曲がりが小さい/描画目的なら軽量で十分な場合あり。
    """
    dyaw = wrap_to_pi(yaw1 - yaw0)
    x = x0 + alpha * (x1 - x0)
    y = y0 + alpha * (y1 - y0)
    yaw = wrap_to_pi(yaw0 + alpha * dyaw)
    return x, y, yaw


# --- デモ ---
if __name__ == "__main__":
    # 例：フレームi と i+1 の姿勢がわかっている
    x0, y0, yaw0 = 0.0, 0.0, math.radians(0.0)
    x1, y1, yaw1 = 5.0, 5.0, math.radians(90.0)  # 90度まで回頭しているケース

    xa, ya, yawa = interpolate_pose_se2(x0, y0, yaw0, x1, y1, yaw1, alpha=0.3)
    print(f"SE(2)補間 0.3フレ後: x={xa:.6f}, y={ya:.6f}, yaw={math.degrees(yawa):.3f}°")

    xl, yl, yawl = interpolate_pose_lerp(x0, y0, yaw0, x1, y1, yaw1, alpha=0.3)
    print(f"LERP近似 0.3フレ後: x={xl:.6f}, y={yl:.6f}, yaw={math.degrees(yawl):.3f}°")