import sys
import random
Japanese = [("あ", "ア", "a"), ("い", "イ", "i"), ("う", "ウ", "u"), ("え", "エ", "e"), ("お", "オ", "o"), ("か", "カ", "ka"), ("き", "キ", "ki"), ("く", "ク", "ku"), ("け", "ケ", "ke"), ("こ", "コ", "ko"), ("さ", "サ", "sa"), ("し", "シ", "shi"), ("す", "ス", "su"), ("せ", "セ", "se"), ("そ", "ソ", "so"), ("た", "タ", "ta"), ("ち", "チ", "chi"), ("つ", "ツ", "tsu"), ("て", "テ", "te"), ("と", "ト", "to"), ("な", "ナ", "na"), ("に", "ニ", "ni"), ("ぬ", "ヌ", "nu"), ("ね", "ネ", "ne"), ("の", "ノ", "no"), ("は", "ハ", "ha"), ("ひ", "ヒ", "hi"), ("ふ", "フ", "fu"), ("へ", "ヘ", "he"), ("ほ", "ホ", "ho"), ("ま", "マ", "ma"), ("み", "ミ", "mi"), ("む", "ム", "mu"), ("め", "メ", "me"), ("も", "モ", "mo"), ("や", "ヤ", "ya"), ("ゆ", "ユ", "yu"), ("よ", "ヨ", "yo"), ("ら", "ラ", "ra"), ("り", "リ", "ri"), ("る", "ル", "ru"), ("れ", "レ", "re"), ("ろ", "ロ", "ro"), ("わ", "ワ", "wa"), ("を", "ヲ", "o"), ("ん", "ン", "n"), ("が", "ガ", "ga"), ("ぎ", "ギ", "gi"), ("ぐ", "グ", "gu"), ("げ", "ゲ", "ge"), ("ご", "ゴ", "go"), ("ざ", "ザ", "za"), ("じ", "ジ", "ji"), ("ず", "ズ", "zu"), ("ぜ", "ゼ", "ze"), ("ぞ", "ゾ", "zo"), ("だ", "ダ", "da"), ("ぢ", "ヂ", "ji"), ("づ", "ヅ","zu"), ("で", "デ", "de"), ("ど", "ド", "do"), ("ば", "バ", "ba"), ("び", "ビ", "bi"), ("ぶ", "ブ", "bu",), ("べ", "ベ", "be"), ("ぼ", "ボ", "bo"), ("ぱ", "パ", "pa"), ("ぴ", "ピ", "pi"), ("ぷ", "プ", "pu"), ("ぺ", "ペ", "pe"), ("ぽ", "ポ", "po")]

def Japanese_search(n):
    for var in Japanese:
        if n == var[2]:
            print(var[0], var[1])
        elif n == var[0]:
            print(var[2])
        elif n == var[1]:
            print(var[2])

def train():
    exit_word = ""
    while exit_word != "exit":
         number  = random.randint(0, 70)
         word1,word2,rome = Japanese[number]
         print(word1, word2)
         input_rome = input(">")
         exit_word = input_rome
         if input_rome == rome :
            print("😁")
            print("")
         else:
            print("😭") 
            print(rome)
            print("")
  
def main():
    if len(sys.argv) > 1:
        to_search = sys.argv[1]
        Japanese_search(to_search)
    else:
        train()

if __name__ == "__main__":
    main()
