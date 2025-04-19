import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import datetime
import pytz
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates # Import matplotlib.dates
import numpy as np
from datetime import datetime
from dateutil import parser
from pyspedas import tplot, data_quants, store_data

def parse_datetime_flexible(ts):
    return parser.isoparse(ts)

def single_plot_内部関数(ax, variable, common_trange, cax=None, legend_label=None, yauto=None, zauto=None): # legend_label 引数を追加、デフォルトはNone
    data = data_quants[variable]
    initialize_plot_options(variable)
    if isinstance(common_trange[0], str):
        start = np.datetime64(common_trange[0])
        end = np.datetime64(common_trange[1])
        data = data.sel(time=slice(start, end))

    """ x axix """
    if common_trange is not None:
      if isinstance(common_trange[0], str):
        datatime_range_utc = [parse_datetime_flexible(ts) for ts in common_trange]
        ax.set_xlim(datatime_range_utc[0], datatime_range_utc[1])
    else:    
      utc_timezone = pytz.utc
      datetime_range_utc = [datetime.datetime.fromtimestamp(ts, tz=utc_timezone) for ts in common_trange]
      # print(datetime_range_utc)
      ax.set_xlim(datetime_range_utc[0], datetime_range_utc[1])

    """ y axix """
    if data.plot_options['yaxis_opt']['axis_subtitle'] is not None or data.plot_options['yaxis_opt']['axis_subtitle'] != '':
        ax.set_ylabel(data.plot_options['yaxis_opt']['axis_label'] + "\n" + data.plot_options['yaxis_opt']['axis_subtitle'])
    else:
        ax.set_ylabel(data.plot_options['yaxis_opt']['axis_label'])

    if data.plot_options['yaxis_opt']['y_axis_type'] == 1 or data.plot_options['yaxis_opt']['y_axis_type'] == 'log':
        ax.set_yscale('log')

    if data.plot_options['yaxis_opt']['y_range'] is None or yauto == True:
      if hasattr(data, 'spec_bins'): 
        if data.plot_options['extras']['spec'] == 0 or data.plot_options['extras']['spec'] is None:
          cleaned_data = data.values[np.isfinite(data.values)]
          if cleaned_data.size == 0:
              print("No finite values found in {} data.".format(variable))
          data.plot_options['yaxis_opt']['y_range'] = [cleaned_data.min()*0.9, cleaned_data.max()*1.1]
          # print(cleaned_data.min(), cleaned_data.max())
        elif data.plot_options['extras']['spec'] == 1:
          y_bins = data.spec_bins.values
          cleaned_data = y_bins[np.isfinite(y_bins)]
          if cleaned_data.size == 0:
              print("No finite values found in {} data.".format(variable))
          data.plot_options['yaxis_opt']['y_range'] = [cleaned_data.min(), cleaned_data.max()]
          cleaned_data = data.values[np.isfinite(data.values)]
          if cleaned_data.size == 0:
              print("No finite values found in {} data.".format(variable))
          data.plot_options['zaxis_opt']['z_range'] = [cleaned_data.min(), cleaned_data.max()]
      else:
        cleaned_data = data.values[np.isfinite(data.values)]
        if cleaned_data.size == 0:
            print("No finite values found in {} data.".format(variable))
        data.plot_options['yaxis_opt']['y_range'] = [cleaned_data.min()*0.9, cleaned_data.max()*1.1]
        

    ax.set_ylim(data.plot_options['yaxis_opt']['y_range'][0], data.plot_options['yaxis_opt']['y_range'][1])

    """ case for no spec_bins """
    # data.plot_options['line_opt']が存在しない場合のif文
    if 'line_opt' not in data.plot_options:
      lc = None
      lw = None
      ls = None
    else:
      if 'line_color' not in data.plot_options['line_opt']:
        lc = None
      else:
        lc = data.plot_options['line_opt']['line_color']
      if 'line_width' not in data.plot_options['line_opt']:
        lw = None
      else:
        lw = data.plot_options['line_opt']['line_width']
      if 'line_style' not in data.plot_options['line_opt']:
        ls = None
      else:
        ls = data.plot_options['line_opt']['line_style']
    spec_value = data.attrs.get('plot_options', {}).get('extras', {}).get('spec')
    legend_names = data.attrs.get('plot_options', {}).get('yaxis_opt', {}).get('legend_names')
    if spec_value is None or spec_value == 0:
        if legend_names is not None:
          if legend_names != []: # legend_names が空リストの場合
            if legend_label is not None: # legend_label が指定されている場合のみ label を設定
              if isinstance(lc, list):
                for i in range(len(data[0])):
                  ax.plot(data.time, data[:, i], label=legend_label, c =lc[i], lw=lw, ls=ls)
              else:
                ax.plot(data.time, data, label=legend_label, c =lc, lw=lw, ls=ls)
            else:
              if isinstance(lc, list):
                for i in range(len(data[0])):
                  ax.plot(data.time, data[:, i], label=legend_names[i], c =lc[i], lw=lw, ls=ls)
              else:
                ax.plot(data.time, data, label=legend_names, c =lc, lw=lw, ls=ls)
            ax.legend(loc='upper right') # 凡例を表示
          else:
            if isinstance(lc, list):
              for i in range(len(data[0])):
                ax.plot(data.time, data[:, i], c =lc[i], lw=lw, ls=ls)
            else:
              ax.plot(data.time, data, c =lc, lw=lw, ls=ls)
        else:
            ax.plot(data.time, data, c =lc, lw=lw, ls=ls)

    ### case for spectrpgram ###
    elif data.plot_options['extras']['spec'] == 1:
        cmap = data.plot_options['extras']['colormap'][0]
        if data.plot_options['zaxis_opt']['z_range'] is None or zauto == True:
            if isinstance(common_trange[0], str):
              start = np.datetime64(common_trange[0])
              end = np.datetime64(common_trange[1])
              data = data.sel(time=slice(start, end))
            cleaned_data = data.values[np.isfinite(data.values)]
            if cleaned_data.size == 0:
              print("No finite values found in {} data.".format(variable))
            data.plot_options['zaxis_opt']['z_range'] = [cleaned_data.min(), cleaned_data.max()]
        if data.plot_options['zaxis_opt']['z_axis_type'] == 1 or data.plot_options['zaxis_opt']['z_axis_type'] == 'log':
            norm = mcolors.LogNorm(vmin=data.plot_options['zaxis_opt']['z_range'][0], vmax=data.plot_options['zaxis_opt']['z_range'][1])
        else:
            norm = None

        mesh = ax.pcolormesh(data.time, data.spec_bins, data.T, shading='nearest',cmap=cmap, norm=norm)

        if cax is not None: # colorbar axes が指定されている場合
            plt.colorbar(mesh, cax=cax, label=data.plot_options['zaxis_opt']['axis_label']) # cax に colorbar を描画
        else: # colorbar axes が指定されていない場合は、axes に隣接して描画 (以前の動作)
            fig = plt.gcf()
            fig.colorbar(mesh, ax=ax, label=data.plot_options['zaxis_opt']['axis_label'])

    elif data.plot_options['extras']['spec'] == 0:
        list_values = data.spec_bins.values.tolist()
        str_list = [str(item)+' '+data.data_att['depend_1_units'] for item in list_values]
        if legend_names is not None:
          if not isinstance(lc, list):
            if legend_names != []: # legend_names が空リストの場合
              if legend_label is not None: # legend_label が指定されている場合のみ label を設定
                  ax.plot(data.time, data, label=legend_label, c =lc, lw=lw, ls=ls)
              else:
                  ax.plot(data.time, data, label=legend_names, c =lc, lw=lw, ls=ls)
              ax.legend(loc='upper right')
          else:
            if legend_names != []:
              for i in range(data.shape[1]):
                if legend_label is not None: # legend_label が指定されている場合のみ label を設定
                  ax.plot(data.time, data, label=legend_label, c =lc[i], lw=lw, ls=ls)
                else:
                  ax.plot(data.time, data, label=legend_names, c =lc[i], lw=lw, ls=ls)
              ax.legend(loc='upper right')
            else:
              for i in range(data.shape[1]):
                ax.plot(data.time, data, c =lc[i], lw=lw, ls=ls)
    else:
        raise ValueError("unexpected spec value")

