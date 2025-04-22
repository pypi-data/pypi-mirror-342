# 本代码适用于25年3月的纵缝提取
import numpy as np
import zelas2.shield as zs
import multiprocessing as mp
from tqdm import tqdm
import cv2

def find_continuous_segments_numpy(arr):
    """
    找到一维数组中所有连续整数段的起始和终止数，返回 NumPy 数组
    :param arr: 一维整数数组（已排序）
    :return: NumPy 数组，每行为 (起始数, 终止数)
    """
    segments = []  # 存储所有连续段
    start = arr[0]  # 当前连续段的起始数
    for i in range(1, len(arr)):
        if arr[i] != arr[i - 1] + 1:  # 检测中断点
            segments.append((start, arr[i - 1]))  # 保存当前连续段
            start = arr[i]  # 开始新的连续段
    # 添加最后一个连续段
    segments.append((start, arr[-1]))
    # 转换为 NumPy 数组
    return np.array(segments, dtype=int)

def get_ρθ(xz_p, xzr):
    '求每个盾构环的极径差和反正切'
    num_p = len(xz_p)  # 当前截面点数量
    ρ = np.sqrt((xz_p[:,0]-xzr[0])**2+(xz_p[:,1]-xzr[1])**2)-xzr[2]
    θ = np.empty(num_p)
    for i in range(num_p):
        θ[i] = zs.get_angle(xz_p[i,0],xz_p[i,1],xzr[0],xzr[1])
    return np.c_[ρ,θ]

def find_seed(θyρvci,ρ_td,r,cpu=mp.cpu_count(),c_ignore=4):
    '寻找符合纵缝特征的种子点'
    θyρvci_up = θyρvci[θyρvci[:,2]>=ρ_td,:]  # 低于衬砌点的不要
    # 准备工作
    pool = mp.Pool(processes=cpu)  # 开启多进程池，数量为cpu
    c_un = np.unique(θyρvci[:,4])
    num_c = len(np.unique(θyρvci[:,4]))  # 截面数
    # good_index = []
    # 并行计算
    multi_res = pool.starmap_async(find_seed_cs, ((θyρvci,np.uint64(θyρvci_up[θyρvci_up[:,4]==c_un[i],5]),c_un[i],r,c_ignore) for i in
                 tqdm(range(num_c),desc='分配任务寻找种子点',unit='个截面',total=num_c)))
    j = 0
    for res in tqdm(multi_res.get(),total=num_c,desc='输出种子点下标'):
        if j==0:
            good_index = res
        else:
            good_index = np.hstack((good_index, res))
        j += 1
    pool.close()  # 关闭所有进程
    pool.join()  # 当所有进程全部计算完毕后，退出并行计算
    return np.int64(good_index)


def find_seed_cs(θyρvci,id_θyρvci_up_c,c,r,c_ignore=4):
    '''
    寻找单个截面符合纵缝特征的种子点
    θyρvci : 点云信息
    id_θyρvci_up_c ：符合搜索的点云下标
    c ：当前截面
    r :当前截面半径
    c_ignore ：忽略的截面数
    '''
    good_ind = []  # 空下标
    θ_l_td = 0.15 * np.pi * r / 180
    for i in id_θyρvci_up_c:
        if θyρvci[i,3]==0:  # 如果当前点为线特征
            # 找到搜索截面
            θyρ_c_ = θyρvci[θyρvci[:, 4] <= c + c_ignore, :]
            θyρ_c_ = θyρ_c_[θyρ_c_[:, 4] >= c - c_ignore, :]
            # 判断左侧是否有球特征
            θ_l_ = θyρvci[i,0] - θ_l_td  # 左侧角度阈值
            θyρ_l_ = θyρ_c_[θyρ_c_[:, 0] < θyρvci[i, 0], :]
            θyρ_l_ = θyρ_l_[θyρ_l_[:, 0] >= θ_l_, :]
            # 判断右侧是否有球特征
            θ_r_ = θyρvci[i,0] + θ_l_td  # 右侧角度阈值
            θyρ_r_ = θyρ_c_[θyρ_c_[:, 0] > θyρvci[i, 0], :]
            θyρ_r_ = θyρ_r_[θyρ_r_[:, 0] <= θ_r_, :]
            if 2 in θyρ_l_[:, 3] and 2 in θyρ_r_[:, 3]:  # 如果左右都有球特征
                good_ind.append(θyρvci[i,5])  # 作为种子点
    return good_ind

