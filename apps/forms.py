from django import forms


class FormMixin(object):
    def get_errors(self):
        # 如果存在errors字段
        if hasattr(self, 'errors'):
            # 获取错误信息
            errors = self.errors.get_json_data()
            new_errors = {}
            for key, message_dicts in errors.items():
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key] = messages
            return new_errors
        else:
            return {}
