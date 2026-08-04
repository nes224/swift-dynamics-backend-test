"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:

    def number_to_thai(self, number: int) -> str:
        if number < 0:
            return "number can not less than 0"

        if number == 0:
            return "ศูนย์"

        digits = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
        units = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]

        result = ""

        if number >= 1_000_000:
            millions = number // 1_000_000
            number %= 1_000_000
            result += self.number_to_thai(millions) + "ล้าน"

        numStr = str(number)
        length = len(numStr)

        for i, digitChar in enumerate(numStr):
            digit = int(digitChar)
            if digit == 0:
                continue

            position = length - i -1

            if position == 1:
                if digit == 1:
                    result += "สิบ"
                elif digit == 2:
                    result += "ยี่สิบ"
                else:
                    result += digits[digit] + "สิบ"
            elif position == 0:
                if digit == 1 and length > 1:
                    result += "เอ็ด"
                else:
                    result += digits[digit]
            else:
                result += digits[digit] + units[position]

        return result

# Test Cases
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        {"input": 101, "expected": "หนึ่งร้อยเอ็ด"},
        {"input": -1, "expected": "number can not less than 0"},
        {"input": 0, "expected": "ศูนย์"},
        {"input": 1, "expected": "หนึ่ง"},
        {"input": 10, "expected": "สิบ"},
        {"input": 21, "expected": "ยี่สิบเอ็ด"},
        {"input": 251, "expected": "สองร้อยห้าสิบเอ็ด"},
        {"input": 10000000, "expected": "สิบล้าน"},
    ]

    print("\n🧪 Running Test Cases for number_to_thai...\n" + "-"*55)
    for i, tc in enumerate(test_cases, 1):
        result = sol.number_to_thai(tc["input"])
        status = "✅ PASS" if result == tc["expected"] else f"❌ FAIL (Got: {result})"
        print(f"Test {i}: Input = {tc['input']:<10} | Expected = {tc['expected']:<18} | {status}")
    print("-" * 55)