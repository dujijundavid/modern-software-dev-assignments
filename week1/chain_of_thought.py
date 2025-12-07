"""
Chain of Thought (CoT) Prompting 实验脚本

本脚本设计了一个科学的对比实验框架，帮助你理解CoT的效果：
1. 对比5种不同的prompting策略
2. 测试多个问题验证泛化能力
3. 评估准确率和推理质量
4. 可视化展示实验结果

学习目标：
- 理解CoT为什么有效
- 区分"引导思考"和"答案泄露"
- 掌握设计有效CoT prompt的原则
"""

import os
import re
from dataclasses import dataclass
from typing import Callable
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 3  # 每个策略运行次数

# =============================================================================
# 实验问题定义
# =============================================================================

@dataclass
class Problem:
    """定义一个测试问题"""
    name: str
    question: str
    expected_answer: str
    difficulty: str  # easy, medium, hard


# 主问题：作业要求的问题
MAIN_PROBLEM = Problem(
    name="Modular Exponentiation (Main)",
    question="What is 3^12345 (mod 100)?",
    expected_answer="43",
    difficulty="hard"
)

# 额外测试问题（验证泛化能力）
EXTRA_PROBLEMS = [
    Problem(
        name="Simple Modular",
        question="What is 2^10 (mod 7)?",
        expected_answer="2",
        difficulty="easy"
    ),
    Problem(
        name="Medium Modular",
        question="What is 7^2023 (mod 13)?",
        expected_answer="11",
        difficulty="medium"
    ),
]

# =============================================================================
# 5种实验策略
# =============================================================================

# 策略A: Baseline - 无任何CoT引导
STRATEGY_A_BASELINE = """You are a mathematician. Answer math questions accurately.
Give your final answer on the last line as "Answer: <number>"."""

# 策略B: Zero-shot CoT - 只用魔法咒语
STRATEGY_B_ZERO_SHOT_COT = """You are a mathematician.
When solving problems, think through each step carefully.
Let's think step by step.
Give your final answer on the last line as "Answer: <number>"."""

# 策略C: Structured CoT - 给出推理框架但不给具体计算
STRATEGY_C_STRUCTURED_COT = """You are a mathematician skilled in modular arithmetic.

When solving modular exponentiation problems (a^n mod m):
1. ANALYZE: Identify the base (a), exponent (n), and modulus (m)
2. SIMPLIFY: Look for patterns or theorems to reduce the problem
3. CALCULATE: Perform the computation step by step
4. VERIFY: Check your answer makes sense

Show each step of your reasoning.
Give your final answer on the last line as "Answer: <number>"."""

# 策略D: Domain-Specific CoT - 提供领域知识但不直接应用
STRATEGY_D_DOMAIN_COT = """You are a mathematician skilled in modular arithmetic.

Useful theorems for modular exponentiation:
- Euler's Theorem: a^φ(n) ≡ 1 (mod n) when gcd(a,n)=1
- Euler's totient: φ(100) = 40, φ(13) = 12, φ(7) = 6
- For prime p: φ(p) = p-1 (Fermat's Little Theorem)

Approach:
1. Check if Euler's theorem or Fermat's Little Theorem applies
2. Find the cycle length using the totient function
3. Reduce the large exponent using: a^n ≡ a^(n mod φ(m)) (mod m)
4. Calculate the final result

Show your work step by step.
Give your final answer on the last line as "Answer: <number>"."""

# 策略E: Few-shot CoT - 用不同问题的示例展示推理过程
STRATEGY_E_FEW_SHOT_COT = """You are a mathematician. Here are examples of solving modular exponentiation:

Example 1: What is 5^100 mod 13?
Thinking:
- 13 is prime, so by Fermat's Little Theorem: 5^12 ≡ 1 (mod 13)
- 100 = 12 × 8 + 4
- So 5^100 ≡ 5^4 (mod 13)
- 5^4 = 625 = 48 × 13 + 1 = 625 - 624 = 1
Answer: 1

Example 2: What is 3^20 mod 7?
Thinking:
- 7 is prime, so by Fermat's Little Theorem: 3^6 ≡ 1 (mod 7)
- 20 = 6 × 3 + 2
- So 3^20 ≡ 3^2 = 9 ≡ 2 (mod 7)
Answer: 2

Now solve the given problem using similar step-by-step reasoning.
Give your final answer on the last line as "Answer: <number>"."""

