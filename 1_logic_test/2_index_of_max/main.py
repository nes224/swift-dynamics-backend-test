"""
เขียบนโปรแกรมหา index ของตัวเลขที่มีค่ามากที่สุดใน list

[Input]
numbers: list of numbers

[Output]
index: index of maximum number in list

[Example 1]
input = [1,2,1,3,5,6,4]
output = 5

[Example 2]
input = []
output = list can not blank
"""


class Solution:

    def find_max_index(self, numbers: list) -> int | str:
        if not numbers:
            return "list can not blank"

        max_index = 0
        for i in range(1, len(numbers)):
            if numbers[i] > numbers[max_index]:
                max_index = i
        return max_index

# Test Cases

if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        {"input": [1, 2, 1, 3, 5, 6, 4], "expected": 5},
        {"input": [], "expected": "list can not blank"},
        {"input": [10], "expected": 0},
        {"input": [-5, -2, -10, -1], "expected": 3},
    ]

    print("\n🧪 Running Test Cases for find_max_index...\n" + "-"*45)
    for i, tc in enumerate(test_cases, 1):
        result = sol.find_max_index(tc["input"])
        status = "✅ PASS" if result == tc["expected"] else f"❌ FAIL (Got: {result})"
        print(f"Test {i}: Input = {str(tc['input']):<25} | Expected = {str(tc['expected']):<18} | {status}")
    print("-" * 45)