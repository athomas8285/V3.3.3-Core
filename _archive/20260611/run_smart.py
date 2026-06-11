import subprocess, sys, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print("=" * 60)
    print("  V3.3.3-Core-Rev1.15 一键全流程（含智能因子）")
    print("=" * 60)

    # Step 1: 智能生成因子参数
    print("\n  [1] 智能生成因子参数...")
    r1 = subprocess.run([sys.executable, os.path.join(BASE_DIR, "smart_factors.py")],
                         capture_output=False, cwd=BASE_DIR)
    if r1.returncode != 0:
        print("  [ERROR] 因子参数生成失败")
        return

    # Step 2: 运行全流程
    print("\n  [2] 运行全流程分析...")
    r2 = subprocess.run([sys.executable, os.path.join(BASE_DIR, "auto_pipeline.py")],
                         capture_output=False, cwd=BASE_DIR)
    if r2.returncode != 0:
        print("  [ERROR] 全流程分析失败")
        return

    print("\n  [OK] 一键全流程完成")


if __name__ == "__main__":
    main()