# 所有策略汇总
STRATEGIES = {
    "A_Baseline": STRATEGY_A_BASELINE,
    "B_ZeroShot_CoT": STRATEGY_B_ZERO_SHOT_COT,
    "C_Structured_CoT": STRATEGY_C_STRUCTURED_COT,
    "D_Domain_CoT": STRATEGY_D_DOMAIN_COT,
    "E_FewShot_CoT": STRATEGY_E_FEW_SHOT_COT,
}

# =============================================================================
# 用于作业提交的最终策略 (TODO: 根据实验结果选择最佳策略)
# =============================================================================

# TODO: 运行完实验后，选择表现最好的策略填入这里
YOUR_SYSTEM_PROMPT = STRATEGY_D_DOMAIN_COT

USER_PROMPT = """Solve this problem step by step, then give the final answer on the last line as "Answer: <number>".

What is 3^12345 (mod 100)?

Remember to:
1. Use modular arithmetic properties
2. Show intermediate calculations
3. End with "Answer: <number>" on the last line"""

EXPECTED_OUTPUT = "Answer: 43"

# =============================================================================
# 辅助函数
# =============================================================================

def extract_final_answer(text: str) -> str:
    """Extract the final 'Answer: ...' line from a verbose reasoning trace."""
    matches = re.findall(r"(?mi)^\\s*answer\\s*:\\s*(.+)\\s*$", text)
    if matches:
        value = matches[-1].strip()
        num_match = re.search(r"-?\\d+(?:\\.\\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def run_single_test(system_prompt: str, problem: Problem, verbose: bool = False) -> tuple[bool, str, str]:
    """运行单次测试，返回(是否成功, 提取的答案, 完整输出)"""
    user_prompt = f"""Solve this problem step by step, then give the final answer on the last line as "Answer: <number>".

{problem.question}"""
    
    response = chat(
        model="mistral-nemo:12b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={"temperature": 0.3},
    )
    
    output_text = response.message.content
    final_answer = extract_final_answer(output_text)
    expected = f"Answer: {problem.expected_answer}"
    success = final_answer.strip() == expected.strip()
    
    if verbose:
        print(f"\\n{'─'*60}")
        print(f"Full Output:\\n{output_text}")
        print(f"{'─'*60}")
        print(f"Extracted: {final_answer} | Expected: {expected} | {'✓' if success else '✗'}")
    
    return success, final_answer, output_text


# =============================================================================
# 实验运行函数
# =============================================================================

def run_experiment(strategies: dict, problems: list[Problem], num_runs: int = 3, verbose: bool = False):
    """运行完整的对比实验"""
    results = {}
    
    print("=" * 70)
    print("Chain of Thought 对比实验")
    print("=" * 70)
    
    for strategy_name, system_prompt in strategies.items():
        print(f"\\n{'='*70}")
        print(f"策略: {strategy_name}")
        print(f"{'='*70}")
        
        strategy_results = {}
        
        for problem in problems:
            print(f"\\n  问题: {problem.name} ({problem.difficulty})")
            print(f"  {problem.question}")
            
            successes = 0
            answers = []
            
            for run_idx in range(num_runs):
                success, answer, output = run_single_test(system_prompt, problem, verbose=verbose)
                successes += 1 if success else 0
                answers.append(answer)
                status = "✓" if success else "✗"
                print(f"    Run {run_idx + 1}: {answer} {status}")
            
            accuracy = successes / num_runs * 100
            strategy_results[problem.name] = {
                "accuracy": accuracy,
                "answers": answers,
                "expected": problem.expected_answer
            }
            print(f"  准确率: {successes}/{num_runs} ({accuracy:.1f}%)")
        
        results[strategy_name] = strategy_results
    
    return results


def print_summary(results: dict):
    """打印实验结果汇总表"""
    print("\\n" + "=" * 70)
    print("实验结果汇总")
    print("=" * 70)
    
    # 收集所有问题名称
    problem_names = []
    for strategy_results in results.values():
        for pname in strategy_results.keys():
            if pname not in problem_names:
                problem_names.append(pname)
    
    # 打印表头
    header = f"{'策略':<20}"
    for pname in problem_names:
        header += f" | {pname[:15]:<15}"
    header += " | 平均"
    print(header)
    print("-" * len(header))
    
    # 打印每个策略的结果
    best_strategy = None
    best_avg = -1
    
    for strategy_name, strategy_results in results.items():
        row = f"{strategy_name:<20}"
        total = 0
        count = 0
        for pname in problem_names:
            if pname in strategy_results:
                acc = strategy_results[pname]["accuracy"]
                row += f" | {acc:>14.1f}%"
                total += acc
                count += 1
            else:
                row += f" | {'N/A':>15}"
        
        avg = total / count if count > 0 else 0
        row += f" | {avg:>5.1f}%"
        print(row)
        
        if avg > best_avg:
            best_avg = avg
            best_strategy = strategy_name
    
    print("-" * len(header))
    print(f"\\n🏆 最佳策略: {best_strategy} (平均准确率: {best_avg:.1f}%)")
    
    return best_strategy


# =============================================================================
# 作业提交用的简单测试函数
# =============================================================================

def test_your_prompt(system_prompt: str, test_name: str = "Standard") -> tuple[int, int]:
    """作业提交用：运行NUM_RUNS_TIMES次测试，返回(成功次数, 总次数)"""
    success_count = 0
    print(f"\\n{'='*50}")
    print(f"Testing: {test_name}")
    print(f"{'='*50}\\n")
    
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="mistral-nemo:12b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.3},
        )
        output_text = response.message.content
        final_answer = extract_final_answer(output_text)
        if final_answer.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            success_count += 1
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {final_answer}")
    
    pass_rate = (success_count / NUM_RUNS_TIMES) * 100
    print(f"\\n{'='*50}")
    print(f"Final Results: {success_count}/{NUM_RUNS_TIMES} tests passed ({pass_rate:.1f}%)")
    print(f"{'='*50}")
    
    return success_count, NUM_RUNS_TIMES


