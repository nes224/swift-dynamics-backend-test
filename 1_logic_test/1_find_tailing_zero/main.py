"""
เขียบนโปรแกรมหาจำนวนเลข 0 ที่ออยู่ติดกันหลังสุดของค่า factorial โดยห้ามใช้ function from math

[Input]
number: as an integer

[Output]
count: count of tailing zero as an integer

[Example 1]
input = 7
output = 1

[Example 2]
input = -10
output = number can not be negative
"""


class Solution:

    def find_tailing_zeroes(self, number: int) -> int | str:
        if number < 0:
            return "number can not be negative"

        count = 0
        i = 5
        for _ in range(number):
            if i > number:
                break
            count += number // i
            i *= 5

        return count

# Test Cases
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        {"input": 7, "expected": 1},
        {"input": -10, "expected": "number can not be negative"},
        {"input": 0, "expected": 0},
        {"input": 25, "expected": 6},
        {"input": 100, "expected": 24},
    ]

    print("\n🧪 Running Test Cases for find_tailing_zeroes...\n" + "-"*45)
    for i, tc in enumerate(test_cases, 1):
        result = sol.find_tailing_zeroes(tc["input"])
        status = "✅ PASS" if result == tc["expected"] else f"❌ FAIL (Got: {result})"
        print(f"Test {i}: Input = {tc['input']:<5} | Expected = {str(tc['expected']):<28} | {status}")
    print("-" * 45)