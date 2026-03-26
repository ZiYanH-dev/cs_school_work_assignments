import os
import sys
import re
import subprocess

def get_corresponding_output(input_filename):
    """
    把 input 开头替换成 output，其余完全不变
    input_abc_123.txt → output_abc_123.txt
    input1.txt        → output1.txt
    """
    if not input_filename.startswith("input"):
        return None
    return "output" + input_filename[5:]  # 去掉 "input"，换成 "output"

def main():
    if len(sys.argv) != 2:
        print(f"用法: python {sys.argv[0]} <lab目录>")
        print(f"示例: python {sys.argv[0]} ./lab1")
        sys.exit(1)

    lab_dir = sys.argv[1]

    # 找 cpp
    cpp_files = [f for f in os.listdir(lab_dir) if f.endswith(".cpp")]
    if not cpp_files:
        print(f"❌ {lab_dir} 下没有 .cpp 文件")
        return
    cpp_path = os.path.join(lab_dir, cpp_files[0])
    exe_path = os.path.splitext(cpp_path)[0]

    # 找测试目录 testcase / testcases
    test_dir = None
    for cand in ["testcase", "testcases"]:
        d = os.path.join(lab_dir, cand)
        if os.path.isdir(d):
            test_dir = d
            break
    if not test_dir:
        print("❌ 未找到 testcase 或 testcases 目录")
        return

    print(f"📁 测试目录: {test_dir}")

    # 编译
    print("\n1. 编译中...")
    comp = subprocess.run(
        ["g++", cpp_path, "-o", exe_path],
        capture_output=True, text=True
    )
    if comp.returncode != 0:
        print("❌ 编译失败")
        print(comp.stderr)
        return
    print("✅ 编译成功")

    # 收集所有 input 文件
    input_files = [
        f for f in os.listdir(test_dir)
        if f.startswith("input") and f.endswith(".txt")
    ]
    if not input_files:
        print("\n⚠️ 没有 input 文件")
        return

    # 按文件名排序
    input_files.sort()

    total = len(input_files)
    passed = 0

    print(f"\n2. 开始测试（共 {total} 组）\n")

    for input_fname in input_files:
        output_fname = get_corresponding_output(input_fname)
        input_path  = os.path.join(test_dir, input_fname)
        output_path = os.path.join(test_dir, output_fname)
        actual_path = os.path.join(test_dir, f"actual_{input_fname}")

        print(f"=== 测试 {input_fname} ===")

        if not os.path.exists(output_path):
            print(f"⚠️  对应输出 {output_fname} 不存在，跳过\n")
            continue

        # 运行程序
        with open(input_path, "r") as fin, open(actual_path, "w") as fout:
            subprocess.run(["./" + exe_path], stdin=fin, stdout=fout, stderr=fout)

        # 对比（忽略首尾空白换行）
        with open(actual_path, "r") as f:
            actual = f.read().strip()
        with open(output_path, "r") as f:
            expect = f.read().strip()

        if actual == expect:
            print("✅ PASS")
            passed += 1
        else:
            print("❌ FAIL")
            print("你的输出:")
            print(actual)
            print("预期输出:")
            print(expect)
        print()

    # 结果
    print("=" * 40)
    print("测试完成")
    print(f"总用例: {total}")
    print(f"通过:   {passed}")
    print(f"失败:   {total - passed}")
    print("=" * 40)

    # 清理
    if os.path.exists(exe_path):
        os.remove(exe_path)

if __name__ == "__main__":
    main()