# =============================================================================
# 主入口
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--experiment":
        # 完整实验模式：对比所有策略
        print("\\n🔬 运行完整对比实验...\\n")
        all_problems = [MAIN_PROBLEM] + EXTRA_PROBLEMS
        results = run_experiment(STRATEGIES, all_problems, num_runs=NUM_RUNS_TIMES, verbose=False)
        best = print_summary(results)
        
        print(f"\\n💡 建议: 将 YOUR_SYSTEM_PROMPT 设置为 STRATEGY_{best[0]}_{best[2:]}")
        print("   然后运行 python chain_of_thought.py 进行最终验证")
        
    elif len(sys.argv) > 1 and sys.argv[1] == "--verbose":
        # 详细模式：显示完整输出
        print("\\n📝 详细模式：显示完整推理过程...\\n")
        success, answer, output = run_single_test(YOUR_SYSTEM_PROMPT, MAIN_PROBLEM, verbose=True)
        
    else:
        # 默认模式：作业提交测试
        results = test_your_prompt(YOUR_SYSTEM_PROMPT, "Chain of Thought Strategy")
        success_count, total_runs = results
        pass_rate = (success_count / total_runs) * 100
        
        print(f"\\n{'='*50}")
        print(f"Final Results: {success_count}/{total_runs} tests passed ({pass_rate:.1f}%)")
        print(f"{'='*50}\\n")
        
        if pass_rate == 100.0:
            print("✅ PERFECT! All tests passed with CoT strategy.")
        elif pass_rate >= 80.0:
            print("✅ EXCELLENT! High success rate achieved.")
        elif pass_rate >= 50.0:
            print("⚠️  MODERATE. Consider trying other strategies.")
            print("   Run: python chain_of_thought.py --experiment")
        else:
            print("❌ LOW. Need to improve the strategy.")
            print("   Run: python chain_of_thought.py --experiment")
