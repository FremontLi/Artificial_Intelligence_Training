#引入依赖库
import time

# num = input()
# if int(num)<60:
#     print("不及格")
# elif int(num)<90:
#     print("良好")
# else:
#     print("优秀")


# def定义函数的关键字 函数名 （参数）:
def get_current_time():
    # 函数体
    l_time = time.localtime()
    str_time = time.strftime('%Y-%m-%d',l_time)
    print(l_time)
# 调用函数
get_current_time()