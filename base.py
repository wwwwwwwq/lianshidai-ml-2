# -*- coding: utf-8 -*-

#量子矩阵类
class QuantumMatrix:
    #定义__init__魔法方法，用于初始化量子矩阵
    def __init__(self, data):
        """
        初始化量子矩阵
        """
        """
        data为二维列表，每个元素为tuple，形式是（数字，字符）
        例如QuantumMatrix([
        [(2.5, 'α'), (-1.8, 'β')],
        [(0.9, 'γ'), (4.2, 'δ')]
        ])
        则表示量子矩阵为
        （2.5，α） （-1.8，β）
        （0.9 ，γ） （4.2，δ）
        （注意量子矩阵和普通矩阵不同，量子矩阵的每个区域是有一个数字和一个字符的）
        所以行数为data的长度，列数为data中每个元素的长度
        """
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0#判断是否非零
    
    #self是类的实例本身，other是传入的参数，other: 'QuantumMatrix'表示other的类型是QuantumMatrix，-> 'QuantumMatrix'表示返回值的类型是QuantumMatrix
    #这里的self就是量子矩阵a本身，而other其实就传入另外一个要相乘的量子矩阵b
    def multiply(self, other: 'QuantumMatrix') -> 'QuantumMatrix':
        """
        矩阵乘法
        """
        #判断矩阵是否可以相乘，也就是检查维度是否匹配
        #如果a的列数≠b的行数，则抛出时空撕裂异常
        if self.cols != other.rows:
            raise QuantumDimensionError("时空撕裂异常 QuantumDimensionError ⚠️")
        
        """
        这里简述一下量子矩阵乘法的运算过程。举一个例子：
        矩阵a：
        （2.5，α） （-1.8，β）
        （0.9 ，γ） （4.2，δ）
        矩阵b：
        （1.1，ε） （2.3，ζ）
        （-0.5，η） （3.4，θ）
        
        a的第一行，b的第一列（i=0,j=0）：
        结果矩阵的(1,1)=a的第一行，b的第一列
        数字运算：(2.5×1.1)+(-1.8×-0.5)=2.75+0.9=3.65
        字符运算：从 α, β, ε, η 中选择ASCII码最大的，记作max_char1

        a的第一行，b的第二列（i=0,j=1）：
        结果矩阵的(1,2)=a的第一行，b的第二列
        数字运算：(2.5×2.3)+(-1.8×3.4)=5.75-6.12=-0.37
        字符运算：从 α, β, ε, ζ 中选择ASCII码最大的，记作max_char2

        a的第二行，b的第一列（i=1,j=0）：
        结果矩阵的(2,1)=a的第二行，b的第一列
        数字运算：(0.9×1.1)+(4.2×-0.5)=0.99-2.1=-1.11
        字符运算：从 γ, δ, ε, η 中选择ASCII码最大的，记作max_char3

        a的第二行，b的第二列（i=1,j=1）：
        结果矩阵的(2,2)=a的第二行，b的第二列
        数字运算：(0.9×2.3)+(4.2×3.4)=2.07+14.28=16.35
        字符运算：从 γ, δ, ζ, θ 中选择ASCII码最大的，记作max_char4

        所以说，我们应该先遍历a的每一行，再遍历b的每一列，然后在b的每一列下面遍历a的每一列，并进行数字运算和字符运算，最后将结果存储到结果矩阵中。
        所以说，应该会有三重循环，并且我们需要在遍历b列时定义一个数字的和num_sum，一个字符的ascii码的最大值max_char
        """
        #这里用O(n^3)的时间复杂度实现矩阵乘法（因为好像一般矩阵乘法都是O(n^3)）
        #初始化结果矩阵
        result=[]
        #因为矩阵的乘法是a的行乘以b的列，所以需要遍历a的行和b的列
        for i in range(self.rows):#遍历矩阵a的每一行
            row=[]#初始化当前行
            for j in range(other.cols):#遍历矩阵b的每一列
                num_sum=0#初始化数字部分的和
                max_char=''#初始化字符部分，找到ASCII码最大的字符
                for k in range(self.cols):#遍历矩阵a的每一列，对应到b的每一行
                    num_sum+=self.data[i][k][0]*other.data[k][j][0]#数字运算
                    #找到最大ASCII码的字符
                    char1=self.data[i][k][1]#对应a的字符
                    char2=other.data[k][j][1]#对应b的字符
                    #ord()函数返回字符的ASCII码
                    cur_max=char1 if ord(char1)>ord(char2) else char2#当前两个字符的ASCII码最大值
                    max_char=cur_max if not max_char or ord(cur_max)>ord(max_char) else max_char#更新当前4个元素的最大ASCII码字符

                row.append((num_sum,max_char))#将计算的数字和字符结果添加到当前行
            result.append(row)#将当前行添加到结果矩阵
        return QuantumMatrix(result)#返回结果矩阵
    
    #这里再定义一个__str__魔法方法，用于打印量子矩阵
    def __str__(self):
        #这里是先将每一行的数据拿出来，每一行的每一个数据用' '连接，也就是大概变成(1,a) (2,b)这样的形式，然后每一行之间用换行符'\n'隔开
        #大概的形式是：
        """
        (1,a) (2,b)
        (3,c) (4,d)
        """
        return '\n'.join([' '.join(f'({v:.2f},{c})' for v,c in row) for row in self.data])
 
        