def distance_to_line(point, line):
    """计算点到直线的几何距离"""
    x0, y0 = point
    x1, y1, x2, y2 = line
    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominator = np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
    return numerator / denominator if denominator != 0 else 0

def merge_similar_lines(lines, angle_thresh=np.pi / 18, rho_thresh=20):
    """合并相似直线（极坐标参数相近的线段）"""
    merged = []
    for line in lines:
        rho, theta = line_to_polar(line[0])
        found = False
        for m in merged:
            m_rho, m_theta = m[0]
            # 检查角度和距离差异
            if abs(theta - m_theta) < angle_thresh and abs(rho - m_rho) < rho_thresh:
                m[0] = ((m_rho + rho) / 2, (m_theta + theta) / 2)  # 合并平均值
                m[1].append(line)
                found = True
                break
        if not found:
            merged.append([(rho, theta), [line]])

    # 转换回线段格式（取合并后的极坐标生成新线段）
    merged_lines = []
    for m in merged:
        rho, theta = m[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        # 生成足够长的线段（覆盖图像范围）
        scale = 1000
        x1 = int(x0 + scale * (-b))
        y1 = int(y0 + scale * (a))
        x2 = int(x0 - scale * (-b))
        y2 = int(y0 - scale * (a))
        merged_lines.append([x1, y1, x2, y2])

    return merged_lines[:5]  # 最多返回前5条

def find_lines(θy):
    '通过数字图像操作将纵缝找到并返回种子点'
    '0.整理数据'
    θy = θy*100
    θy[:, 0] -= np.min(θy[:, 0])
    θy[:, 1] -= np.min(θy[:, 1])
    θy = np.uint64(θy)
    x_max = np.max(θy[:,0])
    y_max = np.max(θy[:,1]) # 求边界
    print('二维边长',x_max,y_max)
    '1.创建图像'
    img = np.zeros((int(y_max)+1, int(x_max)+1), dtype=np.uint8)
    for x,y in θy:
        img[y, x] = 255
    '''
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    '2.直线检测'
    # 霍夫变换检测直线
    lines = cv2.HoughLinesP(img, rho=1, theta=np.pi / 180, threshold=50, minLineLength=50, maxLineGap=50)  # 检测单位像素、角度、超过像素阈值、最小长度阈值、最大间断阈值
    # --- 提取前5条最长的直线 ---
    detected_lines = []
    if lines is not None:
        lines = lines[:, 0, :]
        # 按线段长度排序（从最长到最短）
        lines = sorted(lines, key=lambda x: np.linalg.norm(x[2:] - x[:2]), reverse=True)[:6]
        detected_lines = lines
    threshold_distance = 2.0  # 点到直线的最大允许距离（根据噪声调整）
    # 初始化：所有点标记为未分配
    assigned = np.zeros(len(θy), dtype=bool)
    line_points_list = []  # 存储每条直线的点
    line_indices_list = []  # 存储每条直线的点索引
    for line in detected_lines:
        distances = np.array([distance_to_line(p, line) for p in θy])
        # 筛选未分配且距离小于阈值的点
        mask = (distances < threshold_distance) & ~assigned
        line_points = θy[mask]
        line_points_list.append(line_points)
        indices = np.where(mask)[0]
        line_indices_list.append(indices)
        assigned |= mask  # 标记已分配的点
    # 合并前5条直线的点
    all_line_points = np.vstack(line_points_list)
    # 分离噪声点
    noise_points = θy[~assigned]
    '''
    # --- 可视化结果 ---
    # 创建彩色图像用于显示
    result_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # 绘制检测到的直线（绿色）
    for line in detected_lines:
        x1, y1, x2, y2 = line
        cv2.line(result_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # 绘制属于直线的点（红色）
    for p in all_line_points:
        cv2.circle(result_img, tuple(p), 2, (0, 0, 255), -1)
    '''
    '''
        # 预定义5种颜色（BGR格式）
    colors = [
        (0, 0, 255),   # 红色
        (0, 255, 0),   # 绿色
        (255, 0, 0),   # 蓝色
        (0, 255, 255), # 黄色
        (255, 0, 255)  # 品红色
    ]
    # 绘制每条直线及其对应的点
    for i, (line, line_points) in enumerate(zip(detected_lines, line_points_list)):
        color = colors[i % len(colors)]  # 循环使用颜色列表
        # 绘制直线
        x1, y1, x2, y2 = line
        cv2.line(result_img, (x1, y1), (x2, y2), color, 2)
    '''
    '''
    # 绘制噪声点（蓝色）
    for p in noise_points:
        cv2.circle(result_img, tuple(p.astype(int)), 2, (255, 0, 0), -1)
    cv2.imshow("Result", result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    # 去除 line_indices_list 中的空元素
    line_indices_list = [indices for indices in line_indices_list if len(indices) > 0]
    return line_indices_list


def merge_similar_lines(lines, angle_thresh=5, dist_thresh=10):
    """
    合并角度和位置相近的线段
    :param lines: 线段列表，格式为 [[x1,y1,x2,y2], ...]
    :param angle_thresh: 角度差阈值（度）
    :param dist_thresh: 线段中心点距离阈值（像素）
    :return: 合并后的线段列表
    """
    merged = []
    for line in lines:
        x1, y1, x2, y2 = line
        # 计算线段角度（弧度）
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        # 计算线段中心点
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

        # 检查是否与已合并线段近似
        found = False
        for m in merged:
            m_angle, m_cx, m_cy = m['angle'], m['cx'], m['cy']
            # 角度差和中心点距离
            angle_diff = abs(angle - m_angle)
            dist = np.sqrt((cx - m_cx) ** 2 + (cy - m_cy) ** 2)

            if angle_diff < angle_thresh and dist < dist_thresh:
                # 合并线段（延长端点）
                m['x1'] = min(m['x1'], x1, x2)
                m['y1'] = min(m['y1'], y1, y2)
                m['x2'] = max(m['x2'], x1, x2)
                m['y2'] = max(m['y2'], y1, y2)
                found = True
                break

        if not found:
            merged.append({
                'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                'angle': angle, 'cx': cx, 'cy': cy
            })
    # 转换为坐标格式
    return [[m['x1'], m['y1'], m['x2'], m['y2']] for m in merged]


def fit_3d_line(points):
    """
    Fit a 3D line to a point cloud using PCA.
    Parameters:
    points (numpy.ndarray): Nx3 array of 3D points.
    Returns:
    tuple: (centroid, direction_vector)
        centroid is a point on the line (numpy.ndarray of shape (3,)),
        direction_vector is the direction vector of the line (numpy.ndarray of shape (3,)).
    """
    # 计算点云的质心
    centroid = np.mean(points, axis=0)
    # 将点云中心化
    centered_points = points - centroid
    # 计算协方差矩阵
    cov_matrix = np.cov(centered_points.T)
    # 计算协方差矩阵的特征值和特征向量
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    # 找到最大特征值对应的特征向量作为方向向量
    direction_vector = eigenvectors[:, np.argmax(eigenvalues)]
    # Centroid (a point on the line): [1.5 1.5 1.5]
    # Direction vector: [0.57735027 0.57735027 0.57735027]
    return centroid, direction_vector


def distance_to_line_3D(points, centroid, direction):
    """
    计算点到三维直线的距离。
    Parameters:
    points (numpy.ndarray): Nx3 的3D点。
    centroid (numpy.ndarray): 直线上的一点，形状为 (3,)。
    direction (numpy.ndarray): 直线的单位方向向量，形状为 (3,)。
    Returns:
    numpy.ndarray: 每个点到直线的距离，形状为 (N,)。
    """
    # 计算点与质心的向量差
    vec = points - centroid
    # 计算叉乘 (支持批量计算)
    cross_product = np.cross(vec, direction)
    # 距离为叉乘的模长
    distances = np.linalg.norm(cross_product, axis=1)
    return distances