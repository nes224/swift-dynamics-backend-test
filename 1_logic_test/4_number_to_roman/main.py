"""
เขียบนโปรแกรมแปลงตัวเลยเป็นตัวเลข roman

[Input]
number: list of numbers

[Output]
roman_text: roman number

[Example 1]
input = 101
output = CI

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:

    def number_to_roman(self, number: int) -> str:
        if number <= 0:
            return "number can not less than 0"

        val_map = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ]

        result = ""

        for val, roman in val_map:
            for _ in range(number):
                if number < val:
                    break
                result += roman
                number -= val

        return result

# Test Cases
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        {"input": 101, "expected": "CI"},
        {"input": -1, "expected": "number can not less than 0"},
        {"input": 0, "expected": "number can not less than 0"},
        {"input": 4, "expected": "IV"},
        {"input": 9, "expected": "IX"},
        {"input": 58, "expected": "LVIII"},
        {"input": 1994, "expected": "MCMXCIV"},
    ]

    print("\n🧪 Running Test Cases for number_to_roman...\n" + "-"*55)
    for i, tc in enumerate(test_cases, 1):
        result = sol.number_to_roman(tc["input"])
        status = "✅ PASS" if result == tc["expected"] else f"❌ FAIL (Got: {result})"
        print(f"Test {i}: Input = {tc['input']:<10} | Expected = {tc['expected']:<18} | {status}")
    print("-" * 55)