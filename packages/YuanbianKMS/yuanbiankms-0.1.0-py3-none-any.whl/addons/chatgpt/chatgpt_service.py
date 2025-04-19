# -*- coding=utf-8 -*-
import json
import time
import openai
import tiktoken
from flask import current_app
from .chatgpt_utils import billing_reminder_message
from xp_cms.services.user_service import AccountService, ChatGPTAPIKeyService
from xp_cms.services.chatgpt_service import ChatGPTLogService


openai_api_key = "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"
openai_url = "https://api.openai.com/v1"
# deepseek
deepseek_api_key = "sk-58743caac9ca474486d614435113044f"
# deepseek
deepseek_url = "https://api.deepseek.com/v1"
models = {"gpt-3.5": {"model_name": "gpt-3.5-turbo",
                     "api_base": openai_url,
                     "encoding": "cl100k_base",
                     "price": 1,
                     "key": openai_api_key
                     },
          "gpt-4": {"model_name":"gpt-4o",
                    "api_base": openai_url,
                    "encoding": "o200k_base",
                    "price": 2,
                    "key": openai_api_key
                    },
          "DeepSeek-V3": {"model_name":"deepseek-chat",
                          "api_base": deepseek_url,
                          "encoding": "o200k_base",
                          "price": 1,
                          "key": deepseek_api_key
                          },
          "DeepSeek-R1": {"model_name": "deepseek-reasoner",
                          "api_base": deepseek_url,
                          "encoding": "o200k_base",
                          "price": 1,
                          "key": deepseek_api_key
                          }
          }
# 100万token 3.75美元
# 输出100万token 15美元  - gpt4
# 输出100万token 3美元

class YuanbianChatAPI:
    def __init__(self, user, model, key=None,  log_id=None):
        self.model = models[model]['model_name'] # model = "chatgpt-4o-latest"
        self.user_key = key
        self.api_base = models[model]['api_base']
        self.encoding = models[model]["encoding"]
        self.price = models[model]["price"]

        openai.api_key = self.user_key or models[model]['key']
        if self.api_base:
            openai.api_base = self.api_base
        self.user_id = user['user_id']
        self.log_id = log_id
        self.response_content = ""
        pass

    def check_account(self):
        account = AccountService.get_account(self.user_id)
        if account.token_coin <= 0:
            return True

    def call_openai_chat(self, chat_user, messages):
        if self.check_account():
            yield self.out_sse_data(event="message", data=billing_reminder_message)
            yield self.out_sse_data(event="close")
            return

        try:
            for completion in openai.ChatCompletion.create(model=self.model,
                                                           stream=True,
                                                           user=chat_user,
                                                           messages=messages):
                try:

                    for choice in completion.choices:
                        content = choice.delta.get('content', "")
                        if type(content) != str:
                            continue
                        self.response_content += content
                        yield self.out_sse_data(data=content)
                except Exception as e:
                    yield self.out_sse_data(event="message", data=str(e))
        except Exception as e:
            yield self.out_sse_data(event="message", data=str(e))
        finally:
            yield self.out_sse_data(event="message", data=self.chat_finish(messages))

    @staticmethod
    def test_openai_key(key):
        """用于测试key的有效性"""
        openai.api_key = key
        models = openai.Model.list()
        if models:
            return True

    def chat_finish(self, messages):
        try:
            # encoding = tiktoken.encoding_for_model(models[self.model])
            encoding = tiktoken.get_encoding(self.encoding)
        except Exception as e:
            current_app.logger.error(e)
            return
        prompt = messages[-1]['content']
        num_tokens_messages = 0
        for message in messages:
            try:
                num_tokens_messages += len(encoding.encode(message['content']))
            except Exception as e:
                current_app.logger.error(e)

        num_tokens_reponse = len(encoding.encode(self.response_content))
        num_tokens = num_tokens_messages + num_tokens_reponse
        try:
            user_prompt = {"role": "user", "content": prompt}
            openai_response = {"role": "assistant", "content": self.response_content}
            ChatGPTLogService.add_new_chat(self.log_id, self.user_id, user_prompt, openai_response)
        except Exception as e:
            current_app.logger.error(e)
        if not self.user_key:
            account = AccountService.add_balance(self.user_id, -(num_tokens * self.price), "token_coin", f"AI对话消耗", "")
            return f"——————本次使用模型为{self.model}, 本次对话消耗:{num_tokens}tokens，账户目前还有 {account.token_coin} tokens"
        else:
            return "——————【您正在使用猿变ChatGPT免费模式】"
    # 提示

    @classmethod
    def out_sse_data(cls, event="message", data=""):
        # data = base64.b64encode(data.encode()).decode("utf-8")
        data = json.dumps({"content": data}).replace("\n", "\\u000A")
        return f"event:{event}\ndata:{data}\nid:{time.monotonic_ns()}\n\n"

    @staticmethod
    def load_chat_log(log_id, user_id):
        try:
            chat_log = ChatGPTLogService.get_user_log_detail(log_id, user_id)
        except Exception as e:
            return
        else:
            return chat_log

    @staticmethod
    def get_last_log(chat_log, is_dumps=True):
        last_log = chat_log.chat_content[-10:]
        for log in last_log:
            if len(log['content']) > 200:
                log['content'] = log['content'][:200]
        if is_dumps:
            return json.dumps(last_log)
        else:
            return last_log






    # if log_id and openai_response_content:
    #     save_chat_data(log_id, user_id, prompt, openai_response_content)