def orbit_label_panel(ax, orbit_data, xaxis_ticks, font_size,
                      y_tick_step, y_tick_base, y_orb_lim_max):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(
        axis="y", which="both", length=0, pad=10, labelsize=10, left=False, labelleft=False
    )
    ax.set_ylim(0.0, y_orb_lim_max) # y軸範囲を調整 (ラベルが収まるように)

    y_base = y_tick_base # 全体の垂直位置調整用 (必要に応じて変更)

    xmin, xmax = ax.get_xlim()

    component_labels = orbit_data.attrs.get('plot_options', {}).get('yaxis_opt', {}).get('legend_names')
    num_components = orbit_data.shape[1] if len(orbit_data.shape) > 1 else 1

    # 各ラベルの固定 y 座標
    y_step = y_tick_step
    y_positions = [y_base + 2*y_step, y_base + 1*y_step, y_base + 0*y_step] # R, MLAT, MLT の y 座標を固定

    for i_component in range(num_components):
        orbit_values = []
        if component_labels[i_component] is None:
            component_labels[i_component] = f"Component {i_component + 1}"
        for tick_dt in xaxis_ticks:
            # Convert tick_dt to timezone-naive datetime to match orbit_data.time.values
            tick_dt_naive = tick_dt.replace(tzinfo=None) # Make tick_dt timezone-naive

            time_diff = np.abs(orbit_data.time.values - np.datetime64(tick_dt_naive))
            closest_index = np.argmin(time_diff)
            orbit_values.append(orbit_data.values[closest_index, i_component]) # Use current component

        xaxis_labels = [f"{val:.2f}" for val in orbit_values]

        y_pos = y_positions[i_component] # 固定の y 座標を使用
        for xaxis_tick, xaxis_label in zip(xaxis_ticks, xaxis_labels):
            # Sometimes ticks produced by locator can be outside xlim, so let exclude them
            if xmin <= mdates.date2num(xaxis_tick) <= xmax:
                ax.text(
                    xaxis_tick,
                    y_pos,
                    xaxis_label,
                    fontsize=font_size,
                    ha="center",
                    va="center",
                )
        # y軸ラベル (R, MLAT, MLT)
        ax.text(
            -0.03,
            y_pos/y_orb_lim_max,
            component_labels[i_component],
            fontsize=font_size,
            ha="right",
            va="center",
            transform=ax.transAxes,
        )

