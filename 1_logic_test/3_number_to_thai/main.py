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

    ONES = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
    PLACES = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน"]

    def _chunk_to_text(self, n, prefix=False):
        """แปลงเลข 1-999999 เป็นคำอ่าน, prefix=True ถ้ามีหลักล้านนำหน้า"""
        if n == 0:
            return ""

        text = ""
        s = str(n)
        length = len(s)

        for i, ch in enumerate(s):
            d = int(ch)
            pos = length - 1 - i

            if d == 0:
                continue

            if pos == 1 and d == 1:
                text += "สิบ"
            elif pos == 1 and d == 2:
                text += "ยี่สิบ"
            elif pos == 0 and d == 1 and (n > 1 or prefix):
                text += "เอ็ด"
            else:
                text += self.ONES[d] + self.PLACES[pos]

        return text

    def number_to_thai(self, number: int) -> str:
        if number < 0:
            return "number can not less than 0"
        if number == 0:
            return "ศูนย์"

        mill = number // 1_000_000
        rest = number % 1_000_000

        result = ""
        if mill > 0:
            result += self._chunk_to_text(mill) + "ล้าน"
        if rest > 0:
            result += self._chunk_to_text(rest, prefix=(mill > 0))

        return result