#定义时空撕裂异常类
class QuantumDimensionError(Exception):
    pass

#测试部分
def test():
    #硬编码测试的样例
    matrix_a=QuantumMatrix([
        [(2.5,'a'),(-1.8,'b')],
        [(0.9,'c'),(4.2,'d')]
    ])
    
    matrix_b=QuantumMatrix([
        [(1.1,'e'),(2.3,'f')],
        [(-0.5,'g'),(3.4,'h')]
    ])
    
    #用try，except来捕获异常
    try:
        #打印量子矩阵，共使用者看到
        print("量子矩阵a：")
        print(matrix_a)
        print("量子矩阵b：")
        print(matrix_b)

        #计算矩阵乘法
        result=matrix_a.multiply(matrix_b)
        print("矩阵乘法结果：")
        print(result)
    except QuantumDimensionError as e:
        print(e)

#主体部分
def main():
    #输入量子矩阵a
    print("请输入量子矩阵a: ")
    rows=int(input("请输入a的行数: "))
    cols=int(input("请输入a的列数: "))
    #存储输入到a中的数据
    data_a=[]
    for i in range(rows):
        #初始化a的当前行
        row=[]
        for j in range(cols):
            #输入a的当前行，当前列的数字和字符
            #由于下标是0开始，所以需要i+1和j+1
            num,char=input(f"请输入第{i+1}行第{j+1}列的数字和字符: ").split()
            #将数字转化为浮点数，并添加到当前行
            row.append((float(num),char))
        #将当前行添加到data中
        data_a.append(row)
    #输入量子矩阵b
    print("请输入量子矩阵b: ")
    rows=int(input("请输入b的行数: "))
    cols=int(input("请输入b的列数: "))
    #存储输入到b中的数据
    data_b=[]
    for i in range(rows):
        #初始化b的当前行
        row=[]
        for j in range(cols):
            #输入b的当前行，当前列的数字和字符
            num,char=input(f"请输入第{i+1}行第{j+1}列的数字和字符: ").split()
            #将数字转化为浮点数，并添加到当前行
            row.append((float(num),char))
        #将当前行添加到data中
        data_b.append(row)
    #创建量子矩阵a和b
    matrix_a=QuantumMatrix(data_a)
    matrix_b=QuantumMatrix(data_b)
    #计算矩阵乘法
    result = matrix_a.multiply(matrix_b)
    #打印结果
    print("矩阵乘法结果：")
    print(result)
            

#还是和第一题一样，如果直接运行这个文件，就会执行下面的代码
#如果是作为模块导入，就不会执行下面的代码
if __name__ == '__main__':
    #运行主体部分
    main()
