def calc_error(x, y, z, i_obs, j_obs, camera_params):
    """
    現在の (x, y, z) を投影し、
    観測されたカーソル位置との差を返す
    """
    i_hat, j_hat = project_to_image(x, y, z, camera_params)
    di = i_hat - i_obs
    dj = j_hat - j_obs
    return di, dj

def calc_error(x, y, z, i_obs, j_obs, camera_params):
    """
    現在の (x, y, z) を投影し、
    観測されたカーソル位置との差を返す
    """
    i_hat, j_hat = project_to_image(x, y, z, camera_params)
    di = i_hat - i_obs
    dj = j_hat - j_obs
    return di, dj

def adjust_z(
    x, y, z,
    i_obs, j_obs,
    camera_params,
    step,
    tol,
    max_iter
):
    def eval_z(z_val):
        _, dj = calc_error(x, y, z_val, i_obs, j_obs, camera_params)
        return dj

    return adjust_1d(
        value=z,
        eval_func=eval_z,
        step=step,
        tol=tol,
        max_iter=max_iter,
    )
def adjust_x(
    x, y, z,
    i_obs, j_obs,
    camera_params,
    step,
    tol,
    max_iter
):
    def eval_x(x_val):
        di, _ = calc_error(x_val, y, z, i_obs, j_obs, camera_params)
        return di

    return adjust_1d(
        value=x,
        eval_func=eval_x,
        step=step,
        tol=tol,
        max_iter=max_iter,
    )

def refine_xz(
    x, y, z,
    i_obs, j_obs,
    camera_params,
    step_x=0.01,
    step_z=0.01,
    tol=1.0,
    inner_iter=50,
    outer_iter=5,
):
    """
    人がやっている
    「z → x → z → x」をそのまま再現
    """
    for _ in range(outer_iter):
        z = adjust_z(
            x, y, z,
            i_obs, j_obs,
            camera_params,
            step=step_z,
            tol=tol,
            max_iter=inner_iter,
        )

        x = adjust_x(
            x, y, z,
            i_obs, j_obs,
            camera_params,
            step=step_x,
            tol=tol,
            max_iter=inner_iter,
        )

    return x, z

camera_params = {
    "fx": 1200.0,
    "fy": 1200.0,
    "cx": 960.0,
    "cy": 540.0,
}

# 初期値（ズレている）
x0, y0, z0 = 1.2, 0.0, 10.0

# カーソルで打った正解位置
i_obs, j_obs = 980.0, 560.0

x_refined, z_refined = refine_xz(
    x=x0,
    y=y0,
    z=z0,
    i_obs=i_obs,
    j_obs=j_obs,
    camera_params=camera_params,
    step_x=0.02,
    step_z=0.02,
    tol=1.0,
)

print("refined:", x_refined, z_refined)