def mp(variables,
       var_label=None,
       font_size=10,
       xsize=10,
       ysize=2,
       tr=None,
       plot_title=None, plot_title_fontsize=None,
       display = True,
       yauto=None,
       zauto=None,
       save_path=None,
       orb_label_height=0.6,hspace=0.1,
       y_tick_step=0.5, y_tick_base=0.1, y_orb_lim_max=None):
    
    if y_orb_lim_max is None:
        y_orb_lim_max = y_tick_step * 3

    if not isinstance(variables, list):
        variables = [variables]
    num_plots = len(variables)
    fig = plt.figure(figsize=(xsize, ysize * (num_plots + 1))) # Figure を作成 (orbit row を追加)
    gs = gridspec.GridSpec(num_plots + 1, 2, height_ratios=[1]*num_plots + [orb_label_height], width_ratios=[80, 1], hspace=hspace, wspace=0.05) # GridSpec (orbit row を追加, height_ratios調整)

    plt.rcParams['font.size'] = font_size
    plt.rcParams['axes.titlesize'] = font_size
    plt.rcParams['axes.labelsize'] = font_size
    plt.rcParams['xtick.labelsize'] = font_size
    plt.rcParams['ytick.labelsize'] = font_size
    plt.rcParams['legend.fontsize'] = font_size

    # 共通のx軸範囲を計算
    start_times = []
    end_times = []
    has_spec = [] # スペクトログラムプロットかどうかを記録するリスト
    for variable in variables:
        if isinstance(variable, list):
          for var in variable:
            data = data_quants[var]
            trange = data.plot_options['trange']
            start_times.append(trange[0])
            end_times.append(trange[1])
            spec_value = data.attrs.get('plot_options', {}).get('extras', {}).get('spec')
            if not spec_value == 1:
                pass
            else:
                has_spec.append(True)
                break
          if has_spec == []:
            has_spec.append(False)
        else:
            data = data_quants[variable]
            trange = data.plot_options['trange']
            start_times.append(trange[0])
            end_times.append(trange[1])
            spec_value = data.attrs.get('plot_options', {}).get('extras', {}).get('spec')
            has_spec.append(spec_value == 1) # spec == 1 なら True, それ以外 (None, 0) なら False

    if tr is not None:
        common_trange = tr
    elif trange is None or tr is None or trange == '':
        common_start_time = min(start_times)
        common_end_time = max(end_times)
        common_trange = [common_start_time, common_end_time]

    axes_list = [] # 後で sharex するために axes をリストに保存
    plot_index = 0 # プロットのインデックス
    for i, variable_group in enumerate(variables): # 変数リストをループ処理。variable_group は変数または変数リスト
        ax = fig.add_subplot(gs[plot_index, 0]) # axes 用の subplot を追加 (左側の列)
        axes_list.append(ax)
        cax = None # colorbar axes を初期化
        if has_spec[plot_index]: # スペクトログラムプロットの場合
            cax = fig.add_subplot(gs[plot_index, 1]) # colorbar 用の subplot を追加 (右側の列)
        # if isinstance(variable_group, list):
        #   for var in variable_group:
            # cax = fig.add_subplot(gs[plot_index, 1]) # colorbar 用の subplot を追加 (右側の列)

        if isinstance(variable_group, list): # variable_group がリストの場合 (オーバーラッププロット)
            for j, variable in enumerate(variable_group): # 内側の変数をループ処理
                if j == 0:
                    legend_label = str(variable_group) # 最初の変数に凡例ラベルを設定 (変数リスト自体をラベルにする)
                else:
                    legend_label = None # 2番目以降の変数は凡例ラベルなし
                single_plot_内部関数(ax, variable, common_trange, cax=cax, legend_label=legend_label, yauto=yauto, zauto=zauto)
        else: # variable_group がリストでない場合 (通常のプロット)
            single_plot_内部関数(ax, variable_group, common_trange, cax=cax, yauto=yauto, zauto=zauto)

        ax.set_xlabel('')
        if var_label is not None:
          ax.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=False)
        else:
          if plot_index == num_plots - 1:
            ax.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=True)
          else:
            ax.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=False)
        
        if plot_title is not None:
            if i == 0:
                if plot_title_fontsize is not None:
                    ax.set_title(plot_title, fontsize=plot_title_fontsize)
                else:
                    ax.set_title(plot_title, fontsize=font_size)
        plot_index += 1 # プロットインデックスをインクリメント


    # x軸を共有
    for i in range(1, num_plots):
        axes_list[i].sharex(axes_list[0])

    if var_label is not None:
        # orbit label panel
        orbit_ax = fig.add_subplot(gs[num_plots, 0], sharex=axes_list[0]) # orbit axes を追加 (最下行、axesとx軸共有)
        orbit_data = data_quants[var_label] # orbit データを取得
        locator = axes_list[-1].xaxis.get_major_locator() # 最後の axes の locator を取得
        xaxis_ticks_num = axes_list[-1].get_xticks().tolist() # 数値形式の ticks
        utc_timezone = pytz.utc
        xaxis_ticks_dt = [
            pytz.utc.localize(datetime(*mdates.num2date(tick_val).timetuple()[:6])) # Convert to naive datetime first then localize
            for tick_val in xaxis_ticks_num
        ]  # numeric ticks to timezone-aware datetime

        orbit_label_panel(orbit_ax, orbit_data, xaxis_ticks_dt, font_size, y_tick_step, y_tick_base, y_orb_lim_max) # orbit label panel を描画
        orbit_ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True) # orbit_ax の x軸目盛りとラベルを表示

    # plt.tight_layout() # レイアウト調整
    plt.subplots_adjust(hspace=0.1)
    
    if save_path is not None:
      plt.savefig(save_path)

    if display:
        plt.show()
    else:
        plt.close(fig)

