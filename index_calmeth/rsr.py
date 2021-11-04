import pandas as pd
import numpy as np
import bisect


class Rsr:
    """
    对传入的pd.dataframe数据进行rsr打分
    """

    def __init__(self, dataframe):
        """
        初始化：得到可用数据矩阵及其长宽数据
        """
        self.df = dataframe.copy()
        self.m, self.n = self.df.shape

    def score_matrix1(self, bv_list):
        """
        整次秩和比法计算得分，bv_list是由各指标正向最佳贡献值构成的列表
        注：所谓正向最佳贡献值，指的是从正面考虑指标贡献度时的最佳值。
           比如用不同指标合成金融风险指数(相较于安全而言是一个负面形容)，因此从正面考虑时对于正向指标其最佳值便是最低值，负向指标
           最佳值是最高值，适度指标由文献或前人研究来确定。
        """
        if len(bv_list) != self.n:
            print("重新考虑最佳贡献值列表元素数量")
        else:
            # 计算距离矩阵
            dist_matrix = pd.DataFrame(
                np.empty((self.m, self.n)), columns=self.df.columns)
            for j in range(self.n):
                for i in range(self.m):
                    dist_matrix.iloc[i, j] = np.abs(
                        self.df.iloc[i, j] - bv_list[j])
            # 计算打分矩阵
            rsr_matrix = pd.DataFrame(
                np.empty((self.m, self.n)), columns=self.df.columns)  # 创建与距离矩阵形状相同的空矩阵
            for q in range(self.n):
                for p in range(self.m):
                    compare_list = sorted(list(set(dist_matrix.iloc[:, q])))
                    rsr_matrix.iloc[p, q] = bisect.bisect_left(
                        compare_list, dist_matrix.iloc[p, q])
            score_matrix = rsr_matrix / self.m * 100
            return score_matrix

    def score_matrix2(self, bv_list):
        """
        非整次秩和比法计算得分，方法同上
        """
        if len(bv_list) != self.n:
            print("重新考虑最佳贡献值列表元素数量")
        else:
            # 计算距离矩阵
            dist_matrix = pd.DataFrame(
                np.empty((self.m, self.n)), columns=self.df.columns)
            for j in range(self.n):
                for i in range(self.m):
                    dist_matrix.iloc[i, j] = np.abs(
                        self.df.iloc[i, j] - bv_list[j])
            # 计算打分矩阵
            rsr_matrix = pd.DataFrame(
                np.empty((self.m, self.n)), columns=self.df.columns)  # 创建与距离矩阵形状相同的空矩阵
            for q in range(self.n):
                max_v = dist_matrix.iloc[:, q].max()
                min_v = dist_matrix.iloc[:, q].min()
                for p in range(self.m):
                    rsr_matrix.iloc[p, q] = 1 + ((self.m - 1) * (dist_matrix.iloc[p, q] - min_v) / (max_v - min_v))
            # 得分标准化
            score_matrix = pd.DataFrame(
                np.empty((self.m, self.n)), columns=self.df.columns)
            for q in range(self.n):
                max_v = rsr_matrix.iloc[:, q].max()
                min_v = rsr_matrix.iloc[:, q].min()
                for p in range(self.m):
                    score_matrix.iloc[p, q] = rsr_matrix.iloc[p, q] / (max_v - min_v) * 100
            score_matrix = score_matrix.fillna(0)
            return score_matrix
