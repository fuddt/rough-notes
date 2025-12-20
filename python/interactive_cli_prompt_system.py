class Step:
    """
    各プロンプトのステップを表すクラス
    """
    def __init__(self, message, validator=None):
        self.message = message  # プロンプトメッセージ
        self.validator = validator  # 入力のバリデーション関数（任意）

    def get_message(self):
        """プロンプトメッセージを取得"""
        return self.message

    def validate(self, user_input):
        """バリデーションを実行"""
        if self.validator:
            return self.validator(user_input)
        return True  # バリデータがない場合は常にTrueを返す


class InputValidator:
    """
    入力のバリデーションを行うクラス
    """
    @staticmethod
    def is_positive_number(value):
        """入力が正の数字かどうかをチェック"""
        try:
            return float(value) > 0
        except ValueError:
            return False

    @staticmethod
    def is_non_empty(value):
        """入力が空でないかをチェック"""
        return len(value.strip()) > 0


class UserInput:
    """
    ユーザーの入力を管理するクラス
    """
    def __init__(self):
        self.inputs = []  # 入力値を保存するリスト
        self.current_step = 0  # 現在のステップ

    def add_input(self, value):
        """現在のステップに対応する入力値を追加または更新"""
        if len(self.inputs) > self.current_step:
            self.inputs[self.current_step] = value
        else:
            self.inputs.append(value)
        self.current_step += 1

    def go_back(self):
        """1つ前のステップに戻る"""
        if self.current_step > 0:
            self.current_step -= 1
        else:
            print("これ以上戻れません。")

    def all_inputs(self):
        """全ての入力を取得"""
        return self.inputs


class Prompt:
    """
    プロンプトを管理するクラス
    各ステップのメッセージを表示し、ユーザーに入力を促す
    """
    def __init__(self, steps):
        self.steps = steps  # 各ステップのオブジェクト

    def display(self, step):
        """現在のステップに対応するプロンプトを表示"""
        return self.steps[step].get_message()

    def run(self, user_input):
        """入力の流れを制御する"""
        while user_input.current_step < len(self.steps):
            step = self.steps[user_input.current_step]
            user_response = input(f"{step.get_message()} (戻るには 'back' と入力): ")

            if user_response.lower() == 'back':
                user_input.go_back()  # 1つ前に戻る
            elif step.validate(user_response):
                user_input.add_input(user_response)  # ユーザー入力を保存
            else:
                print("無効な入力です。もう一度入力してください。")

        return user_input.all_inputs()


class PromptController:
    """
    複数のPromptオブジェクトを管理し、全体の流れを制御する
    """
    def __init__(self, prompts):
        self.prompts = prompts  # プロンプトのリスト

    def start(self):
        """全てのプロンプトを実行"""
        user_input = UserInput()
        for prompt in self.prompts:
            prompt.run(user_input)
        return user_input.all_inputs()


if __name__ == "__main__":
    # 各プロンプトのステップを定義
    steps = [
        Step("名前を入力してください", InputValidator.is_non_empty),
        Step("年齢を入力してください", InputValidator.is_positive_number),
        Step("住所を入力してください", InputValidator.is_non_empty)
    ]

    # PromptとPromptControllerクラスのインスタンスを作成
    prompt = Prompt(steps)
    prompt_controller = PromptController([prompt])

    # プロンプトを実行してユーザーの入力を取得
    inputs = prompt_controller.start()

    # 入力結果を表示
    print("\n入力されたデータ:")
    for i, input_value in enumerate(inputs):
        print(f"{steps[i].get_message()}: {input_value}")