# def op(variable_name,
#                       y_label=None,
#                       ylog=None,
#                       y_range=None,
#                       y_sublabel=None,
#                       z_range=None,
#                       zlog=None,
#                       z_sublabel=None,
#                       z_label=None,
#                       spec=None,
#                       colormap=None,
#                       legend_names=None,
#                       line_color=None,
#                       line_width=None,
#                       line_style=None): # options の略
#   """
#   plot_options 辞書を編集し、キーワード引数で指定された項目を上書きします。
#   'yaxis_opt' に 'legend_names' が存在しない場合は空のリストとして追加します。

#   Args:
#     plot_options (dict): 編集対象の plot_options 辞書
#     y_label (str, optional): y軸ラベル (yaxis_opt -> axis_label). Defaults to None.
#     ylog (bool, optional): y軸タイプ (yaxis_opt -> y_axis_type). Defaults to None.
#     y_range (list, optional): y軸レンジ (yaxis_opt -> y_range). Defaults to None.
#     axis_subtitle (str, optional): y軸サブタイトル (yaxis_opt -> axis_subtitle). Defaults to None.
#     z_range (list, optional): z軸レンジ (zaxis_opt -> z_range). Defaults to None.
#     zlog (bool, optional): z軸タイプ (zaxis_opt -> z_axis_type). Defaults to None.
#     spec (int, optional): spec 値 (extras -> spec). Defaults to None.
#     colormap (list, optional): colormap (extras -> colormap). Defaults to None.
#     legend_names (list, optional): legend_names (yaxis_opt -> legend_names). Defaults to None.
#     line_color (str, optional): line_color (line_opt -> line_color). Defaults to None.
#     line_width (int, optional): line_width (line_opt -> line_width). Defaults to None.
#     line_style (str, optional): line_style (line_opt -> line_style). Defaults to None.
#   Returns:
#     dict: 編集後の plot_options 辞書
#   """
#   data = data_quants[variable_name]
#   plot_options = data.plot_options


