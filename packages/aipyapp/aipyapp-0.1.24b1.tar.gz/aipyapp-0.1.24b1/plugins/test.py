class Plugin:
    def on_task_start(self, prompt):
        prompt['lang'] = 'zh-CN'
