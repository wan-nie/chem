import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import pchip_interpolate


class DrawFormat():
    marker_size=20
    dpi = 600
    figure_size=(25,6)
    main_color = 'tab:blue'
    side_color = 'tab:orange'
    interval = 500


# 加载'data.csv'中的data，并且找到除第一列外每列不为空的index
def get_data_and_index_dic():
    data = pd.read_csv('data.csv', header=None)
    columns = ['c' + str(i) for i in data.columns]
    data.columns = columns
    index_dic = {}
    # 找到除第一列外每列不为空的index，并将nan变为对应第一列的值
    for i, col in enumerate(columns):
        series = data[col]
        not_nan_indexes = data[data[col].notnull()].index

        if 'continue' in series.unique():
            continue_index = data[data[col] == 'continue'].index
            not_nan_indexes = (continue_index, not_nan_indexes)

        index_dic[col] = not_nan_indexes
        data[col] = np.where(series.isna(), data[columns[0]], data[col])

    return data, index_dic


def get_x_and_y(x_observed, y_observed):
    n = len(x_observed) - 1
    x = np.linspace(x_observed[0], x_observed[-1], n*DrawFormat.interval)
    y = pchip_interpolate(x_observed, y_observed, x)
    return x, y


def mask_y(y, index, observed=True):
    if not observed:
        index = np.arange(
                            (index[0]) * DrawFormat.interval,
                            (index[-1]) * DrawFormat.interval
                         )

    valid_mask = np.zeros(len(y), np.bool)
    valid_mask[index] = 1
    y = np.where(valid_mask, y, np.nan)
    return y


def draw_one(x_observed, y_observed, x, y, i, ax=None, annotate=True):
    # 对于主路线zorder=100+，辅路线zorder=0+
    if i == 0:
        line_style = '-'
        line_color = DrawFormat.main_color
        zorder = 100
    else:
        line_style = '--'
        line_color = DrawFormat.side_color
        zorder = 0

    ax.plot(x, y,
            color=line_color,
            linestyle=line_style,
            zorder=zorder + 0  # zorder越大图层越在上面
            )
    ax.scatter(x_observed, y_observed,
               color=line_color,
               s=DrawFormat.marker_size,
               zorder=zorder + 1
               )
    if annotate:
        for i, energy in enumerate(y_observed):
            x_i = x_observed[i]
            y_i = y_observed[i]
            plt.annotate('\n\n%s' % str(energy), (x_i, y_i), zorder=zorder + 2)


def draw(annotate=True):
    data, index_dic = get_data_and_index_dic()
    fig, ax = plt.subplots(1, figsize=DrawFormat.figure_size)
    for i, col in enumerate(data.columns):
        continue_index = None
        index = index_dic[col]
        x_observed = data.index.to_numpy()
        y_observed = data[col].to_numpy()

        # 判断该列是否含有'continue'
        if isinstance(index, tuple):
            continue_index = index[0]
            index = index[1]

        if continue_index is None:
            x, y = get_x_and_y(x_observed, y_observed)
            # 将不在区间的y_observed和y设置为nan
            y_observed = mask_y(y_observed, index, observed=True).round(1)
            y = mask_y(y, index, observed=False)
            draw_one(x_observed, y_observed, x, y, i, ax, annotate)

        else:
            df = pd.DataFrame({'x': x_observed, 'y': y_observed})
            df = df.query('x in @index & x not in @continue_index')

            x_observed = df['x'].astype(float).to_numpy()
            y_observed = df['y'].astype(float).to_numpy()

            x, y = get_x_and_y(x_observed, y_observed)

            y_observed = y_observed.astype(float).round(1)
            draw_one(x_observed, y_observed, x, y, i, ax, annotate)

    plt.axis('off')
    plt.savefig('profile.svg', dpi=DrawFormat.dpi, transparent=True,
                bbox_inches='tight', pad_inches=0)
    plt.show()


if __name__ == '__main__':
    draw(annotate=True)