#   # extras の編集
#   if 'extras' not in plot_options:
#     plot_options['extras'] = {}
#   if 'extras' in plot_options and isinstance(plot_options['extras'], dict):
#     if 'spec' not in plot_options['extras']:
#       # もしdata.spec_binsが存在しない場合はspec=0
#       if hasattr(data, 'spec_bins'): 
#         plot_options['extras']['spec'] = 1
#       else:
#         plot_options['extras']['spec'] = 0
#     if 'colormap' not in plot_options['extras']:
#       plot_options['extras']['colormap'] = ['turbo']
#     if spec is not None:
#       plot_options['extras']['spec'] = spec
#     if colormap is not None:
#       plot_options['extras']['colormap'] = [colormap]

#   # yaxis_opt の編集
#   if 'yaxis_opt' not in plot_options:
#     plot_options['yaxis_opt'] = {}
#   if 'yaxis_opt' in plot_options and isinstance(plot_options['yaxis_opt'], dict):
#     if 'legend_names' not in plot_options['yaxis_opt']:
#       plot_options['yaxis_opt']['legend_names'] = []
#     if 'y_axis_type' not in plot_options['yaxis_opt']:
#       plot_options['yaxis_opt']['y_axis_type'] = 0
#     if 'axis_label' not in plot_options['yaxis_opt']:
#       plot_options['yaxis_opt']['axis_label'] = ''
#     if 'y_range' not in plot_options['yaxis_opt']:
#       if not hasattr(data, 'spec_bins'):
#         plot_options['yaxis_opt']['y_range'] = [data.min(), data.max()]
#       else:
#         plot_options['yaxis_opt']['y_range'] = [data.spec_bins.values.min(), data.spec_bins.values.max()]
#     if 'axis_subtitle' not in plot_options['yaxis_opt']:
#       plot_options['yaxis_opt']['axis_subtitle'] = ''
#     if 'legend_names' in plot_options['yaxis_opt']:
#       plot_options['yaxis_opt']['legend_names'] = legend_names
#     if y_label is not None:
#       plot_options['yaxis_opt']['axis_label'] = y_label
#     if ylog is not None:
#       plot_options['yaxis_opt']['y_axis_type'] = ylog
#     if y_range is None:
#       if plot_options['extras']['spec'] == 0:
#         plot_options['yaxis_opt']['y_range'] = [data.min(), data.max()]
#       if plot_options['extras']['spec'] == 1:
#         plot_options['zaxis_opt']['z_range'] = [data.spec_bins.values.min(), data.spec_bins.values.max()]
#     if y_range is not None:
#       plot_options['yaxis_opt']['y_range'] = y_range
#     if y_sublabel is not None:
#       plot_options['yaxis_opt']['axis_subtitle'] = y_sublabel

