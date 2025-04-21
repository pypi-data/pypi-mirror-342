from fuzzywuzzy import process  # 确保你已经安装了 fuzzywuzzy
from loguru import logger


def correct_term(input_word, correct_words, threshold=70):
    """
    纠正输入词
    :param input_word: 输入的词
    :param correct_words: 正确的词列表
    :param threshold: 相似度阈值
    :return: 纠正后的词或原词
    """
    try:
        # 使用模糊匹配找到最相似的词
        result = process.extractOne(input_word, correct_words)
        # logger.success(f"输入: {input_word} → 纠正后: {result[0]} similarity: {result[1]}")

        # 若相似度超过阈值则返回纠正后的词，否则返回原词
        return result[0] if result[1] > threshold else input_word
    except Exception as e:
        logger.error(f"纠正词时发生错误: {e}")
        return input_word  # 纠错失败时返回原词


# correct_words = [ "banana", "orange", "grape"]
# input_word = a
#
# corrected_word = correct_term(input_word, correct_words)
# print(corrected_word)  # 输出: "apple"