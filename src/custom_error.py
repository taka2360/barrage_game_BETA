class ScriptNameError(Exception):
    """スクリプトの関数が存在しなかったときに投げるエラー"""
    def __init__(self, arg:"存在しなかった関数"="") -> None:
        self.arg = arg

    def __str__(self):
        return (
            f"[{self.arg}]という関数は存在しません。スペルが間違っている/すべて小文字である などといったことを確認してください。"
        )

class ScriptArgmentValueError(Exception):
    """スクリプトの関数の引数の型が違うときに投げるエラー"""
    def __init__(self, func:"例外が発生した関数"="", argname:"間違っている引数"="", arg1:"間違っている型"="", arg2:"正しい型"="") -> None:
        self.func = func
        self.argname = argname
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        return (
            f"[{self.func}]関数の引数[{self.argname}]は[{self.arg1}]型ではありません。[{self.arg2}]型を利用してください"
        )