#   # zaxis_opt の編集
#   if 'zaxis_opt' not in plot_options:
#     plot_options['zaxis_opt'] = {}
#   if 'zaxis_opt' in plot_options and isinstance(plot_options['zaxis_opt'], dict):
#     if 'z_range' not in plot_options['zaxis_opt']:
#       if hasattr(data, 'spec_bins'):
#         plot_options['zaxis_opt']['z_range'] = [data.spec_bins.values.min(), data.spec_bins.values.max()]
#       else:
#         plot_options['zaxis_opt']['z_range'] = [0, 1]
#     if 'z_axis_type' not in plot_options['zaxis_opt']:
#       plot_options['zaxis_opt']['z_axis_type'] = 0
#     if 'axis_label' not in plot_options['zaxis_opt']:
#       plot_options['zaxis_opt']['axis_label'] = ''
#     if 'axis_subtitle' not in plot_options['zaxis_opt']:
#       plot_options['zaxis_opt']['axis_subtitle'] = ''
#     if z_range is not None:
#       plot_options['zaxis_opt']['z_range'] = z_range
#     if zlog is not None:
#       plot_options['zaxis_opt']['z_axis_type'] = zlog
#     if z_sublabel is not None:
#       plot_options['zaxis_opt']['axis_subtitle'] = z_sublabel
#     if z_label is not None:
#       plot_options['zaxis_opt']['axis_label'] = z_label

#   if 'line_opt' not in plot_options:
#     plot_options['line_opt'] = {}
#   if 'line_opt' in plot_options and isinstance(plot_options['line_opt'], dict):
#     if 'line_color' not in plot_options['line_opt']:
#       plot_options['line_opt']['line_color'] = line_color
#     if 'line_width' not in plot_options['line_opt']:
#       plot_options['line_opt']['line_width'] = line_width
#     if 'line_style' not in plot_options['line_opt']:
#       plot_options['line_opt']['line_style'] = line_style
#     if 'line_color' in plot_options['line_opt']:
#       plot_options['line_opt']['line_color'] = line_color
#     if 'line_width' in plot_options['line_opt']:
#       plot_options['line_opt']['line_width'] = line_width
#     if 'line_style' in plot_options['line_opt']:
#       plot_options['line_opt']['line_style'] = line_style

#   return

def op(variable_name,
       y_label=None, ylog=None, y_range=None, y_sublabel=None,
       z_range=None, zlog=None, z_sublabel=None, z_label=None,
       spec=None, colormap=None, legend_names=None,
       line_color=None, line_width=None, line_style=None):
    """
    plot_options 辞書を編集し、キーワード引数で指定された項目を上書きします。
    特別に、line_opt は存在しない場合は新規作成します。
    """
    data = data_quants[variable_name]
    plot_options = data.plot_options

    # extras の編集（存在する場合のみ）
    if 'extras' in plot_options and isinstance(plot_options['extras'], dict):
        if spec is not None:
            plot_options['extras']['spec'] = spec
        if colormap is not None:
            plot_options['extras']['colormap'] = [colormap]

    # yaxis_opt の編集（存在する場合のみ）
    if 'yaxis_opt' in plot_options and isinstance(plot_options['yaxis_opt'], dict):
        if legend_names is not None:
            plot_options['yaxis_opt']['legend_names'] = legend_names
        if y_label is not None:
            plot_options['yaxis_opt']['axis_label'] = y_label
        if ylog is not None:
            plot_options['yaxis_opt']['y_axis_type'] = ylog
        if y_range is not None:
            plot_options['yaxis_opt']['y_range'] = y_range
        if y_sublabel is not None:
            plot_options['yaxis_opt']['axis_subtitle'] = y_sublabel

    # zaxis_opt の編集（存在する場合のみ）
    if 'zaxis_opt' in plot_options and isinstance(plot_options['zaxis_opt'], dict):
        if z_range is not None:
            plot_options['zaxis_opt']['z_range'] = z_range
        if zlog is not None:
            plot_options['zaxis_opt']['z_axis_type'] = zlog
        if z_sublabel is not None:
            plot_options['zaxis_opt']['axis_subtitle'] = z_sublabel
        if z_label is not None:
            plot_options['zaxis_opt']['axis_label'] = z_label

    # line_opt の編集（存在しない場合は作成する）
    if 'line_opt' not in plot_options:
        plot_options['line_opt'] = {}
    if isinstance(plot_options['line_opt'], dict):
        if line_color is not None:
            plot_options['line_opt']['line_color'] = line_color
        if line_width is not None:
            plot_options['line_opt']['line_width'] = line_width
        if line_style is not None:
            plot_options['line_opt']['line_style'] = line_style

    return


