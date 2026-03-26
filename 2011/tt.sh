#!/bin/bash

# 仅传1个lab根目录参数
if [ $# -ne 1 ]; then
  echo "用法: $0 <lab根目录>"
  echo "示例: $0 ./lab1  或  $0 ./lab2"
  exit 1
fi

# 核心变量自动推导
LAB_ROOT="$1"
SOURCE_FILE=$(find "${LAB_ROOT}" -maxdepth 1 -name "*.cpp" | head -n1)
TESTCASE_DIR="${LAB_ROOT}/testcase"
EXECUTABLE="${SOURCE_FILE%.cpp}"

# 校验必要文件/目录
if [ -z "${SOURCE_FILE}" ]; then
  echo "❌ 在 ${LAB_ROOT} 下未找到 .cpp 源码文件"
  exit 1
fi
if [ ! -d "${TESTCASE_DIR}" ]; then
  echo "❌ ${LAB_ROOT} 下缺少 testcase 子目录"
  exit 1
fi

# Step 1: 编译程序
echo "1. 编译源码: ${SOURCE_FILE} → ${EXECUTABLE}..."
if ! g++ "${SOURCE_FILE}" -o "${EXECUTABLE}" 2> compile.err; then
  echo "❌ 编译失败！错误信息："
  cat compile.err && rm -f compile.err && exit 1
fi
rm -f compile.err
echo "✅ 编译成功"

# Step 2: 精准扫描+排序测试用例（核心修复）
echo -e "\n2. 扫描测试用例: ${TESTCASE_DIR}"
# 1. 只匹配 input+数字+.txt 格式（input1.txt/input2.txt...）
# 2. 按数字排序，避免乱序
INPUT_FILES=$(
  find "${TESTCASE_DIR}" -type f -name "input[0-9]*.txt" |
  sort -t 't' -k1.6n  # 按input后的数字排序（input1.txt→第6位开始是数字）
)
# 统计真实的用例数（去重+计数）
TOTAL=$(echo "${INPUT_FILES}" | wc -l | xargs)
PASSED=0

if [ "${TOTAL}" -eq 0 ]; then
  echo "⚠️ ${TESTCASE_DIR} 下未找到 input1.txt/input2.txt 等测试用例" && exit 0
fi
echo "🔍 找到 ${TOTAL} 个测试用例"

# Step 3: 执行测试（精准提取每个文件的编号）
for input in ${INPUT_FILES}; do
  # 精准提取编号：从input文件名中截取数字（input4.txt → 4）
  filename=$(basename "${input}")  # 拿到文件名（比如input4.txt）
  num=${filename#input}            # 去掉前缀input → 4.txt
  num=${num%.txt}                  # 去掉后缀.txt → 4

  # 拼接对应的输出文件
  expected="${TESTCASE_DIR}/output${num}.txt"
  actual="${TESTCASE_DIR}/actual_${num}.txt"

  echo -e "\n=== 测试用例 ${num} ==="
  echo "   输入文件: ${input}"
  echo "   预期输出: ${expected}"

  # 检查预期输出是否存在
  if [ ! -f "${expected}" ]; then
    echo "   ⚠️ 缺少 output${num}.txt → 跳过" && continue
  fi

  # 运行程序（重定向输入输出）
  ./"${EXECUTABLE}" < "${input}" > "${actual}" 2>&1

  # 对比输出（显示具体差异）
  if diff -q "${actual}" "${expected}" > /dev/null; then
    echo "   ✅ PASS"
    ((PASSED++))
  else
    echo "   ❌ FAIL"
    echo "   📝 输出差异（左侧=程序输出，右侧=预期输出）："
    diff -y --suppress-common-lines "${actual}" "${expected}"
  fi
done

# Step 4: 测试总结
echo -e "\n=== 测试总结 ==="
echo "Lab目录: ${LAB_ROOT}"
echo "总用例数: ${TOTAL} | 通过: ${PASSED} | 失败: $((TOTAL - PASSED))"

# 可选：清理临时输出文件
# rm -f "${TESTCASE_DIR}/actual_"*.txt