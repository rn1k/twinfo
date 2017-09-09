import joblib
import time

def streaming(base):
    # 結構時間かかる処理とする
    print("sleep{}".format(base))
    time.sleep(base/10000)
    print([base+i for i in range(10)])


def main():
    pass
    # results = joblib.Parallel(n_jobs=-1)([joblib.delayed(heavy_proc)(x) for x in range(1, int(5e4), 10000)])


if __name__ == '__main__':
    main()
