import pandas as pd
import matplotlib.pyplot as plt

# 设置字体以支持中文
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Source Han Sans SC', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
ball_fall_time_file = 'processed_data/steel_ball_fall_time.csv'
tube_diameters_file = 'processed_data/test_tube_diameters.csv'

def read_data(file_path):
    """
    Reads data from a CSV file and returns a DataFrame.
    """
    return pd.read_csv(file_path, encoding='utf-8-sig')

def plot_fall_time(data_file):
    """
    以时间 t 为纵坐标，试管内径的倒数 1/D 为横坐标（均取平均值），在直角坐标系中绘出 steel_ball_fall_time 中的各数据点；用一条直线拟合这些数据点；该直线与纵坐标轴交点的截距为 t₀，从图中测出 t₀。
    """
    # 读取数据
    fall_time_df = read_data(ball_fall_time_file)
    tube_diam_df = read_data(tube_diameters_file)
    # 只取t₁~t₄和D₁~D₄的平均值
    t_means = fall_time_df[fall_time_df['时间/s'].str.startswith('t')]['平均值'].astype(float).values
    D_means = tube_diam_df[tube_diam_df['直径/mm'].str.startswith('D')]['平均值'].astype(float).values
    # 计算1/D
    inv_D = 1 / D_means
    # 拟合直线
    import numpy as np
    coeffs = np.polyfit(inv_D, t_means, 1)
    fit_line = np.poly1d(coeffs)
    # 延长横轴范围以显示截距
    x_min = 0
    x_max = max(inv_D) * 1.1
    x_fit = np.linspace(x_min, x_max, 200)
    # 绘图
    plt.figure(figsize=(8, 6))
    plt.title('图一 钢球自由落体时间与试管内径的关系')
    plt.xlabel('1/D (1/mm)')
    plt.ylabel('t (s)')
    plt.scatter(inv_D, t_means, s=40, c='b', marker='o', label='实验数据')
    # 在每个点旁边标注具体数据
    for x, y in zip(inv_D, t_means):
        plt.text(x, y, f'({x:.5f}, {y:.5f})', fontsize=9, ha='right', va='bottom')
    plt.plot(x_fit, fit_line(x_fit), c='r', linewidth=1, label='线性拟合')
    # 在线性拟合线的legend中添加表达式
    k, b = coeffs[0], coeffs[1]
    expr = fr'$t = {k:.5f} \, (1/D) + {b:.5f}$'
    # 截距t0
    t0 = coeffs[1]
    plt.axhline(y=t0, color='g', linestyle='--', label=fr'$t_0={t0:.5f}$')
    plt.xlim(x_min, x_max)
    plt.legend(["实验数据", expr, fr'$t_0={t0:.5f}$'])
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig('fall_time_vs_invD.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    plot_fall_time(ball_fall_time_file);
