import tkinter as tk


class Window:
    def __init__(self, size_x: int, size_y: int, **options) -> None:
        """
        Windowクラスを生成します
        使用可能なオプション:
            fullscreen : bool　　　フルスクリーンかを指定します
        """

        self.window = tk.Tk()
        self.size_x = size_x
        self.size_y = size_y
        self.window.geometry(f"{self.size_x}x{self.size_y}")

        if options.keys() in "fullscreen":
            if options["fullscreen"]:
                self.window.attributes("-fullscreen", True)      

        self.window.update()
    
    def mainloop(self) -> None:
        """
        ウィンドウの自動アップデートを有効にします
        この関数を実行すると、それ以降のプログラムは処理されません。
        """

        self.window.mainloop()

    def update(self) -> None:
        """
        ウィンドウをアップデートします
        """

        self.window.update()
    
    