def initialize_plot_options(variable_name):
    """
    data_quants[variable_name] に plot_options とその下層キーを、
    存在しないものだけ空値で初期化する。
    """
    data = data_quants[variable_name]

    # plot_options 自体の初期化
    if not hasattr(data, 'plot_options') or not isinstance(data.plot_options, dict):
        data.plot_options = {}

    plot_options = data.plot_options

    # extras の初期化
    plot_options.setdefault('extras', {})
    extras_defaults = {
        'spec': None,       # int or None
        'colormap': ['turbo']      # list
    }
    for key, default in extras_defaults.items():
        plot_options['extras'].setdefault(key, default)

    # yaxis_opt の初期化
    plot_options.setdefault('yaxis_opt', {})
    yaxis_defaults = {
        'axis_label': '',           # str
        'y_axis_type': None,        # bool
        'y_range': None,            # list
        'axis_subtitle': '',        # str
        'legend_names': []          # list
    }
    for key, default in yaxis_defaults.items():
        plot_options['yaxis_opt'].setdefault(key, default)

    # zaxis_opt の初期化
    plot_options.setdefault('zaxis_opt', {})
    zaxis_defaults = {
        'z_range': None,            # list
        'z_axis_type': None,        # bool
        'axis_label': '',           # str
        'axis_subtitle': ''         # str
    }
    for key, default in zaxis_defaults.items():
        plot_options['zaxis_opt'].setdefault(key, default)

"""     # line_opt の初期化
    plot_options.setdefault('line_opt', {})
    line_defaults = {
        'line_color': None,         # str
        'line_width': None,         # int
        'line_style': ''            # str
    }
    for key, default in line_defaults.items():
        plot_options['line_opt'].setdefault(key, default)
 """
from pyspedas import store_data
def sd(variable_name, data): # store_data の略
    store_data(variable_name, data=data)
    data = data_quants[variable_name]
    if hasattr(data, 'spec_bins'):
        op(variable_name, ylog=1, zlog=1, y_range=[data.spec_bins.values.min(), data.spec_bins.values.max()], z_range=[data.values.min(), data.values.max()])
    else:
        op(variable_name, ylog=0, y_range=[data.min(), data.max()])

def split_vec(variable):
    data = data_quants[variable]
    data.shape[1]
    for i in range(data.shape[1]):
        data_temp = data[:,i]
        sd('{}_{}'.format(variable, i), data={'x': data['time'], 'y': data_temp})

import io
import contextlib
from pyspedas import tplot_names

def xlim(tr):
    with contextlib.redirect_stdout(io.StringIO()):
        tplot_list = tplot_names()
    for i in range(len(tplot_list)):
        key = tplot_list[i]
        try:
            data = data_quants[key]
            plot_options = data.plot_options  # ここで AttributeError チェック
        except KeyError:
            # print('no such key in data_quants: {}'.format(key))
            continue
        except AttributeError:
            # print('no plot_options: {}'.format(key))
            continue
        
        initialize_plot_options(key)
        plot_options['trange'] = tr
        data = data.sel(time=slice(tr[0], tr[1]))  # 時間範囲でデータをスライス
        try:
            if hasattr(data, 'spec_bins'):
                if data.plot_options['extras']['spec'] == 1:
                    y_bins = data.spec_bins.values
                    cleaned_data = y_bins[np.isfinite(y_bins)]
                    if cleaned_data.size == 0:
                        print("No finite values found in {} data.".format(key))
                    data.plot_options['yaxis_opt']['y_range'] = [cleaned_data.min(), cleaned_data.max()]
                    cleaned_data = data.values[np.isfinite(data.values)]
                    if cleaned_data.size == 0:
                        print("No finite values found in {} data.".format(key))
                    data.plot_options['zaxis_opt']['z_range'] = [cleaned_data.min(), cleaned_data.max()] 
                elif data.plot_options['extras']['spec'] == 0:
                    cleaned_data = data.values[np.isfinite(data.values)]
                    if cleaned_data.size == 0:
                        print("No finite values found in {} data.".format(key))
                    data.plot_options['yaxis_opt']['y_range'] = [cleaned_data.min()*0.9, cleaned_data.max()*1.1]
                    # print(cleaned_data.min(), cleaned_data.max())

            else:
                cleaned_data = data.values[np.isfinite(data.values)]
                if cleaned_data.size == 0:
                    print("No finite values found in {} data.".format(key))
                data.plot_options['yaxis_opt']['y_range'] = [cleaned_data.min()*0.9, cleaned_data.max()*1.1]
        except Exception as e:
            print(f"Error processing {key}: {e}")
            continue